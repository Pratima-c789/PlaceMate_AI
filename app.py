
import streamlit as st
from progress_tracker import show_progress
from resume_ui import show_resume_analysis
from interview_ui import show_interview
from resume_parser import extract_resume_text
from learning_roadmap import generate_roadmap
from assessment_ui import show_assessment
from skill_matcher import (
    extract_skills,
    calculate_similarity,
    compare_skills,
    extract_preparation_areas
)

st.set_page_config(
    page_title="PlaceMate AI",
    page_icon="🎯",
    layout="wide"
)


# Clear previous job analysis
def clear_job_analysis():
    for key in [
        "job_results",
        "job_description",
        "preparation_areas",
        "similarity"
    ]:
        st.session_state.pop(key, None)


st.title("🎯 PlaceMate AI")

st.subheader(
    "AI-Powered Placement Preparation and Career Assistant"
)

st.write(
    "Understand your skills, identify your gaps "
    "and prepare confidently for your dream job."
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Resume Analyzer",
        "Job Matching",
        "Skill Gap Analysis",
        "Learning Roadmap",
        "Mock Assessment",
        "Interview Preparation",
        "Progress Tracker"
    ]
)


# HOME PAGE
if page == "Home":

    st.header("Welcome to PlaceMate AI")

    st.info(
        "Your personalized companion for "
        "campus placement preparation."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📄 Analyze")
        st.write("Understand your resume and skills.")

    with col2:
        st.subheader("🎯 Improve")
        st.write("Identify skill gaps and learn.")

    with col3:
        st.subheader("🚀 Prepare")
        st.write("Get ready for your interviews.")


# RESUME ANALYZER
elif page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:
            resume_text = extract_resume_text(uploaded_file)

            if resume_text.strip():

                if resume_text != st.session_state.get("resume_text"):
                    clear_job_analysis()

                skills = extract_skills(resume_text)

                st.session_state["resume_text"] = resume_text
                st.session_state["resume_skills"] = skills

                st.success("Resume uploaded successfully!")

            else:
                st.session_state.pop("resume_text", None)
                st.session_state.pop("resume_skills", None)
                clear_job_analysis()

                st.warning("No readable text found in the PDF.")

        except Exception:
            st.session_state.pop("resume_text", None)
            st.session_state.pop("resume_skills", None)
            clear_job_analysis()

            st.error("Unable to process the resume.")

    if "resume_text" in st.session_state:

        resume_text = st.session_state["resume_text"]
        skills = st.session_state["resume_skills"]

        if uploaded_file is None:
            st.info("Using your previously uploaded resume.")

        total_skills = sum(
            len(items) for items in skills.values()
        )

        st.metric("Total Skills Detected", total_skills)

        st.subheader("🎯 Detected Technical Skills")

        if skills:

            for category, items in skills.items():

                st.markdown(f"**{category}**")
                st.write(", ".join(items))

        else:
            st.warning("No recognized technical skills found.")

        with st.expander("View Extracted Resume Content"):
            st.text_area(
                "Resume Text",
                resume_text,
                height=350,
                disabled=True
            )

        show_resume_analysis(resume_text)

        if st.button("Clear Resume"):
            st.session_state.pop("resume_text", None)
            st.session_state.pop("resume_skills", None)
            clear_job_analysis()
            st.info("Resume cleared. Navigate away and return before uploading again.")
            st.stop()


# JOB MATCHING
elif page == "Job Matching":

    st.header("🎯 Job Matching")

    if "resume_text" not in st.session_state:

        st.warning(
            "Please upload your resume in Resume Analyzer first."
        )

    else:

        st.success("Resume is ready for analysis.")

        job_description = st.text_area(
            "Enter the company job description",
            value=st.session_state.get("job_description", ""),
            height=250,
            placeholder="Paste the job requirements here..."
        )

        if job_description != st.session_state.get("job_description", ""):
            clear_job_analysis()

        if st.button("Analyze Job Match"):

            if not job_description.strip():

                st.warning("Please enter a job description.")

            else:

                resume_text = st.session_state["resume_text"]

                similarity = calculate_similarity(
                    resume_text,
                    job_description
                )

                results = compare_skills(
                    resume_text,
                    job_description
                )

                preparation_areas = extract_preparation_areas(
                    job_description
                )

                st.session_state["job_results"] = results
                st.session_state["job_description"] = job_description
                st.session_state["preparation_areas"] = preparation_areas
                st.session_state["similarity"] = similarity

        if "job_results" in st.session_state:

            results = st.session_state["job_results"]
            similarity = st.session_state["similarity"]

            st.subheader("Job Matching Results")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Text Similarity",
                    f"{similarity}%"
                )

            with col2:

                coverage = results["coverage"]

                if coverage is not None:

                    st.metric(
                        "Skill Coverage",
                        f"{coverage}%"
                    )

                    st.progress(coverage / 100)

                else:
                    st.info("No recognized job skills found.")

            st.subheader("✅ Matching Skills")

            if results["matched"]:

                for skill in results["matched"]:
                    st.success(skill)

            else:
                st.info("No matching skills detected.")

            st.subheader("📚 Skills to Improve or Verify")

            if results["missing"]:

                for skill in results["missing"]:
                    st.warning(skill)

            else:
                st.info("No missing recognized skills detected.")

            st.caption(
                "These results measure text similarity and "
                "recognized skill mentions, not hiring probability "
                "or actual skill proficiency."
            )


# SKILL GAP ANALYSIS
elif page == "Skill Gap Analysis":

    st.header("📊 Skill Gap Analysis")

    if "job_results" not in st.session_state:

        st.warning("Please complete Job Matching first.")

    else:

        results = st.session_state["job_results"]

        preparation_areas = st.session_state.get(
            "preparation_areas", []
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Matching Skills",
            len(results["matched"])
        )

        col2.metric(
            "Missing Skill Mentions",
            len(results["missing"])
        )

        col3.metric(
            "Preparation Areas",
            len(preparation_areas)
        )

        st.subheader("✅ Your Matching Skills")

        if results["matched"]:

            for skill in results["matched"]:
                st.success(skill)

        else:
            st.info("No matching skills detected.")

        st.subheader("📚 Skills to Learn or Verify")

        if results["missing"]:

            for skill in results["missing"]:
                st.warning(skill)

        else:
            st.info("No missing recognized skills found.")

        st.subheader("🎯 Placement Preparation Requirements")

        if preparation_areas:

            for area in preparation_areas:
                st.write("📌 " + area)

        else:
            st.info("No specific preparation areas detected.")

        st.caption(
            "Detected requirements are based on the supplied "
            "job description. Assessments are needed to "
            "determine actual knowledge gaps."
        )

# LEARNING ROADMAP
elif page == "Learning Roadmap":

    st.header("📚 Personalized Learning Roadmap")

    if "job_results" not in st.session_state:

        st.warning("Please complete Job Matching first.")

    else:

        results = st.session_state["job_results"]

        missing_skills = results["missing"]

        preparation_areas = st.session_state.get(
            "preparation_areas", []
        )

        st.write(
            "Generate a personalized study plan based "
            "on your resume and company requirements."
        )

        days = st.number_input(
            "How many days do you have for preparation?",
            min_value=1,
            max_value=90,
            value=2,
            step=1
        )

        if st.button("Generate Learning Roadmap"):

            roadmap = generate_roadmap(
                missing_skills,
                preparation_areas,
                days
            )

            if roadmap:

                st.success(
                    "Your personalized roadmap is ready!"
                )

                st.metric(
                    "Total Preparation Areas",
                    len(roadmap)
                )

                for day in range(1, days + 1):

                    daily_tasks = [
                        task for task in roadmap
                        if task["day"] == day
                    ]

                    if daily_tasks:

                        st.subheader(f"📅 Day {day}")

                        for task in daily_tasks:

                            with st.expander(
                                task["area"],
                                expanded=True
                            ):

                                st.markdown(
                                    "**Topics to Study**"
                                )

                                for topic in task["topics"]:
                                    st.write("• " + topic)

                                st.markdown(
                                    "**Learning Resource**"
                                )

                                if task["resource"]:
                                    st.markdown(
                                        f"[Start Learning]({task['resource']})"
                                    )
                                else:
                                    st.info(
                                        "No specific resource available."
                                    )

                                st.markdown(
                                    "**Practice Task**"
                                )

                                st.info(task["practice"])

                st.caption(
                    "This is a suggested preparation plan. "
                    "Adjust it according to your knowledge "
                    "and available study time."
                )

            else:

                st.info(
                    "No specific preparation areas detected. "
                    "Try entering a more detailed job description."
                )


# MOCK ASSESSMENT
elif page == "Mock Assessment":

    show_assessment()

# INTERVIEW PREPARATION
elif page == "Interview Preparation":

    show_interview()

# PROGRESS TRACKER
elif page == "Progress Tracker":

    show_progress()