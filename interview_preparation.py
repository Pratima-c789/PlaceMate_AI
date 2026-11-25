
import random


# Interview question database
INTERVIEW_BANK = {

    "HR Interview": [

        {
            "question": "Tell me about yourself.",
            "difficulty": "Easy",
            "keywords": [
                "education", "skills", "project", "career"
            ],
            "guidance": (
                "Introduce your education, technical skills, "
                "projects, strengths and career goals."
            )
        },

        {
            "question": "Why should we hire you?",
            "difficulty": "Medium",
            "keywords": [
                "skills", "learning", "teamwork", "contribution"
            ],
            "guidance": (
                "Explain your relevant skills, willingness "
                "to learn and how you can contribute."
            )
        },

        {
            "question": "How do you handle failure?",
            "difficulty": "Medium",
            "keywords": [
                "experience", "mistake", "learn", "improve"
            ],
            "guidance": (
                "Describe a real situation, what went wrong, "
                "what you learned and how you improved."
            )
        },

        {
            "question": "Describe a conflict within your team.",
            "difficulty": "Hard",
            "keywords": [
                "situation", "communication", "action", "result"
            ],
            "guidance": (
                "Use the STAR method: Situation, Task, "
                "Action and Result."
            )
        }
    ],

    "Project-Based Interview": [

        {
            "question": "Why did you choose this project?",
            "difficulty": "Easy",
            "keywords": [
                "problem", "motivation", "solution", "users"
            ],
            "guidance": (
                "Explain the real-world problem, your "
                "motivation and how your project helps users."
            )
        },

        {
            "question": "Explain your project architecture.",
            "difficulty": "Medium",
            "keywords": [
                "input", "processing", "output", "modules"
            ],
            "guidance": (
                "Explain the system components, data flow, "
                "technologies and final output."
            )
        },

        {
            "question": "What was your individual contribution?",
            "difficulty": "Easy",
            "keywords": [
                "implementation", "testing", "development"
            ],
            "guidance": (
                "Describe the tasks you personally completed "
                "and the concepts you learned."
            )
        },

        {
            "question": "What are the limitations of your project?",
            "difficulty": "Hard",
            "keywords": [
                "limitations", "accuracy", "improvement"
            ],
            "guidance": (
                "Discuss genuine limitations and explain "
                "how you would improve the system."
            )
        }
    ]
}


# Generate questions using resume skills
def generate_resume_questions(skills):

    questions = []

    for category, items in skills.items():

        for skill in items:

            questions.append({

                "question": (
                    f"You have mentioned {skill} in your resume. "
                    f"Explain how you have used it."
                ),

                "difficulty": "Easy",

                "keywords": [
                    skill.lower(),
                    "example",
                    "project"
                ],

                "guidance": (
                    f"Explain what {skill} is, where you used "
                    "or studied it, and provide a genuine example."
                )
            })

            questions.append({

                "question": (
                    f"What challenges or limitations have "
                    f"you encountered while learning {skill}?"
                ),

                "difficulty": "Medium",

                "keywords": [
                    skill.lower(),
                    "challenge",
                    "solution"
                ],

                "guidance": (
                    "Describe a genuine challenge, how you "
                    "approached it and what you learned."
                )
            })

            questions.append({

                "question": (
                    f"How would you decide whether {skill} "
                    "is suitable for a new project?"
                ),

                "difficulty": "Hard",

                "keywords": [
                    "requirements",
                    "advantages",
                    "limitations"
                ],

                "guidance": (
                    "Discuss project requirements, advantages, "
                    "limitations and possible alternatives."
                )
            })

    return questions


# Select interview questions
def get_interview_questions(
    interview_type,
    difficulty="Mixed",
    skills=None,
    count=5
):

    if interview_type == "Resume-Based Interview":

        questions = generate_resume_questions(
            skills or {}
        )

    else:

        questions = INTERVIEW_BANK.get(
            interview_type, []
        )

    if difficulty != "Mixed":

        questions = [
            q for q in questions
            if q["difficulty"] == difficulty
        ]

    return random.sample(
        questions,
        min(count, len(questions))
    )


# Evaluate keyword coverage in an answer
def evaluate_interview_answer(answer, question):

    answer = answer.strip().lower()

    keywords = question["keywords"]

    matched = [
        word for word in keywords
        if word.lower() in answer
    ]

    missing = [
        word for word in keywords
        if word.lower() not in answer
    ]

    score = round(
        len(matched) / len(keywords) * 100, 2
    ) if keywords else 0

    if not answer:

        message = "Please attempt the question."

    elif score >= 75:

        message = (
            "Good effort! Your answer covers "
            "most suggested keywords."
        )

    elif score >= 50:

        message = (
            "Nice attempt! Try adding more "
            "relevant details and examples."
        )

    else:

        message = (
            "Keep practising! Review the suggested "
            "guidance and improve your answer."
        )

    return {

        "score": score,

        "matched_keywords": matched,

        "missing_keywords": missing,

        "word_count": len(answer.split()),

        "message": message,

        "guidance": question["guidance"]

    }
