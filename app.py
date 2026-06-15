from flask import Flask, render_template, request
import os
import pdfplumber

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Skill database
SKILL_DB = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "data analysis",
    "git",
    "github",
    "flask",
    "django",
    "pandas",
    "numpy",
    "matplotlib",
    "problem solving",
    "dsa"
]

# Resume section database
SECTION_DB = {
    "Education": "education",
    "Projects": "projects",
    "Experience": "experience",
    "Technical Skills": "technical skills",
    "Achievements": "achievements",
    "GitHub": "github",
    "LinkedIn": "linkedin",
    "Certifications": "certification"
}


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    matched_skills = []
    missing_skills = []

    found_sections = []
    missing_sections = []

    if request.method == "POST":

        file = request.files["resume"]
        job_desc = request.form.get("job_desc", "")

        if file.filename != "":

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            # Extract text from PDF
            text = ""

            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text

            text_lower = text.lower()

            # Resume Health Check
            for display_name, keyword in SECTION_DB.items():

                if keyword in text_lower:
                    found_sections.append(display_name)

                else:
                    missing_sections.append(display_name)

            # Resume Skills
            resume_skills = []

            for skill in SKILL_DB:
                if skill in text_lower:
                    resume_skills.append(skill)

            # Job Description Skills
            jd_lower = job_desc.lower()

            jd_skills = []

            for skill in SKILL_DB:
                if skill in jd_lower:
                    jd_skills.append(skill)

            # ATS Matching
            for skill in jd_skills:

                if skill in resume_skills:
                    matched_skills.append(skill)

                else:
                    missing_skills.append(skill)

            if len(jd_skills) > 0:

                score = round(
                    (len(matched_skills) / len(jd_skills)) * 100,
                    2
                )

            else:
                score = 0

    return render_template(
        "index.html",
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        found_sections=found_sections,
        missing_sections=missing_sections
    )


if __name__ == "__main__":
    app.run(debug=True)