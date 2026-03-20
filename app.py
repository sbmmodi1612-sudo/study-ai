import streamlit as st
from agents import study_pipeline, doubt_solver
from database import get_notes

st.title("📚 AI Study Assistant")

# 🧠 SESSION STATE INIT
if "notes" not in st.session_state:
    st.session_state.notes = None

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# -------------------------------
# 🎯 FORM: ENTER TOPIC
# -------------------------------
with st.form("study_form"):
    topic = st.text_input("Enter Topic", value=st.session_state.topic)
    submitted = st.form_submit_button("Generate Study Material")

    if submitted:
        with st.spinner("⏳ Generating content..."):
            try:
                data = study_pipeline(topic)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

        st.session_state.topic = topic

        # Notes
        if "notes" in data:
            notes = data["notes"].replace("\\n", "\n")
            st.session_state.notes = notes
        else:
            st.error("❌ Notes not generated")
            st.stop()

        # Quiz
        quiz_data = data.get("quiz", [])

        if not quiz_data or len(quiz_data) < 5:
            st.warning("⚠️ Quiz generation failed. Try again.")
            st.session_state.quiz = []
        else:
            st.session_state.quiz = quiz_data

        # Reset
        st.session_state.score = 0
        st.session_state.answered = {}

# -------------------------------
# 📘 SHOW NOTES
# -------------------------------
if st.session_state.notes:
    st.subheader("📘 Notes")
    st.markdown(st.session_state.notes)

# -------------------------------
# ❓ QUIZ
# -------------------------------
if st.session_state.quiz:
    st.subheader("❓ MCQ Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "answered" not in st.session_state:
        st.session_state.answered = {}

    for i, q in enumerate(st.session_state.quiz):
        st.write(f"### Q{i+1}: {q['question']}")

        selected = st.radio(
            "Choose an option:",
            q["options"],
            key=f"q_{i}"
        )

        if st.button(f"Check Answer {i}", key=f"btn_{i}"):

            user_choice = selected[0]

            if i not in st.session_state.answered:
                if user_choice == q["answer"]:
                    st.success("✅ Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Wrong! Correct answer: {q['answer']}")

                st.session_state.answered[i] = True
            else:
                st.warning("⚠️ Already answered")

    if st.button("Show Final Score"):
        total = len(st.session_state.quiz)
        st.info(f"Your Score: {st.session_state.score}/{total}")

# -------------------------------
# 💬 DOUBT SECTION
# -------------------------------
st.subheader("💬 Ask Doubt")

with st.form("doubt_form"):
    question = st.text_input("Ask your question")
    doubt_submit = st.form_submit_button("Get Answer")

    if doubt_submit:
        notes = get_notes(st.session_state.topic)

        if not notes:
            st.error("❌ Generate study material first!")
        else:
            answer = doubt_solver(notes, question)
            st.write(answer)