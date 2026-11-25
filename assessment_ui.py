
import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px

from mock_assessment import (
    QUESTION_BANK,
    evaluate_assessment,
    recommend_difficulty
)


# Start a new assessment
def start_assessment(questions, category, difficulty,
                     mode="Practice Mode"):

    st.session_state["assessment_questions"] = questions
    st.session_state["assessment_category"] = category
    st.session_state["assessment_difficulty"] = difficulty
    st.session_state["assessment_mode"] = mode
    st.session_state["assessment_start"] = time.time()
    st.session_state["assessment_result"] = None

    st.session_state["assessment_id"] = (
        st.session_state.get("assessment_id", 0) + 1
    )


# Return to assessment selection
def reset_assessment():

    keys = [
        "assessment_questions",
        "assessment_category",
        "assessment_difficulty",
        "assessment_mode",
        "assessment_start",
        "assessment_result",
        "celebrate_assessment"
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.rerun()


# Assessment history
def show_history():

    history_data = st.session_state.get(
        "assessment_history", []
    )

    if history_data:

        st.divider()
        st.subheader("📈 Your Assessment Journey")

        history = pd.DataFrame(history_data)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Assessments",
            len(history)
        )

        col2.metric(
            "Average Score",
            f"{history['Score'].mean():.1f}%"
        )

        col3.metric(
            "Best Score",
            f"{history['Score'].max():.1f}%"
        )

        history.index = range(1, len(history) + 1)
        history.index.name = "Attempt"

        st.dataframe(
            history,
            use_container_width=True
        )

        st.line_chart(history["Score"])

        st.caption(
            "Scores may vary across subjects and "
            "difficulty levels."
        )


# Main assessment interface
def show_assessment():

    st.header("🎮 PlaceMate Assessment Arena")

    st.write(
        "Learn, practise, challenge yourself and "
        "prepare confidently for your career."
    )

    if "assessment_history" not in st.session_state:
        st.session_state["assessment_history"] = []

    # Assessment selection
    if "assessment_questions" not in st.session_state:

        col1, col2, col3 = st.columns(3)

        total_questions = len(
            QUESTION_BANK.get(
                "All Subjects",
                [
                    q for questions in QUESTION_BANK.values()
                    for q in questions
                ]
            )
        )

        col1.metric(
            "Question Bank",
            total_questions
        )

        col2.metric(
            "Subjects",
            len([
                name for name in QUESTION_BANK
                if name != "All Subjects"
            ])
        )

        col3.metric("Difficulty Levels", 3)

        with st.container(border=True):

            st.subheader("⚙️ Customize Your Assessment")

            categories = list(QUESTION_BANK.keys())

            if "All Subjects" in categories:
                categories.remove("All Subjects")
                categories.insert(0, "All Subjects")

            col1, col2 = st.columns(2)

            with col1:

                category = st.selectbox(
                    "📚 Choose your subject",
                    categories
                )

            with col2:

                difficulty = st.selectbox(
                    "🎚️ Choose difficulty level",
                    ["Easy", "Medium", "Hard", "Mixed"],
                    index=3
                )

            level_details = {
                "Easy": "🌱 Build your foundation.",
                "Medium": "⚡ Strengthen your knowledge.",
                "Hard": "🔥 Challenge yourself.",
                "Mixed": "🎯 Practise different levels."
            }

            st.info(level_details[difficulty])

            available = [
                q for q in QUESTION_BANK[category]
                if difficulty == "Mixed"
                or q["difficulty"] == difficulty
            ]

            topics = sorted({
                q["topic"] for q in available
            })

            selected_topic = st.selectbox(
                "📖 Choose a topic",
                ["All Topics"] + topics
            )

            if selected_topic != "All Topics":

                available = [
                    q for q in available
                    if q["topic"] == selected_topic
                ]

            mode = st.radio(
                "🎮 Choose assessment mode",
                ["Practice Mode", "Exam Mode"],
                horizontal=True
            )

            if mode == "Practice Mode":

                st.success(
                    "Learn at your own pace with hints "
                    "and detailed explanations."
                )

            else:

                st.warning(
                    "Challenge yourself without hints. "
                    "Your completion time will be recorded."
                )

            st.metric(
                "Available Questions",
                len(available)
            )

            if not available:

                st.warning(
                    "No questions available for this "
                    "selection. Try another difficulty."
                )

            else:

                maximum = min(50, len(available))

                if maximum > 1:

                    count = st.slider(
                        "Number of questions",
                        min_value=1,
                        max_value=maximum,
                        value=min(10, maximum)
                    )

                else:
                    count = 1

                st.caption(
                    f"You selected {count} questions."
                )

                if st.button(
                    "🚀 Start Assessment",
                    type="primary",
                    use_container_width=True
                ):

                    questions = random.sample(
                        available, count
                    )

                    selected_questions = []

                    for question in questions:

                        question_copy = question.copy()

                        question_copy["options"] = (
                            random.sample(
                                question["options"],
                                len(question["options"])
                            )
                        )

                        selected_questions.append(
                            question_copy
                        )

                    start_assessment(
                        selected_questions,
                        category,
                        difficulty,
                        mode
                    )

                    st.rerun()

        show_history()
        return

    # Retrieve active assessment
    questions = st.session_state["assessment_questions"]

    assessment_id = st.session_state["assessment_id"]

    category = st.session_state["assessment_category"]

    difficulty = st.session_state["assessment_difficulty"]

    mode = st.session_state.get(
        "assessment_mode", "Practice Mode"
    )

    result = st.session_state.get("assessment_result")

    # Active assessment
    if result is None:

        st.subheader("📝 Your Challenge")

        col1, col2, col3 = st.columns(3)

        col1.metric("Subject", category)
        col2.metric("Difficulty", difficulty)
        col3.metric("Questions", len(questions))

        st.info(f"Current mode: {mode}")

        if st.button("🔙 Cancel and Return to Selection"):

            reset_assessment()

        user_answers = {}

        for index, question in enumerate(questions):

            with st.container(border=True):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.caption(
                    f"Topic: {question['topic']} | "
                    f"Level: {question['difficulty']}"
                )

                st.write(question["question"])

                user_answers[index] = st.radio(
                    "Select your answer",
                    question["options"],
                    index=None,
                    key=f"answer_{assessment_id}_{index}"
                )

                if mode == "Practice Mode":

                    with st.expander("💡 Need a hint?"):

                        st.info(
                            question.get(
                                "hint",
                                "Think about the core concept."
                            )
                        )

        answered = sum(
            answer is not None
            for answer in user_answers.values()
        )

        st.subheader("📊 Assessment Progress")

        st.progress(answered / len(questions))

        st.caption(
            f"{answered} of {len(questions)} "
            "questions answered"
        )

        if answered < len(questions):

            st.warning(
                f"{len(questions) - answered} "
                "questions are still unanswered."
            )

        if st.button(
            "🏁 Submit Assessment",
            type="primary",
            use_container_width=True
        ):

            result = evaluate_assessment(
                questions,
                user_answers
            )

            elapsed = int(
                time.time()
                - st.session_state["assessment_start"]
            )

            result["time_taken"] = elapsed
            result["category"] = category
            result["difficulty"] = difficulty
            result["mode"] = mode

            st.session_state["assessment_result"] = result

            st.session_state["assessment_history"].append({

                "Subject": category,

                "Difficulty": difficulty,

                "Mode": mode,

                "Score": result["percentage"],

                "Time": elapsed

            })

            st.session_state["celebrate_assessment"] = True

            st.rerun()

    # Assessment results
    else:

        st.header("📊 Your Performance Report")

        if st.session_state.pop(
            "celebrate_assessment", False
        ):

            if result["percentage"] >= 80:
                st.balloons()

        with st.container(border=True):

            st.title(result["badge"])

            st.success(result["message"])

            if result["percentage"] >= 90:

                st.write(
                    "🌟 Outstanding! Your hard work "
                    "is paying off."
                )

            elif result["percentage"] >= 75:

                st.write(
                    "👏 Excellent progress! Keep going."
                )

            elif result["percentage"] >= 50:

                st.write(
                    "💪 Good effort! Keep improving "
                    "your weaker topics."
                )

            else:

                st.write(
                    "❤️ Every attempt is an opportunity "
                    "to learn. Keep practising!"
                )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🎯 Score",
            f"{result['score']}/{result['total']}"
        )

        col2.metric(
            "📊 Percentage",
            f"{result['percentage']}%"
        )

        col3.metric(
            "⚡ Accuracy",
            f"{result['accuracy']}%"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "❌ Incorrect",
            result["incorrect"]
        )

        col5.metric(
            "⏭️ Unanswered",
            result["unanswered"]
        )

        minutes, seconds = divmod(
            result["time_taken"], 60
        )

        col6.metric(
            "⏱️ Time Taken",
            f"{minutes}m {seconds}s"
        )

        st.progress(result["percentage"] / 100)

        # Navigation buttons
        st.subheader("🚀 Continue Your Learning")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🔙 Back to Assessment Selection",
                use_container_width=True
            ):

                reset_assessment()

        with col2:

            if st.button(
                "🔁 Retry Incorrect Questions",
                disabled=not result["incorrect_questions"],
                use_container_width=True
            ):

                start_assessment(
                    result["incorrect_questions"],
                    result["category"],
                    result["difficulty"],
                    mode
                )

                st.rerun()

        # Performance chart
        chart_data = pd.DataFrame({

            "Result": [
                "Correct",
                "Incorrect",
                "Unanswered"
            ],

            "Questions": [
                result["score"],
                result["incorrect"],
                result["unanswered"]
            ]

        })

        fig = px.pie(
            chart_data,
            names="Result",
            values="Questions",
            hole=0.65,
            title="Assessment Performance",
            color="Result",
            color_discrete_map={
                "Correct": "#22C55E",
                "Incorrect": "#EF4444",
                "Unanswered": "#F59E0B"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Personalized recommendations
        st.subheader("🧠 Personalized Recommendations")

        next_level = recommend_difficulty(
            result["percentage"],
            result["difficulty"]
        )

        st.info(
            f"Recommended next difficulty: {next_level}"
        )

        if result["weak_topics"]:

            st.write("📚 Topics you should revise:")

            for topic in result["weak_topics"]:

                st.warning(f"Revise: {topic}")

            st.write(
                "Review the explanations below, "
                "revise these topics and attempt "
                "another assessment."
            )

        else:

            st.success(
                "Excellent! No mistakes were detected "
                "in this assessment."
            )

        # Detailed answer review
        st.subheader("🔍 Review Your Answers")

        review_filter = st.selectbox(
            "Filter answers",
            [
                "All Questions",
                "Incorrect and Skipped",
                "Correct Answers"
            ]
        )

        for index, item in enumerate(result["feedback"]):

            if (
                review_filter == "Incorrect and Skipped"
                and item["correct"]
            ):
                continue

            if (
                review_filter == "Correct Answers"
                and not item["correct"]
            ):
                continue

            status = "✅" if item["correct"] else "❌"

            with st.expander(
                f"{status} Question {index + 1}",
                expanded=not item["correct"]
            ):

                st.write(item["question"])

                st.write(
                    "Your answer:",
                    item["user_answer"] or "Not answered"
                )

                st.success(
                    f"Correct answer: "
                    f"{item['correct_answer']}"
                )

                st.info(
                    f"Explanation: {item['explanation']}"
                )

                st.caption(
                    f"Topic: {item['topic']} | "
                    f"Difficulty: {item['difficulty']}"
                )

        st.caption(
            "Assessment results indicate practice "
            "performance, not hiring probability "
            "or overall placement readiness."
        )

        show_history()
