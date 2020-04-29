#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.0.11
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

# Ask user if they want to add questions / answers. Print header.
# TO:DO - Make header generic and move into data.json file.
print("\n2019-2023 General Class Pool")
print("2nd & Final Public Release with Errata - March 15, 2019\n")
selection = input("Would you like to enter new questions? (Y/N): ").lower()
while selection == "y":
    # Ask user to input the question id.
    question_id = input("\nQuestion ID: ")

    # Ask user to input the question.
    question = input("Question: ")

    # Ask user to input answers A - D.
    answer_list = []
    answer_letter = {0:"A", 1:"B", 2:"C", 3:"D"}
    for x in range(4):
        letter = answer_letter[x]
        answer = input("Answer %s: " % (letter))
        answer_list.append(answer)

    # Ask user which one is the right answer.
    correct = input("Which answer is correct?: ").upper()
    
    # Save Q&A to a JSON formatted file.
    question_data = {'question_id':question_id,'question':question,'answers':[{"A":answer_list[0], "B":answer_list[1], "C":answer_list[2], "D":answer_list[3]}],'right_answer':correct}
    
    # Append new questions to data.json.
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['question_pool']
        temp.append(question_data)

    write_json(file_data)

    # Ask user if they would like to enter another question / answer.
    selection = input("\nWould you like to add another question? (Y/N): ").lower()
    
# Load questions file.
with open('data.json', 'r') as f:
    pool = json.load(f)

# Get length of question pool.
pool_len = len(pool['question_pool'])
print("\nThere are %d total questions in the pool.\n" % (pool_len))

# Ask user if they would like to review or take practice exam.
selection = input("Would you like to practice or review? (P/R): ").lower()
if selection == "r":
    # Show review questions until user selects no.
    another = "y"
    while another == "y":
        index = get_random(pool_len)
        print("\n" + pool['question_pool'][index - 1]['question_id'])
        print(pool['question_pool'][index - 1]['question'])
        answer = pool['question_pool'][index - 1]['right_answer']
        print(answer + ": " + pool['question_pool'][index - 1]['answers'][0][answer])
        another = input("\nAnother review question? (Y/N): ").lower()
else:
    print("Found P")

# Pick a random question and ask user to answer it.
