import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re
import tempfile
import os
from fpdf import FPDF
from PIL import Image

# Function to extract skills using regex
def extract_skills_from_text(text):
    skill_pattern = re.compile(r'(?i)\b(html|css|javascript|react(?:\.js)?|node(?:\.js)?|redux|vue(?:\.js)?|ui/ux design|responsive web development|rest(?:ful)? apis?|git|version control|flask|django|python|sql|excel|tableau|c\+\+|java|r|aws|azure|google cloud|linux|docker|kubernetes|machine learning|data analysis|tensorflow|pytorch|communication|leadership|agile|scrum|project management|technical writing|selenium|bug tracking|data visualization|microcontrollers|rtos|hardware interfacing|adobe xd|sketch|prototyping|research|product management|teamwork|statistics|virtualization|testing|manual testing|automation testing|penetration testing|risk management|networking|cisco|routing|switching|firewalls|threat analysis|security|documentation|rest api|api integration|sql server|oracle|mysql|database tuning|backup and recovery)\b')
    matches = skill_pattern.findall(text.lower())
    return list(set([m.lower().replace(".js", "") for m in matches]))

# Function to generate PDF
def generate_pdf(match_score, matched_skills, missing_skills, chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Match Score: {match_score}%", ln=True)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Matching Skills:", ln=True)
    pdf.set_font("Arial", '', 12)
    for skill in matched_skills:
        pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Missing Skills:", ln=True)
    pdf.set_font("Arial", '', 12)
    for skill in missing_skills:
        pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.ln(10)
    pdf.image(chart_path, w=170)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# Web UI
st.title("🎯 Resume vs Job Description Matcher")

resume_input = st.text_area("Paste your Resume", height=300, placeholder="Paste your resume here...")
# Define job descriptions for all roles
job_descriptions = {
    "Frontend Developer": "Experience in building responsive and interactive web interfaces. Skills required: HTML, CSS, JavaScript, React, Vue, UI/UX design, responsive web development, Git, Redux.",
    "Backend Developer": "Experience in server-side logic and database design. Skills required: Node.js, Express, Python, Django, Flask, SQL, REST APIs, MongoDB, MySQL, version control, Git.",
    "Full Stack Developer": "Experience in both frontend and backend development. Skills required: HTML, CSS, JavaScript, React, Node.js, Express, MongoDB, SQL, REST APIs, Git, deployment.",
    "Software Developer": "Experience in programming, debugging, and software design. Skills required: Python, Java, C++, problem-solving, teamwork.",
    "Python Developer": "Expertise in Python development, API integration, and automation. Skills required: Python, Django, Flask, REST APIs, SQL.",
    "Data Scientist": "Expertise in data analysis, statistical modeling, and machine learning. Skills required: Python, R, machine learning, statistics, data visualization.",
    "Data Analyst": "Experience in data wrangling, analysis, and reporting. Skills required: Python, SQL, Excel, Tableau, data analysis.",
    "Machine Learning Engineer": "Experience in developing machine learning models and AI systems. Skills required: Python, TensorFlow, PyTorch, deep learning, data analysis.",
    "Web Developer": "Experience with front-end and back-end development. Skills required: HTML, CSS, JavaScript, React, Node.js, UI/UX design.",
    "Mobile Developer": "Experience in developing mobile applications. Skills required: Java, Kotlin, Swift, React Native, Flutter, UI design.",
    "DevOps Engineer": "Expertise in CI/CD, containerization, and cloud infrastructure. Skills required: Docker, Kubernetes, AWS, Azure, Linux, Python.",
    "System Administrator": "Experience in managing servers and networks. Skills required: Linux, Windows Server, networking, security, scripting.",
    "Project Manager": "Strong leadership and organizational skills. Skills required: project management, communication, leadership, agile, scrum, planning.",
    "Business Analyst": "Experience in analyzing business processes and data. Skills required: data analysis, communication, Excel, SQL, reporting.",
    "QA Engineer": "Expertise in testing and quality assurance processes. Skills required: manual testing, automation testing, Selenium, bug tracking, attention to detail.",
    "Network Engineer": "Experience with network design, implementation, and troubleshooting. Skills required: networking, Cisco, routing, switching, security.",
    "Cybersecurity Analyst": "Expertise in protecting systems and networks. Skills required: cybersecurity, threat analysis, firewalls, penetration testing, risk management.",
    "Cloud Engineer": "Experience with cloud services and infrastructure management. Skills required: AWS, Azure, Google Cloud, virtualization, automation.",
    "Database Administrator": "Expertise in managing databases and data integrity. Skills required: SQL, Oracle, MySQL, database tuning, backup and recovery.",
    "Embedded Systems Engineer": "Experience with hardware and low-level programming. Skills required: C, C++, microcontrollers, RTOS, hardware interfacing.",
    "UI/UX Designer": "Experience in designing user interfaces and improving user experience. Skills required: UI design, UX research, Adobe XD, Sketch, prototyping.",
    "Technical Writer": "Ability to explain complex technical concepts clearly. Skills required: technical writing, documentation, communication, research.",
    "Product Manager": "Experience in managing product development from ideation to launch. Skills required: product management, communication, market research, agile."
}

# Dropdown to select job role
job_input = st.selectbox("Select the Job Role", list(job_descriptions.keys()))
job_text = job_descriptions[job_input]

if st.button("Analyze"):
    if not resume_input.strip():
        st.warning("Please paste your resume.")
    else:
        job_text = job_descriptions.get(job_input, "")
        resume_skills = extract_skills_from_text(resume_input)
        job_skills = extract_skills_from_text(job_text)

        matched_skills = sorted(set(resume_skills) & set(job_skills))
        missing_skills = sorted(set(job_skills) - set(resume_skills))
        match_score = round((len(matched_skills) / len(job_skills)) * 100, 2) if job_skills else 0

        st.success(f"✅ Match Score: {match_score}%")

        # Tables
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎯 Matching Skills")
            st.table(pd.DataFrame({"Skills": matched_skills}))
        with col2:
            st.markdown("### ❌ Missing Skills")
            st.table(pd.DataFrame({"Skills": missing_skills}))

        # Bar chart
        labels = ['Matching Skills', 'Missing Skills']
        values = [len(matched_skills), len(missing_skills)]
        colors = ['#28a745', '#dc3545']

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=colors)
        ax.set_title("Skill Match Analysis")
        ax.set_ylabel("Number of Skills")

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        chart_path = os.path.join(tempfile.gettempdir(), "skill_chart.png")
        fig.tight_layout()
        plt.savefig(chart_path)
        st.pyplot(fig)

        # Generate PDF
        pdf_path = generate_pdf(match_score, matched_skills, missing_skills, chart_path)
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="resume_match_report.pdf",
                mime="application/pdf"
            )
