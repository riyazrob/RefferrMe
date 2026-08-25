# Reffery — Complete Application Workflow

*(Companion to the Product Overview & User Flow doc — this version is the source of truth for status naming; see that doc for detailed screen-level descriptions of each step.)*

---

## 1. User Visits Reffery
Visit website/app → learn about Reffery → click Get Started.

## 2. Sign Up
LinkedIn, Google, or Email.

## 3. Select Your Role
- Looking for Referrals (Candidate)
- I Can Refer People (Referrer)
- Both — users can switch roles anytime.

## 4. Complete Profile
**Candidate:** resume, LinkedIn, experience, skills, education, certifications, portfolio/GitHub/Behance/LeetCode, work authorization, preferred locations.

**Referrer:** verify company, connect company email (optional but recommended), verify employment.

## 5. AI Profile Analysis
AI analyzes resume, skills, experience, career progression, certifications, projects — and generates a profile summary, referral readiness score, and resume suggestions.

## 6. Candidate Requests Endorsements *(optional)*
From manager, professor, team lead, or senior colleague.

## 7. Referrer Creates Referral
Adds company, job link, job ID, job description, referral deadline, number of slots.

## 8. AI Parses Job Description
Extracts role, experience, required/preferred skills, education, certifications, visa sponsorship, location. Referrer reviews and edits before publishing.

## 9. Referral Published
Discoverable via search, filters, or AI recommendations.

## 10. Candidate Finds Referral
Via search (company, role, technology, location, remote, visa sponsorship, experience level) or AI auto-recommendation.

## 11. Candidate Opens Referral
Views company, job description, referrer, required skills, deadline, slots, and an AI match explanation.

## 12. Candidate Requests Referral
Selects resume version, portfolio, cover message → clicks Request Referral.

## 13. AI Evaluates Candidate
Compares candidate profile vs. job requirements → generates match explanation, strengths, missing skills, recommendation.

## 14. Referrer Reviews Requests
Dashboard shows AI summary, resume, LinkedIn, portfolio, endorsements. Referrer accepts or declines.

## 15. Referral Accepted
Candidate is notified. Status → **Accepted**.

## 16. Referral Submitted
Referrer submits the candidate through the company's internal referral process. Status → **Submitted**.

## 17. Referral Tracking

**Canonical status list:**
Requested → Accepted → Submitted → Application Received → Recruiter Reviewing → Interview Scheduled → Interview Completed → Offer Received → Offer Accepted → Joined

Terminal/exit states, reachable from any point: **Rejected**, **Withdrawn**.

## 18. Notifications
Referral accepted/declined, status updates, interview, offer, new endorsements, matching referrals.

## 19. Reputation Updates
**Candidate:** successful referrals, endorsements, profile completion, response rate.
**Referrer:** referral completion rate, successful hires, response time, verification badge.

## 20. AI Learning
After every completed referral, the AI learns from successful referrals, interview outcomes, and hiring trends — continuously improving future match recommendations.

*This is a concrete mechanism behind the moat argument in the Founder FAQ (Q12): match quality compounds with real usage data, not just network size.*

## 21. Candidate Gets Hired 🎉
Candidate marks **Hired**; availability automatically changes to **Not Looking**.

## 22. Candidate Becomes Future Referrer
When ready, they click **Become a Referrer** — the cycle restarts, reinforcing the self-sustaining loop described in the Founder FAQ (Q22).

---

## Complete Ecosystem Flow (Summary Diagram)

```
User Visits Reffery
        │
        ▼
      Sign Up
        │
        ▼
   Choose Role (Candidate / Referrer / Both)
        │
        ▼
   Complete Profile
        │
        ▼
   AI Profile Analysis
        │
        ▼
Candidate Requests Endorsements
        │
        ▼
  Referrer Creates Referral
        │
        ▼
  AI Parses Job Description
        │
        ▼
    Referral Published
        │
        ▼
   Candidate Finds Referral
        │
        ▼
   AI Match Evaluation
        │
        ▼
  Candidate Requests Referral
        │
        ▼
  Referrer Reviews Request
        │
   ┌────┴────┐
   ▼         ▼
 Accept   Decline
   │
   ▼
Submit Referral
   │
   ▼
Track Hiring Process
   │
   ▼
 Interview
   │
   ▼
   Offer
   │
   ▼
Joined Company
   │
   ▼
Candidate Marks "Hired"
   │
   ▼
Later Becomes a Referrer
   │
   ▼
Repeats the Cycle
```

This workflow captures the end-to-end journey of the platform while keeping the focus on Reffery's core purpose: enabling trusted employee referrals with AI-assisted decision support.
