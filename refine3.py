import os
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def build_prompt(subject_title, program, semester, prerequisites, credits, aim, units, program_goals, graduate_attributes):
    unit_prompts = ""
    for idx, unit in enumerate(units, start=1):
        unit_prompts += f"""
Unit {idx}: {unit['title']}
- Focus: {unit['focus']}
- Outcome Focus: {unit['outcome_focus']}
- Bloom’s Taxonomy Levels: {', '.join(unit['blooms_levels'])}
"""

    graduate_attr_str = "\n".join(f"- {attr}" for attr in graduate_attributes)

    prompt = f"""
You are an education expert helping generate course and program outcomes for university syllabi following **VTU (Visvesvaraya Technological University)** guidelines.

Subject Title: {subject_title}
Program: {program}
Semester: {semester}
Prerequisites: {prerequisites}
Credits: {credits}

Overall Subject Aim:
{aim}

{unit_prompts}

Based on this information:

### Instructions:
Generate exactly 2–3 **Course Outcomes (COs)** per unit, numbered like:
- CO1: ...
- CO2: ...
- ...

Also, generate exactly 6 **Program Outcomes (POs)** based on the program goals and graduate attributes, numbered like:
- PO1: ...
- PO2: ...
- ...

Each outcome must be:
- Actionable and measurable
- Use verbs aligned with Bloom's Taxonomy
- Written in concise, academic language

Output only two sections:
---
### Course Outcomes
- CO1: ...
- CO2: ...
...

### Program Outcomes
- PO1: ...
- PO2: ...
...
---
Do NOT include any other text or explanation.
"""
    return prompt


def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(data["subject_title"], styles["Title"]))
    story.append(Spacer(1, 12))

    # Metadata
    metadata = [
        f"Program: {data['program']}",
        f"Semester: {data['semester']}",
        f"Prerequisites: {data['prerequisites']}",
        f"Credits: {data['credits']}"
    ]
    for line in metadata:
        story.append(Paragraph(line, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Aim
    story.append(Paragraph("Overall Aim", styles["Heading2"]))
    story.append(Paragraph(data["aim"], styles["Normal"]))
    story.append(Spacer(1, 12))

    # Course Outcomes
    story.append(Paragraph("Course Outcomes (COs)", styles["Heading2"]))
    for co in data["course_outcomes"]:
        story.append(Paragraph(f"<b>{co.split(':')[0]}:</b> {':'.join(co.split(':')[1:])}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Program Outcomes
    story.append(Paragraph("Program Outcomes (POs)", styles["Heading2"]))
    for po in data["program_outcomes"]:
        story.append(Paragraph(f"<b>{po.split(':')[0]}:</b> {':'.join(po.split(':')[1:])}", styles["Normal"]))

    story.append(Spacer(1, 24))
    doc.build(story)



subjects = [
    {
        "subject_title": "Machine Learning",
        "program": "B.Tech in Computer Science",
        "semester": "5th Semester",
        "prerequisites": "Linear Algebra, Python Programming",
        "credits": "3 Lecture Hours, 1 Tutorial, 2 Practical",
        "aim": "To enable students to understand and apply key machine learning algorithms and evaluate their performance in real-world applications.",
        "units": [
            {"title": "Introduction to ML", "focus": "Foundations and key concepts", "outcome_focus": "Define ML types, Explain real-world applications", "blooms_levels": ["Remembering", "Understanding"]},
            {"title": "Regression Techniques", "focus": "Linear and logistic regression", "outcome_focus": "Apply regression models", "blooms_levels": ["Applying", "Analyzing"]},
            {"title": "Classification", "focus": "Decision trees, k-NN, SVM", "outcome_focus": "Compare classifiers", "blooms_levels": ["Analyzing", "Evaluating"]},
            {"title": "Clustering", "focus": "K-means, hierarchical clustering", "outcome_focus": "Evaluate clustering effectiveness", "blooms_levels": ["Evaluating"]},
            {"title": "Model Evaluation", "focus": "Bias-variance trade-off, cross-validation", "outcome_focus": "Design model selection strategy", "blooms_levels": ["Creating", "Evaluating"]}
        ],
        "program_goals": "To produce graduates capable of applying machine learning to solve practical problems and contribute to AI innovations.",
        "graduate_attributes": [
            "Strong foundation in algorithms and mathematics",
            "Problem-solving using data-driven techniques",
            "Effective communication and teamwork",
            "Ethical decision-making in AI",
            "Lifelong learning and adaptability"
        ]
    },
    {
        "subject_title": "Database Management Systems",
        "program": "B.Tech in Computer Science",
        "semester": "4th Semester",
        "prerequisites": "Data Structures, Basic SQL",
        "credits": "3 Lecture Hours, 1 Tutorial, 1 Practical",
        "aim": "To provide students with foundational knowledge of relational databases, query languages, normalization, and transaction management.",
        "units": [
            {"title": "Introduction to DBMS", "focus": "Database architecture, ER Model", "outcome_focus": "Explain DBMS vs File System", "blooms_levels": ["Remembering", "Understanding"]},
            {"title": "Relational Model", "focus": "Keys, Constraints, Relational Algebra", "outcome_focus": "Apply relational algebra operations", "blooms_levels": ["Applying", "Analyzing"]},
            {"title": "SQL Queries", "focus": "DDL, DML, Joins", "outcome_focus": "Write complex queries", "blooms_levels": ["Applying", "Creating"]},
            {"title": "Normalization", "focus": "1NF to BCNF", "outcome_focus": "Normalize database schema", "blooms_levels": ["Analyzing", "Evaluating"]},
            {"title": "Transactions", "focus": "ACID properties, Concurrency Control", "outcome_focus": "Manage transactions", "blooms_levels": ["Understanding", "Applying"]}
        ],
        "program_goals": "To prepare students to design, implement, and manage robust database systems for enterprise applications.",
        "graduate_attributes": [
            "Proficiency in data modeling and query writing",
            "Ability to handle large-scale data",
            "Attention to data integrity and security",
            "Collaboration and documentation skills",
            "Ethical handling of sensitive data"
        ]
    },
    {
        "subject_title": "Operating System",
        "program": "B.Tech in Computer Science",
        "semester": "5th Semester",
        "prerequisites": "C Programming, Computer Organization",
        "credits": "3 Lecture Hours, 1 Tutorial, 0 Practical",
        "aim": "To introduce the core principles of operating systems including process scheduling, memory management, and file systems.",
        "units": [
            {"title": "Introduction to OS", "focus": "Types, Functions, Structure", "outcome_focus": "Describe functions of an OS", "blooms_levels": ["Remembering", "Understanding"]},
            {"title": "Process Management", "focus": "Scheduling, Deadlock", "outcome_focus": "Implement scheduling algorithms", "blooms_levels": ["Applying", "Analyzing"]},
            {"title": "Memory Management", "focus": "Paging, Segmentation", "outcome_focus": "Analyze memory allocation strategies", "blooms_levels": ["Analyzing", "Evaluating"]},
            {"title": "File Systems", "focus": "Directory structures, Allocation methods", "outcome_focus": "Explain file system design", "blooms_levels": ["Understanding"]},
            {"title": "Concurrency & Synchronization", "focus": "Semaphores, Monitors", "outcome_focus": "Design synchronization solutions", "blooms_levels": ["Creating", "Evaluating"]}
        ],
        "program_goals": "To equip students with the ability to understand and work with system-level software and resource management.",
        "graduate_attributes": [
            "Understanding of system-level abstraction",
            "Efficient problem-solving in constrained environments",
            "Logical reasoning and algorithmic thinking",
            "Team collaboration and project-based learning"
        ]
    },
    {
        "subject_title": "Computer Networks",
        "program": "B.Tech in Computer Science",
        "semester": "6th Semester",
        "prerequisites": "Digital Electronics, Data Communication Basics",
        "credits": "3 Lecture Hours, 1 Tutorial, 2 Practical",
        "aim": "To provide a strong foundation in network architecture, protocols, and communication mechanisms used in modern computer networks.",
        "units": [
            {"title": "Network Fundamentals", "focus": "OSI & TCP/IP Models", "outcome_focus": "Describe network layers and functions", "blooms_levels": ["Remembering", "Understanding"]},
            {"title": "Physical Layer", "focus": "Transmission media, Encoding", "outcome_focus": "Explain signal encoding techniques", "blooms_levels": ["Understanding", "Analyzing"]},
            {"title": "Data Link Layer", "focus": "Error detection, Flow control", "outcome_focus": "Apply error correction techniques", "blooms_levels": ["Applying", "Analyzing"]},
            {"title": "Network Layer", "focus": "Routing, IP Addressing", "outcome_focus": "Configure basic routing", "blooms_levels": ["Applying", "Creating"]},
            {"title": "Transport & Application Layer", "focus": "TCP/UDP, HTTP, FTP", "outcome_focus": "Differentiate between transport layer protocols", "blooms_levels": ["Analyzing", "Evaluating"]}
        ],
        "program_goals": "To develop competence in designing and managing networked systems and understanding internet-based communication.",
        "graduate_attributes": [
            "Knowledge of modern networking standards",
            "Ability to configure and troubleshoot network setups",
            "Awareness of network security principles",
            "Collaborative and analytical mindset"
        ]
    }
]

# Process each subject
for subj in subjects:
    print(f"\n📘 GENERATING SYLLABUS FOR: {subj['subject_title']}")

    full_prompt = build_prompt(**subj)
    try:
        response = model.generate_content(full_prompt)
        text_output = response.text

        # Parse COs and POs
        lines = [line.strip() for line in text_output.splitlines()]

        course_outcomes = []
        program_outcomes = []

        in_cos = False
        in_pos = False

        for line in lines:
            if line.startswith("### Course Outcomes"):
                in_cos = True
                in_pos = False
            elif line.startswith("### Program Outcomes"):
                in_cos = False
                in_pos = True
            elif line.startswith("- CO") and in_cos:
                course_outcomes.append(line[2:].strip())
            elif line.startswith("- PO") and in_pos:
                program_outcomes.append(line[2:].strip())

        # Fallback in case parsing failed
        if not course_outcomes or not program_outcomes:
            print("⚠️ Failed to parse COs/POs from response. Using dummy ones.")
            course_outcomes = ["CO1: Understand basic concepts", "CO2: Apply principles"]
            program_outcomes = ["PO1: Apply engineering knowledge", "PO2: Solve complex problems"]

        pdf_data = {
            "subject_title": subj["subject_title"],
            "program": subj["program"],
            "semester": subj["semester"],
            "prerequisites": subj["prerequisites"],
            "credits": subj["credits"],
            "aim": subj["aim"],
            "course_outcomes": course_outcomes,
            "program_outcomes": program_outcomes
        }

        # Save as PDF
        filename = f"{subj['subject_title'].replace(' ', '_')}_Syllabus.pdf"
        create_pdf(pdf_data, filename)
        print(f"✅ Saved PDF: {filename}")

    except Exception as e:
        print(f"❌ Error generating content for {subj['subject_title']}: {e}")