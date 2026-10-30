
import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: white;
}
[data-testid="stSidebar"] {
    background: #131b30;
}
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #8b9cff;
}
.subtitle {
    color: #aab4cc;
    font-size: 16px;
}
.section-title {
    color: #a5b4fc;
    font-size: 22px;
    font-weight: bold;
}
.stButton button {
    background: #667eea;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    height: 45px;
    font-weight: bold;
}
.stButton button:hover {
    background: #5265c9;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown(
    '<div class="main-title">🚀 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart Resume Analysis | ATS Keyword Matching | Career Guidance</div>',
    unsafe_allow_html=True
)

st.divider()


# RESUME REFERENCE LIBRARY

resume_library = {

    "Python Full Stack Developer": {
        "skills": [
            "Python", "Django", "Flask", "HTML", "CSS",
            "JavaScript", "React", "SQL", "MySQL",
            "MongoDB", "REST API", "Git", "OOP",
            "Bootstrap", "PostgreSQL"
        ],
        "description": """
Python Full Stack Developer

Required Skills:
Python, Django, Flask, HTML, CSS, JavaScript,
React, SQL, MySQL, MongoDB, REST API,
Git, OOP, Bootstrap, PostgreSQL.

Responsibilities:
Develop web applications using Python and Django.
Build responsive frontend interfaces.
Develop REST APIs and manage databases.
Debug and maintain web applications.
Work with Git and GitHub.
"""
    },

    "Java Full Stack Developer": {
        "skills": [
            "Java", "Spring Boot", "HTML", "CSS",
            "JavaScript", "React", "SQL", "MySQL",
            "REST API", "Git", "OOP", "Bootstrap"
        ],
        "description": """
Java Full Stack Developer

Required Skills:
Java, Spring Boot, HTML, CSS, JavaScript,
React, SQL, MySQL, REST API, Git, OOP,
Bootstrap.

Responsibilities:
Develop backend applications using Java.
Build responsive web interfaces.
Create REST APIs.
Manage databases and application testing.
"""
    },

    "Java Backend Developer": {
        "skills": [
            "Java", "Spring Boot", "SQL", "MySQL",
            "MongoDB", "REST API", "Git", "OOP",
            "Data Structures"
        ],
        "description": """
Java Backend Developer

Required Skills:
Java, Spring Boot, SQL, MySQL, MongoDB,
REST API, Git, OOP, Data Structures.

Responsibilities:
Develop backend services.
Design REST APIs.
Manage databases.
Write reusable and maintainable code.
Debug and test applications.
"""
    },

    "Data Analyst": {
        "skills": [
            "Python", "SQL", "Excel", "Power BI",
            "Pandas", "NumPy", "Data Analysis",
            "Machine Learning"
        ],
        "description": """
Data Analyst

Required Skills:
Python, SQL, Excel, Power BI, Pandas,
NumPy, Data Analysis, Machine Learning.

Responsibilities:
Analyze datasets.
Create reports and dashboards.
Clean and process data.
Identify business trends.
Present analytical insights.
"""
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python", "Machine Learning", "Data Science",
            "Pandas", "NumPy", "SQL", "Scikit-learn",
            "Deep Learning", "Git"
        ],
        "description": """
Machine Learning Engineer

Required Skills:
Python, Machine Learning, Data Science,
Pandas, NumPy, SQL, Scikit-learn,
Deep Learning, Git.

Responsibilities:
Build machine learning models.
Process and analyze datasets.
Train and evaluate algorithms.
Develop predictive systems.
Deploy machine learning applications.
"""
    }
}


# SKILL DATABASE

skills = list(dict.fromkeys(
    skill
    for role in resume_library.values()
    for skill in role["skills"]
))


def detect_skills(text):

    found = []

    for skill in skills:

        pattern = (
            r'(?<![a-zA-Z0-9])'
            + re.escape(skill)
            + r'(?![a-zA-Z0-9])'
        )

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return found


# SIDEBAR

with st.sidebar:

    st.title("⚙️ Dashboard")

    page = st.radio(
        "Choose Section",
        [
            "Resume Analyzer",
            "Resume Reference Library"
        ]
    )

    st.divider()

    st.write("📄 PDF Resume")
    st.write("🧠 Skill Detection")
    st.write("📊 ATS Keyword Matching")
    st.write("🎯 Career Suggestions")


# REFERENCE LIBRARY PAGE

if page == "Resume Reference Library":

    st.title("📚 Resume Reference Library")

    st.write(
        "Explore sample job profiles and their required skills."
    )

    selected_role = st.selectbox(
        "Select a Job Role",
        list(resume_library.keys())
    )

    role_data = resume_library[selected_role]

    st.subheader("🎯 " + selected_role)

    st.write("### Required Skills")

    for skill in role_data["skills"]:
        st.success("✓ " + skill)

    st.write("### Sample Job Description")

    st.text_area(
        "Job Description",
        role_data["description"],
        height=250
    )

    st.info(
        "These are sample role profiles for practice, "
        "not actual employer-approved resumes or job vacancies."
    )


# RESUME ANALYZER PAGE

else:

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            reader = PdfReader(uploaded_file)

            resume_text = ""

            for page in reader.pages:
                resume_text += page.extract_text() or ""

            if not resume_text.strip():

                st.error(
                    "No text found. Upload a text-based PDF."
                )

                st.stop()

            st.success("Resume uploaded successfully!")

            with st.expander("View Resume Content"):
                st.text(resume_text[:5000])

            # DETECT SKILLS

            resume_skills = detect_skills(resume_text)

            st.subheader("🧠 Detected Resume Skills")

            if resume_skills:

                st.write(", ".join(resume_skills))

            else:

                st.warning("No skills detected.")

            # SELECT REFERENCE ROLE

            st.divider()

            st.subheader("🎯 Select Target Job Role")

            selected_role = st.selectbox(
                "Choose a reference job profile",
                list(resume_library.keys())
            )

            default_description = resume_library[
                selected_role
            ]["description"]

            job_description = st.text_area(
                "Edit or enter Job Description",
                value=default_description,
                height=200
            )

            # ANALYZE

            if st.button("🚀 ANALYZE MY RESUME"):

                if not job_description.strip():

                    st.warning("Enter a job description.")

                else:

                    required_skills = detect_skills(
                        job_description
                    )

                    matched_skills = [
                        skill for skill in required_skills
                        if skill in resume_skills
                    ]

                    missing_skills = [
                        skill for skill in required_skills
                        if skill not in resume_skills
                    ]

                    score = (
                        len(matched_skills) /
                        len(required_skills) * 100
                    ) if required_skills else 0

                    # DASHBOARD

                    st.divider()

                    st.subheader("📊 Analysis Dashboard")

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "ATS Keyword Match",
                        f"{score:.1f}%"
                    )

                    c2.metric(
                        "Matched Skills",
                        len(matched_skills)
                    )

                    c3.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )

                    st.subheader("Resume Compatibility")

                    st.progress(int(score))

                    if score >= 80:

                        st.success(
                            "Excellent keyword alignment!"
                        )

                    elif score >= 50:

                        st.info(
                            "Good match. Improve missing skills."
                        )

                    else:

                        st.warning(
                            "More relevant skills are needed."
                        )

                    # TABS

                    tab1, tab2, tab3, tab4 = st.tabs([
                        "Matched Skills",
                        "Missing Skills",
                        "Skill Chart",
                        "Suggestions"
                    ])

                    with tab1:

                        for skill in matched_skills:
                            st.success("✓ " + skill)

                        if not matched_skills:
                            st.info("No matched skills.")

                    with tab2:

                        for skill in missing_skills:
                            st.error("✗ " + skill)

                        if not missing_skills:
                            st.success("No missing skills detected.")

                    with tab3:

                        st.bar_chart({
                            "Skill Count": {
                                "Matched": len(matched_skills),
                                "Missing": len(missing_skills)
                            }
                        })

                    with tab4:

                        st.subheader("Improvement Suggestions")

                        if missing_skills:

                            for skill in missing_skills:
                                st.write(
                                    "📚 Learn and gain experience in **"
                                    + skill + "**"
                                )

                        else:

                            st.success(
                                "All detected required skills are present."
                            )

                        st.write("""
                        - Add practical projects.
                        - Highlight internships.
                        - Include measurable achievements.
                        - Add GitHub project links.
                        - Use clear section headings.
                        """)

                    # DOWNLOAD REPORT

                    report = f"""
AI RESUME ANALYZER REPORT

Target Role: {selected_role}

ATS Keyword Match: {score:.2f}%

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}

Required Skills:
{', '.join(required_skills)}

Note: This is a keyword-based score,
not a guaranteed ATS score or hiring prediction.
"""

                    st.divider()

                    st.download_button(
                        "📥 Download Analysis Report",
                        report,
                        file_name="resume_report.txt",
                        mime="text/plain"
                    )

        except Exception as e:

            st.error(f"Error reading resume: {e}")

    else:

        st.info(
            "Upload your PDF resume to start analysis."
        )
