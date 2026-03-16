def calculate_match(user_skills, job_skills):

    job_skills = [skill.strip().lower() for skill in job_skills.split(",")]

    matched = set(user_skills).intersection(set(job_skills))
    missing = set(job_skills) - set(user_skills)

    score = (len(matched) / len(job_skills)) * 100

    return score, list(missing)