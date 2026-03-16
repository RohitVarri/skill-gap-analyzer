from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(user_skills, job_skills):

    job_skills = [skill.strip().lower() for skill in job_skills.split(",")]

    matched = []
    missing = []

    for job_skill in job_skills:

        found = False

        job_embedding = model.encode(job_skill, convert_to_tensor=True)

        for user_skill in user_skills:

            user_embedding = model.encode(user_skill, convert_to_tensor=True)

            similarity = util.cos_sim(job_embedding, user_embedding)

            if similarity.item() > 0.6:
                matched.append(job_skill)
                found = True
                break

        if not found:
            missing.append(job_skill)

    score = (len(matched) / len(job_skills)) * 100

    return score, missing