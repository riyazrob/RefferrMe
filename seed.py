"""Seed the database with demo data for testing the full workflow."""

from app.database import SessionLocal, init_db
from app.enums import ReferralListingStatus, UserRole
from app.models.profile import CandidateProfile, ReferrerProfile
from app.models.referral import Referral
from app.models.user import User
from app.services.ai_service import parse_job_description
from app.services.auth_service import hash_password


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).first():
            print("Database already seeded.")
            return

        candidate = User(
            email="candidate@example.com",
            name="Alex Candidate",
            password_hash=hash_password("password123"),
            role=UserRole.CANDIDATE,
        )
        referrer = User(
            email="referrer@example.com",
            name="Jordan Referrer",
            password_hash=hash_password("password123"),
            role=UserRole.BOTH,
        )
        db.add_all([candidate, referrer])
        db.flush()

        db.add(CandidateProfile(
            user_id=candidate.id,
            skills="Python, AWS, Backend Development, SQL, Docker",
            experience="6 years building scalable backend systems at tech companies.",
            education="BS Computer Science",
            resume_text="Experienced backend engineer with Python and cloud expertise.",
            linkedin_url="https://linkedin.com/in/alexcandidate",
            github_url="https://github.com/alexcandidate",
        ))
        db.add(ReferrerProfile(
            user_id=referrer.id,
            company="TechCorp",
            company_email="jordan@techcorp.com",
            title="Senior Engineer",
            employment_verified=True,
        ))

        job_desc = """
        Senior Backend Engineer — TechCorp
        Location: San Francisco, CA (Hybrid)
        5+ years experience required.

        Required: Python, AWS, Backend Development, SQL
        Preferred: Kubernetes, Docker, leadership experience
        Visa sponsorship available.
        """
        parsed = parse_job_description(job_desc, "Senior Backend Engineer")
        referral = Referral(
            referrer_id=referrer.id,
            company="TechCorp",
            job_title="Senior Backend Engineer",
            job_link="https://techcorp.com/jobs/123",
            job_id="TC-123",
            job_description=job_desc,
            parsed_role=parsed.parsed_role,
            parsed_experience=parsed.parsed_experience,
            required_skills=parsed.required_skills,
            preferred_skills=parsed.preferred_skills,
            education_required=parsed.education_required,
            certifications_required=parsed.certifications_required,
            visa_sponsorship=parsed.visa_sponsorship,
            location=parsed.location,
            remote_ok=parsed.remote_ok,
            slots=3,
            status=ReferralListingStatus.PUBLISHED,
        )
        db.add(referral)
        db.commit()
        print("Seeded demo users:")
        print("  Candidate: candidate@example.com / password123")
        print("  Referrer:  referrer@example.com / password123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
