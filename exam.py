#!/usr/bin/env python3

# exam.py
# C. Frishkorn 07/29/2020
# version: 1.1.153
# ------------------------
import json
from random import randint
from datetime import datetime

answer_letter = {0:"A", 1:"B", 2:"C", 3:"D"}

# ANSI escape sequences to produce colors.
class bcolors:
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# JSON write function (pretty print).
def write_json(data, filename):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

def store_result(score):
    now = datetime.now()
    score = float("{:.1f}".format(score))
    result = {'date':now.strftime("%m/%d/%Y"),'time':now.strftime("%H:%M:%S"),'score':score}
    with open('scores.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['score_history']
        temp.append(result)
        write_json(file_data, 'scores.json')

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

# Practice complete question pool in reverse order.
def series_mode(selection):
    index = pool_len
    count = 1
    last_index = pool["last_index"]
    if last_index < index:
        index = last_index
    if last_index == 0:
        index = pool_len
    while index != 0:
        print("\n" + pool['question_pool'][index - 1]['question_id'] + " [" + str(pool['question_pool'][index - 1]['cr_attempts']) + "|" + str(pool['question_pool'][index - 1]['in_attempts']) + "]")
        print(pool['question_pool'][index - 1]['question'])
        answer = pool['question_pool'][index - 1]['right_answer']
        for x in range(4):
            letter = answer_letter[x]
            print(letter + ": " + pool['question_pool'][index - 1]['answers'][letter])
        entry = input("\nWhat is the correct answer? or e(X)it: ").upper()
        selection = entry
        if entry == answer:
            print(bcolors.BOLD + "Correct!" + bcolors.ENDC)
            result = "C"
        elif entry == "X":
            break
        else:
            print(bcolors.WARNING + "\nSorry the correct answer was %s." % (answer) + bcolors.ENDC)
            result = "I"
        update_attempt(result, index)
        if count == 5:
            print(bcolors.BOLD + "\n%d questions remaining!" % (index - 1) + bcolors.ENDC)
            count = 0
        index -= 1
        count += 1

    # Get index and write it to the data.json file.
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        file_data['last_index'] = index
    write_json(file_data, 'data.json')

# 35 Question exam with only a selected number of questions per group.
# TO:DO - Add a time limit of 45 minutes for FCC test. Make configurable?
def exam_mode(selection):
    size = len(pool['group_questions'])
    total_num = 0
    num_wrong = 0
    attempted = []
    for x in range(size):
        remaining = pool['group_questions'][str(x)]
        while remaining != 0:
            # Get a question and skip if doesn't match desired question group.
            index = get_random(pool_len)
            if index in attempted:
                continue
            elif pool['question_pool'][index - 1]['question_group'] == x:
                print("\n" + pool['question_pool'][index - 1]['question_id'] + " [" + str(pool['question_pool'][index - 1]['cr_attempts']) + "|" + str(pool['question_pool'][index - 1]['in_attempts']) + "]")
                print(pool['question_pool'][index - 1]['question'])
                answer = pool['question_pool'][index - 1]['right_answer']
                for y in range(4):
                    letter = answer_letter[y]
                    print(letter + ": " + pool['question_pool'][index - 1]['answers'][letter])
                entry = input("\nWhat is the correct answer? ").upper()
                if entry == answer:
                    print(bcolors.BOLD + "Correct!" + bcolors.ENDC)
                    result = "C"
                else:
                    print(bcolors.WARNING + "\nSorry the correct answer was %s." % (answer) + bcolors.ENDC)
                    result = "I"
                    num_wrong += 1
                update_attempt(result, index)
                remaining -= 1
                total_num += 1
            else:
                continue
            attempted.append(index)
    score = (((total_num - num_wrong) / total_num) * 100)
    final = "\nYour score was "
    if num_wrong != 0:
        if score <= 73:
            print(final + bcolors.FAIL + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
        elif score <= 90:
            print(final + bcolors.WARNING + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
        else:
            print(final + bcolors.BOLD + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
    else:
        print(final + bcolors.BOLD + "100%" + bcolors.ENDC + "!")
    store_result(score)

def add_question(selection):
    while selection != "N":
        # Ask user to input the question id.
        question_id = input("\nQuestion ID: ")

        # Ask user to input question group.
        question_group = input("Question Group: ").upper()
        question_group = int(question_group)

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
        question_data = {'question_id':question_id,'question_group':question_group,'question':question,'answers':{"A":answer_list[0], "B":answer_list[1], "C":answer_list[2], "D":answer_list[3]},'right_answer':correct,'cr_attempts':0,'in_attempts':0}

        # Append new questions to data.json.
        with open('data.json') as json_file:
            file_data = json.load(json_file)
            temp = file_data['question_pool']
            temp.append(question_data)
        write_json(file_data, 'data.json')

        # Ask user if they would like to enter another question / answer.
        selection = input("\nWould you like to add another question? (Y/N): ").upper()
    return selection

def review_question(selection):
    # Show review questions until user selects no.
    another = "Y"
    while selection != "N":
        index = random_question()
        answer = pool['question_pool'][index - 1]['right_answer']
        print(answer + ": " + pool['question_pool'][index - 1]['answers'][answer])
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
    write_json(file_data, 'data.json')

def reset_attempts():
    with open('data.json') as json_file:
        file_data = json.load(json_file)
        temp = file_data['question_pool']
        length = len(temp)
        for x in range(length):
            temp[x]['cr_attempts'] = 0
            temp[x]['in_attempts'] = 0
            file_data['last_index'] = 0
    write_json(file_data, 'data.json')

def practice_quiz(selection):
    total_num = 0
    num_wrong = 0
    # Continue picking random questions to quiz the user enters the answer X.
    while selection != "X":
        index = random_question()
        answer = pool['question_pool'][index - 1]['right_answer']
        for x in range(4):
            letter = answer_letter[x]
            print(letter + ": " + pool['question_pool'][index - 1]['answers'][letter])
        entry = input("\nWhat is the correct answer? or e(X)it: ").upper()
        selection = entry
        if entry == answer:
            print(bcolors.BOLD + "Correct!" + bcolors.ENDC)
            result = "C"
            total_num += 1
        elif entry == "X":
            continue
        else:
            print(bcolors.WARNING + "\nSorry the correct answer was %s." % (answer) + bcolors.ENDC)
            result = "I"
            total_num += 1
            num_wrong += 1
        update_attempt(result, index)

    # Show user score after they hit X.
    final = "\nYou answered a total of %d questions and your score was " % (total_num)
    if num_wrong != 0:
        score = (((total_num - num_wrong) / total_num) * 100)
        if score <= 73:
            print(final + bcolors.FAIL + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
        elif score <= 90:
            print(final + bcolors.WARNING + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
        else:
            print(final + bcolors.BOLD + "{:.1f}".format(score) + "%" + bcolors.ENDC + "!")
    else:
        print(final + bcolors.BOLD + "100%" + bcolors.ENDC + "!") 

def load_pool():
    with open('data.json', 'r') as f:
        pool = json.load(f)
        return pool

# Load questions file.
pool = load_pool()

# Ask user if they want to add questions / answers. Print header.
print(pool['exam_title'])
print(pool['exam_description'])
print("Question ID's Show [Correct|Incorrect] Attempts\n")
selection = input("(A)dd Question, (R)eview, (P)ractice, (E)xam Mode, (S)eries Mode, or E(X)it?: ").upper()
if selection == "A":
    selection = add_question(selection)
    pool = load_pool()

# Get length of question pool.
pool_len = len(pool['question_pool'])
print("\nThere are %d total questions in the pool." % (pool_len))

if selection == "N":
    selection = input("\n(R)eview, (P)ractice, (S)eries Mode, or E(X)it?: ").upper()

if selection == "R":
    review_question(selection)

if selection == "P":
    practice_quiz(selection)

if selection == "S":
    series_mode(selection)

if selection == "E":
    exam_mode(selection)

if selection == "C":
    print(bcolors.WARNING + "\nAre you sure? This will reset all correct / incorrect attempts!!!" + bcolors.ENDC) 
    selection = input("\n(Y/N?): ").upper()
    if selection == "Y":
        reset_attempts()
    else:
        pass

else:
    pass
