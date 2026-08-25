# Reffery — Product Overview & User Flow

---

## What is Reffery?

Reffery is an AI-powered employee referral platform that connects qualified job seekers with employees willing to provide genuine referrals.

Unlike LinkedIn, which focuses on networking, or traditional job boards that focus on applications, Reffery focuses on one objective: **helping the right candidate receive a genuine employee referral quickly and transparently.**

The platform uses AI to evaluate candidates, simplify referral requests, reduce spam, and help employees make informed referral decisions.

Our goal is not to keep users engaged on the platform, but to help them secure the right opportunity and move forward in their careers.

---

## The Users

Reffery has four primary user types.

### 1. Candidate

Someone actively looking for a new opportunity.

Candidates can:
- Create a professional profile
- Upload their resume
- Connect LinkedIn
- Add GitHub, Portfolio, Behance, Kaggle, LeetCode, etc.
- Receive endorsements
- Request referrals
- Track referral progress

### 2. Referrer

An employee willing to refer candidates within their company. Every user can become a referrer simply by posting a referral.

Referrers can:
- Post referral opportunities
- Specify available referral slots
- Upload or paste Job Descriptions
- Select mandatory requirements
- Review AI-ranked candidates
- Accept or decline referral requests
- Track referral progress

### 3. Hiring Team (Future)

Talent Acquisition teams and Hiring Managers.

Future capabilities include:
- Receive AI-ranked candidates
- Manage referrals
- View referral analytics
- Collaborate with employees

### 4. Administrator

Platform moderation.

Responsibilities include:
- Verify users
- Review reports
- Remove spam
- Prevent abuse
- Manage companies

---

## Candidate Journey

**Step 1 — Sign up.** LinkedIn, Google, or Email. LinkedIn is recommended because it verifies professional identity.

**Step 2 — Complete profile.** Resume, skills, experience, education, certifications, portfolio, GitHub, LinkedIn, work authorization, preferred locations, salary expectations, visa status (optional).

**Step 3 — AI Profile Analysis.** AI evaluates technical skills, soft skills, experience, career progression, strengths, missing skills, and resume quality — then gives the user recommendations to improve their profile.

**Step 4 — Collect Endorsements.** From managers, team leads, professors, senior colleagues. Endorsements increase trust and help referrers make decisions.

**Step 5 — Search Referrals.** Filters: company, role, location, remote, experience, visa sponsorship, salary (optional), technology.

**Step 6 — Open Referral.** Each referral listing shows: company, position, official job link, job ID, referral deadline, number of slots, experience required, mandatory skills, preferred skills, visa sponsorship, location, about the team, referrer profile.

**Step 7 — Request Referral.** One click. The request bundles resume, AI match score, endorsements, portfolio, and a cover message — no unnecessary back-and-forth messaging before the request goes in.

**Step 8 — Referral Queue.** The request enters the employee's queue. Instead of hundreds of random LinkedIn messages, the employee receives organized referral requests.

---

## AI Evaluation

When a request arrives, AI automatically compares the candidate's resume against the job description, evaluating: mandatory requirements, preferred skills, experience, transferable skills, career progression, education, certifications, projects, portfolio, and soft skills.

Rather than searching for keywords, AI explains *why* someone is or isn't a good match.

**Example output:**

> **Overall Match: 87%**
>
> **Strengths**
> ✓ Python ✓ AWS ✓ Backend Development ✓ 6 years experience
>
> **Potential Concerns**
> - Kubernetes experience is limited
> - Leadership experience not demonstrated
>
> **Recommendation:** Strong candidate for referral.

---

## Employee Workflow

The employee opens the referral dashboard. For each request they see: AI summary, resume, LinkedIn, portfolio, endorsements, recommendation.

Instead of reviewing 100 resumes manually, employees review AI-assisted summaries.

**Employee decisions:** Accept Referral / Decline Referral / Need More Information.

If accepted, referral status changes to **Accepted**.

---

## Referral Tracking

*(Canonical status list — used consistently across all Reffery documents.)*

Requested → Accepted → Submitted → Application Received → Recruiter Reviewing → Interview Scheduled → Interview Completed → Offer Received → Offer Accepted → Joined

Terminal/exit states, reachable from any point in the flow: **Rejected**, **Withdrawn**.

Both parties can update the status where appropriate, creating transparency throughout the process.

---

## Referrer Journey

1. Employee signs in, clicks **Become a Referrer**.
2. Creates a referral, inputs: official job URL, job description, job ID, referral deadline, referral slots, experience, mandatory skills, preferred skills, visa sponsorship, location, optional salary.
3. AI extracts the requirements automatically from the job description; the referrer reviews and edits before publishing.

### AI Job Parsing

When the employee pastes the job description, AI automatically extracts: role, experience, required technologies, preferred technologies, soft skills, education, certifications, employment type, location, visa sponsorship. The employee simply confirms or edits.

---

## Reputation System

**Candidates:** referral success rate, profile completion, endorsements, response rate, verification status.

**Referrers:** referral completion rate, response rate, acceptance rate, successful hires, verification, company verification.

---

## Notifications

Users are notified when: a referral is accepted or declined, an interview is scheduled, status changes, a new endorsement is received, or a new referral matches their profile.

---

## Pricing Tiers

**Free:** daily referral requests, basic AI, basic filters.

**Premium:** more referral requests, advanced AI analysis, resume improvement suggestions, advanced search filters, priority support.

---

## Future Enterprise Platform

After validating the marketplace, Reffery expands into enterprise hiring tools: ATS integrations, AI-ranked candidate recommendations, referral performance analytics, hiring metrics, employee referral program management, and hiring insight reports.

The marketplace remains the foundation; enterprise capabilities become an additional product line — not a launch dependency.

---

## Product Philosophy

Everything in Reffery is designed around one principle:

> We don't measure success by how long users stay on our platform. We measure success by how quickly we help the right candidate connect with the right employee, earn a genuine referral, and secure the right opportunity.

Reffery is not trying to become another social network or replace LinkedIn. It exists to solve one problem exceptionally well: making trusted employee referrals easier, faster, and more transparent for everyone involved.

---

## Suggested Next Documents

1. **Functional Requirements Specification (FRS)** — every feature in engineering detail.
2. **Database Design** — tables, relationships, data models.
3. **UI/UX Specification** — every screen and interaction.
4. **API Specification** — endpoints and integrations.
5. **AI Design Document** — how the AI evaluates candidates, parses job descriptions, and generates recommendations.

Together with this Product Overview, these form a complete blueprint a development team can build from.
