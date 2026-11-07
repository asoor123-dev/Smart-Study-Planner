import streamlit as st

st.set_page_config(

    page_title="SmartStudy Planner",

    page_icon="📚",

    layout="wide"

)

st.title("📚 SmartStudy Planner")

st.write("Your university study assistant")

if "courses" not in st.session_state:

    st.session_state.courses = []

page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Courses",

        "Notes & Materials",

        "Study Planner",

        "Practice Quizzes",

        "Grades"

    ]

)

if page == "Dashboard":

    st.header("📊 Dashboard")

    st.metric("Total Courses", len(st.session_state.courses))

    st.success("Welcome to SmartStudy Planner!")

elif page == "Courses":

    st.header("📚 My Courses")

    with st.form("add_course"):

        name = st.text_input("Course name")

        code = st.text_input("Course code")

        submitted = st.form_submit_button("Add Course")

    if submitted:

        if name.strip():

            st.session_state.courses.append({

                "name": name.strip(),

                "code": code.strip()

            })

            st.success("Course added successfully!")

        else:

            st.warning("Please enter a course name.")

    st.subheader("Your Courses")

    for course in st.session_state.courses:

        st.write(f"📖 {course['code']} — {course['name']}")

elif page == "Notes & Materials":

    st.header("📝 Notes & Materials")

    st.info("This section will be developed next.")

elif page == "Study Planner":

    st.header("📅 Study Planner")

    st.info("This section will be developed next.")

elif page == "Practice Quizzes":

    st.header("🧠 Practice Quizzes")

    st.info("This section will be developed next.")

elif page == "Grades":

    st.header("🎓 Grades")

    st.info("This section will be developed next.")
