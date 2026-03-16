def calculate_ats_score(user_skills, job_skills):

    matched = len(set(user_skills).intersection(set(job_skills)))
    total = len(job_skills)

    if total == 0:
        return 0

    score = (matched / total) * 100

    return round(score,2)
