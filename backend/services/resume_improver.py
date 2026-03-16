def generate_resume_tips(missing_skills):

    tips = []

    for skill in missing_skills:

        tips.append(
            f"Add project experience related to {skill}"
        )

    return tips