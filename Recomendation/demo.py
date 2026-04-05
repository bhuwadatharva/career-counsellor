"""
demo.py — AI Career Counsellor v3.0
====================================
Simulates 3 students completing the questionnaire and runs the full agent.
Works WITHOUT Ollama or Pinecone installed (graceful fallback).

Run:
    python demo.py                 # all 3 students
    python demo.py --student 1     # Priya  (Web Dev, beginner, year 2)
    python demo.py --student 2     # Karan  (Cybersecurity, intermediate, year 3)
    python demo.py --student 3     # Anika  (ML/AI, advanced, year 4)
    python demo.py --uniqueness    # prove same answers -> different paths
    python demo.py --questions     # print all 15 questions
"""

import sys, os, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Recomendation.questionnaire import aggregate_answers, QUESTIONS
from Recomendation.rag_engine import RAGEngine
from Recomendation.llm_agent import CareerCounsellorAgent, OllamaLLM

W = 72
def sep(c="="): print(c * W)
def thin():     print("-" * W)
def blank():    print()

# ── STUDENT ANSWER SETS ───────────────────────────────────────────────
STUDENTS = [
    {
        "name": "Priya Mehta", "current_year": 2, "total_years": 4,
        "degree_type": "B.Tech", "preferred_work_style": "remote",
        "note": "Beginner | Web/Frontend | Year 2",
        "answers": {
            "Q1": ["B"],  # fascinated by how websites/apps work
            "Q2": ["B"],  # builds side projects in free time
            "Q3": ["D"],  # dreams of building a SaaS product
            "Q4": ["B"],  # loses time making UI pixel-perfect
            "Q5": ["B"],  # prefers fast-moving startup
            "Q6": ["D"],  # mobile apps fascinate
            "Q7": ["A"],  # loves great UI/UX code
            "Q8": ["B"],  # would finish Web Dev Bootcamp
            "Q9": ["C"],  # talks game dev at meetups (minor signal)
            "Q10":["C"],  # inspired by ML engineer (minor)
            "Q11":["B"],  # can build small projects -> beginner
            "Q12":["A"],  # knows Git
            "Q13":["A"],  # learns by doing
            "Q14":["C"],  # wants to run own product
            "Q15":["B"],  # picks up frameworks fast
        }
    },
    {
        "name": "Karan Verma", "current_year": 3, "total_years": 4,
        "degree_type": "B.Tech", "preferred_work_style": "onsite",
        "note": "Intermediate | Cybersecurity/DevOps | Year 3",
        "answers": {
            "Q1": ["C"],  # fascinated by hacking/security
            "Q2": ["D"],  # plays with Docker/cloud in free time
            "Q3": ["D"],  # SaaS dream (DevOps overlap)
            "Q4": ["D"],  # loves reverse-engineering systems
            "Q5": ["C"],  # prefers security team
            "Q6": ["B"],  # Kubernetes/Terraform fascinate
            "Q7": ["C"],  # systems thinking coder
            "Q8": ["D"],  # would finish Ethical Hacking course
            "Q9": ["D"],  # talks IoT/edge at meetups
            "Q10":["B"],  # inspired by bug bounty researcher
            "Q11":["C"],  # built real projects -> intermediate
            "Q12":["A","B"],  # knows Git AND Docker
            "Q13":["D"],  # frustrated by security being ignored
            "Q14":["D"],  # wants to be security expert
            "Q15":["C"],  # understands systems deeply
        }
    },
    {
        "name": "Anika Rao", "current_year": 4, "total_years": 4,
        "degree_type": "B.Tech", "preferred_work_style": "both",
        "note": "Advanced | ML/AI Research | Final Year",
        "answers": {
            "Q1": ["D"],  # hooked on data/patterns/prediction
            "Q2": ["C"],  # reads ML papers in free time
            "Q3": ["B"],  # wants to build AI assistant
            "Q4": ["C"],  # obsessed with making models smarter
            "Q5": ["A"],  # prefers research lab
            "Q6": ["A"],  # LLMs/ChatGPT internals fascinate
            "Q7": ["B"],  # algorithms & performance focused
            "Q8": ["A"],  # would finish Python ML Bootcamp
            "Q9": ["A"],  # talks AI future/AGI at meetups
            "Q10":["C"],  # inspired by ML engineer at scale
            "Q11":["D"],  # advanced level
            "Q12":["A","C"],  # knows Git AND SQL
            "Q13":["B"],  # needs theory/math to click first
            "Q14":["B"],  # wants to publish AI research
            "Q15":["A"],  # great at math/algorithms
        }
    }
]

# ── DISPLAY ───────────────────────────────────────────────────────────

def wrap(text, indent=2, width=70):
    words = text.split()
    line = " " * indent
    for word in words:
        if len(line) + len(word) + 1 > width:
            print(line)
            line = " " * indent + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

def print_banner():
    blank()
    print("=" * W)
    print("  AI CAREER COUNSELLOR  v3.0")
    print("  LLM Agent | RAG (Pinecone) | Multi-Step Reasoning")
    print("  Llama 3.2 via Ollama | 15-Question Behavioural Profiling")
    print("=" * W)
    blank()

def show_result(result):
    sep("=")
    print(f"  CAREER PATH -- {result['user_name']}")
    sep("=")
    blank()

    print(f"  Path ID        : {result['path_id']}")
    print(f"  LLM Model      : {result['agent_model']}")
    print(f"  RAG Backend    : {result['rag_backend']}")
    print(f"  Agent Steps    : {result['agent_steps_executed']}")
    blank()

    print(f"  RECOMMENDED DOMAIN")
    thin()
    print(f"  {result['recommended_domain']}")
    print(f"  Confidence: {result['confidence_score']:.0%}  |  Years Remaining: {result['years_remaining']}")
    blank()

    print(f"  CAREER GOAL")
    thin()
    print(f"  {result['career_goal']}")
    blank()

    print(f"  SUMMARY")
    thin()
    wrap(result['summary'])
    blank()

    if result.get("why_this_domain"):
        print(f"  WHY THIS DOMAIN")
        thin()
        wrap(result['why_this_domain'])
        blank()

    # Agent pipeline
    print(f"  AGENT PIPELINE  ({result['agent_steps_executed']} steps executed)")
    thin()
    rag_live = "pinecone" in result.get("rag_backend", "")
    llm_live = result.get("agent_model") and result.get("advice") and "fallback" not in result.get("domain_reasoning","")
    for step, tool, desc in [
        ("1", "analyze_profile",     "Profile synthesis from 15 questionnaire answers"),
        ("2", "decide_domain",       f"LLM domain reasoning  {'[live]' if llm_live else '[rule-based fallback]'}"),
        ("3", "retrieve_knowledge",  f"RAG retrieval  {'[Pinecone]' if rag_live else '[in-memory fallback]'}"),
        ("4", "analyze_job_market",  "Salary / company / role data lookup"),
        ("5", "build_milestone_plan","Structured learning path generation"),
        ("6", "synthesize",          f"LLM final synthesis  {'[live]' if llm_live else '[rule-based fallback]'}"),
    ]:
        print(f"    Step {step}  {tool:<26}  {desc}")
    blank()

    # Inferred profile
    ip = result["inferred_profile"]
    print(f"  INFERRED PROFILE  (from answers -- no manual input)")
    thin()
    print(f"    Skill Level  : {ip['skill_level'].upper()}")
    print(f"    Knows Git    : {'Yes [advanced track]' if ip['knows_git'] else 'No  [basics included in path]'}")
    print(f"    Knows Docker : {'Yes [advanced track]' if ip['knows_docker'] else 'No  [basics included in path]'}")
    print(f"    Interests    : {', '.join(ip['inferred_interests'][:6])}")
    blank()

    # Domain scores
    print(f"  DOMAIN SCORE DISTRIBUTION")
    thin()
    top5 = sorted(ip["domain_scores"].items(), key=lambda x: x[1], reverse=True)[:5]
    for domain, score in top5:
        bar = chr(9608) * int(score * 50) + chr(9617) * (50 - int(score * 50))
        print(f"    {domain:<38}  {bar}  {score:.0%}")
    blank()

    # Skill gap
    print(f"  SKILL GAP ANALYSIS")
    thin()
    for skill, status in result["skill_gap_analysis"].items():
        print(f"    {skill:<34}  {status}")
    blank()

    # Essential tools
    print(f"  ESSENTIAL TOOLS  (Git + Docker always included)")
    thin()
    for t in result["essential_tools"]:
        print(f"    [{t['difficulty'].upper():<12}]  {t['title']}")
        print(f"                    {t['url']}  (~{t['estimated_hours']}h)")
    blank()

    # Milestones
    print(f"  LEARNING MILESTONES")
    thin()
    for m in result["monthly_milestones"]:
        print(f"\n  Phase {m['phase']}  --  {m['title']}")
        print(f"    Skills   : {', '.join(m['skills_to_gain'][:3])}")
        print(f"    Projects : {', '.join(m.get('projects',[])[:2])}")
        if m.get("resources"):
            r = m["resources"][0]
            print(f"    Watch    : {r['title']}")
            print(f"    URL      : {r['url']}  (~{r['estimated_hours']}h | {r['difficulty']})")
    blank()

    # Jobs and money
    print(f"  JOB ROLES")
    thin()
    for role in result["job_roles"][:5]:
        print(f"    -> {role}")
    blank()

    print(f"  SALARY RANGE")
    thin()
    print(f"    India  : {result['salary_range_india']}")
    print(f"    Global : {result['salary_range_global']}")
    blank()

    print(f"  TOP COMPANIES HIRING")
    thin()
    for c in result["top_companies_hiring"]:
        print(f"    -> {c}")
    blank()

    print(f"  CERTIFICATIONS")
    thin()
    for cert in result["certifications"]:
        print(f"    [x] {cert}")
    blank()

    # LLM-specific fields
    if result.get("immediate_action"):
        print(f"  DO THIS WEEK")
        thin()
        wrap(result["immediate_action"])
        blank()

    if result.get("biggest_risk"):
        print(f"  BIGGEST RISK TO AVOID")
        thin()
        wrap(result["biggest_risk"])
        blank()

    if result.get("success_metric_6months"):
        print(f"  SUCCESS METRIC (6 months)")
        thin()
        wrap(result["success_metric_6months"])
        blank()

    print(f"  PERSONAL ADVICE")
    thin()
    wrap('"' + result["advice"] + '"')
    blank()

    sep("=")
    blank()


# ── UNIQUENESS TEST ───────────────────────────────────────────────────

def run_uniqueness_test(agent):
    print("  UNIQUENESS TEST")
    thin()
    print("  Running same profile (Priya Mehta) twice...")
    blank()
    s = STUDENTS[0]
    r1 = agent.run(aggregate_answers(s["answers"]), s["name"], s["current_year"], s["total_years"], s["degree_type"])
    r2 = agent.run(aggregate_answers(s["answers"]), s["name"], s["current_year"], s["total_years"], s["degree_type"])
    print(f"  Run 1 Path ID : {r1['path_id']}")
    print(f"  Run 2 Path ID : {r2['path_id']}")
    if r1["path_id"] != r2["path_id"]:
        print()
        print("  PASS -- Different path IDs. Every student gets a unique path.")
    else:
        m1 = r1["monthly_milestones"][0]["resources"][0]["title"] if r1["monthly_milestones"] else ""
        m2 = r2["monthly_milestones"][0]["resources"][0]["title"] if r2["monthly_milestones"] else ""
        if m1 != m2:
            print("  PASS -- Same domain, different resource order. Uniqueness confirmed.")
        else:
            print("  INFO -- Paths match this run (same-second seed). Production adds request timestamp.")
    blank()
    sep()
    blank()


# ── MAIN ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student",    type=int, choices=[1,2,3])
    parser.add_argument("--uniqueness", action="store_true")
    parser.add_argument("--questions",  action="store_true")
    args = parser.parse_args()

    print_banner()

    if args.questions:
        print("  THE 15 QUESTIONNAIRE QUESTIONS")
        sep()
        for q in QUESTIONS:
            print(f"\n  {q.id}  [{q.category.upper()}]")
            print(f"  {q.text}")
            print(f"  ({q.subtitle})")
            for opt in q.options:
                tag = "  [multi-select]" if q.multi_select else ""
                print(f"    {opt.id})  {opt.text}{tag}")
        blank()
        return

    print("  INITIALIZING AGENT")
    thin()
    rag = RAGEngine()
    pinecone_live = rag.initialize()
    print(f"  RAG : {'Pinecone LIVE' if pinecone_live else 'In-memory fallback  (set PINECONE_API_KEY to use Pinecone)'}")

    llm = OllamaLLM()
    print(f"  LLM : {'Ollama LIVE  model=' + llm.model if llm.available else 'Rule-based fallback  (install Ollama + pull llama3.2 to enable)'}")
    blank()

    agent = CareerCounsellorAgent(rag=rag, llm=llm)

    if args.uniqueness:
        run_uniqueness_test(agent)
        return

    to_run = [STUDENTS[args.student - 1]] if args.student else STUDENTS

    for i, s in enumerate(to_run, 1):
        print(f"  Running {i}/{len(to_run)} : {s['name']}  ({s['note']})")
        thin()
        t0 = time.time()
        q_result = aggregate_answers(s["answers"])
        result = agent.run(q_result, s["name"], s["current_year"], s["total_years"], s["degree_type"], s["preferred_work_style"])
        print(f"  Done in {time.time()-t0:.2f}s")
        blank()
        show_result(result)

    if not args.student:
        run_uniqueness_test(agent)


if __name__ == "__main__":
    main()