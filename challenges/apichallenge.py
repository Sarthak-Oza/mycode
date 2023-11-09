#!/usr/bin/env python3
"""Friday Warmup | Returning Data From Complex JSON"""

import requests
import html
import random
import os
import time

URL= "https://opentdb.com/api.php?amount=5&category=9&difficulty=medium"

def main():

    # data will be a python dictionary rendered from your API link's JSON!
    data= requests.get(URL).json()

    for question in data.get("results"):
        os.system("cls" if os.name == "nt" else "clear")
        while True:
            # print(question,end="\n\n")

            print("Question: ", html.unescape(question.get("question")), end="\n\n")

            answers = [None]
            answers.extend([html.unescape(a) for a in question.get("incorrect_answers")])
            correct_answer = html.unescape(question.get("correct_answer"))
            answers.append(correct_answer)
            random.shuffle(answers[1:])

            for i in range(1, len(answers)):
                print(f"{i}: {answers[i]}")

            user_answer_input = int(input("Please enter your answer: "))
            if user_answer_input >= 1 and user_answer_input <= len(answers)-1:
                if answers[user_answer_input] == correct_answer:
                    print("--> Correct Answer")
                else:
                    print("--> Incorrect Answer")
                time.sleep(2)
                break

            else:
                print("Invalid Answer, please try again!")
        

if __name__ == "__main__":
    main()