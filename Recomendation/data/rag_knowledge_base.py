# rag_knowledge_base.py
# Documents to embed and store in Pinecone for RAG retrieval

RAG_DOCUMENTS = [

    # ── DOMAIN OVERVIEWS ─────────────────────────────────────────────
    {
        "id": "dom_webdev_001",
        "category": "domain_overview",
        "domain": "Full Stack Web Development",
        "text": """Full Stack Web Development covers both frontend (what users see) and backend (server, database, APIs).
        Key technologies: HTML, CSS, JavaScript, React or Vue for frontend, Node.js or Django for backend,
        PostgreSQL or MongoDB for databases. Full stack developers are among the most in-demand professionals
        in India and globally. Entry salary in India ranges from ₹5-8 LPA at service companies to ₹8-20 LPA
        at product startups like Zepto, Razorpay, Swiggy. Global salary: $60K-$140K USD.
        Core skills to master: React, TypeScript, REST APIs, SQL, Git, Docker, CI/CD with GitHub Actions.
        The MERN stack (MongoDB, Express, React, Node) and the T3 stack (TypeScript, Tailwind, tRPC) are
        popular choices for modern full stack development."""
    },
    {
        "id": "dom_ml_001",
        "category": "domain_overview",
        "domain": "Machine Learning & AI",
        "text": """Machine Learning and AI is one of the fastest growing and highest paying domains in tech.
        Python is the primary language. Core libraries: NumPy, Pandas, Scikit-learn, PyTorch, TensorFlow.
        Specializations include Computer Vision, NLP, Reinforcement Learning, and MLOps.
        Entry salary in India: ₹8-15 LPA at product companies, ₹20-40 LPA at AI-first companies.
        Global salary: $80K-$180K USD. Top employers: Google DeepMind, OpenAI, Microsoft, Flipkart, CRED.
        Essential path: Python → Statistics → Scikit-learn → PyTorch → Hugging Face → MLOps.
        Kaggle competitions are the fastest way to build a credible portfolio."""
    },
    {
        "id": "dom_security_001",
        "category": "domain_overview",
        "domain": "Cybersecurity",
        "text": """Cybersecurity professionals protect systems, networks, and data from attacks.
        Specializations: Penetration Testing, Security Operations (SOC), Threat Intelligence, Bug Bounty, Forensics.
        Core tools: Kali Linux, Nmap, Burp Suite, Metasploit, Wireshark, OWASP ZAP.
        Linux CLI mastery and networking fundamentals are non-negotiable prerequisites.
        Salary in India: ₹5-10 LPA entry, ₹15-30 LPA for experienced professionals.
        Global salary: $70K-$160K USD. Key certifications: CompTIA Security+, CEH, OSCP (gold standard).
        TryHackMe and HackTheBox are the best platforms to learn ethical hacking hands-on.
        Bug bounty programs on HackerOne and Bugcrowd offer real income while learning."""
    },
    {
        "id": "dom_devops_001",
        "category": "domain_overview",
        "domain": "Cloud & DevOps Engineering",
        "text": """Cloud & DevOps Engineering involves building, deploying, and maintaining scalable infrastructure.
        Core technologies: Docker, Kubernetes, Terraform, Ansible, GitHub Actions, Jenkins.
        Cloud platforms: AWS (most in-demand), Google Cloud, Microsoft Azure.
        SRE (Site Reliability Engineering) is the high-end specialization at companies like Google.
        Salary in India: ₹7-15 LPA entry, ₹20-40 LPA for cloud architects.
        Global salary: $80K-$170K USD. Top certifications: AWS Solutions Architect, CKA (Kubernetes), Terraform Associate.
        Go programming language is increasingly important for DevOps tooling (Kubernetes is written in Go).
        DevOps engineers are required at every company that runs software in production."""
    },
    {
        "id": "dom_mobile_001",
        "category": "domain_overview",
        "domain": "Mobile App Development",
        "text": """Mobile App Development covers native Android (Kotlin/Java), native iOS (Swift/SwiftUI),
        and cross-platform development using Flutter (Dart) or React Native (JavaScript).
        Flutter is increasingly the top choice for cross-platform due to performance and Google backing.
        India has a massive mobile app market — PhonePe, CRED, Paytm, Dream11 all hire mobile engineers.
        Salary in India: ₹5-10 LPA entry, ₹15-28 LPA for senior engineers.
        Global salary: $65K-$145K USD. Firebase is the most popular backend for mobile apps.
        Publishing on Google Play Store and Apple App Store is a key portfolio milestone.
        React Native is preferred if you already know JavaScript from web development."""
    },
    {
        "id": "dom_data_eng_001",
        "category": "domain_overview",
        "domain": "Data Engineering",
        "text": """Data Engineering is the backbone of data-driven companies — building pipelines that move,
        transform, and store data at scale. Core technologies: Apache Spark, Apache Kafka, Apache Airflow,
        dbt, Apache Hive. Data warehouses: BigQuery, Snowflake, Redshift. Languages: Python and SQL.
        Data engineers work upstream of data scientists — without clean data, ML cannot work.
        Salary in India: ₹6-12 LPA entry, ₹18-30 LPA senior. Global salary: $75K-$155K USD.
        Top employers in India: Flipkart, Amazon, Swiggy, Ola, BigBasket.
        The Data Engineering Zoomcamp by DataTalks.Club is the best free resource.
        dbt (data build tool) is currently the hottest skill in the data engineering job market."""
    },
    {
        "id": "dom_blockchain_001",
        "category": "domain_overview",
        "domain": "Blockchain Development",
        "text": """Blockchain Development involves building decentralized applications (dApps), smart contracts,
        and DeFi protocols. Ethereum is the dominant platform. Solidity is the primary smart contract language.
        Tools: Hardhat, Foundry, Ethers.js, Web3.js, IPFS, MetaMask.
        The Web3 space is volatile but high-paying during bull markets.
        Salary in India: ₹8-15 LPA at Web3 startups. Global salary: $90K-$200K USD.
        Top companies: Polygon (Bangalore-based!), CoinDCX, WazirX, Consensys, Chainlink.
        Smart contract auditing is a high-value specialization — auditors earn $200-$500 per hour.
        Patrick Collins on YouTube and freeCodeCamp are the best free learning resources for Solidity."""
    },
    {
        "id": "dom_gamedev_001",
        "category": "domain_overview",
        "domain": "Game Development",
        "text": """Game Development involves building interactive experiences using game engines like Unity (C#)
        or Unreal Engine (C++/Blueprints). India has a growing gaming industry — Dream11, Nazara Games,
        Moonfrog Labs, and many mobile gaming studios are hiring.
        Unity is recommended for beginners and indie devs. Unreal Engine for AAA quality.
        Salary in India: ₹4-8 LPA entry, ₹12-22 LPA senior. Global salary: $55K-$130K USD.
        Portfolio is everything — ship a game on itch.io or Google Play Store.
        Brackeys on YouTube is the legendary free Unity tutorial channel.
        Game development uniquely combines programming, math, art, and design thinking."""
    },
    {
        "id": "dom_embedded_001",
        "category": "domain_overview",
        "domain": "Embedded Systems & IoT",
        "text": """Embedded Systems involves programming microcontrollers and processors for hardware products.
        IoT (Internet of Things) connects physical devices to the cloud.
        Languages: C and C++ are dominant. Python is used for Raspberry Pi projects.
        Platforms: Arduino (beginner), STM32 (professional), Raspberry Pi (Linux-based).
        Communication protocols: I2C, SPI, UART, MQTT, Zigbee, Bluetooth, WiFi.
        Real-time operating systems (RTOS): FreeRTOS is the most widely used.
        Salary in India: ₹5-10 LPA entry, ₹15-25 LPA senior at automotive/robotics companies.
        Top employers: Bosch, Texas Instruments, Qualcomm, Ather Energy, Samsung R&D.
        Embedded systems engineers are the most difficult to replace with AI — extremely stable career."""
    },
    {
        "id": "dom_nlp_001",
        "category": "domain_overview",
        "domain": "AI Research & NLP",
        "text": """AI Research and NLP (Natural Language Processing) focuses on building systems that understand
        and generate human language. This is the domain of ChatGPT, Claude, Gemini.
        Core technologies: Transformers, BERT, GPT, Hugging Face, LangChain, RAG, vector databases.
        Languages: Python exclusively. PyTorch is the research framework of choice.
        This domain requires the strongest mathematical foundation — linear algebra, calculus, statistics.
        Salary in India: ₹12-20 LPA entry at AI companies, ₹30-60 LPA at top AI labs.
        Global salary: $100K-$250K USD at companies like OpenAI, Google DeepMind.
        Indian AI companies hiring: Sarvam AI, AI4Bharat, Krutrim, Jio GenAI.
        Andrej Karpathy's YouTube channel and fast.ai are the best starting points."""
    },

    # ── RESOURCES ─────────────────────────────────────────────────────
    {
        "id": "res_git_001",
        "category": "resource",
        "domain": "all",
        "text": """Git and GitHub are mandatory for every developer regardless of domain.
        Best free resource: Kunal Kushwaha's Git & GitHub tutorial on YouTube (6 hours, in English with Indian context).
        URL: https://www.youtube.com/watch?v=apGV9Kg7ics
        Topics covered: git init, commit, branch, merge, rebase, GitHub pull requests, GitHub Actions basics.
        After Git basics, learn branching strategy: https://www.youtube.com/watch?v=e2IbNHi4uCI (Fireship, 1 hour).
        Create a GitHub profile with pinned repositories and a good README — this is your tech resume."""
    },
    {
        "id": "res_docker_001",
        "category": "resource",
        "domain": "all",
        "text": """Docker containerization is mandatory for every modern developer.
        Best free resource: TechWorld with Nana Docker Tutorial for Beginners on YouTube (5 hours).
        URL: https://www.youtube.com/watch?v=3c-iBn73dDE
        Topics: Dockerfile, docker build, docker run, docker-compose, container networking.
        After basics, learn Docker Compose for multi-container apps.
        Every deployed project should be containerized — it shows professionalism to hiring managers."""
    },
    {
        "id": "res_webdev_001",
        "category": "resource",
        "domain": "Full Stack Web Development",
        "text": """Best free YouTube resources for Full Stack Web Development:
        1. HTML & CSS Full Course by freeCodeCamp: https://www.youtube.com/watch?v=mU6anWqZJcc (12 hours, beginner)
        2. JavaScript Full Course by Bro Code: https://www.youtube.com/watch?v=8dWL3wF_OMw (14 hours, beginner)
        3. React Tutorial by Programming with Mosh: https://www.youtube.com/watch?v=SqcY0GlETPk (5 hours, intermediate)
        4. Node.js Crash Course by Traversy Media: https://www.youtube.com/watch?v=fBNz5xF-Kx4 (3 hours, intermediate)
        5. Full Stack MERN Project by JavaScript Mastery: https://www.youtube.com/watch?v=ngc9gnGgUdA (8 hours)
        6. Next.js 14 Full Course by Traversy Media: https://www.youtube.com/watch?v=ZVnjOPwW4ZA (5 hours, advanced)
        The Odin Project (free curriculum) is the best structured learning path for web development."""
    },
    {
        "id": "res_ml_001",
        "category": "resource",
        "domain": "Machine Learning & AI",
        "text": """Best free YouTube resources for Machine Learning and AI:
        1. Python for Everybody by freeCodeCamp: https://www.youtube.com/watch?v=8DvywoWv6fI (14 hours)
        2. ML with Python by Sentdex: https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v
        3. Neural Networks from Scratch by Andrej Karpathy: https://www.youtube.com/watch?v=VMj-3S1tku0
        4. Statistics for ML by StatQuest: https://www.youtube.com/@joshstarmer (essential)
        5. PyTorch Full Course by Patrick Loeber: https://www.youtube.com/watch?v=c36lUUr864M
        6. Let's build GPT by Andrej Karpathy: https://www.youtube.com/watch?v=kCc8FmEb1nY
        7. Hugging Face NLP Course: https://www.youtube.com/watch?v=00GKzGyWFEs
        DeepLearning.AI Specialization on Coursera (Andrew Ng) is the gold standard structured course."""
    },
    {
        "id": "res_security_001",
        "category": "resource",
        "domain": "Cybersecurity",
        "text": """Best free YouTube resources for Cybersecurity:
        1. Ethical Hacking Full Course by freeCodeCamp: https://www.youtube.com/watch?v=3Kq1MIfTWCE (15 hours)
        2. Linux for Hackers by NetworkChuck: https://www.youtube.com/playlist?list=PLIhvC56v63IJIujb5cyE13oLuyORZpdkL
        3. TryHackMe Walkthroughs by John Hammond: https://www.youtube.com/@_JohnHammond
        4. Web App Pentesting by TCM Security: https://www.youtube.com/watch?v=pHnA_8m60Co
        5. CompTIA Security+ by Professor Messer: https://www.youtube.com/c/professormesser (free, comprehensive)
        Platforms: TryHackMe (best for beginners), HackTheBox (intermediate), PentesterLab (web security).
        Communities: r/netsec, r/hacking, DEF CON talks on YouTube are valuable."""
    },
    {
        "id": "res_devops_001",
        "category": "resource",
        "domain": "Cloud & DevOps Engineering",
        "text": """Best free YouTube resources for Cloud & DevOps:
        1. Docker Full Course by TechWorld with Nana: https://www.youtube.com/watch?v=3c-iBn73dDE
        2. Kubernetes Full Course by TechWorld with Nana: https://www.youtube.com/watch?v=X48VuDVv0do
        3. AWS Full Course by freeCodeCamp: https://www.youtube.com/watch?v=NhDYbskXRgc (12 hours)
        4. Terraform Full Course by freeCodeCamp: https://www.youtube.com/watch?v=SLB_c_ayRMo
        5. GitHub Actions CI/CD by TechWorld with Nana: https://www.youtube.com/watch?v=R8_veQiYBjI
        6. DevOps Bootcamp by TechWorld with Nana: https://www.youtube.com/c/TechWorldwithNana
        Practice platforms: AWS Free Tier (12 months free), Google Cloud free tier, KodeKloud for Kubernetes labs."""
    },

    # ── JOB MARKET DATA ───────────────────────────────────────────────
    {
        "id": "job_india_2024_001",
        "category": "job_market",
        "domain": "all",
        "text": """Indian tech job market 2024-2025 trends:
        Highest paying fresher domains: AI/ML (₹12-20 LPA), Cloud/DevOps (₹8-15 LPA), Full Stack (₹6-12 LPA).
        Most in-demand skills: Python, React, AWS, Kubernetes, Docker, TypeScript, SQL.
        Top product companies hiring freshers: Razorpay, Zepto, CRED, PhonePe, Juspay, Groww, Meesho.
        Service companies hiring in bulk: TCS, Infosys, Wipro (₹3.5-4.5 LPA but very large numbers).
        Remote work: Very common for product companies, rare for service companies.
        Internship importance: 6-month internship at a product startup is worth more than 2 years at a service company.
        Portfolio projects: 3-5 deployed projects on GitHub is the minimum competitive requirement in 2024."""
    },
    {
        "id": "job_india_2024_002",
        "category": "job_market",
        "domain": "Machine Learning & AI",
        "text": """AI/ML job market in India 2024-2025:
        GenAI and LLM engineering roles are the hottest new category — companies need engineers who can
        fine-tune models, build RAG systems, and deploy LLM-powered products.
        New hot roles: LLM Engineer, AI Product Engineer, Prompt Engineer (declining), RAG Engineer.
        Indian AI startups hiring aggressively: Sarvam AI, Krutrim, Jio GenAI, Yellow.ai, Uniphore.
        Skills that dramatically increase salary: LangChain/LlamaIndex, vector databases (Pinecone, ChromaDB),
        fine-tuning open source LLMs (Llama, Mistral), MLOps (MLflow, Weights & Biases).
        Kaggle rank: Top 1000 globally in any competition is a strong resume signal."""
    },
    {
        "id": "job_global_001",
        "category": "job_market",
        "domain": "all",
        "text": """Global tech job market for Indian CS students:
        Top destinations: USA (H1B visa), Canada (easy PR pathway), Germany (skilled worker visa), Singapore.
        Remote-first companies hiring India-based engineers: GitLab, Automattic, Shopify, Vercel, Figma.
        Salary gap: India vs USA is roughly 5-10x for same role. Senior engineer India ₹25 LPA = USA $150K.
        FAANG India offices hiring: Google Hyderabad/Bangalore, Microsoft Hyderabad, Amazon Hyderabad/Bangalore.
        Key for global jobs: Strong GitHub portfolio, open source contributions, excellent English communication,
        system design knowledge, and LeetCode preparation (150+ medium problems minimum)."""
    },

    # ── CERTIFICATIONS ────────────────────────────────────────────────
    {
        "id": "cert_001",
        "category": "certifications",
        "domain": "Cloud & DevOps Engineering",
        "text": """Top certifications for Cloud & DevOps:
        1. AWS Solutions Architect Associate — Most recognized cloud cert globally. Exam cost: $150 USD.
        2. CKA (Certified Kubernetes Administrator) — Gold standard for K8s. Exam: $395 USD.
        3. Terraform Associate by HashiCorp — Growing importance as IaC becomes standard. Exam: $70 USD.
        4. Google Cloud Professional Cloud Architect — Strong for GCP-focused roles.
        5. AWS DevOps Engineer Professional — Advanced, commands ₹5-8 LPA salary premium.
        Study resources: A Cloud Guru, Adrian Cantrill, TechWorld with Nana (all YouTube).
        Timeline: AWS SAA in 2-3 months of dedicated study. CKA in 3-4 months."""
    },
    {
        "id": "cert_002",
        "category": "certifications",
        "domain": "Cybersecurity",
        "text": """Top certifications for Cybersecurity in order of difficulty:
        1. CompTIA Security+ — Best entry-level cert. Recognized by US DoD. Cost: ~$380 USD.
        2. CEH (Certified Ethical Hacker) — Popular in India. EC-Council certification. Cost: ~$1000 USD.
        3. OSCP (Offensive Security Certified Professional) — The most respected hands-on hacking cert.
           24-hour practical exam. Cost: ~$1499 USD. This alone can get you a ₹20+ LPA role.
        4. CISSP — For management-track security professionals. Requires 5 years experience.
        Timeline: CompTIA Sec+ in 3 months. CEH in 6 months. OSCP requires 1+ year of preparation."""
    },

    # ── CAREER ADVICE ─────────────────────────────────────────────────
    {
        "id": "advice_portfolio_001",
        "category": "career_advice",
        "domain": "all",
        "text": """Portfolio building is the most important career activity for CS students in India.
        A deployed project beats a certificate every single time in interviews.
        Minimum portfolio requirements for 2024 job market:
        - 3-5 projects on GitHub with clean READMEs and live demo links
        - At least 1 full-stack or end-to-end project (not just frontend or just scripts)
        - Projects should solve real problems — not just tutorial clones
        - GitHub profile should show consistent commits (green squares) over 6+ months
        - LinkedIn must be updated with projects and skills
        Best project ideas: Build something you actually use. Fix a problem in your college or local community.
        Clone a popular product with your own twist (not just copy-paste)."""
    },
    {
        "id": "advice_internship_001",
        "category": "career_advice",
        "domain": "all",
        "text": """Internship strategy for Indian CS students:
        Start applying for internships in 2nd year, not 3rd or 4th year.
        Best platforms for internships in India: Internshala, LinkedIn, AngelList/Wellfound, company career pages.
        Tier 1 internships: Google STEP, Microsoft Explore, Amazon SDE intern (highly competitive, apply early).
        Startup internships: Often easier to get, better learning, sometimes convert to full-time.
        Stipend range: ₹10,000-₹80,000 per month depending on company and role.
        Remote internships: Now very common — apply to companies across India, not just local.
        Internship > No internship always. Even unpaid internships provide portfolio projects and references.
        How to get one: Cold email developers on LinkedIn, contribute to open source, build projects first."""
    },
    {
        "id": "advice_opensource_001",
        "category": "career_advice",
        "domain": "all",
        "text": """Open source contribution is the fastest way to level up as a developer.
        Start small: Fix typos in documentation, improve READMEs, add test cases.
        Then: Fix small bugs labelled 'good first issue' on GitHub.
        Programs to participate in: Google Summer of Code (GSoC) — ₹4-6 lakh stipend for 3 months.
        Outreachy — paid internships for underrepresented groups in open source.
        Hacktoberfest — contribute in October, get free swag, build GitHub history.
        Benefits: Real code review from experienced engineers, networking, resume credibility.
        Top projects for Indian students: AI4Bharat (Indian language AI), FOSSEE (IIT Bombay), OpenStreetMap."""
    }
]