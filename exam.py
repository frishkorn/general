#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.0.5
# ------------------------
import json

# JSON write function (pretty print).
def write_json(data, filename='data.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

# Ask user if they want to add questions / answers.
selection = input("Would you like to enter new questions? (Y/N): ")
while selection == "Y":
    # Ask user to input the question.
    question = input("Question: ")

    # Ask user to input answers A - D.
    answerList = []
    for x in range(4):
        answer = input("Answer: ")
        answerList.append(answer)

    # Ask user which one is the right answer.
    correct = input("Which answer is correct?: ")
    
    # Save Q&A to a JSON formatted file.
    question_data = {'question':question,'answers':[{'A':answerList[0],'B':answerList[1],'C':answerList[2],'D':answerList[3]}],'right_answer':correct}
    
    # Append new questions to data.json.
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['question_pool']
        temp.append(question_data)

    write_json(file_data)

    # Ask user if they would like to enter another question / answer.
    selection = input("Would you like to add another question? (Y/N): ")
    
# Load questions file.

# Pick a random question and ask user to answer it.
