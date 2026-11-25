
import streamlit as st

from interview_preparation import (
    get_interview_questions,
    evaluate_interview_answer
)

from question_bank import QUESTION_BANK


def show_interview():

    st.header("🎤 PlaceMate Interview Coach")

    st.write(
        "Practise interview questions, improve your "
        "answers and build your confidence."
    )

    # Interview selection
    with st.container(border=True):

        st.subheader("⚙️ Customize Your Interview")

        col1, col2 = st.columns(2)

        with col1:

            interview_type = st.selectbox(
                "Choose interview type",
                [
                    "Resume-Based Interview",
                    "Technical Interview",
                    "HR Interview",
                    "Project-Based Interview",
                    "Company-Based Interview"
                ]
            )

        with col2:

            difficulty = st.selectbox(
                "Choose difficulty",
                ["Easy", "Medium", "Hard", "Mixed"],
                index=3
            )

        subject = None
        company = ""
        job_role = ""

        if interview_type == "Technical Interview":

            subject = st.selectbox(
                "Choose technical subject",
                list(QUESTION_BANK.keys())
            )

        elif interview_type == "Company-Based Interview":

            company = st.text_input("Company name")

            job_role = st.text_input("Target job role")

        elif interview_type == "Resume-Based Interview":

            if not st.session_state.get("resume_skills"):

                st.warning(
                    "Upload your resume in Resume "
                    "Analyzer first."
                )

        count = st.slider(
            "Number of interview questions",
            1, 20, 5
        )

        if st.button(
            "🚀 Start Interview",
            type="primary",
            use_container_width=True
        ):

            if interview_type == "Technical Interview":

                import random

                available = [
                    q for q in QUESTION_BANK[subject]
                    if difficulty == "Mixed"
                    or q["difficulty"] == difficulty
                ]

                selected = random.sample(
                    available,
                    min(count, len(available))
                )

                questions = []

                for q in selected:

                    questions.append({

                        "question": q["question"],

                        "difficulty": q["difficulty"],

                        "keywords": [
                            str(q["answer"])
                        ],

                        "guidance": (
                            f"Expected answer: {q['answer']}. "
                            f"{q['explanation']}"
                        )

                    })

            elif interview_type == "Company-Based Interview":

                if not company.strip() or not job_role.strip():

                    st.warning(
                        "Enter the company and job role."
                    )

                    return

                questions = [

                    {
                        "question": (
                            f"Why do you want to join {company}?"
                        ),
                        "difficulty": "Easy",
                        "keywords": [
                            "skills", "learning", "growth"
                        ],
                        "guidance": (
                            "Research the company and explain "
                            "your genuine motivation."
                        )
                    },

                    {
                        "question": (
                            f"Why are you suitable for the "
                            f"{job_role} role?"
                        ),
                        "difficulty": "Medium",
                        "keywords": [
                            "skills", "project", "experience"
                        ],
                        "guidance": (
                            "Connect your actual skills and "
                            "projects to the job requirements."
                        )
                    },

                    {
                        "question": (
                            f"How would you solve an unfamiliar "
                            f"problem as a {job_role}?"
                        ),
                        "difficulty": "Hard",
                        "keywords": [
                            "problem", "research",
                            "solution", "testing"
                        ],
                        "guidance": (
                            "Explain how you understand the "
                            "problem, research, implement "
                            "and test a solution."
                        )
                    }
                ]

                questions = [
                    q for q in questions
                    if difficulty == "Mixed"
                    or q["difficulty"] == difficulty
                ][:count]

            else:

                questions = get_interview_questions(
                    interview_type,
                    difficulty,
                    st.session_state.get(
                        "resume_skills", {}
                    ),
                    count
                )

            if questions:

                st.session_state["interview_questions"] = (
                    questions
                )

                st.session_state["interview_index"] = 0

                st.session_state["interview_feedback"] = {}

                st.session_state["interview_id"] = (
                    st.session_state.get(
                        "interview_id", 0
                    ) + 1
                )

                st.session_state["interview_finished"] = False

            else:

                st.warning(
                    "No questions available. Try another "
                    "subject or difficulty."
                )

    # Active interview
    questions = st.session_state.get(
        "interview_questions", []
    )

    if not questions:

        st.info(
            "Customize your interview to begin practising."
        )

        return

    feedback = st.session_state["interview_feedback"]

    interview_id = st.session_state["interview_id"]

    st.divider()

    # Final interview report
    if st.session_state.get("interview_finished"):

        st.header("🏆 Interview Performance Report")

        scores = [
            item["score"] for item in feedback.values()
        ]

        average = (
            sum(scores) / len(scores)
            if scores else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Questions",
            len(questions)
        )

        col2.metric(
            "Answers Evaluated",
            len(scores)
        )

        col3.metric(
            "Keyword Coverage",
            f"{average:.1f}%"
        )

        if average >= 75:

            st.success(
                "🌟 Great effort! Keep refining your answers."
            )

        else:

            st.info(
                "💪 Keep practising. Review the guidance "
                "and strengthen your answers."
            )

        st.subheader("📚 Review Your Interview")

        for i, question in enumerate(questions):

            with st.expander(
                f"Question {i + 1}: "
                f"{question['question']}"
            ):

                result = feedback.get(i)

                if result:

                    st.write(
                        "Your answer:",
                        result["answer"]
                    )

                    st.write(
                        "Keyword coverage:",
                        f"{result['score']}%"
                    )

                else:

                    st.warning("Not evaluated")

                st.info(question["guidance"])

        st.caption(
            "Keyword coverage is not a measure of "
            "technical correctness or hiring readiness."
        )

        if st.button("🔙 Return to Interview Selection"):

            for key in [
                "interview_questions",
                "interview_index",
                "interview_feedback",
                "interview_finished"
            ]:

                st.session_state.pop(key, None)

            st.rerun()

        return

    # Display current question
    index = st.session_state["interview_index"]

    question = questions[index]

    st.progress((index + 1) / len(questions))

    st.caption(
        f"Question {index + 1} of {len(questions)}"
    )

    with st.container(border=True):

        st.subheader(question["question"])

        st.caption(
            f"Difficulty: {question['difficulty']}"
        )

        answer = st.text_area(
            "Write your interview answer",
            height=200,
            value=feedback.get(index, {}).get("answer", ""),
            key=f"interview_answer_{interview_id}_{index}",
            placeholder="Explain your answer in your own words..."
        )

        if st.button(
            "✨ Evaluate My Answer",
            type="primary"
        ):

            if not answer.strip():

                st.warning("Please enter your answer.")

            else:

                result = evaluate_interview_answer(
                    answer,
                    question
                )

                result["answer"] = answer

                feedback[index] = result

        if index in feedback:

            result = feedback[index]

            st.metric(
                "Keyword Coverage",
                f"{result['score']}%"
            )

            st.metric(
                "Word Count",
                result["word_count"]
            )

            st.success(result["message"])

            if result["matched_keywords"]:

                st.write("✅ Keywords covered:")

                st.write(
                    ", ".join(result["matched_keywords"])
                )

            if result["missing_keywords"]:

                st.write("📚 Concepts to consider:")

                st.write(
                    ", ".join(result["missing_keywords"])
                )

        with st.expander("💡 Suggested Answer Guidance"):

            st.info(question["guidance"])

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬅️ Previous",
            disabled=index == 0
        ):

            st.session_state["interview_index"] -= 1

            st.rerun()

    with col2:

        if st.button(
            "Next Question ➡️",
            disabled=index == len(questions) - 1
        ):

            st.session_state["interview_index"] += 1

            st.rerun()

    with col3:

        if st.button("🏁 Finish Interview"):

            st.session_state["interview_finished"] = True

            st.rerun()

    st.caption(
        "Evaluate each answer before moving to the next "
        "question to include it in your performance report."
    )
