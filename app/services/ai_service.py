"""AI services — rule-based stubs ready to swap for an LLM provider."""

import re

from app.models.profile import CandidateProfile
from app.models.referral import Referral
from app.schemas import AIJobParse, AIMatchEvaluation, AIProfileAnalysis


def _extract_skills(text: str) -> set[str]:
    common = {
        "python", "java", "javascript", "typescript", "react", "aws", "azure", "gcp",
        "kubernetes", "docker", "sql", "node", "go", "rust", "c++", "machine learning",
        "data science", "backend", "frontend", "devops", "leadership", "agile",
    }
    lower = text.lower()
    return {skill for skill in common if skill in lower}


def analyze_profile(profile: CandidateProfile) -> AIProfileAnalysis:
    skills = profile.skills or ""
    experience = profile.experience or ""
    resume = profile.resume_text or ""
    combined = f"{skills} {experience} {resume}"
    found = _extract_skills(combined)

    completion_fields = [
        profile.resume_text, profile.skills, profile.experience,
        profile.education, profile.linkedin_url,
    ]
    completion = sum(1 for f in completion_fields if f) / len(completion_fields)
    readiness = round(min(95.0, 40 + completion * 40 + len(found) * 3), 1)

    summary = (
        f"Candidate profile shows {len(found)} recognized skills. "
        f"Experience highlights: {(experience[:200] + '...') if len(experience) > 200 else experience or 'Not provided'}."
    )
    suggestions = []
    if not profile.linkedin_url:
        suggestions.append("Add your LinkedIn profile to increase trust.")
    if not profile.github_url and "python" in found:
        suggestions.append("Link GitHub projects to demonstrate technical depth.")
    if len(found) < 3:
        suggestions.append("Expand your skills section with specific technologies.")
    if not suggestions:
        suggestions.append("Profile looks strong — consider requesting endorsements.")

    return AIProfileAnalysis(
        ai_summary=summary,
        referral_readiness_score=readiness,
        resume_suggestions="\n".join(f"- {s}" for s in suggestions),
    )


def parse_job_description(job_description: str, job_title: str = "") -> AIJobParse:
    text = f"{job_title} {job_description}"
    found = _extract_skills(text)
    required = ", ".join(sorted(found)[:5]) or "General professional skills"
    preferred = ", ".join(sorted(found)[5:8]) or "Communication, teamwork"

    years_match = re.search(r"(\d+)\+?\s*years?", text, re.I)
    experience = f"{years_match.group(1)}+ years" if years_match else "3+ years"

    remote_ok = bool(re.search(r"\bremote\b", text, re.I))
    visa = bool(re.search(r"visa|sponsorship|h1b|work authorization", text, re.I))
    location_match = re.search(r"(?:location|based in|office in)[:\s]+([^\n,.]+)", text, re.I)
    location = location_match.group(1).strip() if location_match else ("Remote" if remote_ok else "Not specified")

    return AIJobParse(
        parsed_role=job_title or "Software Engineer",
        parsed_experience=experience,
        required_skills=required,
        preferred_skills=preferred,
        education_required="Bachelor's degree or equivalent experience",
        certifications_required="None required" if "certification" not in text.lower() else "See job description",
        visa_sponsorship=visa,
        location=location,
        remote_ok=remote_ok,
    )


def evaluate_match(profile: CandidateProfile, referral: Referral) -> AIMatchEvaluation:
    candidate_skills = _extract_skills(
        f"{profile.skills or ''} {profile.experience or ''} {profile.resume_text or ''}"
    )
    job_skills = _extract_skills(
        f"{referral.required_skills or ''} {referral.preferred_skills or ''} {referral.job_description}"
    )

    if not job_skills:
        match_pct = 75.0
        matched = candidate_skills
        missing = set()
    else:
        matched = candidate_skills & job_skills
        missing = job_skills - candidate_skills
        match_pct = round(len(matched) / max(len(job_skills), 1) * 100, 1)

    strengths = ", ".join(sorted(matched)) or "Relevant professional background"
    gaps = ", ".join(sorted(missing)) or "None significant"
    recommendation = "Strong candidate for referral." if match_pct >= 70 else "Moderate match — review carefully."

    explanation = (
        f"Overall Match: {match_pct}%\n\n"
        f"Strengths: {strengths}\n"
        f"Potential Concerns: {gaps}\n"
        f"Recommendation: {recommendation}"
    )

    return AIMatchEvaluation(
        match_score=match_pct,
        match_explanation=explanation,
        strengths=strengths,
        missing_skills=gaps,
        ai_recommendation=recommendation,
    )
