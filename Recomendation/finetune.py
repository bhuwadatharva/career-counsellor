"""
finetune.py — Fine-tune Llama 3.2 on career counselling data
Uses PEFT (LoRA) for efficient fine-tuning on consumer hardware.

Requirements:
    pip install torch transformers peft datasets trl bitsandbytes accelerate

Hardware: Works on GPU with 8GB+ VRAM (RTX 3060 / T4 / A10).
          On CPU: Much slower but still works for small dataset.

After fine-tuning, the model is exported and loaded via Ollama locally.
"""

import json
import os
import sys
from pathlib import Path


# ── CONFIG ────────────────────────────────────────────────────────────
BASE_MODEL = "meta-llama/Llama-3.2-3B-Instruct"   # 3B — runs on 8GB GPU
OUTPUT_DIR = "./models/career-llama-finetuned"
DATASET_PATH = "./data/finetune_dataset.json"
MAX_SEQ_LENGTH = 1024
NUM_EPOCHS = 3
BATCH_SIZE = 2
LEARNING_RATE = 2e-4
LORA_R = 16         # LoRA rank — higher = more parameters, better quality
LORA_ALPHA = 32
LORA_DROPOUT = 0.05


# ── PROMPT TEMPLATE ───────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AI career counsellor specializing in Computer Science and IT.
You analyze student profiles and questionnaire answers to recommend personalized career paths.
You provide structured, actionable guidance with specific resources, milestones, and realistic timelines.
Always consider the Indian job market while also providing global context.
Your responses must be specific, practical, and encouraging."""

def format_prompt(instruction: str, output: str = "") -> str:
    """Format a training sample into Llama 3.2 chat template."""
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{SYSTEM_PROMPT}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{instruction}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{output}<|eot_id|>"""
    return prompt


def load_dataset(path: str):
    """Load and format the fine-tuning dataset."""
    with open(path, "r") as f:
        raw = json.load(f)

    formatted = []
    for item in raw:
        text = format_prompt(item["instruction"], item["output"])
        formatted.append({"text": text})

    print(f"✅ Loaded {len(formatted)} training samples")
    return formatted


def run_finetuning():
    """Main fine-tuning pipeline using PEFT LoRA."""
    try:
        import torch
        from transformers import (
            AutoTokenizer, AutoModelForCausalLM,
            TrainingArguments, BitsAndBytesConfig
        )
        from peft import LoraConfig, get_peft_model, TaskType
        from trl import SFTTrainer
        from datasets import Dataset
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstall with:")
        print("  pip install torch transformers peft datasets trl bitsandbytes accelerate")
        sys.exit(1)

    print("🚀 Starting fine-tuning pipeline...")
    print(f"   Base model : {BASE_MODEL}")
    print(f"   Output dir : {OUTPUT_DIR}")
    print(f"   Epochs     : {NUM_EPOCHS}")
    print(f"   LoRA rank  : {LORA_R}")

    # ── 1. Load dataset ───────────────────────────────────────────────
    raw_data = load_dataset(DATASET_PATH)
    dataset = Dataset.from_list(raw_data)
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    print(f"   Train: {len(dataset['train'])} | Val: {len(dataset['test'])}")

    # ── 2. Quantization config (4-bit) for memory efficiency ──────────
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # ── 3. Load base model ────────────────────────────────────────────
    print(f"\n📥 Loading base model: {BASE_MODEL}")
    print("   (First run will download ~6GB — subsequent runs use cache)")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # ── 4. Apply LoRA ─────────────────────────────────────────────────
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── 5. Training arguments ─────────────────────────────────────────
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=4,
        learning_rate=LEARNING_RATE,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="cosine",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=10,
        report_to="none",   # set to "wandb" if you use Weights & Biases
    )

    # ── 6. Trainer ────────────────────────────────────────────────────
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        dataset_text_field="text",
        tokenizer=tokenizer,
        args=training_args,
        max_seq_length=MAX_SEQ_LENGTH,
        packing=False,
    )

    # ── 7. Train ──────────────────────────────────────────────────────
    print("\n🏋️  Training started...")
    trainer.train()

    # ── 8. Save ───────────────────────────────────────────────────────
    print(f"\n💾 Saving fine-tuned model to {OUTPUT_DIR}")
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("\n✅ Fine-tuning complete!")
    print(f"   Model saved at: {OUTPUT_DIR}")
    print("\n📦 Next step: Export to GGUF and load in Ollama:")
    print("   python finetune.py --export")


def export_to_ollama():
    """
    Export fine-tuned model to GGUF format and create Ollama Modelfile.
    Requires llama.cpp to be installed.
    """
    print("📦 Exporting fine-tuned model to Ollama format...")

    # Create Ollama Modelfile
    modelfile_content = f"""FROM {OUTPUT_DIR}

SYSTEM \"\"\"{SYSTEM_PROMPT}\"\"\"

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 2048
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"
"""

    modelfile_path = Path(OUTPUT_DIR) / "Modelfile"
    with open(modelfile_path, "w") as f:
        f.write(modelfile_content)

    print(f"✅ Modelfile created at: {modelfile_path}")
    print("\n🚀 To load in Ollama, run:")
    print(f"   ollama create career-counsellor -f {modelfile_path}")
    print("   ollama run career-counsellor")
    print("\nThen update OLLAMA_MODEL in llm_agent.py to 'career-counsellor'")


def test_model():
    """Quick inference test on the fine-tuned model."""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        from peft import PeftModel
    except ImportError:
        print("❌ transformers/peft not installed")
        return

    print(f"🧪 Testing fine-tuned model from {OUTPUT_DIR}...")

    tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR)
    base_model_path = BASE_MODEL

    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        device_map="auto",
        torch_dtype="auto"
    )
    model = PeftModel.from_pretrained(model, OUTPUT_DIR)
    model = model.merge_and_unload()

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
    )

    test_prompt = format_prompt(
        "A student loves Python, spends free time on ML experiments, wants to build an AI chatbot, "
        "reads research papers, and is in 3rd year of B.Tech. What career path should they take?",
        ""
    )

    result = pipe(test_prompt)[0]["generated_text"]
    # Extract just the assistant response
    response = result.split("<|start_header_id|>assistant<|end_header_id|>")[-1]
    response = response.replace("<|eot_id|>", "").strip()

    print("\n🤖 Model Response:")
    print("─" * 60)
    print(response)
    print("─" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fine-tune Llama 3.2 for career counselling")
    parser.add_argument("--train", action="store_true", help="Run fine-tuning")
    parser.add_argument("--export", action="store_true", help="Export to Ollama format")
    parser.add_argument("--test", action="store_true", help="Test the fine-tuned model")
    args = parser.parse_args()

    if args.train:
        run_finetuning()
    elif args.export:
        export_to_ollama()
    elif args.test:
        test_model()
    else:
        print("Usage:")
        print("  python finetune.py --train    # Fine-tune the model")
        print("  python finetune.py --export   # Export to Ollama")
        print("  python finetune.py --test     # Test inference")