#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.0.9
# ------------------------
import json
from random import randint

# JSON write function (pretty print).
def write_json(data, filename='data.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

# Get random function.
def get_random(length):
    value = randint(1, length)
    return value

# Ask user if they want to add questions / answers.
print("2019-2023 General Class Pool")
print("2nd & Final Public Release with Errata - March 15, 2019")
selection = input("Would you like to enter new questions? (Y/N): ").lower()
while selection == "y":
    # Ask user to input the question.
    question = input("Question: ")

    # Ask user to input answers A - D.
    answerList = []
    for x in range(4):
        answer = input("Answer: ")
        answerList.append(answer)

    # Ask user which one is the right answer.
    correct = input("Which answer is correct?: ").upper()
    
    # Save Q&A to a JSON formatted file.
    question_data = {'question':question,'answers':[{'A':answerList[0],'B':answerList[1],'C':answerList[2],'D':answerList[3]}],'right_answer':correct}
    
    # Append new questions to data.json.
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['question_pool']
        temp.append(question_data)

    write_json(file_data)

    # Ask user if they would like to enter another question / answer.
    selection = input("Would you like to add another question? (Y/N): ").lower()
    
# Load questions file.
with open('data.json', 'r') as f:
    pool = json.load(f)

# Get length of question pool.
pool_len = len(pool['question_pool'])
print("There are %d total questions in the pool." % (pool_len))

# for question in pool:
    # print(pool)
    # print(pool['question_pool'][1])

# Ask user if they would like to review or take practice exam.
selection = input("Would you like to practice or review? (P/R): ").lower()
if selection == "r":
     index = get_random(pool_len)
     print(pool['question_pool'][index - 1])
else:
    print("Found P")



# Pick a random question and ask user to answer it.
