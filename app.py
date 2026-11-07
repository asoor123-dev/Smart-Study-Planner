import streamlit as st
from datetime import date

st.set_page_config(page_title="SmartStudy Planner", page_icon="📚", layout="wide")

for key, default in {"courses": [], "notes": [], "tasks": [], "grades": [], "quiz_questions": []}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("📚 SmartStudy Planner")
st.caption("Your university study assistant")

pages = ["Dashboard", "Courses", "Notes & Materials", "Study Planner", "Practice Quizzes", "Grades"]
page = st.sidebar.radio("Navigation", pages)

if page == "Dashboard":
    st.header("Dashboard")
    a, b, c = st.columns(3)
    a.metric("Courses", len(st.session_state.courses))
    b.metric("Study tasks", len(st.session_state.tasks))
    c.metric("Grades recorded", len(st.session_state.grades))
    st.subheader("Upcoming tasks")
    pending = sorted((t for t in st.session_state.tasks if not t["done"]), key=lambda t: t["due"])
    if pending:
        for task in pending[:10]:
            st.write(f"📅 {task['due']} — {task['course']}: {task['title']}")
    else:
        st.info("No upcoming tasks yet.")

elif page == "Courses":
    st.header("My Courses")
    with st.form("add_course", clear_on_submit=True):
        name = st.text_input("Course name")
        code = st.text_input("Course code")
        submitted = st.form_submit_button("Add Course")
    if submitted:
        if not name.strip():
            st.warning("Please enter a course name.")
        elif any(c["name"].casefold() == name.strip().casefold() and c["code"].casefold() == code.strip().casefold() for c in st.session_state.courses):
            st.warning("This course is already in your list.")
        else:
            st.session_state.courses.append({"name": name.strip(), "code": code.strip()})
            st.success("Course added successfully!")
    st.subheader("Your Courses")
    if not st.session_state.courses:
        st.info("Add your first course above.")
    for i, course in enumerate(st.session_state.courses):
        left, right = st.columns([5, 1])
        left.write(f"📖 {course['code']} — {course['name']}")
        if right.button("🗑️ Delete", key=f"delete_course_{i}"):
            st.session_state.courses.pop(i)
            st.rerun()

elif page == "Notes & Materials":
    st.header("Notes & Materials")
    course_names = [c["name"] for c in st.session_state.courses]
    if not course_names:
        st.info("Add a course first in the Courses section.")
    else:
        with st.form("add_note", clear_on_submit=True):
            course = st.selectbox("Course", course_names)
            title = st.text_input("Note title")
            note = st.text_area("Your notes")
            uploaded = st.file_uploader("Attach a PDF lecture (session only)", type=["pdf"])
            submitted = st.form_submit_button("Save note")
        if submitted:
            if not title.strip() and not note.strip() and uploaded is None:
                st.warning("Add a title, some notes, or a PDF.")
            else:
                st.session_state.notes.append({"course": course, "title": title.strip() or "Untitled", "text": note, "filename": uploaded.name if uploaded else None, "pdf": uploaded.getvalue() if uploaded else None})
                st.success("Saved for this session.")
        for i, item in enumerate(st.session_state.notes):
            with st.expander(f"{item['course']} — {item['title']}"):
                st.write(item["text"] or "No text notes.")
                if item["pdf"]:
                    st.download_button("Download attached PDF", item["pdf"], file_name=item["filename"], mime="application/pdf", key=f"pdf_{i}")

elif page == "Study Planner":
    st.header("Study Planner")
    course_names = [c["name"] for c in st.session_state.courses]
    if not course_names:
        st.info("Add a course first.")
    else:
        with st.form("add_task", clear_on_submit=True):
            course = st.selectbox("Course", course_names)
            title = st.text_input("Study task")
            due = st.date_input("Due date", value=date.today())
            submitted = st.form_submit_button("Add Task")
        if submitted:
            if title.strip():
                st.session_state.tasks.append({"course": course, "title": title.strip(), "due": due, "done": False})
                st.success("Task added.")
            else:
                st.warning("Enter a task description.")
    for i, task in enumerate(st.session_state.tasks):
        checked = st.checkbox(f"{task['due']} — {task['course']}: {task['title']}", value=task["done"], key=f"task_{i}")
        task["done"] = checked

elif page == "Practice Quizzes":
    st.header("Practice Quizzes")
    st.info("AI quiz generation from your uploaded lecture PDFs will be added in the next stage. No questions are invented from unrelated material.")
    st.write("Your course and lecture material sections are ready for the next stage.")

elif page == "Grades":
    st.header("Grades")
    course_names = [c["name"] for c in st.session_state.courses]
    if not course_names:
        st.info("Add a course first.")
    else:
        with st.form("add_grade", clear_on_submit=True):
            course = st.selectbox("Course", course_names)
            assessment = st.text_input("Assessment name (e.g. Midterm)")
            earned = st.number_input("Points earned", min_value=0.0, value=0.0)
            possible = st.number_input("Points possible", min_value=0.01, value=100.0)
            submitted = st.form_submit_button("Save Grade")
        if submitted:
            if earned > possible:
                st.warning("Points earned cannot exceed points possible.")
            else:
                st.session_state.grades.append({"course": course, "assessment": assessment.strip() or "Assessment", "earned": earned, "possible": possible})
                st.success("Grade saved for this session.")
    for item in st.session_state.grades:
        st.write(f"{item['course']} — {item['assessment']}: {item['earned'] / item['possible'] * 100:.1f}%")
    if st.session_state.grades:
        total_earned = sum(item["earned"] for item in st.session_state.grades)
        total_possible = sum(item["possible"] for item in st.session_state.grades)
        st.metric("Overall points-based percentage", f"{total_earned / total_possible * 100:.1f}%")

st.sidebar.caption("Prototype: session data is not permanent. Do not upload sensitive files.")
