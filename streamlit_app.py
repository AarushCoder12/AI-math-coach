
import streamlit as st
import openai
import os

st.set_page_config(page_title="AI Math Coach", page_icon="🧠")

st.title("🧠 Personalized Math Coach")
st.write("Answer the following questions. If you get any wrong, your AI coach will generate a lesson to help you improve!")

# Questions
questions = {
    "fractions": {
        "question": "What is 1/2 + 1/4?",
        "options": ["1/4", "3/4", "1/2"],
        "answer": "3/4"
    },
    "decimals": {
        "question": "What is 0.6 + 0.15?",
        "options": ["0.65", "0.75", "0.85"],
        "answer": "0.75"
    },
    "percentages": {
        "question": "What is 25% of 80?",
        "options": ["15", "20", "25"],
        "answer": "20"
    },
    "algebra": {
        "question": "Solve: x + 3 = 7. What is x?",
        "options": ["x=10", "x=4", "x=3"],
        "answer": "x=4"
    },
    "geometry": {
        "question": "What is the area of a rectangle with length 5 and width 3?",
        "options": ["8", "15", "10"],
        "answer": "15"
    }
}

user_answers = {}
with st.form("quiz_form"):
    for topic, q in questions.items():
        user_answers[topic] = st.radio(q["question"], q["options"], key=topic)
    submitted = st.form_submit_button("Submit Answers")

if submitted:
    incorrect_topics = []
    for topic, q in questions.items():
        if user_answers[topic] != q["answer"]:
            incorrect_topics.append(topic)

    st.subheader("✅ Quiz Results")
    for topic in questions:
        if topic in incorrect_topics:
            st.error(f"{topic.title()}: Incorrect ❌")
        else:
            st.success(f"{topic.title()}: Correct ✅")

    if incorrect_topics:
       st.subheader("📘 Personalized Lesson")

openai.api_key = st.secrets["OPENAI_API_KEY"]

prompt = (
    "You are a friendly 6th grade math tutor. "
    "Create a short and simple lesson for the following topics:\n"
    + ", ".join(incorrect_topics)
    + "\nInclude examples and 1 practice problem per topic."
)
with st.spinner("Generating your lesson..."):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
           try:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7,
    )
    st.write(response.choices[0].message.content)
except Exception as e:
    st.error("There was an error generating the lesson. Check your OpenAI key and try again.")
else:
    st.balloons()
    st.success("You got everything right! Great job! 🎉")

