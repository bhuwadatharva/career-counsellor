"""
questionnaire.py — Smart Questionnaire Engine

Instead of asking "what are your interests?", we ask behavioral/situational
questions and INFER interests, domain affinity, and skill level from answers.

Each question has weighted answer-to-domain mappings.
The engine accumulates domain scores across all answers.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Option:
    id: str          # e.g. "A", "B", "C", "D"
    text: str
    domain_weights: Dict[str, float]   # domain → score boost
    skill_hint: Optional[str] = None   # "beginner", "intermediate", "advanced"
    interest_tags: List[str] = field(default_factory=list)


@dataclass
class Question:
    id: str
    category: str    # "curiosity", "style", "tools", "scenario", "background"
    text: str
    subtitle: str
    options: List[Option]
    multi_select: bool = False   # can pick more than one option


# ─────────────────────────────────────────────────────────────────────────────
# THE QUESTIONNAIRE  (15 questions, covers all 10 domains)
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS: List[Question] = [

    # Q1 ── What got you into CS/IT?
    Question(
        id="Q1",
        category="background",
        text="What first got you excited about computers and technology?",
        subtitle="Pick the one that feels most like you.",
        options=[
            Option("A", "I loved playing video games and wondered how they were built.",
                   {"Game Development": 8, "Full Stack Web Development": 2},
                   interest_tags=["Gaming", "Game Development"]),
            Option("B", "I was always curious about how websites and apps work.",
                   {"Full Stack Web Development": 8, "Mobile App Development": 4},
                   interest_tags=["Web Development", "Mobile Apps"]),
            Option("C", "I was fascinated by hacking, security exploits, and how systems can be broken or protected.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Ethical Hacking"]),
            Option("D", "I got hooked on data — finding patterns, making predictions, understanding the world through numbers.",
                   {"Machine Learning & AI": 8, "Data Engineering": 5},
                   interest_tags=["Machine Learning", "Data Science"]),
        ]
    ),

    # Q2 ── Free time activity
    Question(
        id="Q2",
        category="curiosity",
        text="On a Sunday with nothing to do, you'd most naturally spend time...",
        subtitle="Be honest — there's no right answer.",
        options=[
            Option("A", "Tinkering with hardware, a Raspberry Pi, or some IoT gadget.",
                   {"Embedded Systems & IoT": 10, "Cloud & DevOps Engineering": 2},
                   interest_tags=["IoT", "Embedded Systems", "Hardware"]),
            Option("B", "Building or designing a side project — an app, website, or tool.",
                   {"Full Stack Web Development": 7, "Mobile App Development": 5},
                   interest_tags=["Web Development", "Mobile Apps"]),
            Option("C", "Reading about AI research, watching ML papers get explained, or trying out new models.",
                   {"Machine Learning & AI": 9, "AI Research & NLP": 8},
                   interest_tags=["AI/ML", "Research", "NLP"]),
            Option("D", "Playing with cloud infra, Docker containers, or automating something annoying.",
                   {"Cloud & DevOps Engineering": 10},
                   interest_tags=["Cloud", "DevOps", "Docker"]),
        ]
    ),

    # Q3 ── Dream project
    Question(
        id="Q3",
        category="scenario",
        text="If you had 3 months to build anything — what would you build?",
        subtitle="Don't think too hard. Go with your gut.",
        options=[
            Option("A", "A multiplayer online game with custom mechanics and graphics.",
                   {"Game Development": 10, "Full Stack Web Development": 2},
                   interest_tags=["Game Development", "Unity"]),
            Option("B", "An AI assistant or chatbot that actually understands context.",
                   {"Machine Learning & AI": 7, "AI Research & NLP": 9},
                   interest_tags=["AI/ML", "NLP", "LLM"]),
            Option("C", "A DeFi protocol or NFT platform on a blockchain.",
                   {"Blockchain Development": 10},
                   interest_tags=["Blockchain", "Web3", "DeFi"]),
            Option("D", "A full-featured SaaS product — dashboard, auth, payments, the works.",
                   {"Full Stack Web Development": 10, "Cloud & DevOps Engineering": 4},
                   interest_tags=["Web Development", "Backend", "Cloud"]),
        ]
    ),

    # Q4 ── What kind of problems excite you
    Question(
        id="Q4",
        category="curiosity",
        text="What kind of technical problem makes you lose track of time?",
        subtitle="The one where you blink and 3 hours have passed.",
        options=[
            Option("A", "Optimizing a slow query or pipeline — squeezing every millisecond.",
                   {"Data Engineering": 9, "Cloud & DevOps Engineering": 5},
                   interest_tags=["Databases", "Data Engineering", "SQL"]),
            Option("B", "Making a UI pixel-perfect and buttery smooth.",
                   {"Full Stack Web Development": 9, "Mobile App Development": 6},
                   interest_tags=["Frontend", "UI/UX", "Mobile Apps"]),
            Option("C", "Figuring out how to make a model smarter, more accurate, or more efficient.",
                   {"Machine Learning & AI": 10, "AI Research & NLP": 7},
                   interest_tags=["Machine Learning", "Deep Learning", "AI/ML"]),
            Option("D", "Reverse-engineering how a system works, finding its weak points.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Penetration Testing", "Security"]),
        ]
    ),

    # Q5 ── Work environment preference
    Question(
        id="Q5",
        category="style",
        text="What kind of work environment sounds most like your ideal?",
        subtitle="Where would you thrive?",
        options=[
            Option("A", "A research lab or AI team — deep technical work, paper reading, experiments.",
                   {"Machine Learning & AI": 6, "AI Research & NLP": 10},
                   interest_tags=["Research", "NLP", "AI/ML"], skill_hint="advanced"),
            Option("B", "A fast-moving startup — shipping features, full ownership, wearing many hats.",
                   {"Full Stack Web Development": 7, "Mobile App Development": 5, "Cloud & DevOps Engineering": 3},
                   interest_tags=["Web Development", "Mobile Apps"]),
            Option("C", "A security team — red team/blue team, threat hunting, incident response.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Security", "Networking"]),
            Option("D", "Infrastructure / platform team — everything runs because of you, even if no one sees you.",
                   {"Cloud & DevOps Engineering": 10},
                   interest_tags=["DevOps", "Cloud", "Kubernetes"], skill_hint="intermediate"),
        ]
    ),

    # Q6 ── Technology that fascinates you most
    Question(
        id="Q6",
        category="curiosity",
        text="Which of these technologies fascinates you the most right now?",
        subtitle="Pick the one you'd click on if you saw it on YouTube.",
        options=[
            Option("A", "Large Language Models (ChatGPT, Claude, Gemini) and how they work internally.",
                   {"Machine Learning & AI": 7, "AI Research & NLP": 10},
                   interest_tags=["LLM", "NLP", "Transformers", "Research"]),
            Option("B", "Kubernetes, Terraform, and cloud-native infrastructure.",
                   {"Cloud & DevOps Engineering": 10},
                   interest_tags=["Kubernetes", "Cloud", "DevOps", "CI/CD"]),
            Option("C", "Blockchain, smart contracts, and decentralized systems.",
                   {"Blockchain Development": 10},
                   interest_tags=["Blockchain", "Web3", "Smart Contracts"]),
            Option("D", "Mobile apps and how they work across iOS and Android.",
                   {"Mobile App Development": 10},
                   interest_tags=["Mobile Apps", "Android", "iOS", "Flutter"]),
        ]
    ),

    # Q7 ── Coding style
    Question(
        id="Q7",
        category="style",
        text="When you write code, what describes you best?",
        subtitle="Pick the most accurate description.",
        options=[
            Option("A", "I love making things look great — I care about UI, animations, and user experience.",
                   {"Full Stack Web Development": 8, "Mobile App Development": 6},
                   interest_tags=["Frontend", "UI/UX"]),
            Option("B", "I'm obsessed with efficiency — algorithms, data structures, performance.",
                   {"Machine Learning & AI": 5, "Data Engineering": 6, "Embedded Systems & IoT": 7},
                   interest_tags=["Algorithms", "Data Science"], skill_hint="intermediate"),
            Option("C", "I like systems thinking — how components connect, scale, and fail gracefully.",
                   {"Cloud & DevOps Engineering": 9, "Data Engineering": 5},
                   interest_tags=["DevOps", "Cloud", "Infrastructure"]),
            Option("D", "I like experimenting — trying new libraries, breaking things, learning from errors.",
                   {"Machine Learning & AI": 6, "Blockchain Development": 4, "Full Stack Web Development": 4},
                   interest_tags=["Machine Learning", "Blockchain", "Web Development"]),
        ]
    ),

    # Q8 ── Which course would you actually finish
    Question(
        id="Q8",
        category="scenario",
        text="You have 4 weeks free. Which course would you actually complete?",
        subtitle="Be realistic — pick what you'd genuinely stick with.",
        options=[
            Option("A", "Complete Python for Data Science & Machine Learning Bootcamp.",
                   {"Machine Learning & AI": 9, "Data Engineering": 5},
                   interest_tags=["Machine Learning", "Data Science", "Python"]),
            Option("B", "The Web Developer Bootcamp — HTML, CSS, JS, Node, MongoDB.",
                   {"Full Stack Web Development": 10},
                   interest_tags=["Web Development", "JavaScript", "Node.js"]),
            Option("C", "AWS Certified Solutions Architect course.",
                   {"Cloud & DevOps Engineering": 10},
                   interest_tags=["AWS", "Cloud", "DevOps"]),
            Option("D", "Ethical Hacking A-Z: From Zero to Bug Bounty.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Ethical Hacking", "Linux"]),
        ]
    ),

    # Q9 ── Favourite thing to talk about in tech
    Question(
        id="Q9",
        category="curiosity",
        text="At a tech meetup, what topic would you most enjoy talking about?",
        subtitle="The conversation you could have for hours.",
        options=[
            Option("A", "The future of AI — AGI, autonomous agents, AI safety.",
                   {"Machine Learning & AI": 7, "AI Research & NLP": 9},
                   interest_tags=["AI/ML", "Research", "NLP", "LLM"]),
            Option("B", "Real-time data pipelines and how companies like Uber process billions of events.",
                   {"Data Engineering": 10},
                   interest_tags=["Data Engineering", "Big Data", "Databases"]),
            Option("C", "Game physics, rendering engines, or how AAA games are made.",
                   {"Game Development": 10},
                   interest_tags=["Game Development", "3D", "Unity"]),
            Option("D", "Smart devices, edge computing, and the future of connected hardware.",
                   {"Embedded Systems & IoT": 10},
                   interest_tags=["IoT", "Embedded Systems", "Hardware"]),
        ]
    ),

    # Q10 ── Which person's career path excites you most
    Question(
        id="Q10",
        category="scenario",
        text="Whose career story excites you the most?",
        subtitle="Don't overthink — just pick your gut reaction.",
        options=[
            Option("A", "A developer who built a viral indie game solo and now makes passive income from it.",
                   {"Game Development": 10},
                   interest_tags=["Game Development", "Gaming"]),
            Option("B", "A security researcher who found a critical vulnerability in a major app and got paid $50K.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Penetration Testing", "Security"]),
            Option("C", "An ML engineer who built the recommendation system used by millions of people.",
                   {"Machine Learning & AI": 10},
                   interest_tags=["Machine Learning", "Deep Learning", "AI/ML"]),
            Option("D", "A blockchain developer who launched a DeFi protocol with $100M+ TVL.",
                   {"Blockchain Development": 10},
                   interest_tags=["Blockchain", "Web3", "DeFi", "Smart Contracts"]),
        ]
    ),

    # Q11 ── Skill self-assessment
    Question(
        id="Q11",
        category="background",
        text="How would you honestly describe your current coding skill level?",
        subtitle="This helps calibrate the depth of your path.",
        options=[
            Option("A", "I'm just starting out — I know some basics but haven't built real projects.",
                   {}, skill_hint="beginner"),
            Option("B", "I can build small projects, I know one or two languages reasonably well.",
                   {}, skill_hint="beginner"),
            Option("C", "I've built real projects, I'm comfortable with databases, APIs, and version control.",
                   {}, skill_hint="intermediate"),
            Option("D", "I'm advanced — I've worked on production systems, know design patterns, and I'm confident with complex architectures.",
                   {}, skill_hint="advanced"),
        ]
    ),

    # Q12 ── Tool familiarity
    Question(
        id="Q12",
        category="tools",
        text="Which of these tools or concepts are you already comfortable with?",
        subtitle="Pick all that apply.",
        multi_select=True,
        options=[
            Option("A", "Git & GitHub (commits, branches, pull requests)",
                   {"Cloud & DevOps Engineering": 1, "Full Stack Web Development": 1},
                   interest_tags=["Git"]),
            Option("B", "Docker (building images, running containers)",
                   {"Cloud & DevOps Engineering": 3},
                   interest_tags=["Docker"]),
            Option("C", "SQL (writing queries, joins, subqueries)",
                   {"Data Engineering": 3, "Full Stack Web Development": 1},
                   interest_tags=["SQL", "Databases"]),
            Option("D", "None of the above — these are new to me.",
                   {}, skill_hint="beginner"),
        ]
    ),

    # Q13 ── What frustrates you about tech
    Question(
        id="Q13",
        category="style",
        text="What frustrates you most when learning something new in tech?",
        subtitle="Your answer reveals how you like to learn.",
        options=[
            Option("A", "Too much theory, not enough building — I learn by doing.",
                   {"Full Stack Web Development": 4, "Game Development": 4, "Mobile App Development": 4},
                   interest_tags=["Web Development", "Mobile Apps"]),
            Option("B", "Not understanding the 'why' behind something — I need the math/theory to click first.",
                   {"Machine Learning & AI": 5, "AI Research & NLP": 6, "Data Engineering": 3},
                   interest_tags=["Research", "Machine Learning"], skill_hint="intermediate"),
            Option("C", "Poor tooling or documentation — I'm productive with good tools and miserable without them.",
                   {"Cloud & DevOps Engineering": 5, "Data Engineering": 4},
                   interest_tags=["DevOps", "Cloud"]),
            Option("D", "Security vulnerabilities — every tutorial feels like it ignores real-world risks.",
                   {"Cybersecurity": 7},
                   interest_tags=["Cybersecurity", "Security"]),
        ]
    ),

    # Q14 ── 5-year vision
    Question(
        id="Q14",
        category="scenario",
        text="Where do you see yourself in 5 years?",
        subtitle="Dream big — what's the version of you that makes you proud?",
        options=[
            Option("A", "Leading the backend/infrastructure team at a unicorn startup.",
                   {"Cloud & DevOps Engineering": 7, "Full Stack Web Development": 5},
                   interest_tags=["DevOps", "Backend", "Cloud"]),
            Option("B", "Publishing AI research or building products that use cutting-edge ML.",
                   {"Machine Learning & AI": 7, "AI Research & NLP": 9},
                   interest_tags=["Research", "AI/ML", "NLP"]),
            Option("C", "Running my own tech product — a SaaS, a game, or a DeFi protocol.",
                   {"Full Stack Web Development": 5, "Game Development": 4, "Blockchain Development": 4},
                   interest_tags=["Web Development", "Blockchain", "Gaming"]),
            Option("D", "Being the go-to security expert at a top firm or doing independent research.",
                   {"Cybersecurity": 10},
                   interest_tags=["Cybersecurity", "Security", "Penetration Testing"]),
        ]
    ),

    # Q15 ── Last question: biggest strength
    Question(
        id="Q15",
        category="background",
        text="What's your single biggest technical strength right now?",
        subtitle="Be honest — this shapes your path.",
        options=[
            Option("A", "I'm great at logic, math, and algorithmic thinking.",
                   {"Machine Learning & AI": 6, "Data Engineering": 4, "AI Research & NLP": 5},
                   interest_tags=["Algorithms", "Machine Learning"], skill_hint="intermediate"),
            Option("B", "I pick up languages and frameworks fast — I'm a quick learner.",
                   {"Full Stack Web Development": 5, "Mobile App Development": 4, "Blockchain Development": 3},
                   interest_tags=["Web Development", "Mobile Apps"]),
            Option("C", "I understand systems deeply — networking, OS concepts, how things run under the hood.",
                   {"Cybersecurity": 6, "Cloud & DevOps Engineering": 6, "Embedded Systems & IoT": 5},
                   interest_tags=["Networking", "Linux", "DevOps"]),
            Option("D", "I'm creative — I come up with ideas, design UIs, and think about user experience.",
                   {"Full Stack Web Development": 7, "Game Development": 5, "Mobile App Development": 5},
                   interest_tags=["UI/UX", "Frontend", "Gaming"]),
        ]
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# Score Aggregator
# ─────────────────────────────────────────────────────────────────────────────

ALL_DOMAINS = [
    "Full Stack Web Development",
    "Machine Learning & AI",
    "Cybersecurity",
    "Cloud & DevOps Engineering",
    "Mobile App Development",
    "Data Engineering",
    "Blockchain Development",
    "Game Development",
    "Embedded Systems & IoT",
    "AI Research & NLP",
]


@dataclass
class QuestionnaireResult:
    domain_scores: Dict[str, float]
    inferred_interests: List[str]
    inferred_skill_level: str
    knows_git: bool
    knows_docker: bool
    top_domain: str
    confidence: float
    answer_summary: Dict[str, str]  # question_id -> chosen option text


def aggregate_answers(answers: Dict[str, List[str]]) -> QuestionnaireResult:
    """
    answers: { "Q1": ["A"], "Q2": ["B"], "Q12": ["A", "C"], ... }
    Returns aggregated domain scores, inferred interests, skill level.
    """
    domain_scores = {d: 0.0 for d in ALL_DOMAINS}
    interest_tags = []
    skill_hints = []
    knows_git = False
    knows_docker = False
    answer_summary = {}

    question_map = {q.id: q for q in QUESTIONS}

    for q_id, selected_option_ids in answers.items():
        question = question_map.get(q_id)
        if not question:
            continue

        option_map = {opt.id: opt for opt in question.options}

        for opt_id in selected_option_ids:
            option = option_map.get(opt_id)
            if not option:
                continue

            # Accumulate domain weights
            for domain, weight in option.domain_weights.items():
                if domain in domain_scores:
                    domain_scores[domain] += weight

            # Collect interest tags
            interest_tags.extend(option.interest_tags)

            # Collect skill hints
            if option.skill_hint:
                skill_hints.append(option.skill_hint)

            # Detect Git/Docker knowledge from Q12
            if q_id == "Q12":
                if opt_id == "A":
                    knows_git = True
                if opt_id == "B":
                    knows_docker = True

            # Build answer summary
            if q_id not in answer_summary:
                answer_summary[q_id] = option.text
            else:
                answer_summary[q_id] += f" | {option.text}"

    # Deduplicate interest tags, preserve order
    seen = set()
    unique_interests = []
    for tag in interest_tags:
        if tag not in seen:
            seen.add(tag)
            unique_interests.append(tag)

    # Infer skill level from hints
    skill_level = _infer_skill_level(skill_hints)

    # Normalize domain scores
    total = sum(domain_scores.values()) or 1
    normalized = {d: round(s / total, 4) for d, s in domain_scores.items()}

    # Top domain
    sorted_domains = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
    top_domain, confidence = sorted_domains[0]

    return QuestionnaireResult(
        domain_scores=normalized,
        inferred_interests=unique_interests[:8],  # cap at 8
        inferred_skill_level=skill_level,
        knows_git=knows_git,
        knows_docker=knows_docker,
        top_domain=top_domain,
        confidence=confidence,
        answer_summary=answer_summary
    )


def _infer_skill_level(hints: List[str]) -> str:
    if not hints:
        return "beginner"
    counts = {"beginner": 0, "intermediate": 0, "advanced": 0}
    for h in hints:
        if h in counts:
            counts[h] += 1
    # Weight: advanced > intermediate > beginner
    if counts["advanced"] >= 1:
        return "advanced"
    if counts["intermediate"] >= 2:
        return "intermediate"
    if counts["intermediate"] == 1 and counts["beginner"] <= 1:
        return "intermediate"
    return "beginner"


def get_questions_for_api() -> list:
    """Serialize questions for API response."""
    result = []
    for q in QUESTIONS:
        result.append({
            "id": q.id,
            "category": q.category,
            "text": q.text,
            "subtitle": q.subtitle,
            "multi_select": q.multi_select,
            "options": [
                {"id": opt.id, "text": opt.text}
                for opt in q.options
            ]
        })
    return result