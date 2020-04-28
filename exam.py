#!/usr/bin/env python3

# exam.py
# C. Frishkorn 04/28/2020
# version: 0.0.1
# ------------------------

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
    for y in answerList:
        print(y)
    print(correct)
else:
    print("Saw N")

# Create a questions file if it does not exist.
# with open('question_file.gef', 'a+') as outputFile:

# Ask user if they would like to enter another question / answer.


# Load questions file.

# Pick a random question and ask user to answer it.
