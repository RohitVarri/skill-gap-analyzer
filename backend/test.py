from services.resume_parser import parse_resume
from services.skill_extractor import extract_skills
from services.skill_matcher import calculate_match
from data.job_data_loader import load_jobs
resume_path = "../datasets/resumes/sample_resume.pdf"

resume_text = parse_resume(resume_path)

user_skills = extract_skills(resume_text)

jobs = load_jobs()

for index,row in jobs.iterrows():

    score,missing = calculate_match(user_skills,row["skills"])

    print("\nJob Role:",row["job_title"])
    print("Match Score:",round(score,2),"%")
    print("Missing Skills:",missing)