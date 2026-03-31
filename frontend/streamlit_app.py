import streamlit as st
import requests

BACKEND = "http://localhost:8000"

st.title("Gemini AI Interview Assistant")

mode = st.selectbox("Mode", ["Ask Assistant", "Mock Interview"])

if mode == "Ask Assistant":
    query = st.text_input("Ask about DSA / ML / Code")

    if st.button("Ask", key="ask_button"):
        res = requests.post(f"{BACKEND}/ask", json={"query": query})
        if res.status_code == 200:
            st.write(res.json())
        else:
            st.error(f"Error {res.status_code}")
            st.write(res.text)

if mode == "Mock Interview":
    # Predefined topics
    topics = ["DSA", "Machine Learning", "Backend", "Frontend", "System Design"]

    # Add a placeholder at index 0
    topic = st.selectbox(
        "Select Topic",
        ["Select a topic"] + topics,
        index=0
    )

    # Map placeholder to empty value
    selected_topic = None if topic == "Select a topic" else topic

    # Initialize session state for question
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""

    # Generate Question
    if st.button("Generate Question", key="generate_question"):
        if not selected_topic:
            st.warning("Please select a topic first.")
        else:
            res = requests.post(f"{BACKEND}/mock-question", json={"topic": selected_topic})
            if res.status_code == 200:
                data = res.json()
                # Use the entire 'answer' as the question
                question_text = data.get("answer", "").strip()

                if not question_text:
                    st.warning("No question was generated. Try again.")
                else:
                    st.session_state.current_question = question_text
                    st.success(f"Question generated.")
            else:
                st.error(f"Error {res.status_code}")
                st.write(res.text)


    # Show the current question for evaluation
    question = st.text_input(
        "Question for evaluation",
        value=st.session_state.get("current_question", ""),
        key="evaluation_question"
    )
    answer = st.text_area("Your Answer", key="evaluation_answer")

    # Evaluate the answer
    if st.button("Evaluate", key="evaluate_button"):
        if not question or not answer:
            st.warning("Please provide both question and your answer.")
        else:
            res = requests.post(
                f"{BACKEND}/evaluate",
                json={"question": question, "answer": answer}
            )
            if res.status_code == 200:
                data = res.json()

                st.subheader("Score:")
                score = data.get("score", {})
                if score:
                    for k, v in score.items():
                        st.write(f"{k}: {v}")
                else:
                    st.write("N/A")

                st.subheader("Feedback:")
                feedback = data.get("feedback", "")
                st.write(feedback or "No feedback")

                st.subheader("Suggested Improved Answer:")
                improved = data.get("improved_answer", "")
                st.write(improved or "N/A")
