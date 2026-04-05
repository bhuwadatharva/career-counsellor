"""
llm_agent.py — Autonomous Multi-Step LLM Career Counselling Agent

Architecture:
    Questionnaire Answers
           │
           ▼
    [AgentOrchestrator]  ← Llama 3.2 via Ollama (or fine-tuned variant)
           │
    ┌──────┼──────────────┬───────────────┐
    ▼      ▼              ▼               ▼
  Tool1  Tool2          Tool3           Tool4
  Profile RAG Retrieve  Job Market      Milestone
  Analyze (Pinecone)    Reasoner        Builder
           │
           ▼
    Final Career Path  ← LLM synthesizes all tool outputs

Each tool call feeds the next. The agent loops until a complete path is built.
"""

import json
import re
import time
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Try importing Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from Recomendation.rag_engine import RAGEngine, RetrievedChunk
from Recomendation.questionnaire import QuestionnaireResult


# ── CONFIG ────────────────────────────────────────────────────────────
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")   # or "career-counsellor" after fine-tuning
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MAX_AGENT_STEPS = 6
TEMPERATURE = 0.7


# ── Tool definitions ──────────────────────────────────────────────────
@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any]
    result: Optional[str] = None
    duration_ms: Optional[int] = None


@dataclass
class AgentState:
    """Tracks the agent's reasoning state across all steps."""
    user_name: str
    q_result: QuestionnaireResult
    degree_info: Dict
    steps: List[ToolCall] = field(default_factory=list)
    inferred_domain: Optional[str] = None
    domain_reasoning: Optional[str] = None
    retrieved_context: Optional[str] = None
    job_market_analysis: Optional[str] = None
    milestones: Optional[List[Dict]] = None
    final_response: Optional[str] = None
    total_tokens_used: int = 0


# ─────────────────────────────────────────────────────────────────────
# TOOLS — each tool is a function the agent can call
# ─────────────────────────────────────────────────────────────────────

class AgentTools:
    """All tools available to the LLM agent."""

    def __init__(self, rag: RAGEngine):
        self.rag = rag

    # ── Tool 1: Analyze profile ───────────────────────────────────────
    def analyze_profile(self, state: AgentState) -> str:
        """
        Tool 1: Synthesize questionnaire answers into a coherent profile summary.
        Returns structured profile analysis.
        """
        q = state.q_result
        profile_lines = [
            f"Student: {state.user_name}",
            f"Degree: {state.degree_info.get('degree_type')} | Year {state.degree_info.get('current_year')} of {state.degree_info.get('total_years')}",
            f"Years remaining: {state.degree_info.get('total_years') - state.degree_info.get('current_year') + 1}",
            f"Inferred skill level: {q.inferred_skill_level}",
            f"Knows Git: {q.knows_git} | Knows Docker: {q.knows_docker}",
            f"Top inferred interests: {', '.join(q.inferred_interests[:6])}",
            "",
            "Domain affinity scores (from questionnaire):"
        ]
        for domain, score in sorted(q.domain_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
            bar = "█" * int(score * 50)
            profile_lines.append(f"  {domain}: {bar} {score:.1%}")

        profile_lines.append("")
        profile_lines.append("Answer summary:")
        for q_id, answer in list(q.answer_summary.items())[:8]:
            profile_lines.append(f"  {q_id}: {answer[:80]}")

        return "\n".join(profile_lines)

    # ── Tool 2: RAG retrieve ──────────────────────────────────────────
    def retrieve_knowledge(self, query: str, domain: str, state: AgentState) -> str:
        """
        Tool 2: Retrieve relevant career knowledge from Pinecone vector DB.
        Returns formatted context chunks.
        """
        # Retrieve domain-specific + general chunks
        domain_chunks = self.rag.retrieve(query, top_k=3, domain_filter=domain)
        general_chunks = self.rag.retrieve(f"career advice resources {query}", top_k=2, domain_filter=None)

        # Deduplicate
        seen_ids = set()
        all_chunks = []
        for chunk in domain_chunks + general_chunks:
            if chunk.id not in seen_ids:
                seen_ids.add(chunk.id)
                all_chunks.append(chunk)

        return self.rag.format_context(all_chunks[:5])

    # ── Tool 3: Reason about job market ──────────────────────────────
    def analyze_job_market(self, domain: str, skill_level: str, years_remaining: float) -> str:
        """
        Tool 3: Retrieve and synthesize job market data for the domain.
        """
        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        data = DOMAIN_KNOWLEDGE.get(domain, {})

        analysis = [
            f"JOB MARKET ANALYSIS for {domain}:",
            f"Salary (India)   : {data.get('salary_india', 'N/A')}",
            f"Salary (Global)  : {data.get('salary_global', 'N/A')}",
            f"Target companies : {', '.join(data.get('companies', [])[:5])}",
            f"Top roles        : {', '.join(data.get('job_roles', [])[:4])}",
            f"Certifications   : {', '.join(data.get('certifications', [])[:3])}",
            "",
            f"Timeline context: {years_remaining:.1f} year(s) remaining in degree.",
        ]

        if years_remaining < 1:
            analysis.append("⚠️  URGENT: Less than 1 year left — prioritize job applications and portfolio completion NOW.")
        elif years_remaining <= 2:
            analysis.append("📋 RECOMMENDATION: Balance learning with active internship applications this semester.")
        else:
            analysis.append("✅ OPPORTUNITY: Enough time to build solid expertise. Focus on depth over breadth.")

        return "\n".join(analysis)

    # ── Tool 4: Build milestone plan ──────────────────────────────────
    def build_milestone_plan(self, domain: str, skill_level: str, years_remaining: float) -> str:
        """
        Tool 4: Generate structured milestone data from knowledge base.
        """
        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        data = DOMAIN_KNOWLEDGE.get(domain, {})
        templates = data.get("milestone_templates", [])
        yt_resources = data.get("youtube_resources", [])

        skill_start = {"beginner": 0, "intermediate": 1, "advanced": 2}.get(skill_level, 0)
        selected = templates[skill_start:]
        total_months = int(years_remaining * 12)
        months_per = max(1, total_months // max(len(selected), 1))

        plan_lines = [f"MILESTONE PLAN — {domain} ({len(selected)} phases):"]
        for i, t in enumerate(selected):
            month = (i + 1) * months_per
            # Pick 2 resources
            resources = yt_resources[:2] if yt_resources else []
            plan_lines.append(
                f"\nPhase {i+1} | By Month {month}: {t['title']}"
                f"\n  Skills  : {', '.join(t['skills'])}"
                f"\n  Projects: {', '.join(t.get('projects', []))}"
            )
            for r in resources:
                plan_lines.append(f"  Resource: {r['title']} — {r['url']}")

        return "\n".join(plan_lines)


# ─────────────────────────────────────────────────────────────────────
# LLM INTERFACE — talks to Ollama
# ─────────────────────────────────────────────────────────────────────

class OllamaLLM:
    """Interface to Ollama for local LLM inference."""

    SYSTEM_PROMPT = """You are an expert AI career counsellor for CS and IT students.
You have deep knowledge of the Indian and global tech job market, programming languages,
frameworks, learning resources, and career paths.

You are part of a multi-step reasoning agent. At each step you will:
1. Receive tool outputs (profile analysis, knowledge retrieval, job market data, milestones)
2. Reason about the information
3. Generate structured, specific, actionable career advice

Always be concrete — name specific YouTube URLs, company names, salary numbers, and timelines.
Format your final output as valid JSON when requested."""

    def __init__(self):
        self.model = OLLAMA_MODEL
        self.available = False
        self._check_availability()

    def _check_availability(self):
        """Check if Ollama is running and the model is available."""
        if not OLLAMA_AVAILABLE:
            print("⚠️  ollama Python package not installed. Run: pip install ollama")
            return

        try:
            client = ollama.Client(host=OLLAMA_HOST)
            models = client.list()
            model_names = [m.model for m in models.models]
            if any(self.model in name for name in model_names):
                self.available = True
                print(f"✅ Ollama connected | Model: {self.model}")
            else:
                print(f"⚠️  Model '{self.model}' not found in Ollama.")
                print(f"   Available models: {model_names}")
                print(f"   Run: ollama pull {self.model}")
        except Exception as e:
            print(f"⚠️  Ollama not reachable at {OLLAMA_HOST}: {e}")
            print("   Start Ollama with: ollama serve")

    def chat(self, messages: List[Dict], temperature: float = TEMPERATURE) -> str:
        """Send messages to Ollama and return response."""
        if not self.available:
            raise RuntimeError(
                f"Ollama not available. Install with: curl https://ollama.ai/install.sh | sh\n"
                f"Then run: ollama pull {self.model}"
            )

        client = ollama.Client(host=OLLAMA_HOST)
        response = client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature}
        )
        return response.message.content

    def complete(self, prompt: str, temperature: float = TEMPERATURE) -> str:
        """Simple completion interface."""
        return self.chat([
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ], temperature)


# ─────────────────────────────────────────────────────────────────────
# AGENT ORCHESTRATOR — the main multi-step reasoning loop
# ─────────────────────────────────────────────────────────────────────

class CareerCounsellorAgent:
    """
    Autonomous multi-step agent that:
    1. Analyzes the student profile (Tool 1)
    2. Retrieves relevant knowledge from Pinecone RAG (Tool 2)
    3. Analyzes job market data (Tool 3)
    4. Builds a milestone plan (Tool 4)
    5. Synthesizes everything with the LLM (Tool 5 — final reasoning)

    Each step feeds context into the next.
    Final output is a rich, LLM-generated career path grounded in RAG knowledge.
    """

    def __init__(self, rag: RAGEngine, llm: OllamaLLM):
        self.rag = rag
        self.llm = llm
        self.tools = AgentTools(rag)

    def run(
        self,
        q_result: QuestionnaireResult,
        name: str,
        current_year: int,
        total_years: int,
        degree_type: str,
        preferred_work_style: str = "both"
    ) -> Dict:
        """
        Main agent loop. Runs 5 tools in sequence, then synthesizes.
        Returns the final career path as a dictionary.
        """
        years_remaining = max(0.25, total_years - current_year + 1)

        state = AgentState(
            user_name=name,
            q_result=q_result,
            degree_info={
                "current_year": current_year,
                "total_years": total_years,
                "degree_type": degree_type,
                "preferred_work_style": preferred_work_style,
                "years_remaining": years_remaining
            }
        )

        print(f"\n🤖 Agent starting for: {name}")
        print(f"   Model: {self.llm.model} | Steps: {MAX_AGENT_STEPS}")
        print("─" * 50)

        # ── STEP 1: Profile Analysis ──────────────────────────────────
        state = self._step_analyze_profile(state)

        # ── STEP 2: Domain Decision via LLM ──────────────────────────
        state = self._step_decide_domain(state)

        # ── STEP 3: RAG Retrieval ─────────────────────────────────────
        state = self._step_retrieve_knowledge(state)

        # ── STEP 4: Job Market Analysis ───────────────────────────────
        state = self._step_analyze_job_market(state)

        # ── STEP 5: Build Milestones ──────────────────────────────────
        state = self._step_build_milestones(state)

        # ── STEP 6: Final Synthesis ───────────────────────────────────
        return self._step_synthesize(state)

    # ── Step implementations ─────────────────────────────────────────

    def _step_analyze_profile(self, state: AgentState) -> AgentState:
        print("  [Step 1] Analyzing student profile...")
        t0 = time.time()
        result = self.tools.analyze_profile(state)
        ms = int((time.time() - t0) * 1000)
        state.steps.append(ToolCall("analyze_profile", {}, result, ms))
        print(f"           ✅ Profile analyzed ({ms}ms)")
        return state

    def _step_decide_domain(self, state: AgentState) -> AgentState:
        print("  [Step 2] LLM reasoning about best domain...")
        t0 = time.time()

        profile_summary = state.steps[0].result
        top_domains = sorted(state.q_result.domain_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        domain_options = "\n".join([f"  {d}: {s:.1%}" for d, s in top_domains])

        prompt = f"""Based on this student profile, decide the BEST career domain.

STUDENT PROFILE:
{profile_summary}

TOP DOMAIN CANDIDATES (from questionnaire scoring):
{domain_options}

Reason carefully. Consider:
1. Which domain aligns best with the student's behavioral patterns?
2. Is there a clear winner or mixed signals?
3. What is the student's skill level readiness for this domain?

Respond in this exact format:
DOMAIN: <exact domain name from the candidates>
CONFIDENCE: <high/medium/low>
REASONING: <2-3 sentences explaining why this domain fits best>
SECONDARY_DOMAIN: <second best option if applicable>"""

        try:
            response = self.llm.complete(prompt, temperature=0.4)
            # Parse LLM response
            domain = self._extract_field(response, "DOMAIN")
            reasoning = self._extract_field(response, "REASONING")

            # Validate domain exists in our knowledge base
            from Recomendation.dataset import DOMAIN_KNOWLEDGE
            if domain not in DOMAIN_KNOWLEDGE:
                # Fall back to top scoring domain
                domain = top_domains[0][0]
                reasoning = f"Defaulting to highest-scored domain: {domain}"

            state.inferred_domain = domain
            state.domain_reasoning = reasoning
            ms = int((time.time() - t0) * 1000)
            state.steps.append(ToolCall("decide_domain", {"prompt_length": len(prompt)}, response, ms))
            print(f"           ✅ Domain: {domain} ({ms}ms)")

        except RuntimeError as e:
            # Ollama not available — use scoring fallback
            domain = top_domains[0][0]
            state.inferred_domain = domain
            state.domain_reasoning = f"Selected based on questionnaire scoring (LLM unavailable): {domain}"
            state.steps.append(ToolCall("decide_domain", {}, f"FALLBACK: {domain}", 0))
            print(f"           ⚠️  LLM unavailable, using scoring: {domain}")

        return state

    def _step_retrieve_knowledge(self, state: AgentState) -> AgentState:
        print("  [Step 3] RAG retrieval from Pinecone...")
        t0 = time.time()

        domain = state.inferred_domain
        interests = ", ".join(state.q_result.inferred_interests[:5])
        query = f"{domain} career path resources learning {interests}"

        context = self.tools.retrieve_knowledge(query, domain, state)
        state.retrieved_context = context

        ms = int((time.time() - t0) * 1000)
        state.steps.append(ToolCall("retrieve_knowledge", {"query": query}, context, ms))
        print(f"           ✅ Retrieved {context.count('[Source')} chunks ({ms}ms)")
        return state

    def _step_analyze_job_market(self, state: AgentState) -> AgentState:
        print("  [Step 4] Analyzing job market data...")
        t0 = time.time()

        years_remaining = state.degree_info["years_remaining"]
        result = self.tools.analyze_job_market(
            state.inferred_domain,
            state.q_result.inferred_skill_level,
            years_remaining
        )
        state.job_market_analysis = result

        ms = int((time.time() - t0) * 1000)
        state.steps.append(ToolCall("analyze_job_market", {}, result, ms))
        print(f"           ✅ Job market analyzed ({ms}ms)")
        return state

    def _step_build_milestones(self, state: AgentState) -> AgentState:
        print("  [Step 5] Building milestone plan...")
        t0 = time.time()

        years_remaining = state.degree_info["years_remaining"]
        result = self.tools.build_milestone_plan(
            state.inferred_domain,
            state.q_result.inferred_skill_level,
            years_remaining
        )

        ms = int((time.time() - t0) * 1000)
        state.steps.append(ToolCall("build_milestone_plan", {}, result, ms))
        print(f"           ✅ Milestones built ({ms}ms)")
        return state

    def _step_synthesize(self, state: AgentState) -> Dict:
        print("  [Step 6] LLM synthesizing final career path...")
        t0 = time.time()

        # Gather all tool outputs
        profile_analysis = state.steps[0].result if len(state.steps) > 0 else ""
        rag_context = state.retrieved_context or ""
        job_market = state.job_market_analysis or ""
        milestone_plan = state.steps[4].result if len(state.steps) > 4 else ""

        synthesis_prompt = f"""You have gathered the following information about a student.
Synthesize it into a comprehensive, personalized career path response.

=== STUDENT PROFILE ===
{profile_analysis}

=== RECOMMENDED DOMAIN ===
{state.inferred_domain}

=== DOMAIN REASONING ===
{state.domain_reasoning}

=== RETRIEVED KNOWLEDGE (RAG) ===
{rag_context}

=== JOB MARKET ANALYSIS ===
{job_market}

=== MILESTONE PLAN ===
{milestone_plan}

Now generate a final career path JSON with this EXACT structure (valid JSON only):
{{
  "career_goal": "<specific, inspiring goal statement>",
  "summary": "<2-3 sentence personalized summary mentioning the student by name>",
  "advice": "<personalized, motivating advice paragraph addressing the student directly>",
  "immediate_action": "<the single most important thing to do THIS WEEK>",
  "why_this_domain": "<1-2 sentences explaining why this domain fits them specifically>",
  "biggest_risk": "<the most common mistake students in this domain make>",
  "success_metric_6months": "<how to know they're on track after 6 months>"
}}"""

        try:
            response = self.llm.complete(synthesis_prompt, temperature=0.7)
            # Extract JSON from response
            parsed = self._extract_json(response)
            ms = int((time.time() - t0) * 1000)
            print(f"           ✅ Synthesis complete ({ms}ms)")
        except (RuntimeError, json.JSONDecodeError):
            # LLM fallback — generate structured response without LLM
            parsed = self._generate_fallback_synthesis(state)
            ms = 0
            print(f"           ⚠️  Using fallback synthesis (LLM unavailable)")

        state.steps.append(ToolCall("synthesize", {}, json.dumps(parsed), ms))

        # ── Combine everything into final response ────────────────────
        return self._build_final_response(state, parsed)

    def _build_final_response(self, state: AgentState, synthesis: Dict) -> Dict:
        """Assemble the complete agent response."""
        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        import random

        domain = state.inferred_domain
        data = DOMAIN_KNOWLEDGE.get(domain, {})
        years_remaining = state.degree_info["years_remaining"]
        q = state.q_result

        # Parse milestones from tool output
        milestones = self._parse_milestones_from_tool(state.steps[4].result if len(state.steps) > 4 else "", domain)

        # Essential tools
        essential_tools = []
        if not q.knows_git:
            essential_tools.append({
                "title": "Git & GitHub Complete Tutorial – Kunal Kushwaha",
                "url": "https://www.youtube.com/watch?v=apGV9Kg7ics",
                "type": "youtube", "estimated_hours": 6, "difficulty": "beginner"
            })
        else:
            essential_tools.append({
                "title": "Advanced Git Techniques – Atlassian",
                "url": "https://www.youtube.com/watch?v=0SJCsDQIkw4",
                "type": "youtube", "estimated_hours": 2, "difficulty": "intermediate"
            })
        if not q.knows_docker:
            essential_tools.append({
                "title": "Docker Tutorial for Beginners – TechWorld with Nana",
                "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
                "type": "youtube", "estimated_hours": 5, "difficulty": "beginner"
            })
        else:
            essential_tools.append({
                "title": "Docker Advanced: Multi-stage Builds – TechWorld with Nana",
                "url": "https://www.youtube.com/watch?v=sak6rCW4MaY",
                "type": "youtube", "estimated_hours": 3, "difficulty": "advanced"
            })
        essential_tools.append({
            "title": "GitHub Actions CI/CD – TechWorld with Nana",
            "url": "https://www.youtube.com/watch?v=R8_veQiYBjI",
            "type": "youtube", "estimated_hours": 3, "difficulty": "intermediate"
        })

        rng = random.Random(hash(state.user_name) % 10**8)
        companies = data.get("companies", []).copy()
        rng.shuffle(companies)

        return {
            "user_name": state.user_name,
            "path_id": self._generate_path_id(state),
            "agent_model": self.llm.model,
            "agent_steps_executed": len(state.steps),
            "rag_backend": self.rag.get_stats().get("backend", "unknown"),
            "recommended_domain": domain,
            "confidence_score": round(q.domain_scores.get(domain, 0), 3),
            "years_remaining": round(years_remaining, 1),
            "career_goal": synthesis.get("career_goal", f"Become a top {domain} professional"),
            "summary": synthesis.get("summary", ""),
            "why_this_domain": synthesis.get("why_this_domain", ""),
            "domain_reasoning": state.domain_reasoning,
            "inferred_profile": {
                "inferred_interests": q.inferred_interests,
                "skill_level": q.inferred_skill_level,
                "knows_git": q.knows_git,
                "knows_docker": q.knows_docker,
                "domain_scores": {k: round(v, 3) for k, v in
                                  sorted(q.domain_scores.items(), key=lambda x: x[1], reverse=True)},
            },
            "skill_gap_analysis": self._build_skill_gap(domain, q),
            "monthly_milestones": milestones,
            "essential_tools": essential_tools,
            "job_roles": data.get("job_roles", []),
            "salary_range_india": data.get("salary_india", ""),
            "salary_range_global": data.get("salary_global", ""),
            "top_companies_hiring": companies[:5],
            "certifications": data.get("certifications", [])[:3],
            "advice": synthesis.get("advice", ""),
            "immediate_action": synthesis.get("immediate_action", ""),
            "biggest_risk": synthesis.get("biggest_risk", ""),
            "success_metric_6months": synthesis.get("success_metric_6months", ""),
            "generated_at": datetime.now().isoformat()
        }

    # ── Utility methods ───────────────────────────────────────────────

    def _extract_field(self, text: str, field: str) -> str:
        pattern = rf"{field}:\s*(.+?)(?:\n|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extract_json(self, text: str) -> Dict:
        """Extract JSON block from LLM response."""
        # Try finding JSON block
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
        raise json.JSONDecodeError("No JSON found", text, 0)

    def _generate_fallback_synthesis(self, state: AgentState) -> Dict:
        """Generate synthesis without LLM (pure rule-based fallback)."""
        domain = state.inferred_domain
        name = state.user_name
        skill = state.q_result.inferred_skill_level
        years = state.degree_info["years_remaining"]

        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        import random
        data = DOMAIN_KNOWLEDGE.get(domain, {})
        rng = random.Random(hash(name) % 10**8)
        goal = rng.choice(data.get("career_goals", [f"Become a top {domain} professional"]))

        return {
            "career_goal": goal,
            "summary": (f"{name} is a {skill}-level student with {years:.1f} year(s) remaining, "
                        f"best matched to {domain} based on questionnaire responses. "
                        f"The path ahead is structured with clear milestones, curated resources, and realistic targets."),
            "advice": (f"Focus and consistency are your superpowers, {name}. "
                       f"Build projects, not just knowledge. Every line of code you ship publicly "
                       f"is worth more than ten tutorials watched passively."),
            "immediate_action": f"Open GitHub, create a new repo called '{domain.lower().replace(' ', '-')}-journey', and push your first project this week.",
            "why_this_domain": f"Your questionnaire answers consistently pointed toward {domain} — your curiosity, preferred work style, and dream projects all align here.",
            "biggest_risk": "Tutorial hell — watching content without building anything. Enforce a 1-project-per-milestone rule.",
            "success_metric_6months": f"After 6 months, you should have 2 deployed projects on GitHub, know the core tools of {domain}, and be ready for your first internship application."
        }

    def _build_skill_gap(self, domain: str, q: QuestionnaireResult) -> Dict:
        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        data = DOMAIN_KNOWLEDGE.get(domain, {})
        required = data.get("core_skills", [])
        user_langs = set(l.lower() for l in [])

        gap = {}
        for i, skill in enumerate(required):
            sl = skill.lower()
            if skill in ["Git", "GitHub"] and q.knows_git:
                gap[skill] = "already known ✅"
            elif skill == "Docker" and q.knows_docker:
                gap[skill] = "already known ✅"
            elif q.inferred_skill_level == "beginner" and i < 3:
                gap[skill] = "critical — start immediately 🔴"
            elif q.inferred_skill_level == "intermediate" and i >= 2:
                gap[skill] = "high priority 🟠"
            else:
                gap[skill] = "medium priority 🟡"
        return gap

    def _parse_milestones_from_tool(self, tool_output: str, domain: str) -> List[Dict]:
        """Parse milestone plan tool output into structured list."""
        from Recomendation.dataset import DOMAIN_KNOWLEDGE
        import random
        data = DOMAIN_KNOWLEDGE.get(domain, {})
        templates = data.get("milestone_templates", [])
        yt = data.get("youtube_resources", [])
        rng = random.Random(hash(domain) % 10**8)

        milestones = []
        for i, t in enumerate(templates):
            shuffled = yt.copy()
            rng.shuffle(shuffled)
            milestones.append({
                "phase": i + 1,
                "title": t["title"],
                "skills_to_gain": t["skills"],
                "projects": t.get("projects", []),
                "resources": [
                    {"title": r["title"], "url": r["url"],
                     "estimated_hours": r["hours"], "difficulty": r["difficulty"]}
                    for r in shuffled[:2]
                ]
            })
        return milestones

    def _generate_path_id(self, state: AgentState) -> str:
        import hashlib
        seed = f"{state.user_name}{state.inferred_domain}{datetime.now().microsecond}"
        return hashlib.md5(seed.encode()).hexdigest()[:10].upper()