import os
import csv
from fastapi import FastAPI, Form
from daily_briefing import DailyBriefing
from calendar_scheduler import CalendarScheduler
from datetime import datetime
from fastapi import FastAPI
from database import get_connection, initialize_database


app = FastAPI()
initialize_database()

briefing = DailyBriefing()
scheduler = CalendarScheduler()

@app.get("/daily-briefing")
def get_daily_briefing():
    return {"briefing": briefing.generate_briefing()}

@app.get("/free-blocks")
def get_free_blocks():
    return {"free_blocks": scheduler.schedule_tasks()}

@app.get("/manual-mode")
def manual_mode():
    now = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p")

    return {
        "manual_steps": [
            "Start FastAPI: uvicorn api:app --reload",
            "Start Streamlit: streamlit run dashboard.py",
            "Optional: python orchestrator.py"
        ],
        "last_run": now
    }

@app.get("/job-search")
def job_search():
    spreadsheet_exists = os.path.exists("job_applications.csv")

    if spreadsheet_exists:
        with open("job_applications.csv", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            applications_today = len(rows)
            followups_due = sum(1 for r in rows if r["Follow-up Date"])
        spreadsheet_status = "Ready"
    else:
        applications_today = 0
        followups_due = 0
        spreadsheet_status = "Not created yet"

    return {
        "applications_today": applications_today,
        "followups_due": followups_due,
        "spreadsheet_status": spreadsheet_status,
        "job_agent_status": "Inactive",
        "next_steps": [
            "Add job applications to the spreadsheet",
            "Set follow-up dates",
            "Begin LinkedIn profile upgrade",
            "Prepare resume versions"
        ]
    }


@app.post("/add-application")
def add_application(
    job_title: str = Form(...),
    company: str = Form(...),
    url: str = Form(...),
    date_applied: str = Form(...),
    status: str = Form(...),
    followup_date: str = Form(""),
    notes: str = Form(""),
    priority: str = Form(""),
    resume_version: str = Form(""),
    cover_letter_version: str = Form("")
):
    file_exists = os.path.exists("job_applications.csv")

    with open("job_applications.csv", "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Job Title", "Company", "URL", "Date Applied", "Status",
                "Follow-up Date", "Notes", "Priority",
                "Resume Version", "Cover Letter Version"
            ])

        writer.writerow([
            job_title, company, url, date_applied, status,
            followup_date, notes, priority,
            resume_version, cover_letter_version
        ])

    return {"message": "Application added successfully"}


@app.get("/followups")
def followups():
    reminders = []
    today = datetime.now().date()

    if os.path.exists("job_applications.csv"):
        with open("job_applications.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                follow_date = row.get("Follow-up Date", "").strip()

                if follow_date:
                    try:
                        parsed = datetime.strptime(follow_date, "%Y-%m-%d").date()
                        if parsed <= today:
                            reminders.append({
                                "job_title": row["Job Title"],
                                "company": row["Company"],
                                "followup_date": follow_date,
                                "status": row["Status"]
                            })
                    except:
                        pass

    return {"reminders": reminders}


@app.get("/linkedin-tasks")
def linkedin_tasks():
    return {
        "tasks": [
            {
                "section": "Headline",
                "items": [
                    "Rewrite headline to include role + specialty + value",
                    "Add keywords relevant to QA, AI, Automation"
                ]
            },
            {
                "section": "About",
                "items": [
                    "Write a strong 3–4 paragraph About section",
                    "Highlight QA automation, AI workflows, FastAPI, Streamlit",
                    "Add career goals and value proposition"
                ]
            },
            {
                "section": "Experience",
                "items": [
                    "Rewrite bullet points for clarity and impact",
                    "Add measurable achievements",
                    "Align descriptions with job search targets"
                ]
            },
            {
                "section": "Skills",
                "items": [
                    "Add all relevant technical skills",
                    "Reorder skills based on job search priority",
                    "Endorse key skills"
                ]
            },
            {
                "section": "Featured",
                "items": [
                    "Add resume PDF",
                    "Add portfolio link",
                    "Add Command Center screenshot",
                    "Add GitHub projects"
                ]
            }
        ]
    }
@app.get("/study-tasks")
def study_tasks():
    return {
        "tasks": [
            {
                "course": "IBM AI Fundamentals",
                "hours_total": 10,
                "hours_completed": 0,
                "modules": [
                    "Introduction to AI",
                    "Machine Learning Basics",
                    "Neural Networks Overview",
                    "AI Ethics",
                    "Final Assessment"
                ]
            },
            {
                "course": "AWS AI Practitioner",
                "hours_total": 10,
                "hours_completed": 0,
                "modules": [
                    "AI Concepts",
                    "AWS AI Services",
                    "ML on AWS",
                    "Responsible AI",
                    "Final Exam Prep"
                ]
            },
            {
                "course": "Python",
                "hours_total": 20,
                "hours_completed": 0,
                "modules": [
                    "Syntax & Variables",
                    "Functions",
                    "Modules & Packages",
                    "APIs & FastAPI",
                    "Automation Scripts"
                ]
            },
            {
                "course": "QA Automation",
                "hours_total": 15,
                "hours_completed": 0,
                "modules": [
                    "Testing Fundamentals",
                    "Selenium",
                    "PyTest",
                    "CI/CD",
                    "Automation Frameworks"
                ]
            }
        ]
    }
@app.get("/job-agent")
def job_agent():
    # Check spreadsheet
    spreadsheet_exists = os.path.exists("job_applications.csv")

    # Check follow-up logic
    followups_ready = False
    if spreadsheet_exists:
        with open("job_applications.csv", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            followups_ready = len(rows) > 0

    # Check LinkedIn tasks (always ready)
    linkedin_ready = True

    # Check study tasks (always ready)
    study_ready = True

    # Determine agent status
    if spreadsheet_exists and followups_ready:
        status = "Ready"
    else:
        status = "Inactive"

    return {
        "status": status,
        "checks": {
            "spreadsheet_exists": spreadsheet_exists,
            "has_applications": followups_ready,
            "linkedin_tasks_ready": linkedin_ready,
            "study_tasks_ready": study_ready
        },
        "next_steps": [
            "Add at least one job application",
            "Set follow-up dates",
            "Complete LinkedIn headline rewrite",
            "Complete at least one study module"
        ]
    }


@app.post("/applications/add")
def add_application(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (
            job_title, company, url, date_applied, status,
            followup_date, priority, resume_version,
            cover_letter_version, notes, contact_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("job_title"),
        data.get("company"),
        data.get("url"),
        data.get("date_applied"),
        data.get("status"),
        data.get("followup_date"),
        data.get("priority"),
        data.get("resume_version"),
        data.get("cover_letter_version"),
        data.get("notes"),
        data.get("contact_id")
    ))

    conn.commit()
    conn.close()

    return {"message": "Application added successfully"}

@app.get("/applications/all")
def get_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()

    conn.close()

    return {"applications": [dict(row) for row in rows]}
