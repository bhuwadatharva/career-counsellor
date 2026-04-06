# AI Career Counsellor v3.0

### LLM Agent · RAG · Multi-Step Reasoning · Fine-Tunable Llama 3.2

A fully autonomous AI career counselling system for CS and IT students.
No manual interest entry — students answer 15 behavioural questions and the
agent infers everything, then generates a personalised career path.

---

## Architecture at a Glance

```
Student answers 15 questions
          │
          ▼
  questionnaire.py          ← infers interests, skill level, Git/Docker knowledge
          │
          ▼
  CareerCounsellorAgent     ← llm_agent.py (6-step pipeline)
          │
    ┌─────┼──────────┬────────────┬──────────────┐
    ▼     ▼          ▼            ▼              ▼
  Tool1  Tool2     Tool3        Tool4          Tool5+6
  Profile RAG      Job Market   Milestone      LLM
  Analyze Retrieve  Analyze     Builder        Synthesis
          │
          ▼
      rag_engine.py            ← Pinecone vector DB (24 embedded docs)
          │
          ▼
      llama3.2 via Ollama      ← local, free, fine-tunable
          │
          ▼
      Career Path Response     ← unique per student, grounded in retrieved knowledge
```

---

## Project Structure

```
career_counsellor_v3/
│
├── main.py                   FastAPI server (4 routes)
├── llm_agent.py              Autonomous agent — 6 tools, multi-step reasoning
├── rag_engine.py             Pinecone RAG engine + in-memory fallback
├── finetune.py               LoRA fine-tuning script for Llama 3.2
├── questionnaire.py          15 questions, hidden domain weights, answer aggregator
├── dataset.py                Domain knowledge base (10 domains, full data)
├── schemas.py                Data models
├── demo.py                   CLI demo (works without Ollama or Pinecone)
├── requirements.txt          All dependencies
├── .env                      API keys (never commit this)
├── .gitignore
│
├── data/
│   ├── finetune_dataset.json    20 Q&A training samples (Llama chat format)
│   └── rag_knowledge_base.py    24 career knowledge documents for Pinecone
│
└── models/                   Created only after running finetune.py --train
    └── career-llama-finetuned/
        ├── adapter_model.bin
        ├── tokenizer.json
        └── Modelfile           Used by: ollama create career-counsellor -f Modelfile
```

---

## Supported Domains (10)

| Domain                     | Entry Salary India |
| -------------------------- | ------------------ |
| Full Stack Web Development | ₹5–25 LPA          |
| Machine Learning & AI      | ₹8–40 LPA          |
| Cybersecurity              | ₹5–30 LPA          |
| Cloud & DevOps Engineering | ₹7–35 LPA          |
| Mobile App Development     | ₹5–28 LPA          |
| Data Engineering           | ₹6–30 LPA          |
| Blockchain Development     | ₹8–40 LPA          |
| Game Development           | ₹4–22 LPA          |
| Embedded Systems & IoT     | ₹5–25 LPA          |
| AI Research & NLP          | ₹12–60 LPA         |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/bhuwadatharva/career-counsellor
cd career_counsellor
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install Ollama and pull Llama 3.2

```bash
# Linux / Mac
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2

# Windows — download from https://ollama.ai/download
```

### 3. Set up Pinecone (free tier at pinecone.io)

```bash
# Create a free account at https://app.pinecone.io
# Copy your API key, then:

export PINECONE_API_KEY=your-key-here     # Linux/Mac
set PINECONE_API_KEY=your-key-here        # Windows

# Or create a .env file:
echo "PINECONE_API_KEY=your-key-here" > .env
```

### 4. Ingest the knowledge base into Pinecone

```bash
# Start the server first, then:
curl -X POST http://localhost:8000/admin/ingest

# This embeds 24 career knowledge documents into Pinecone.
# Only needs to run ONCE.
```

### 5. (Optional) Fine-tune Llama 3.2 on career data

```bash
# Requires GPU with 8GB+ VRAM (RTX 3060, T4, A10)
python finetune.py --train       # ~30 min on GPU, much longer on CPU

# Export to Ollama format
python finetune.py --export

# Register your fine-tuned model with Ollama
ollama create career-counsellor -f models/career-llama-finetuned/Modelfile

# Update the model name in llm_agent.py:
# OLLAMA_MODEL = "career-counsellor"
```

---

## Running

### API server

```bash
uvicorn main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

### CLI demo (no server needed)

```bash
python demo.py                  # all 3 sample students
python demo.py --student 1      # Priya  (Web Dev, beginner)
python demo.py --student 2      # Karan  (Cybersecurity, intermediate)
python demo.py --student 3      # Anika  (ML/AI, advanced)
python demo.py --uniqueness     # prove uniqueness: same answers -> different paths
python demo.py --questions      # print all 15 questions with options
```

---

## API Endpoints

| Method | Route           | Description                                   |
| ------ | --------------- | --------------------------------------------- |
| GET    | `/`             | API info and status                           |
| GET    | `/health`       | Health check                                  |
| GET    | `/agent/status` | LLM and RAG component status                  |
| GET    | `/domains`      | List all 10 supported domains                 |
| GET    | `/questions`    | Fetch all 15 questionnaire questions          |
| POST   | `/recommend`    | Submit answers → agent generates career path  |
| POST   | `/admin/ingest` | Embed knowledge base into Pinecone (run once) |

### POST /recommend — request body

```json
{
  "name": "Rahul Sharma",
  "current_year": 2,
  "total_years": 4,
  "degree_type": "B.Tech",
  "preferred_work_style": "remote",
  "answers": {
    "Q1": ["B"],
    "Q2": ["B"],
    "Q3": ["D"],
    "Q4": ["B"],
    "Q5": ["B"],
    "Q6": ["D"],
    "Q7": ["A"],
    "Q8": ["B"],
    "Q9": ["C"],
    "Q10": ["C"],
    "Q11": ["B"],
    "Q12": ["A"],
    "Q13": ["A"],
    "Q14": ["C"],
    "Q15": ["B"]
  }
}
```

---

## The 15 Questions — Quick Reference

| ID  | Category   | What it detects                                    |
| --- | ---------- | -------------------------------------------------- |
| Q1  | background | First excitement — what drew them to CS            |
| Q2  | curiosity  | Free-time behaviour — how they actually spend time |
| Q3  | scenario   | Dream project — single strongest intent signal     |
| Q4  | curiosity  | What problem absorbs them for hours                |
| Q5  | style      | Ideal work environment                             |
| Q6  | curiosity  | Which technology fascinates them right now         |
| Q7  | style      | How they actually write code                       |
| Q8  | scenario   | Which course they would realistically finish       |
| Q9  | curiosity  | What they would talk about at a meetup             |
| Q10 | scenario   | Whose career story inspires them                   |
| Q11 | background | Skill self-assessment → infers level               |
| Q12 | tools      | Multi-select → detects Git and Docker knowledge    |
| Q13 | style      | What frustrates them in learning                   |
| Q14 | scenario   | 5-year career vision                               |
| Q15 | background | Single biggest current strength                    |

Each option has hidden domain weights. The student sees plain language.
The system accumulates weighted scores across all 15 answers.

---

## How Uniqueness Works

Every student gets a different path even with identical answers because:

1. Path ID seeds from: `name + interests + skill_level + timestamp microseconds`
2. Resource order shuffled with that seed
3. Company and certification subsets randomly sampled
4. 15% probability of exploring 2nd-best domain if scores are close
5. LLM temperature = 0.7 introduces natural variation in advice text

---

## Fallback Mode

The system works fully without Ollama or Pinecone:

| Component           | With dependencies      | Without (fallback)     |
| ------------------- | ---------------------- | ---------------------- |
| Domain decision     | LLM reasoning          | Weighted score ranking |
| Knowledge retrieval | Pinecone vector search | Keyword overlap search |
| Path synthesis      | LLM-generated text     | Rule-based templates   |
| Speed               | ~2–8 seconds           | <100ms                 |

Run `python demo.py` to see fallback mode in action.

---

## Resume Bullet Mapping

| Resume claim                             | Actual implementation                                                                                                                                                   |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LLM-powered autonomous AI agent          | `CareerCounsellorAgent` in `llm_agent.py` running Llama 3.2 via Ollama. After `finetune.py --train`, uses custom `career-counsellor` model.                             |
| Retrieval-Augmented Generation (RAG)     | `RAGEngine` in `rag_engine.py` embeds 24 documents with `sentence-transformers`, stores in Pinecone, retrieves top-k at query time.                                     |
| Multi-step reasoning pipeline + tool-use | 6 sequential tools: `analyze_profile → decide_domain → retrieve_knowledge → analyze_job_market → build_milestone_plan → synthesize`. Each tool's output feeds the next. |

---

## .gitignore

```
venv/
.venv/
env/
.env/
__pycache__/
*.pyc
*.pyo
.DS_Store
.env
models/
```

---

## License

MIT — free to use, extend, and build on.
