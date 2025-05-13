
import os
import google.generativeai as genai

# Load API key securely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY is not set!")
genai.configure(api_key=GOOGLE_API_KEY)

# List available models
models = genai.list_models()
print("Available models:")
for model in models:
    print(model.name)

# Initialize model (use a valid model name)
model = genai.GenerativeModel('gemini-1.5-flash')  # Or 'gemini-pro'

response = model.generate_content("Say hello!")
print(response.text)
# Prompt builder function remains unchanged
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
You are an education expert helping generate course and program outcomes for a university syllabus.

Subject Title: {subject_title}
Program: {program}
Semester: {semester}
Prerequisites: {prerequisites}
Credits: {credits}

Overall Subject Aim:
{aim}

{unit_prompts}

Now, generate 2–3 clear Course Outcomes (COs) for each unit, using Bloom’s taxonomy levels.

Also, based on the overall subject and program, generate 5–6 Program Outcomes (POs) with measurable, action-based language.

Program Goals: {program_goals}

Graduate Attributes:
{graduate_attr_str}

Output the result in a clear format with:
- Course Outcomes per Unit
- Final Program Outcomes
"""
    return prompt

# Example usage (unchanged)
subject_title = "Machine Learning"
program = "B.Tech in Computer Science"
semester = "5th Semester"
prerequisites = "Linear Algebra, Python Programming"
credits = "3 Lecture Hours, 1 Tutorial, 2 Practical"

aim = "To enable students to understand and apply key machine learning algorithms and evaluate their performance in real-world applications."

units = [
    {"title": "Introduction to ML", "focus": "Foundations and key concepts", "outcome_focus": "Define ML types, Explain real-world applications", "blooms_levels": ["Remembering", "Understanding"]},
    {"title": "Regression Techniques", "focus": "Linear and logistic regression", "outcome_focus": "Apply regression models", "blooms_levels": ["Applying", "Analyzing"]},
    {"title": "Classification", "focus": "Decision trees, k-NN, SVM", "outcome_focus": "Compare classifiers", "blooms_levels": ["Analyzing", "Evaluating"]},
    {"title": "Clustering", "focus": "K-means, hierarchical clustering", "outcome_focus": "Evaluate clustering effectiveness", "blooms_levels": ["Evaluating"]},
    {"title": "Model Evaluation", "focus": "Bias-variance trade-off, cross-validation", "outcome_focus": "Design model selection strategy", "blooms_levels": ["Creating", "Evaluating"]}
]

program_goals = "To produce graduates capable of applying machine learning to solve practical problems and contribute to AI innovations."

graduate_attributes = [
    "Strong foundation in algorithms and mathematics",
    "Problem-solving using data-driven techniques",
    "Effective communication and teamwork",
    "Ethical decision-making in AI",
    "Lifelong learning and adaptability"
]

# Generate prompt
full_prompt = build_prompt(subject_title, program, semester, prerequisites, credits, aim, units, program_goals, graduate_attributes)

# Generate outcome using Gemini with optional safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
]

try:
    response = model.generate_content(full_prompt, safety_settings=safety_settings)
    print("\n📘 GENERATED COURSE AND PROGRAM OUTCOMES:\n")
    print(response.text)
except Exception as e:
    print(f"Failed to generate response: {e}")