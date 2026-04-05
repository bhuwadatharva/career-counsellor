"""
AI Career Counsellor — FastAPI Server v3.0
Autonomous LLM Agent + RAG + Multi-step Reasoning
Run: uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import os

from questionnaire import aggregate_answers, get_questions_for_api
from rag_engine import RAGEngine
from llm_agent import CareerCounsellorAgent, OllamaLLM

app = FastAPI(
    title="AI Career Counsellor — LLM Agent Edition",
    description="""
## Autonomous AI Career Counselling Agent

**Architecture:**
- 🧠 **LLM**: Llama 3.2 via Ollama (local, free) — fine-tunable to `career-counsellor` model
- 🔍 **RAG**: Pinecone vector DB for dynamic knowledge retrieval
- ⚙️ **Agent**: 6-step multi-tool reasoning pipeline
- 📋 **Questionnaire**: 15 behavioral questions → inferred profile

**Flow:** `GET /questions` → answer 15 Qs → `POST /recommend` → agent runs 6 steps → career path

**Setup:**
1. Install Ollama: `curl https://ollama.ai/install.sh | sh`
2. Pull model: `ollama pull llama3.2`
3. Set Pinecone key: `export PINECONE_API_KEY=your-key`
4. Ingest knowledge: `POST /admin/ingest`
5. Optionally fine-tune: `python finetune.py --train`
    """,
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize RAG + LLM + Agent ─────────────────────────────────────
print("\n🚀 Initializing AI Career Counsellor Agent...")
rag = RAGEngine()
rag.initialize()

llm = OllamaLLM()
agent = CareerCounsellorAgent(rag=rag, llm=llm)
print("✅ Agent ready\n")


# ── Request Models ────────────────────────────────────────────────────
class SubmitAnswersRequest(BaseModel):
    name: str = Field(..., example="Rahul Sharma")
    current_year: int = Field(..., ge=1, le=5, example=2)
    total_years: int = Field(default=4, ge=3, le=5, example=4)
    degree_type: str = Field(..., example="B.Tech")
    preferred_work_style: str = Field(default="both", example="remote")
    answers: Dict[str, List[str]] = Field(
        ...,
        example={
            "Q1": ["B"], "Q2": ["B"], "Q3": ["D"], "Q4": ["B"],
            "Q5": ["B"], "Q6": ["D"], "Q7": ["A"], "Q8": ["B"],
            "Q9": ["C"], "Q10": ["C"], "Q11": ["B"], "Q12": ["A"],
            "Q13": ["A"], "Q14": ["C"], "Q15": ["B"]
        }
    )


# ── Routes ────────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
def root():
    return {
        "service": "AI Career Counsellor — LLM Agent v3.0",
        "agent_model": llm.model,
        "llm_available": llm.available,
        "rag_stats": rag.get_stats(),
        "flow": "GET /questions → POST /recommend",
        "endpoints": {
            "GET  /questions":      "Fetch 15 questionnaire questions",
            "POST /recommend":      "Submit answers → LLM agent generates career path",
            "GET  /domains":        "List all 10 supported CS/IT domains",
            "POST /admin/ingest":   "Ingest knowledge base into Pinecone (run once)",
            "GET  /agent/status":   "Check LLM + RAG status",
            "GET  /health":         "Health check",
            "GET  /docs":           "Swagger UI"
        }
    }


@app.get("/health", tags=["Info"])
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "llm": {"model": llm.model, "available": llm.available},
        "rag": rag.get_stats()
    }


@app.get("/agent/status", tags=["Info"])
def agent_status():
    """Detailed status of LLM and RAG components."""
    return {
        "llm": {
            "model": llm.model,
            "available": llm.available,
            "host": "http://localhost:11434",
            "setup_command": f"ollama pull {llm.model}",
            "finetune_command": "python finetune.py --train"
        },
        "rag": rag.get_stats(),
        "ingest_command": "POST /admin/ingest"
    }


@app.get("/domains", tags=["Info"])
def get_domains():
    from Recomendation.dataset import DOMAIN_KNOWLEDGE
    return {"domains": list(DOMAIN_KNOWLEDGE.keys())}


@app.get("/questions", tags=["Questionnaire"])
def get_questions():
    """
    Returns all 15 questionnaire questions.
    Present these to the user one by one, collect answers as:
    `{ "Q1": ["A"], "Q12": ["A", "C"] }`
    Then POST to /recommend.
    """
    questions = get_questions_for_api()
    return {
        "total": len(questions),
        "instructions": "Answer all questions. multi_select=true means you can pick multiple options.",
        "questions": questions
    }


@app.post("/recommend", tags=["Career Path"])
def recommend(request: SubmitAnswersRequest):
    """
    ## Submit Questionnaire → Autonomous Agent Generates Career Path

    The agent runs a **6-step reasoning pipeline**:
    1. `analyze_profile` — synthesizes questionnaire answers into profile
    2. `decide_domain` — LLM reasons about best career domain
    3. `retrieve_knowledge` — RAG fetches relevant chunks from Pinecone
    4. `analyze_job_market` — retrieves salary/company/role data
    5. `build_milestone_plan` — generates structured learning milestones
    6. `synthesize` — LLM generates personalized advice, goals, warnings

    Returns a rich career path grounded in retrieved knowledge.
    Falls back to rule-based model if Ollama is not running.
    """
    try:
        q_result = aggregate_answers(request.answers)
        result = agent.run(
            q_result=q_result,
            name=request.name,
            current_year=request.current_year,
            total_years=request.total_years,
            degree_type=request.degree_type,
            preferred_work_style=request.preferred_work_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin/ingest", tags=["Admin"])
def ingest_knowledge_base():
    """
    Embed and upload the career knowledge base into Pinecone.
    Run this ONCE after setting up Pinecone.
    Requires PINECONE_API_KEY environment variable.
    """
    try:
        from Recomendation.data.rag_knowledge_base import RAG_DOCUMENTS
        count = rag.ingest(RAG_DOCUMENTS)
        return {
            "status": "success",
            "documents_ingested": count,
            "pinecone_stats": rag.get_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)