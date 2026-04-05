"""
Dummy dataset used for model training and recommendation.
Each entry represents a student profile + ideal career path mapping.
"""

DUMMY_DATASET = [
    {
        "profile": {
            "interests": ["Web Development", "UI/UX"],
            "skill_level": "beginner",
            "year": 1,
            "languages_known": ["HTML", "CSS"]
        },
        "recommended_domain": "Full Stack Web Development",
        "success_rate": 0.92
    },
    {
        "profile": {
            "interests": ["Machine Learning", "Data Analysis"],
            "skill_level": "intermediate",
            "year": 2,
            "languages_known": ["Python"]
        },
        "recommended_domain": "Machine Learning & AI",
        "success_rate": 0.95
    },
    {
        "profile": {
            "interests": ["Networking", "Security", "Linux"],
            "skill_level": "beginner",
            "year": 2,
            "languages_known": ["Python", "Bash"]
        },
        "recommended_domain": "Cybersecurity",
        "success_rate": 0.88
    },
    {
        "profile": {
            "interests": ["Mobile Apps", "Android", "iOS"],
            "skill_level": "intermediate",
            "year": 3,
            "languages_known": ["Java", "Kotlin"]
        },
        "recommended_domain": "Mobile App Development",
        "success_rate": 0.90
    },
    {
        "profile": {
            "interests": ["Cloud", "DevOps", "Infrastructure"],
            "skill_level": "intermediate",
            "year": 3,
            "languages_known": ["Python", "Bash", "YAML"]
        },
        "recommended_domain": "Cloud & DevOps Engineering",
        "success_rate": 0.93
    },
    {
        "profile": {
            "interests": ["Databases", "SQL", "Data Warehousing"],
            "skill_level": "beginner",
            "year": 2,
            "languages_known": ["SQL", "Python"]
        },
        "recommended_domain": "Data Engineering",
        "success_rate": 0.87
    },
    {
        "profile": {
            "interests": ["Blockchain", "Smart Contracts", "Web3"],
            "skill_level": "advanced",
            "year": 3,
            "languages_known": ["Solidity", "JavaScript", "Python"]
        },
        "recommended_domain": "Blockchain Development",
        "success_rate": 0.82
    },
    {
        "profile": {
            "interests": ["Game Development", "3D", "Unity"],
            "skill_level": "intermediate",
            "year": 2,
            "languages_known": ["C#", "C++"]
        },
        "recommended_domain": "Game Development",
        "success_rate": 0.85
    },
    {
        "profile": {
            "interests": ["Embedded Systems", "IoT", "Hardware"],
            "skill_level": "intermediate",
            "year": 3,
            "languages_known": ["C", "C++", "Python"]
        },
        "recommended_domain": "Embedded Systems & IoT",
        "success_rate": 0.86
    },
    {
        "profile": {
            "interests": ["AI/ML", "Research", "NLP"],
            "skill_level": "advanced",
            "year": 4,
            "languages_known": ["Python", "R", "MATLAB"]
        },
        "recommended_domain": "AI Research & NLP",
        "success_rate": 0.91
    },
]

# Domain knowledge base — resources, tools, roles, companies
DOMAIN_KNOWLEDGE = {
    "Full Stack Web Development": {
        "career_goals": [
            "Full Stack Developer at a top tech company",
            "Frontend Architect building scalable web apps",
            "Software Engineer specializing in React + Node.js"
        ],
        "job_roles": ["Full Stack Developer", "Frontend Developer", "Backend Developer", "Software Engineer", "Web Architect"],
        "salary_india": "₹5 LPA – ₹25 LPA",
        "salary_global": "$60K – $140K USD",
        "companies": ["Razorpay", "Zepto", "Swiggy", "Atlassian", "Shopify", "Stripe", "Vercel", "Netlify"],
        "certifications": ["AWS Certified Developer", "Meta Frontend Developer Certificate", "Google UX Design Certificate"],
        "core_skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "REST APIs", "MongoDB/PostgreSQL", "Git", "Docker"],
        "youtube_resources": [
            {"title": "HTML & CSS Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=mU6anWqZJcc", "hours": 12, "difficulty": "beginner"},
            {"title": "JavaScript Full Course – Bro Code", "url": "https://www.youtube.com/watch?v=8dWL3wF_OMw", "hours": 14, "difficulty": "beginner"},
            {"title": "React Tutorial for Beginners – Programming with Mosh", "url": "https://www.youtube.com/watch?v=SqcY0GlETPk", "hours": 5, "difficulty": "intermediate"},
            {"title": "Node.js Crash Course – Traversy Media", "url": "https://www.youtube.com/watch?v=fBNz5xF-Kx4", "hours": 3, "difficulty": "intermediate"},
            {"title": "Full Stack MERN Project – JavaScript Mastery", "url": "https://www.youtube.com/watch?v=ngc9gnGgUdA", "hours": 8, "difficulty": "intermediate"},
            {"title": "TypeScript Full Course – Jack Herrington", "url": "https://www.youtube.com/watch?v=SpwzRDXQ3po", "hours": 4, "difficulty": "intermediate"},
            {"title": "Next.js 14 Full Course – Traversy Media", "url": "https://www.youtube.com/watch?v=ZVnjOPwW4ZA", "hours": 5, "difficulty": "advanced"},
            {"title": "PostgreSQL Full Tutorial – freeCodeCamp", "url": "https://www.youtube.com/watch?v=SpwzRDXQ3po", "hours": 6, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Foundation: HTML, CSS & JS", "skills": ["HTML5", "CSS3", "Flexbox", "Grid", "Vanilla JS"], "projects": ["Personal Portfolio Website", "Responsive Landing Page"]},
            {"title": "Frontend Frameworks", "skills": ["React.js", "State Management", "Hooks", "React Router"], "projects": ["Todo App with React", "Weather Dashboard"]},
            {"title": "Backend Basics", "skills": ["Node.js", "Express.js", "REST APIs", "JWT Auth"], "projects": ["Blog API", "User Authentication System"]},
            {"title": "Databases & Deployment", "skills": ["MongoDB", "PostgreSQL", "Docker", "CI/CD"], "projects": ["Full Stack E-commerce App", "Social Media Clone"]},
            {"title": "Advanced Topics", "skills": ["TypeScript", "Next.js", "Redis", "WebSockets"], "projects": ["Real-time Chat App", "SaaS Dashboard"]},
        ]
    },

    "Machine Learning & AI": {
        "career_goals": [
            "ML Engineer at a top product company",
            "Data Scientist driving business decisions with AI",
            "AI Research Engineer building next-gen models"
        ],
        "job_roles": ["ML Engineer", "Data Scientist", "AI Engineer", "Research Scientist", "NLP Engineer"],
        "salary_india": "₹8 LPA – ₹40 LPA",
        "salary_global": "$80K – $180K USD",
        "companies": ["Google DeepMind", "OpenAI", "Microsoft", "Amazon", "Flipkart", "PhonePe", "Ola", "CRED"],
        "certifications": ["Google ML Engineer Certificate", "AWS ML Specialty", "DeepLearning.AI Specialization (Coursera)", "TensorFlow Developer Certificate"],
        "core_skills": ["Python", "NumPy/Pandas", "Scikit-learn", "TensorFlow/PyTorch", "SQL", "Statistics", "Git", "Docker"],
        "youtube_resources": [
            {"title": "Python for Everybody – freeCodeCamp", "url": "https://www.youtube.com/watch?v=8DvywoWv6fI", "hours": 14, "difficulty": "beginner"},
            {"title": "Machine Learning with Python – Sentdex", "url": "https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v", "hours": 10, "difficulty": "intermediate"},
            {"title": "Deep Learning Specialization Summary – Andrej Karpathy", "url": "https://www.youtube.com/watch?v=VMj-3S1tku0", "hours": 8, "difficulty": "advanced"},
            {"title": "Statistics for Data Science – StatQuest", "url": "https://www.youtube.com/c/joshstarmer", "hours": 12, "difficulty": "intermediate"},
            {"title": "PyTorch Full Course – Patrick Loeber", "url": "https://www.youtube.com/watch?v=c36lUUr864M", "hours": 6, "difficulty": "intermediate"},
            {"title": "Natural Language Processing – Hugging Face", "url": "https://www.youtube.com/watch?v=00GKzGyWFEs", "hours": 8, "difficulty": "advanced"},
            {"title": "MLOps Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=NGq7sum03pA", "hours": 7, "difficulty": "advanced"},
        ],
        "milestone_templates": [
            {"title": "Python & Math Foundations", "skills": ["Python", "NumPy", "Pandas", "Linear Algebra", "Statistics"], "projects": ["Data Analysis on Kaggle Dataset", "EDA Notebook"]},
            {"title": "Core ML Algorithms", "skills": ["Regression", "Classification", "Clustering", "Scikit-learn"], "projects": ["House Price Predictor", "Customer Churn Model"]},
            {"title": "Deep Learning", "skills": ["Neural Networks", "CNNs", "RNNs", "PyTorch"], "projects": ["Image Classifier", "Text Sentiment Analyzer"]},
            {"title": "Specialization (NLP/CV/RL)", "skills": ["Transformers", "BERT", "YOLO", "Reinforcement Learning"], "projects": ["Chatbot", "Object Detection System"]},
            {"title": "MLOps & Deployment", "skills": ["MLflow", "FastAPI", "Docker", "AWS SageMaker"], "projects": ["End-to-end ML Pipeline", "Model API Deployment"]},
        ]
    },

    "Cybersecurity": {
        "career_goals": [
            "Penetration Tester at a global security firm",
            "Security Engineer protecting enterprise systems",
            "SOC Analyst defending against cyber threats"
        ],
        "job_roles": ["Penetration Tester", "Security Analyst", "SOC Analyst", "Security Engineer", "Bug Bounty Hunter"],
        "salary_india": "₹5 LPA – ₹30 LPA",
        "salary_global": "$70K – $160K USD",
        "companies": ["Palo Alto Networks", "CrowdStrike", "Deloitte", "PwC", "Wipro CyberSecurity", "Tata Consultancy", "HackerOne"],
        "certifications": ["CompTIA Security+", "CEH (Certified Ethical Hacker)", "OSCP", "CISSP"],
        "core_skills": ["Linux", "Networking", "Python/Bash", "Kali Linux", "OWASP Top 10", "Cryptography", "Git"],
        "youtube_resources": [
            {"title": "Ethical Hacking Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "hours": 15, "difficulty": "intermediate"},
            {"title": "Linux for Hackers – NetworkChuck", "url": "https://www.youtube.com/playlist?list=PLIhvC56v63IJIujb5cyE13oLuyORZpdkL", "hours": 6, "difficulty": "beginner"},
            {"title": "TryHackMe Walkthrough Series – John Hammond", "url": "https://www.youtube.com/@_JohnHammond", "hours": 20, "difficulty": "intermediate"},
            {"title": "Web App Penetration Testing – TCM Security", "url": "https://www.youtube.com/watch?v=pHnA_8m60Co", "hours": 10, "difficulty": "intermediate"},
            {"title": "CompTIA Security+ Full Course – Professor Messer", "url": "https://www.youtube.com/c/professormesser", "hours": 14, "difficulty": "intermediate"},
            {"title": "Malware Analysis – OALabs", "url": "https://www.youtube.com/@OALABS", "hours": 8, "difficulty": "advanced"},
        ],
        "milestone_templates": [
            {"title": "Linux & Networking Fundamentals", "skills": ["Linux CLI", "TCP/IP", "DNS", "HTTP/S", "Firewalls"], "projects": ["Set up home lab with VirtualBox", "Packet analysis with Wireshark"]},
            {"title": "Security Concepts & Tools", "skills": ["OWASP Top 10", "Nmap", "Burp Suite", "Metasploit"], "projects": ["TryHackMe – 50 rooms completed", "CTF Competitions"]},
            {"title": "Ethical Hacking", "skills": ["Web App Pen Testing", "Network Pen Testing", "Social Engineering"], "projects": ["Hack The Box machines", "Bug Bounty (HackerOne)"]},
            {"title": "Specialization", "skills": ["Malware Analysis", "Forensics", "Cloud Security", "SIEM"], "projects": ["SOC simulation lab", "Incident response report"]},
            {"title": "Certification & Portfolio", "skills": ["CompTIA Sec+", "CEH", "OSCP prep"], "projects": ["Full pentest report", "Personal security blog"]},
        ]
    },

    "Cloud & DevOps Engineering": {
        "career_goals": [
            "DevOps Engineer scaling infrastructure at a unicorn startup",
            "Cloud Architect designing AWS/GCP enterprise solutions",
            "SRE at a FAANG-level company"
        ],
        "job_roles": ["DevOps Engineer", "Cloud Engineer", "SRE", "Infrastructure Engineer", "Platform Engineer"],
        "salary_india": "₹7 LPA – ₹35 LPA",
        "salary_global": "$80K – $170K USD",
        "companies": ["Amazon AWS", "Google Cloud", "Microsoft Azure", "HashiCorp", "Zomato", "Razorpay", "Juspay"],
        "certifications": ["AWS Solutions Architect", "CKA (Kubernetes)", "Google Cloud Professional", "HashiCorp Terraform Associate"],
        "core_skills": ["Linux", "Docker", "Kubernetes", "Terraform", "CI/CD", "AWS/GCP/Azure", "Python/Bash", "Git"],
        "youtube_resources": [
            {"title": "Docker Full Course – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "hours": 5, "difficulty": "beginner"},
            {"title": "Kubernetes Full Course – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "hours": 5, "difficulty": "intermediate"},
            {"title": "AWS Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=NhDYbskXRgc", "hours": 12, "difficulty": "intermediate"},
            {"title": "DevOps Bootcamp – TechWorld with Nana", "url": "https://www.youtube.com/c/TechWorldwithNana", "hours": 15, "difficulty": "intermediate"},
            {"title": "Terraform Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=SLB_c_ayRMo", "hours": 6, "difficulty": "intermediate"},
            {"title": "CI/CD with GitHub Actions – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "hours": 4, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Linux & Scripting", "skills": ["Linux CLI", "Bash", "Python scripting", "SSH", "Cron jobs"], "projects": ["Automate system tasks with Bash", "Python server monitoring script"]},
            {"title": "Containers & Docker", "skills": ["Docker", "Docker Compose", "Container networking", "Docker Hub"], "projects": ["Containerize a web app", "Multi-service Docker Compose setup"]},
            {"title": "Kubernetes & Orchestration", "skills": ["K8s architecture", "Deployments", "Services", "Helm"], "projects": ["Deploy app on Minikube", "Kubernetes cluster on AWS EKS"]},
            {"title": "Cloud Platform (AWS/GCP)", "skills": ["EC2/S3/RDS", "IAM", "VPC", "Lambda", "CloudFormation"], "projects": ["3-tier web app on AWS", "Serverless API with Lambda"]},
            {"title": "CI/CD & Infrastructure as Code", "skills": ["GitHub Actions", "Jenkins", "Terraform", "Ansible"], "projects": ["Full CI/CD pipeline", "Infrastructure provisioning with Terraform"]},
        ]
    },

    "Mobile App Development": {
        "career_goals": [
            "Android/iOS Developer at a product startup",
            "Flutter Developer building cross-platform apps",
            "Mobile Lead at a fintech company"
        ],
        "job_roles": ["Android Developer", "iOS Developer", "Flutter Developer", "React Native Developer", "Mobile Engineer"],
        "salary_india": "₹5 LPA – ₹28 LPA",
        "salary_global": "$65K – $145K USD",
        "companies": ["Google", "PhonePe", "Paytm", "CRED", "Meesho", "Dream11", "Airtel"],
        "certifications": ["Google Associate Android Developer", "Apple WWDC Scholarship", "Meta React Native Certificate"],
        "core_skills": ["Kotlin/Java", "Swift/SwiftUI", "Flutter/Dart", "REST APIs", "Firebase", "Git", "Play Store/App Store deployment"],
        "youtube_resources": [
            {"title": "Android Development Full Course – Philipp Lackner", "url": "https://www.youtube.com/@PhilippLackner", "hours": 20, "difficulty": "beginner"},
            {"title": "Flutter Full Course – Academind", "url": "https://www.youtube.com/watch?v=x0uinJvhNxI", "hours": 12, "difficulty": "intermediate"},
            {"title": "Kotlin Crash Course – Traversy Media", "url": "https://www.youtube.com/watch?v=5flXf8nuq60", "hours": 3, "difficulty": "beginner"},
            {"title": "React Native Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=0-S5a0eXPoc", "hours": 10, "difficulty": "intermediate"},
            {"title": "Firebase with Flutter – FireShip", "url": "https://www.youtube.com/watch?v=sfA3NWDBPZ4", "hours": 5, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Language Fundamentals", "skills": ["Kotlin/Java or Dart", "OOP concepts", "Data structures"], "projects": ["Console-based Kotlin app", "Dart OOP exercises"]},
            {"title": "UI Development", "skills": ["XML layouts / Flutter widgets", "Navigation", "State management"], "projects": ["Calculator App", "Quiz App"]},
            {"title": "Networking & Backend", "skills": ["REST API calls", "JSON parsing", "Firebase", "SQLite"], "projects": ["Weather App with API", "Notes App with DB"]},
            {"title": "Advanced Features", "skills": ["Push notifications", "Camera/GPS", "In-app payments", "Animations"], "projects": ["E-commerce App", "Food Delivery Clone"]},
            {"title": "Publishing & DevOps", "skills": ["Play Store publishing", "CI/CD for mobile", "Testing", "Crash reporting"], "projects": ["Published app on Play Store/App Store"]},
        ]
    },

    "Data Engineering": {
        "career_goals": [
            "Data Engineer building ETL pipelines at scale",
            "Analytics Engineer at a data-driven company",
            "Big Data Engineer with Spark & Hadoop expertise"
        ],
        "job_roles": ["Data Engineer", "Analytics Engineer", "ETL Developer", "Big Data Engineer", "BI Developer"],
        "salary_india": "₹6 LPA – ₹30 LPA",
        "salary_global": "$75K – $155K USD",
        "companies": ["Flipkart", "Amazon", "Microsoft", "Uber", "Ola", "BigBasket", "Freshworks"],
        "certifications": ["AWS Data Engineer Associate", "Google Professional Data Engineer", "Databricks Certified Associate Developer"],
        "core_skills": ["Python", "SQL", "Apache Spark", "Kafka", "Airflow", "dbt", "AWS/GCP", "Git", "Docker"],
        "youtube_resources": [
            {"title": "SQL Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "hours": 4, "difficulty": "beginner"},
            {"title": "Apache Spark with Python – freeCodeCamp", "url": "https://www.youtube.com/watch?v=_C8kWso4ne4", "hours": 6, "difficulty": "intermediate"},
            {"title": "Data Engineering Zoomcamp – DataTalks.Club", "url": "https://www.youtube.com/@DataTalksClub", "hours": 30, "difficulty": "intermediate"},
            {"title": "Apache Kafka Full Course – Stephane Maarek", "url": "https://www.youtube.com/watch?v=gg-VwXSWhD8", "hours": 5, "difficulty": "intermediate"},
            {"title": "dbt Tutorial for Beginners – Kahan Data Solutions", "url": "https://www.youtube.com/watch?v=5rNquRnNb4E", "hours": 4, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "SQL & Python Mastery", "skills": ["Advanced SQL", "Python", "Pandas", "Data modeling"], "projects": ["Sales analytics with SQL", "ETL with Python"]},
            {"title": "Data Warehousing", "skills": ["Star schema", "Snowflake/BigQuery", "dbt", "Dimensional modeling"], "projects": ["Build a DWH on BigQuery", "dbt transformation project"]},
            {"title": "Big Data Tools", "skills": ["Apache Spark", "Hadoop", "Hive", "Parquet/Avro"], "projects": ["Spark job processing 10M rows", "Log analysis pipeline"]},
            {"title": "Streaming & Real-time", "skills": ["Kafka", "Flink", "Redis Streams", "Lambda architecture"], "projects": ["Real-time dashboard with Kafka", "Clickstream analytics"]},
            {"title": "Orchestration & Cloud", "skills": ["Airflow", "Prefect", "AWS Glue", "Docker"], "projects": ["Scheduled ETL pipeline", "Cloud data lake on AWS"]},
        ]
    },

    "Blockchain Development": {
        "career_goals": [
            "Solidity Developer at a DeFi protocol",
            "Web3 Full Stack Engineer building dApps",
            "Smart Contract Auditor"
        ],
        "job_roles": ["Blockchain Developer", "Solidity Developer", "Web3 Engineer", "Smart Contract Auditor", "DeFi Engineer"],
        "salary_india": "₹8 LPA – ₹40 LPA",
        "salary_global": "$90K – $200K USD",
        "companies": ["Polygon", "CoinDCX", "WazirX", "Consensys", "Chainlink", "OpenSea", "Alchemy"],
        "certifications": ["Certified Ethereum Developer", "Blockchain Council Certification", "Chainlink Developer Expert"],
        "core_skills": ["Solidity", "JavaScript/TypeScript", "Hardhat/Foundry", "Ethers.js/Web3.js", "IPFS", "Git", "Docker"],
        "youtube_resources": [
            {"title": "Solidity Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=gyMwXuJrbJQ", "hours": 16, "difficulty": "intermediate"},
            {"title": "Web3.js Tutorial – Dapp University", "url": "https://www.youtube.com/watch?v=kDo_MdyNJzI", "hours": 5, "difficulty": "intermediate"},
            {"title": "Foundry Full Course – Patrick Collins", "url": "https://www.youtube.com/watch?v=umepbfKp5rI", "hours": 10, "difficulty": "advanced"},
            {"title": "DeFi Deep Dive – Whiteboard Crypto", "url": "https://www.youtube.com/@WhiteboardCrypto", "hours": 8, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Blockchain Fundamentals", "skills": ["How blockchain works", "Ethereum", "Wallets", "Transactions"], "projects": ["Set up MetaMask", "Send test ETH on testnet"]},
            {"title": "Solidity Programming", "skills": ["Solidity syntax", "Smart contracts", "ERC-20/ERC-721"], "projects": ["Simple ERC-20 token", "NFT minting contract"]},
            {"title": "dApp Development", "skills": ["Ethers.js", "React + Web3", "Hardhat", "IPFS"], "projects": ["NFT marketplace frontend", "DAO voting dApp"]},
            {"title": "DeFi & Advanced Contracts", "skills": ["AMMs", "Lending protocols", "Flash loans", "Oracles"], "projects": ["DEX clone", "Lending protocol"]},
            {"title": "Security & Auditing", "skills": ["Smart contract vulnerabilities", "Slither", "Mythril", "Audit reports"], "projects": ["Audit a public contract", "Bug bounty on Immunefi"]},
        ]
    },

    "Game Development": {
        "career_goals": [
            "Unity/Unreal Developer at a gaming studio",
            "Indie game developer launching on Steam",
            "Technical Game Designer at AAA studio"
        ],
        "job_roles": ["Unity Developer", "Unreal Developer", "Game Designer", "Technical Artist", "VR/AR Developer"],
        "salary_india": "₹4 LPA – ₹22 LPA",
        "salary_global": "$55K – $130K USD",
        "companies": ["Dream11", "Nazara Games", "Moonfrog", "Electronic Arts", "Ubisoft India", "Unity Technologies"],
        "certifications": ["Unity Certified Associate", "Unreal Online Learning Certification"],
        "core_skills": ["C#/C++", "Unity/Unreal Engine", "3D math", "Physics engines", "Shader programming", "Git"],
        "youtube_resources": [
            {"title": "Unity Full Course – Brackeys", "url": "https://www.youtube.com/c/Brackeys", "hours": 20, "difficulty": "beginner"},
            {"title": "Unreal Engine 5 Beginner Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=k-zMkzmduqI", "hours": 8, "difficulty": "beginner"},
            {"title": "C# for Unity – Jason Weimann", "url": "https://www.youtube.com/@Unity3dCollege", "hours": 10, "difficulty": "beginner"},
            {"title": "Game Design Fundamentals – Extra Credits", "url": "https://www.youtube.com/@ExtraCredits", "hours": 6, "difficulty": "beginner"},
            {"title": "Shader Graph Tutorial – Unity", "url": "https://www.youtube.com/watch?v=Ar9eIn4TEFU", "hours": 4, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Engine & Language Basics", "skills": ["C# basics", "Unity Editor", "GameObjects", "Physics"], "projects": ["Flappy Bird clone", "Endless Runner"]},
            {"title": "Core Game Systems", "skills": ["Collision detection", "Animation", "Audio", "UI systems"], "projects": ["2D Platformer", "Simple RPG"]},
            {"title": "3D Development", "skills": ["3D modeling basics", "Lighting", "Shaders", "Navigation"], "projects": ["3D FPS prototype", "Third-person adventure"]},
            {"title": "Multiplayer & Networking", "skills": ["Unity Netcode", "Mirror", "Photon", "Dedicated servers"], "projects": ["Multiplayer shooter", "Online board game"]},
            {"title": "Publishing & Monetization", "skills": ["Steam SDK", "In-app purchases", "Analytics", "Performance"], "projects": ["Published game on itch.io / Steam"]},
        ]
    },

    "Embedded Systems & IoT": {
        "career_goals": [
            "Embedded Systems Engineer at an automotive/robotics firm",
            "IoT Architect designing connected device ecosystems",
            "Firmware Engineer at a hardware startup"
        ],
        "job_roles": ["Embedded Engineer", "IoT Developer", "Firmware Engineer", "RTOS Developer", "Robotics Engineer"],
        "salary_india": "₹5 LPA – ₹25 LPA",
        "salary_global": "$65K – $140K USD",
        "companies": ["Texas Instruments", "Qualcomm", "Bosch", "Samsung R&D", "Ather Energy", "RIL Jio", "Robert Bosch"],
        "certifications": ["ARM Accredited Engineer", "AWS IoT Core Certification", "Coursera Embedded Systems Specialization"],
        "core_skills": ["C/C++", "RTOS", "Arduino/Raspberry Pi", "MQTT", "I2C/SPI", "PCB design basics", "Git", "Docker"],
        "youtube_resources": [
            {"title": "Embedded C Full Course – Fastbit Embedded Brain Academy", "url": "https://www.youtube.com/c/FastbitEmbeddedBrainAcademy", "hours": 20, "difficulty": "intermediate"},
            {"title": "Arduino Tutorial Series – Paul McWhorter", "url": "https://www.youtube.com/@paulmcwhorter", "hours": 15, "difficulty": "beginner"},
            {"title": "Raspberry Pi Projects – Jeff Geerling", "url": "https://www.youtube.com/@JeffGeerling", "hours": 8, "difficulty": "intermediate"},
            {"title": "FreeRTOS Full Course – Shawn Hymel", "url": "https://www.youtube.com/watch?v=F321087yYy4", "hours": 6, "difficulty": "advanced"},
            {"title": "MQTT & IoT – Andreas Spiess", "url": "https://www.youtube.com/@AndreasSpiess", "hours": 6, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "C Programming & Hardware Basics", "skills": ["C pointers", "Memory management", "GPIO", "Interrupts"], "projects": ["LED blinker", "Button input handler"]},
            {"title": "Microcontroller Programming", "skills": ["Arduino", "STM32", "Timers", "ADC/DAC"], "projects": ["Temperature sensor display", "PWM motor control"]},
            {"title": "Communication Protocols", "skills": ["UART/SPI/I2C", "Bluetooth", "WiFi", "MQTT"], "projects": ["IoT weather station", "Smart home sensor"]},
            {"title": "RTOS & Linux Embedded", "skills": ["FreeRTOS", "Linux kernel basics", "Device drivers", "Yocto"], "projects": ["RTOS task scheduler", "Custom Linux image"]},
            {"title": "Advanced IoT & Cloud", "skills": ["AWS IoT", "Edge computing", "OTA updates", "Security"], "projects": ["Fleet management system", "Industrial monitoring dashboard"]},
        ]
    },

    "AI Research & NLP": {
        "career_goals": [
            "NLP Research Scientist at an AI lab",
            "Conversational AI Engineer building LLM-powered products",
            "AI PhD researcher or postdoctoral fellow"
        ],
        "job_roles": ["Research Scientist", "NLP Engineer", "LLM Engineer", "Prompt Engineer", "AI Product Engineer"],
        "salary_india": "₹12 LPA – ₹60 LPA",
        "salary_global": "$100K – $250K USD",
        "companies": ["Google DeepMind", "Microsoft Research", "Meta AI", "OpenAI", "Cohere", "AI4Bharat", "Sarvam AI"],
        "certifications": ["DeepLearning.AI NLP Specialization", "Hugging Face NLP Course", "Stanford CS224N (audit)"],
        "core_skills": ["Python", "PyTorch", "Transformers", "Hugging Face", "CUDA", "Research writing", "Git", "Docker"],
        "youtube_resources": [
            {"title": "Andrej Karpathy – Neural Nets from Scratch", "url": "https://www.youtube.com/watch?v=VMj-3S1tku0", "hours": 10, "difficulty": "advanced"},
            {"title": "Hugging Face NLP Course", "url": "https://www.youtube.com/playlist?list=PLo2EIpI_JMQvWfQndUesu0nPBAtZ9gP1o", "hours": 12, "difficulty": "advanced"},
            {"title": "Stanford CS231n – CNNs for Visual Recognition", "url": "https://www.youtube.com/playlist?list=PLC1qU-LWwrF64f4Qkte0VV_Lu1HH-dwsS", "hours": 20, "difficulty": "advanced"},
            {"title": "Let's build GPT – Andrej Karpathy", "url": "https://www.youtube.com/watch?v=kCc8FmEb1nY", "hours": 4, "difficulty": "advanced"},
            {"title": "LangChain Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=lG7Uxts9SXs", "hours": 5, "difficulty": "intermediate"},
        ],
        "milestone_templates": [
            {"title": "Math & Python Fundamentals", "skills": ["Linear algebra", "Calculus", "Probability", "NumPy"], "projects": ["Implement gradient descent from scratch"]},
            {"title": "Deep Learning", "skills": ["CNNs", "RNNs", "Attention mechanism", "PyTorch"], "projects": ["Train ResNet on CIFAR-10", "Seq2Seq translation model"]},
            {"title": "NLP Foundations", "skills": ["Tokenization", "Word embeddings", "Language models", "BERT"], "projects": ["Text classifier", "Named entity recognizer"]},
            {"title": "LLMs & Modern NLP", "skills": ["Transformers", "Fine-tuning LLMs", "RAG", "Prompt engineering"], "projects": ["Fine-tune GPT-2", "Build RAG system with LangChain"]},
            {"title": "Research & Publication", "skills": ["Paper reading", "LaTeX", "Experiment design", "HuggingFace Hub"], "projects": ["Reproduce a research paper", "Submit to arXiv / conference"]},
        ]
    }
}

# Mandatory tools for all developers
MANDATORY_TOOLS = [
    {
        "title": "Git & GitHub Complete Tutorial – Kunal Kushwaha",
        "url": "https://www.youtube.com/watch?v=apGV9Kg7ics",
        "type": "youtube",
        "estimated_hours": 6,
        "difficulty": "beginner"
    },
    {
        "title": "Git Branching Strategy – Fireship",
        "url": "https://www.youtube.com/watch?v=e2IbNHi4uCI",
        "type": "youtube",
        "estimated_hours": 1,
        "difficulty": "intermediate"
    },
    {
        "title": "Docker Tutorial for Beginners – TechWorld with Nana",
        "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
        "type": "youtube",
        "estimated_hours": 5,
        "difficulty": "beginner"
    },
    {
        "title": "GitHub Actions CI/CD – TechWorld with Nana",
        "url": "https://www.youtube.com/watch?v=R8_veQiYBjI",
        "type": "youtube",
        "estimated_hours": 3,
        "difficulty": "intermediate"
    }
]

INTEREST_TO_DOMAIN_MAP = {
    "Web Development": "Full Stack Web Development",
    "UI/UX": "Full Stack Web Development",
    "Frontend": "Full Stack Web Development",
    "Backend": "Full Stack Web Development",
    "JavaScript": "Full Stack Web Development",
    "React": "Full Stack Web Development",
    "Node.js": "Full Stack Web Development",

    "Machine Learning": "Machine Learning & AI",
    "AI/ML": "Machine Learning & AI",
    "Deep Learning": "Machine Learning & AI",
    "Data Science": "Machine Learning & AI",
    "Artificial Intelligence": "Machine Learning & AI",
    "Computer Vision": "Machine Learning & AI",

    "Cybersecurity": "Cybersecurity",
    "Ethical Hacking": "Cybersecurity",
    "Networking": "Cybersecurity",
    "Security": "Cybersecurity",
    "Linux": "Cybersecurity",
    "Penetration Testing": "Cybersecurity",

    "Cloud": "Cloud & DevOps Engineering",
    "DevOps": "Cloud & DevOps Engineering",
    "AWS": "Cloud & DevOps Engineering",
    "Kubernetes": "Cloud & DevOps Engineering",
    "Infrastructure": "Cloud & DevOps Engineering",
    "CI/CD": "Cloud & DevOps Engineering",

    "Mobile Apps": "Mobile App Development",
    "Android": "Mobile App Development",
    "iOS": "Mobile App Development",
    "Flutter": "Mobile App Development",
    "React Native": "Mobile App Development",

    "Databases": "Data Engineering",
    "SQL": "Data Engineering",
    "Big Data": "Data Engineering",
    "Data Warehousing": "Data Engineering",
    "ETL": "Data Engineering",

    "Blockchain": "Blockchain Development",
    "Web3": "Blockchain Development",
    "Smart Contracts": "Blockchain Development",
    "Cryptocurrency": "Blockchain Development",
    "DeFi": "Blockchain Development",

    "Game Development": "Game Development",
    "Unity": "Game Development",
    "Unreal": "Game Development",
    "3D": "Game Development",
    "Gaming": "Game Development",

    "Embedded Systems": "Embedded Systems & IoT",
    "IoT": "Embedded Systems & IoT",
    "Hardware": "Embedded Systems & IoT",
    "Arduino": "Embedded Systems & IoT",
    "Robotics": "Embedded Systems & IoT",

    "NLP": "AI Research & NLP",
    "Research": "AI Research & NLP",
    "LLM": "AI Research & NLP",
    "Natural Language Processing": "AI Research & NLP",
    "Transformers": "AI Research & NLP",
}