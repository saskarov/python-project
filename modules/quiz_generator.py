import random
import pandas as pd
import numpy as np


class IMDBQuiz:
    def __init__(self, data):
        self.data = data


    def generate_dir_question(self, df):
        non_empty = df[df["category"].notnull()]
        filtered = non_empty[non_empty['category'] == 'director']
        show_row = filtered.sample(n=1).iloc[0]
        show, correct_opt = show_row["primaryTitle"], show_row["primaryName"]

        question = f"Who directed the '{show}'?"

        incorrect_opts = (
            filtered[filtered["primaryName"] != correct_opt]
            .sample(n=3)["primaryName"]
            .tolist()
        )

        options = [correct_opt, *incorrect_opts]
        random.shuffle(options)
        return question, correct_opt, options

    def generate_genre_question(self, df):
        non_empty = df[df["genres"].notnull()]
        show = non_empty.sample()["primaryTitle"].iloc[0]

        question = f"What genre does the '{show}' belong to?"

        correct_opt = non_empty.sample()["genres"].iloc[0]

        incorrect_opts = non_empty.sample(n=3)[
            "genres"
        ].tolist()  # convert the pandas Series into a Python list

        options = [correct_opt, *incorrect_opts]  # * is unpacking operator
        random.shuffle(options)
        return question, correct_opt, options

    def generate_rating_question(self, df):
        non_empty = df[df["averageRating"].notnull()]
        show_row = non_empty.sample(n=1).iloc[0]
        show, correct_opt = show_row["primaryTitle"], show_row["averageRating"]
        question = f"What kind of average rating from viewers does the '{show}' have according to IMDB?"
        incorrect_opts = (
            non_empty[non_empty["averageRating"] != correct_opt]
            .sample(n=3)["averageRating"]
            .tolist()
        )

        options = [correct_opt, *incorrect_opts]
        random.shuffle(options)
        return question, correct_opt, options

    def generate_cast_question(self, df):
        non_empty = df[df["category"].notnull()]
        filtered = non_empty[non_empty['category'] == 'actor']
        show_row = filtered.sample(n=1).iloc[0]
        show, character, correct_opt = show_row["primaryTitle"], show_row["characters"].strip("[]"), show_row["primaryName"]

        question = f"Who played {character} in the '{show}'?"
        incorrect_opts = (
            filtered[filtered["primaryName"] != correct_opt]
            .sample(n=3)["primaryName"]
            .tolist()
        )

        options = [correct_opt, *incorrect_opts]

        random.shuffle(options)
        return question, correct_opt, options

    def generate_year_question(self, df):
        non_empty = df[df["startYear"].notnull()]
        show_row = non_empty.sample(n=1).iloc[0]
        show, correct_opt = show_row["primaryTitle"], show_row["startYear"]

        question = f"What year was the '{show}' released?"

        incorrect_opts = (
            non_empty[non_empty["startYear"] != correct_opt]
            .sample(n=3)["startYear"]
            .tolist()
        )
        options = [correct_opt, *incorrect_opts]

        random.shuffle(options)
        return question, correct_opt, options

    def generate_question(self, difficulty):
        filtered = self.data[self.data['numVotes'] > 2000]
    
        question_types_hard = [self.generate_year_question, self.generate_genre_question]
        if difficulty == "Easy":
            filtered_data = filtered[filtered['numVotes'] > 13000]
        elif difficulty == "Moderate":
            filtered_data = filtered[(filtered['numVotes'] < 13000) & (filtered['numVotes'] > 4000)]
        elif difficulty == "Hard":
            filtered_data = filtered[filtered['numVotes'] < 4000]
           
        question_types = [
        self.generate_dir_question,
        self.generate_genre_question,
        self.generate_cast_question,
        self.generate_rating_question,
        self.generate_year_question,
        ]

         # Generate one question from each type
        questions = [question_type(filtered_data) for question_type in question_types]
        return questions
