
import random
from question_bank import QUESTION_BANK, make_question


# Select questions based on subject and difficulty
def get_questions(category, difficulty="Mixed", count=3):

    questions = QUESTION_BANK.get(category, [])

    if difficulty != "Mixed":

        questions = [
            q for q in questions
            if q["difficulty"] == difficulty
        ]

    selected = random.sample(
        questions,
        min(count, len(questions))
    )

    final_questions = []

    for question in selected:

        question_copy = question.copy()

        question_copy["options"] = random.sample(
            question["options"],
            len(question["options"])
        )

        final_questions.append(question_copy)

    return final_questions


# Appreciation and achievement system
def get_achievement(percentage):

    if percentage >= 90:

        return {
            "badge": "🏆 Placement Champion",
            "message": "Outstanding performance! Keep challenging yourself."
        }

    elif percentage >= 75:

        return {
            "badge": "🥇 Rising Star",
            "message": "Excellent progress! Keep up the great work."
        }

    elif percentage >= 50:

        return {
            "badge": "🥈 Skill Builder",
            "message": "Good effort! Revise the topics you missed."
        }

    else:

        return {
            "badge": "🌱 Learning Explorer",
            "message": "Every mistake helps you learn. Keep practising!"
        }


# Recommend the next difficulty
def recommend_difficulty(percentage, difficulty):

    levels = ["Easy", "Medium", "Hard"]

    if difficulty == "Mixed":
        difficulty = "Medium"

    index = levels.index(difficulty)

    if percentage >= 80:

        index = min(index + 1, 2)

    elif percentage < 50:

        index = max(index - 1, 0)

    return levels[index]


# Evaluate assessment performance
def evaluate_assessment(questions, user_answers):

    score = 0
    feedback = []
    weak_topics = []
    incorrect_questions = []
    unanswered = 0

    for index, question in enumerate(questions):

        user_answer = user_answers.get(index)

        correct = user_answer == question["answer"]

        if user_answer is None:
            unanswered += 1

        if correct:

            score += 1

        else:

            weak_topics.append(question["topic"])

            incorrect_questions.append(question)

        feedback.append({

            "question": question["question"],

            "user_answer": user_answer,

            "correct_answer": question["answer"],

            "correct": correct,

            "explanation": question["explanation"],

            "topic": question["topic"],

            "difficulty": question["difficulty"]

        })

    total = len(questions)

    percentage = (
        round(score / total * 100, 2)
        if total else 0
    )

    attempted = total - unanswered

    accuracy = (
        round(score / attempted * 100, 2)
        if attempted else 0
    )

    achievement = get_achievement(percentage)

    return {

        "score": score,

        "total": total,

        "percentage": percentage,

        "accuracy": accuracy,

        "incorrect": attempted - score,

        "unanswered": unanswered,

        "feedback": feedback,

        "weak_topics": list(dict.fromkeys(weak_topics)),

        "incorrect_questions": incorrect_questions,

        "badge": achievement["badge"],

        "message": achievement["message"]

    }
