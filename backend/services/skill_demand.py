from collections import Counter

def analyze_skill_demand(jobs):

    all_skills = []

    for job in jobs:

        skills = job["skills"]

        # Convert string to list if needed
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",")]

        for skill in skills:
            all_skills.append(skill.lower())

    skill_count = Counter(all_skills)

    return dict(skill_count.most_common(10))
