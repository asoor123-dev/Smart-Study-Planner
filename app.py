

import streamlit as st

st.set_page_config(

    page_title="SmartStudy Planner",

    page_icon="📚",

    layout="wide"

)

st.title("📚 SmartStudy Planner")

st.write("Your AI-powered university study assistant")

st.success("Welcome to SmartStudy Planner!")

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "Choose a section",

    [

        "Dashboard",

        "Courses",

        "Notes & Materials",

        "Study Planner",

        "Practice Quizzes",

        "Grades"

    ]

)

st.header(page)

st.info("This section will be developed next.")
