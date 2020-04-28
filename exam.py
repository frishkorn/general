#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.0.2
# ------------------------
import json

# Ask user if they want to add questions / answers.
selection = input("Would you like to enter new questions? (Y/N): ")
if selection == "Y":
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
    data = {}
    data = {'question':question,'answers':[{'A':answerList[0],'B':answerList[1],'C':answerList[2],'D':answerList[3]}],'right_answer':correct}
    with open('question_file.gef', 'a+') as outFile:
        json.dump(data, outFile)

        print(json.dumps(data, sort_keys=True, indent=4))

else:
    print("Saw N")


# Ask user if they would like to enter another question / answer.

# Load questions file.

# Pick a random question and ask user to answer it.
