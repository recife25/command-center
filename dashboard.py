import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Command Center", layout="wide")

st.title("🧭 Felipe's Command Center")

# Daily Briefing
st.header("📅 Daily Briefing")
briefing = requests.get(f"{API_BASE}/daily-briefing").json()["briefing"]
st.text(briefing)

# Free Time Blocks
st.header("⏱ Free Time Blocks for Tomorrow")
blocks = requests.get(f"{API_BASE}/free-blocks").json()["free_blocks"]
st.text(blocks)

# Manual Mode
st.header("🛠 Manual Mode")

manual = requests.get(f"{API_BASE}/manual-mode").json()

st.subheader("Steps")
for step in manual["manual_steps"]:
    st.text(step)

st.subheader("Last Manual Run")
st.text(manual["last_run"])

st.header("💼 Job Search")

job = requests.get(f"{API_BASE}/job-search").json()

st.subheader("Applications Today")
st.text(job["applications_today"])

st.subheader("Follow-ups Due")
st.text(job["followups_due"])

st.subheader("Spreadsheet Status")
st.text(job["spreadsheet_status"])

st.subheader("Job Agent Status")
st.text(job["job_agent_status"])

st.subheader("Next Steps")
for step in job["next_steps"]:
    st.text(f"- {step}")

# Add Application Form
st.header("➕ Add Job Application")

with st.form("application_form"):
    col1, col2 = st.columns(2)

    with col1:
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        url = st.text_input("URL")
        status = st.selectbox("Status", ["Applied", "Interviewing", "Rejected", "Offer", "Saved"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    
    with col2:
        date_applied = st.date_input("Date Applied", datetime.now())
        followup_date = st.date_input("Follow-up Date", None)
        resume_version = st.text_input("Resume Version")
        cover_letter_version = st.text_input("Cover Letter Version")
        notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add Application")
    cleared = st.form_submit_button("Clear Form")
    
    if cleared:
        st.session_state["clear_application_form"] = True

    if submitted:
        payload = {
            "job_title": job_title,
            "company": company,
            "url": url,
            "date_applied": str(date_applied),
            "status": status,
            "followup_date": str(followup_date),
            "notes": notes,
            "priority": priority,
            "resume_version": resume_version,
            "cover_letter_version": cover_letter_version
        }

        response = requests.post(f"{API_BASE}/applications/add", json=payload)


        if response.status_code == 200:
            st.success("Application added successfully!")
        else:
            st.error("Failed to add application.")
            
# OUTSIDE the form block
if "application_form" in st.session_state:
    del st.session_state["clear_application_form"]
    st.rerun()

            
# Follow-ups
st.header("🔔 Follow-Up Reminders")

follow = requests.get(f"{API_BASE}/followups").json()
reminders = follow["reminders"]

if len(reminders) == 0:
    st.success("No follow-ups due today.")
else:
    for r in reminders:
        st.warning(
            f"{r['job_title']} at {r['company']} — Follow-up was due on {r['followup_date']} (Status: {r['status']})"
        )
# LinkedIn Tasks
st.header("💼 LinkedIn Upgrade Tasks")

linkedin = requests.get(f"{API_BASE}/linkedin-tasks").json()

for section in linkedin["tasks"]:
    st.subheader(section["section"])
    for item in section["items"]:
        st.text(f"- {item}")
# Study Tasks
st.header("📚 Study Tasks")

study = requests.get(f"{API_BASE}/study-tasks").json()

for course in study["tasks"]:
    st.subheader(course["course"])
    st.write(f"Total Hours: {course['hours_total']}")
    st.write(f"Completed: {course['hours_completed']}")
    st.write("Modules:")
    for module in course["modules"]:
        st.text(f"- {module}")

# Job Agent Status
st.header("🤖 Job Agent Status")

agent = requests.get(f"{API_BASE}/job-agent").json()

st.write(f"Status: {agent['status']}")

st.subheader("System Checks")
for key, value in agent["checks"].items():
    st.write(f"- {key}: {value}")

st.subheader("Next Steps")
for step in agent["next_steps"]:
    st.text(f"- {step}")


