from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from services.ats_scorer import calculate_ats_score

from services.resume_parser import parse_resume
from services.skill_extractor import extract_skills
from services.semantic_matcher import semantic_match
from data.job_data_loader import load_jobs
from services.roadmap_generator import generate_roadmap
from services.skill_demand import analyze_skill_demand
from services.resume_improver import generate_resume_tips

import shutil
import traceback

router = APIRouter()

jobs = load_jobs()


# ---------------------------
# API RESPONSE (JSON)
# ---------------------------

@router.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):

    try:
        temp_file = "temp_resume.pdf"

        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = parse_resume(temp_file)
        user_skills = extract_skills(resume_text)

        results = []

        for index, row in jobs.iterrows():

            score, missing = semantic_match(user_skills, row["skills"])
            roadmap = generate_roadmap(row["job_title"], missing)
            resume_tips = generate_resume_tips(missing)
            ats_score = calculate_ats_score(user_skills, row["skills"])

            job_skills = [skill.strip().lower() for skill in row["skills"].split(",")]

            results.append({
                "job_role": row["job_title"],
                "match_score": round(score, 2),
                "ats_score": ats_score,
                "missing_skills": missing,
                "job_skills": job_skills,
                "user_skills": user_skills,
                "roadmap": roadmap,
                "resume_tips": resume_tips
            })

        best_role = max(results, key=lambda x: x["match_score"])
        skill_market = analyze_skill_demand(jobs.to_dict("records"))

        career_insight = (
            f"Based on your resume, you are closest to becoming a "
            f"{best_role['job_role']}. Focus on improving "
            f"{', '.join(best_role['missing_skills'][:3])}."
        )

        return {
            "best_role": best_role,
            "all_results": results,
            "market_skills": skill_market,
            "career_insight": career_insight
        }

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }


# ---------------------------
# UI RESPONSE (HTML)
# ---------------------------

@router.post("/analyze-resume-ui", response_class=HTMLResponse)
async def analyze_resume_ui(file: UploadFile = File(...)):

    temp_file = "temp_resume.pdf"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = parse_resume(temp_file)
    user_skills = extract_skills(resume_text)

    results = []

    for index, row in jobs.iterrows():

        score, missing = semantic_match(user_skills, row["skills"])
        roadmap = generate_roadmap(row["job_title"], missing)
        resume_tips = generate_resume_tips(missing)
        ats_score = calculate_ats_score(user_skills, row["skills"])

        job_skills = [skill.strip().lower() for skill in row["skills"].split(",")]

        roadmap_html = "".join(
            [f"Week {r['week']} → {r['skill']}<br>" for r in roadmap]
        )

        tips_html = "".join(
            [f"{tip}<br>" for tip in resume_tips]
        )

        results.append({
            "job_role": row["job_title"],
            "match_score": round(score, 2),
            "ats_score": ats_score,
            "missing_skills": missing,
            "job_skills": job_skills,
            "user_skills": user_skills,
            "roadmap_html": roadmap_html,
            "tips_html": tips_html
        })

    best_role = max(results, key=lambda x: x["match_score"])
    skill_market = analyze_skill_demand(jobs.to_dict("records"))

    market_html = ""
    for skill, count in skill_market.items():
        market_html += f"{skill} ({count})<br>"

    career_insight = (
        f"You are closest to becoming a {best_role['job_role']}. "
        f"Focus on improving {', '.join(best_role['missing_skills'][:3])}."
    )

    html_results = ""

    for job in results:
        html_results += f"""
        <div style="margin-top:30px;padding:20px;border:1px solid #ccc;border-radius:10px">

        <h3>{job['job_role']}</h3>

        <b>Match Score:</b> {job['match_score']}% <br>
        <b>ATS Score:</b> {job['ats_score']}% <br><br>

        <b>Missing Skills:</b> {job['missing_skills']} <br><br>

        <b>Learning Roadmap</b><br>
        {job['roadmap_html']}<br>

        <b>Resume Improvement Tips</b><br>
        {job['tips_html']}

        </div>
        """

    return f"""
    <h1>AI Skill Gap Analyzer</h1>

    <h2>Best Career Match</h2>
    {best_role['job_role']} ({best_role['match_score']}%)

    <h2>AI Career Insight</h2>
    {career_insight}

    <h2>Trending Skills in Market</h2>
    {market_html}

    {html_results}
    """
