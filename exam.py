#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.2.33
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

#TO:DO - Add function to update cr_attempts value for question object.
#TO:DO - Add function to update in_attempts value for question obhect.

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

def practice_quiz(selection):
    # Continue picking random questions to quiz the user enters the answer X.
    while selection != "X":
        index = random_question()
        answer = pool['question_pool'][index - 1]['right_answer']
        for x in range(4):
            letter = answer_letter[x]
            print(letter + ": " + pool['question_pool'][index - 1]['answers'][0][letter])
        entry = input("\nWhat is the correct answer?: ").upper()
        selection = entry
        if entry == answer:
            print(bcolors.BOLD + "Correct!" + bcolors.ENDC)
            #TO:DO - Add 1 to cr_attempts value.
        elif entry == "X":
            continue
        else:
            print(bcolors.WARNING + "\nSorry the correct answer was %s." % (answer) + bcolors.ENDC)
            # TO:DO - Add 1 to in_attempts value.

# Ask user if they want to add questions / answers. Print header.
# TO:DO - Make header generic and move into data.json file.
print("\n2019-2023 General Class Pool - Exam Tool")
print("2nd & Final Public Release with Errata - March 15, 2019")
print("Question ID's show [correct|incorrect] attempts.\n")
selection = input("(A)dd Question, (R)eview, (P)ractice, or E(X)it?: ").upper()
if selection == "A":
    selection = add_question(selection)

# Load questions file.
with open('data.json', 'r') as f:
    pool = json.load(f)

# Get length of question pool.
pool_len = len(pool['question_pool'])
print("\nThere are %d total questions in the pool." % (pool_len))

if selection == "N":
    selection = input("\n(R)eview, (P)ractice, or E(X)it?: ")

if selection == "R":
    review_question(selection)

if selection == "P":
    practice_quiz(selection)
else:
    pass
