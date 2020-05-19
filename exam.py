#!/usr/bin/env python3

# exam.py
# C. Frishkorn 05/19/2020
# version: 0.3.42
# ------------------------
import json
from random import randint

answer_letter = {0:"A", 1:"B", 2:"C", 3:"D"}

class bcolors:
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# JSON write function (pretty print).
def write_json(data, filename='data.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

# Get random function.
def get_random(length):
    value = randint(1, length)
    return value

# Get random question function.
def random_question():
    index = get_random(pool_len)
    print("\n" + pool['question_pool'][index - 1]['question_id'] + " [" + str(pool['question_pool'][index - 1]['cr_attempts']) + "|" + str(pool['question_pool'][index - 1]['in_attempts']) + "]")
    print(pool['question_pool'][index - 1]['question'])
    return index

def add_question(selection):
    while selection != "N":
        # Ask user to input the question id.
        question_id = input("\nQuestion ID: ")

        # Ask user to input the question.
        question = input("Question: ")

        # Ask user to input answers A - D.
        answer_list = []
        for x in range(4):
            letter = answer_letter[x]
            answer = input("Answer %s: " % (letter))
            answer_list.append(answer)

        # Ask user which one is the right answer.
        correct = input("Which answer is correct?: ").upper()

        # Save Q&A to a JSON formatted file.
        question_data = {'question_id':question_id,'question':question,'answers':[{"A":answer_list[0], "B":answer_list[1], "C":answer_list[2], "D":answer_list[3]}],'right_answer':correct,'cr_attempts':0,'in_attempts':0}

        # Append new questions to data.json.
        with open('data.json') as json_file:
            file_data = json.load(json_file)
            temp = file_data['question_pool']
            temp.append(question_data)
        write_json(file_data)

        # Ask user if they would like to enter another question / answer.
        selection = input("\nWould you like to add another question? (Y/N): ").upper()
    return selection

def review_question(selection):
    # Show review questions until user selects no.
    another = "Y"
    while selection != "N":
        index = random_question()
        answer = pool['question_pool'][index - 1]['right_answer']
        print(answer + ": " + pool['question_pool'][index - 1]['answers'][0][answer])
        selection = input("\nAnother review question? (Y/N): ").upper()

# Update attempts function.
def update_attempt(result, index):
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['question_pool']
        if result == "C":
            temp[index - 1]['cr_attempts'] = temp[index - 1]['cr_attempts'] + 1
        else:
            temp[index - 1]['in_attempts'] = temp[index - 1]['in_attempts'] + 1
    write_json(file_data)

def practice_quiz(selection):
    # Continue picking random questions to quiz the user enters the answer X.
    while selection != "X":
        index = random_question()
        answer = pool['question_pool'][index - 1]['right_answer']
        for x in range(4):
            letter = answer_letter[x]
            print(letter + ": " + pool['question_pool'][index - 1]['answers'][0][letter])
        entry = input("\nWhat is the correct answer? (X) to e(X)it: ").upper()
        selection = entry
        if entry == answer:
            print(bcolors.BOLD + "Correct!" + bcolors.ENDC)
            result = "C"
        elif entry == "X":
            continue
        else:
            print(bcolors.WARNING + "\nSorry the correct answer was %s." % (answer) + bcolors.ENDC)
            result = "I"
        update_attempt(result, index)

def load_pool():
    with open('data.json', 'r') as f:
        pool = json.load(f)
        return pool

# Load questions file.
pool = load_pool()

# Ask user if they want to add questions / answers. Print header.
# TO:DO - Make header generic and move into data.json file.
print("\n2019-2023 General Class Pool - Exam Tool")
print("2nd & Final Public Release with Errata - March 15, 2019")
print("Question ID's show [correct|incorrect] attempts.\n")
selection = input("(A)dd Question, (R)eview, (P)ractice, or E(X)it?: ").upper()
if selection == "A":
    selection = add_question(selection)
    pool = load_pool()

# Get length of question pool.
pool_len = len(pool['question_pool'])
print("\nThere are %d total questions in the pool." % (pool_len))

if selection == "N":
    selection = input("\n(R)eview, (P)ractice, or E(X)it?: ").upper()

if selection == "R":
    review_question(selection)

if selection == "P":
    practice_quiz(selection)
else:
    pass
