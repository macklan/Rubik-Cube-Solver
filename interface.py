'''
interface.py

Macklan Badger
macklanb
CSE 415
Project: Option 3

Usage: python3 interface.py

Prompts the user for input for the following
 - Number of rotations for initial state
 - Number of q learning iterations
 - Discount
 - Learning rate

Uses the State and MDP class to execute Q Learning of a 2x2x2 rubik cube

'''

from q_learn import *
from rubik_cube import *

directions = ['Front', 'Down', 'Back', 'Up', 'Left', 'Right']
sides = ['f', 'd', 'b', 'u', 'l', 'r']

OPERATORS = [Operator("Rotate " + str(directions[i]) + " 180 degrees",
                      lambda s, dir1=sides[i]: s.can_move(dir1),
                      lambda s, dir1=sides[i]: s.move(dir1))
             for i in range(len(sides))]

ACTIONS = [op.name for op in OPERATORS]

mix_choices = {
    1: 1,
    2: 5,
    3: 10,
    4: 50,
    5: 100
}

discount_choices = {
    1: 1.0,
    2: 0.99,
    3: 0.9,
    4: 0.5
}

learning_choices = {
    1: 0.1,
    2: 0.2,
    3: "Other"
}

iteration_choices = {
    1: 1,
    2: 5,
    3: 10,
    4: 15,
    5: 20,
    6: 25
}

def printOptions(choices):
    for choice in choices:
        print(choice, ":", choices[choice])

print("Q Learning Menu:")
print("How many random mixes should be done to the Rubik Cube?")
printOptions(mix_choices)
mix_choice = input("")

if mix_choice is "":
    mix_choice = 3
else:
    mix_choice = int(mix_choice)
print("\n")

print("How many iterations of Q Learning?")
printOptions(iteration_choices)
iteration_choice = input("")

if iteration_choice is "":
    iteration_choice = 5
else:
    iteration_choice = int(iteration_choice)
print("\n")

print("What should the discount be?")
printOptions(discount_choices)
discount_choice = input("")

if discount_choice is "":
    discount_choice = 1
else:
    discount_choice = int(discount_choice)
print("\n")

print("What should be the learning rate be?")
printOptions(learning_choices)
learning_choice = input("")

if learning_choice is "":
    learning_choice = 2
else:
    learning_choice = int(learning_choice)
print("\n")

num_mixes = mix_choices[mix_choice]
num_iterations = iteration_choices[iteration_choice]
num_discount = discount_choices[discount_choice]

if learning_choice is 3:
    print("What is the custom learning rate?")
    num_learning = float(input(""))
    print("\n")
else:
    num_learning = learning_choices[learning_choice]

print("\n")

state = State()
state = state.mix_up(num_mixes)
print("Initial State:")
print(state)
print("Possible Actions:")
print(ACTIONS)

print("\n")

mdp = MDP(state, ACTIONS, OPERATORS)
mdp.Q_Learning(num_iterations, num_discount, num_discount)
policy = mdp.policies()
print("Best first Action for initial state is:", policy[state])
print("Q Value for initial state and the best first action:", mdp.q_values[(state, policy[state])])

