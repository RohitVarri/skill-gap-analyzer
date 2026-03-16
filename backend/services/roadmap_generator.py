roadmaps = {
    "Backend Developer": [
        "REST API Development",
        "Django / Flask",
        "Docker",
        "AWS Deployment"
    ],
    "Data Scientist": [
        "Pandas",
        "Data Visualization",
        "Machine Learning",
        "TensorFlow / PyTorch"
    ],
    "AI Engineer": [
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Model Deployment"
    ]
}

def generate_roadmap(role, missing_skills):
    roadmap = roadmaps.get(role, [])
    
    plan = []
    week = 1

    for skill in missing_skills:
        plan.append({
            "week": week,
            "skill": skill
        })
        week += 1

    return plan