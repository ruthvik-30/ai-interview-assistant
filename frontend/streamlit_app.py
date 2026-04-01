import streamlit as st
import requests
import re

BACKEND = "http://localhost:8000"

st.set_page_config(page_title="AI Interview Assistant", layout="centered")

st.title("🧠 Gemini AI Interview Assistant")

mode = st.selectbox("Mode", ["Ask Assistant", "Mock Interview"])


# ---------------- Helper: Parse Question ----------------
def parse_question(text):
    category, difficulty, question = "", "", text

    try:
        category_match = re.search(r"Category:\s*(.*)", text)
        difficulty_match = re.search(r"Difficulty:\s*(.*)", text)
        question_match = re.search(r"Question:\s*(.*)", text)

        if category_match:
            category = category_match.group(1).strip()

        if difficulty_match:
            difficulty = difficulty_match.group(1).strip()

        if question_match:
            question = question_match.group(1).strip()

    except:
        pass

    return category, difficulty, question


# ---------------- Ask Assistant ----------------
if mode == "Ask Assistant":
    st.markdown("### 💬 Ask Anything")

    query = st.text_input("Ask about DSA / ML / Code")

    if st.button("Ask"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            res = requests.post(f"{BACKEND}/ask", json={"query": query})

            if res.status_code == 200:
                data = res.json()

                st.markdown("### 🤖 Answer")
                st.success(data.get("answer", "No answer"))

                st.caption(f"⏱ Latency: {data.get('latency_seconds', 0)}s")
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)


# ---------------- Mock Interview ----------------
if mode == "Mock Interview":

    st.markdown("### 🎯 Mock Interview")

    topics = ["DSA", "Machine Learning", "Backend", "Frontend", "System Design"]

    topic = st.selectbox(
        "Select Topic",
        ["Select a topic"] + topics,
        index=0
    )

    selected_topic = None if topic == "Select a topic" else topic

    # Session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "category" not in st.session_state:
        st.session_state.category = ""
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = ""
    if "evaluation_question" not in st.session_state:
        st.session_state.evaluation_question = ""

    # -------- Generate Question --------
    if st.button("🚀 Generate Question"):
        if not selected_topic:
            st.warning("Please select a topic first.")
        else:
            res = requests.post(
                f"{BACKEND}/mock-question",
                json={"topic": selected_topic}
            )

            if res.status_code == 200:
                data = res.json()
                raw_text = data.get("answer", "").strip()

                if not raw_text:
                    st.warning("No question generated. Try again.")
                else:
                    category, difficulty, clean_q = parse_question(raw_text)

                    st.session_state.current_question = clean_q
                    st.session_state.category = category
                    st.session_state.difficulty = difficulty
                    st.session_state.evaluation_question = clean_q

                    st.success("Question generated!")
                    st.rerun()
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)

    # -------- Display Question --------
    if st.session_state.current_question:
        st.markdown("---")
        st.markdown("## 🧠 Generated Question")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**📚 Category:** {st.session_state.category or 'N/A'}")

        with col2:
            st.markdown(f"**⚡ Difficulty:** {st.session_state.difficulty or 'N/A'}")

        st.markdown("### ❓ " + st.session_state.current_question)

    # -------- Answer Section --------
    st.markdown("---")
    st.markdown("### ✍️ Your Answer")

    question = st.text_input(
        "Question for evaluation",
        key="evaluation_question"
    )

    answer = st.text_area("", height=150)

    # -------- Evaluate --------
    if st.button("📊 Evaluate"):
        if not question.strip() or not answer.strip():
            st.warning("Please provide both question and answer.")
        else:
            res = requests.post(
                f"{BACKEND}/evaluate",
                json={"question": question, "answer": answer}
            )

            if res.status_code == 200:
                data = res.json()

                st.markdown("---")
                st.markdown("## 📊 Evaluation Results")

                score = data.get("score", {})

                col1, col2, col3 = st.columns(3)

                col1.metric("Correctness", score.get("Correctness", 0))
                col2.metric("Depth", score.get("Depth", 0))
                col3.metric("Clarity", score.get("Clarity", 0))

                st.markdown("### 💬 Feedback")
                st.info(data.get("feedback", "No feedback"))

                st.markdown("### 🚀 Suggested Improved Answer")
                st.success(data.get("improved_answer", "N/A"))

            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)
