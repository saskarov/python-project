import streamlit as st
import pandas as pd
from modules.quiz_generator import IMDBQuiz


def main():
    data = pd.read_csv('data/films_data.csv')
    quiz_data = IMDBQuiz(data)

    st.title("IMDB movies Quiz")

    st.write(
        "Welcome to the film quiz! This quiz is based on IMDB dataset of movies and TV shows."
    )

    st.header("First Ten Rows of prepared data")
    st.write(data.head(10))

    st.header("Let's find out your cinema knowledge!")
    st.write("Choose the difficulty and answer the questions")
    difficulty = st.selectbox("Level", ["Easy", "Moderate", "Hard"])

    # Initializing session variables
    if "questions" not in st.session_state or st.session_state.difficulty != difficulty:
        st.session_state.difficulty = difficulty
        st.session_state.questions = quiz_data.generate_question(difficulty) 
        
        st.session_state.user_answers = [""] * 5
        st.session_state.score = 0
        st.session_state.show_results = False

    for i, (question, correct_option, options) in enumerate(st.session_state.questions):
        st.header(f"{i + 1}. {question}")
        selected_option = st.radio(f"Options:", options, key=f"q{i}")
        st.session_state.user_answers[i] = selected_option

    # Checking answers and calculating score
    if st.button("Check"):
        st.session_state.show_results = True
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            if st.session_state.user_answers[i] == correct_option:
                st.session_state.score += 1

    # Displaying final score after submitting all answers
    if st.session_state.show_results and all(st.session_state.user_answers):
        st.success(f"Your total score: {st.session_state.score}/5")
        st.markdown("Right Answers:")
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            st.write(f"Question {i + 1}: {correct_option}")

if __name__ == "__main__":
    main()
