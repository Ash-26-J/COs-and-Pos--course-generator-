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
You are an education expert helping generate course and program outcomes for university syllabi.

Subject Title: {subject_title}
Program: {program}
Semester: {semester}
Prerequisites: {prerequisites}
Credits: {credits}

Overall Subject Aim:
{aim}

{unit_prompts}

Now, generate 2–3 clear Course Outcomes (COs) for each unit using Bloom's Taxonomy levels.

Also, based on the overall subject and program, generate 5–6 Program Outcomes (POs) with measurable, action-based language.

Program Goals: {program_goals}

Graduate Attributes:
{graduate_attr_str}

Output the result in a clear format with:
- Course Outcomes per Unit
- Final Program Outcomes
"""
    return prompt


def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Course Outcomes", styles["Heading1"]))
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

    # Units
    story.append(Paragraph("Units and Course Outcomes", styles["Heading2"]))
    for idx, co in enumerate(data["course_outcomes"], start=1):
        story.append(Paragraph(f"<b>Unit {idx}:</b> {co}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Program Outcomes
    story.append(Paragraph("Program Outcomes", styles["Heading2"]))
    for po in data["program_outcomes"]:
        story.append(Paragraph(po, styles["Normal"]))
    story.append(Spacer(1, 24))

    doc.build(story)


# Example Subjects
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
    }
]

# Process each subject
for subj in subjects:
    print(f"\n📘 GENERATING SYLLABUS FOR: {subj['subject_title']}")

    full_prompt = build_prompt(**subj)
    try:
        response = model.generate_content(full_prompt)
        text_output = response.text

        # Extract COs and POs from response (basic parsing — adjust if needed)
        lines = text_output.splitlines()
        course_outcomes = [line.strip("- ") for line in lines if line.startswith("- CO") or line.startswith("CO")]
        program_outcomes = [line.strip("- ") for line in lines if line.startswith("- PO") or line.startswith("PO")]

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