
LEARNING_DATABASE = {

    "Quantitative Aptitude": {
        "topics": [
            "Percentages",
            "Profit and Loss",
            "Ratio and Proportion",
            "Time and Work",
            "Probability"
        ],
        "resource": "https://www.indiabix.com/aptitude/questions-and-answers/",
        "practice": "Solve 20 aptitude questions."
    },

    "Logical Reasoning": {
        "topics": [
            "Number Series",
            "Coding-Decoding",
            "Blood Relations",
            "Direction Sense",
            "Logical Puzzles"
        ],
        "resource": "https://www.indiabix.com/logical-reasoning/questions-and-answers/",
        "practice": "Solve 15 reasoning questions."
    },

    "English and Verbal Ability": {
        "topics": [
            "Grammar",
            "Vocabulary",
            "Sentence Correction",
            "Reading Comprehension"
        ],
        "resource": "https://www.indiabix.com/verbal-ability/questions-and-answers/",
        "practice": "Solve 15 verbal ability questions."
    },

    "Programming and Coding": {
        "topics": [
            "Variables and Data Types",
            "Loops and Conditions",
            "Functions",
            "Arrays and Strings",
            "Basic Problem Solving"
        ],
        "resource": "https://www.hackerrank.com/domains/python",
        "practice": "Solve 5 beginner coding problems."
    },

    "Computer Science Fundamentals": {
        "topics": [
            "Operating Systems",
            "DBMS and SQL",
            "Computer Networks",
            "Object-Oriented Programming",
            "Data Structures"
        ],
        "resource": "https://www.geeksforgeeks.org/",
        "practice": "Revise 20 core CS interview questions."
    },

    "Technical Interview": {
        "topics": [
            "Resume-Based Questions",
            "Project Explanation",
            "Technical Fundamentals",
            "Problem Solving"
        ],
        "resource": "https://www.geeksforgeeks.org/",
        "practice": "Explain each resume project aloud."
    },

    "HR Interview": {
        "topics": [
            "Self Introduction",
            "Strengths and Weaknesses",
            "Why Should We Hire You?",
            "Career Goals",
            "Why This Company?"
        ],
        "resource": "https://www.indiabix.com/hr-interview/questions-and-answers/",
        "practice": "Practice 5 HR answers aloud."
    },

    "Python": {
        "topics": [
            "Python Basics",
            "Functions",
            "Lists and Dictionaries",
            "Exception Handling"
        ],
        "resource": "https://docs.python.org/3/tutorial/",
        "practice": "Write 5 simple Python programs."
    },

    "Machine Learning": {
        "topics": [
            "Supervised Learning",
            "Unsupervised Learning",
            "Classification",
            "Regression",
            "Model Evaluation"
        ],
        "resource": "https://developers.google.com/machine-learning/crash-course",
        "practice": "Build a simple classification model."
    },

    "SQL": {
        "topics": [
            "SELECT",
            "WHERE",
            "GROUP BY",
            "JOIN",
            "Subqueries"
        ],
        "resource": "https://www.w3schools.com/sql/",
        "practice": "Execute 10 SQL queries."
    },

    "TensorFlow": {
        "topics": [
            "Tensors",
            "Neural Networks",
            "Keras",
            "Model Training"
        ],
        "resource": "https://www.tensorflow.org/tutorials",
        "practice": "Build a basic neural network."
    },

    "NLP": {
        "topics": [
            "Text Preprocessing",
            "Tokenization",
            "TF-IDF",
            "Cosine Similarity"
        ],
        "resource": "https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html",
        "practice": "Build a text similarity application."
    }
}


def generate_roadmap(missing_skills, preparation_areas, days):

    roadmap = []

    areas = list(
        dict.fromkeys(
            preparation_areas + missing_skills
        )
    )

    days = max(1, int(days))

    for index, area in enumerate(areas):

        details = LEARNING_DATABASE.get(
            area,
            {
                "topics": [
                    area + " Fundamentals",
                    "Important Concepts",
                    "Practical Applications"
                ],
                "resource": None,
                "practice": "Complete a beginner exercise on " + area
            }
        )

        day = min(
            days,
            (index * days) // len(areas) + 1
        )

        roadmap.append({
            "day": day,
            "area": area,
            "topics": details["topics"],
            "resource": details["resource"],
            "practice": details["practice"]
        })

    return roadmap
