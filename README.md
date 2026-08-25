# Reffery

AI-powered employee referral platform — Python implementation of the complete application workflow.

## Features

This MVP implements the full Reffery workflow:

1. **Sign up** — Email auth (LinkedIn/Google stubs ready)
2. **Role selection** — Candidate, Referrer, or Both
3. **Profile completion** — Resume, skills, experience, links
4. **AI profile analysis** — Readiness score and resume suggestions
5. **Endorsements** — Request and approve endorsements
6. **Referrer creates referral** — Job description with AI parsing
7. **Referral published** — Searchable with filters
8. **Candidate finds referral** — Search and AI recommendations
9. **Request referral** — AI match evaluation
10. **Referrer review** — Accept or decline with AI summary
11. **Status tracking** — Full canonical status flow
12. **Notifications & reputation** — Points and alerts

## Prerequisites

- Python 3.11+

## Setup

```powershell
cd C:\Users\princ\Downloads\Reffery
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

## Demo Accounts

After running `seed.py`:

| Role | Email | Password |
|------|-------|----------|
| Candidate | candidate@example.com | password123 |
| Referrer | referrer@example.com | password123 |

## API Documentation

Interactive API docs: **http://127.0.0.1:8000/docs**

Authentication uses the `X-User-Id` header (set automatically by the web UI after login).

## Project Structure

```
Reffery/
├── app/
│   ├── main.py              # FastAPI app + web UI
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # API endpoints
│   ├── services/            # AI, auth, notifications, reputation
│   ├── static/              # CSS + JS
│   └── templates/           # HTML pages
├── docs/                    # Product documentation
├── requirements.txt
└── seed.py                  # Demo data
```

## Referral Status Flow

```
Requested → Accepted → Submitted → Application Received → Recruiter Reviewing
→ Interview Scheduled → Interview Completed → Offer Received → Offer Accepted → Joined
```

Terminal states: **Rejected**, **Withdrawn**

## Next Steps

- Plug in OpenAI/Anthropic for real AI analysis in `app/services/ai_service.py`
- Add OAuth for LinkedIn and Google
- Switch SQLite to PostgreSQL for production
- Add email notifications
