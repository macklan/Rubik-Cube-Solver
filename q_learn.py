'''
q_learn.py

Macklan Badger
macklanb
CSE 415
Project: Option 3

This is the MDP class that uses the State class from rubik_cube_180.py
This class does the Q learning

'''

from random import *
from rubik_cube_180 import *


class MDP:

    def __init__(self, initial_state, actions, operators):
        self.start_state = initial_state
        self.current_state = initial_state

        self.actions = actions
        self.operators = operators

        self.q_values = {}
        self.visits = {}
        self.feature_weights = [0, 0, 0, 0]
        self.states = set()

    # ** ACTION BASED METHODS **

    # Finds the best action for the given state
    # Uses the learning rate to determine whether or not to
    # use the get_best_action method
    def choose_action(self, s, learning_rate):
        if learning_rate < random():
            best_action = self.get_best_action(s)
            if best_action is None:
                return choice(self.actions)
            return best_action
        return choice(self.actions)

    # Returns the best possible action for the given state
    def get_best_action(self, s):
        best_action = None
        max_value = -100000
        for action in self.actions:
            if (s, action) in self.q_values:
                q = self.q_values[(s, action)]
                if q > max_value:
                    best_action = action
                    max_value = q
        return best_action

    # Takes the given action and executes it to the current state
    # Returns the new state
    def implement_action(self, action):
        for operator in self.operators:
            if operator.name == action:
                new_state = operator.apply(self.current_state)
                self.states.add(new_state)
                return new_state

    # ** Q LEARNING BASED METHODS **

    # Resets everything needed for Q Learning
    def reset(self):
        self.feature_weights = [0] * len(self.feature_weights)

        for s in self.states:
            num_visits = 0
            if s in self.visits:
                num_visits = self.visits[s]
            self.visits[s] = num_visits + 1

            for action in self.actions:
                self.q_values[(s, action)] = 0

    # The main method for this MDP
    # Does n iterations of Q Learning based on the user input
    # Uses the user input for the discount and original learning rate for Q Learning
    # Gives a little report for each iteration and overall report
    def Q_Learning(self, num_iterations, discount, learning_rate):
        self.states.add(self.start_state)
        self.reset()

        min_rotations = 10000000000000000

        for i in range(num_iterations):
            print("Q-Learning Iteration: ", i)
            self.current_state = self.start_state

            count = 0

            # while not goal_test(self.current_state):
            print(count)
            s = self.current_state
            action = self.choose_action(s, learning_rate)

            num_visits = 0
            if s in self.visits:
                num_visits = self.visits[s]
            self.visits[s] = num_visits + 1

            self.q_values[(s, action)] = self.Q(s, action, discount)
            count += 1

            min_rotations = min(min_rotations, count)

            print("Rotations to goal:", count)
            print("States expanded:", len(self.states))
            print("Feature Weights:", self.feature_weights)
            print("\n")

        print("Fewest number of rotations:", min_rotations)
        print("Total States Expanded:", len(self.states))

        max_weight = max(self.feature_weights)
        if self.feature_weights[0] is max_weight:
            print("Feature 0 was most effective the reinforcement learning")
        if self.feature_weights[1] is max_weight:
            print("Feature 1 was most effective the reinforcement learning")
        if self.feature_weights[2] is max_weight:
            print("Feature 2 was most effective the reinforcement learning")
        if self.feature_weights[3] is max_weight:
            print("Feature 3 was most effective the reinforcement learning")

        print("")

    # The Q function to generate the value for the give state and action
    # Also will update the weights for the features
    def Q(self, s, action, discount):

        learning_rate = self.learning_rate(s)

        s_prime = self.implement_action(action)
        self.current_state = s_prime

        action_prime = self.get_best_action(s_prime)

        q_prime = self.sarsa(s_prime)
        self.q_values[(s_prime, action_prime)] = q_prime
        q = self.sarsa(s)

        # Update the weights for the features based on delta calculated by the SARSA method
        delta = self.R(s, action, s_prime) + discount * q_prime - q

        for i in range(len(self.feature_weights)):
            feature_score = None
            if i is 0:
                feature_score = 1
            elif i is 1:
                feature_score = self.feature_1(s)
            elif i is 2:
                feature_score = self.feature_2(s)
            elif i is 3:
                feature_score = self.feature_3(s)

            self.feature_weights[i] = self.feature_weights[i] + learning_rate * delta * feature_score

        total_weight = sum(self.feature_weights)
        if total_weight != 0.0:
            self.feature_weights = [(w * 1.0) / total_weight for w in self.feature_weights]

        return q

    # Calculate the Q value using the SARSA method from the reading
    def sarsa(self, s):
        return self.feature_weights[0] * 1 + \
               self.feature_weights[1] * self.feature_1(s) + \
               self.feature_weights[2] * self.feature_2(s) + \
               self.feature_weights[3] * self.feature_3(s)

    def learning_rate(self, s):
        return 1 / self.visits[s]

    # ** FEATURE METHODS **

    # Find the total number of complete sides
    def feature_1(self, s):
        num_sides = 0
        cube = s.cube
        for i in range(6):
            index = i * 4

            if cube[index] == cube[index + 1] and \
                cube[index] == cube[index + 2] and \
                cube[index] == cube[index + 3]:
                num_sides += 1
        return num_sides

    # Find the total number of matching pairs
    # These pairs are only counted horizontally
    def feature_2(self, s):
        num_pairs = 0
        cube = s.cube
        for i in range(6):
            index = i * 4

            if cube[index] == cube[index + 1]:
                num_pairs += 1
            if cube[index + 2] == cube[index + 3]:
                num_pairs += 1
        return num_pairs

    # Check if there are any sides that are only 1 move away from being complete
    def feature_3(self, s):
        count = 0
        cube = s.cube

        if cube[0] == cube[1] and cube[1] == cube[8] and cube[8] == cube[9]:
            count += 1
        if cube[2] == cube[3] and cube[3] == cube[10] and cube[10] == cube[11]:
            count += 1
        if cube[4] == cube[5] and cube[5] == cube[14] and cube[14] == cube[15]:
            count += 1
        if cube[6] == cube[7] and cube[7] == cube[12] and cube[12] == cube[13]:
            count += 1
        if cube[16] == cube[17] and cube[17] == cube[22] and cube[22] == cube[23]:
            count += 1
        if cube[18] == cube[19] and cube[19] == cube[20] and cube[20] == cube[21]:
            count += 1

        return count

    # ** OTHER HELPERS **

    # Get the current policy for the states
    def policies(self):
        policy = {}
        for s in self.states:
            policy[s] = self.get_best_action(s)
        return policy

    # Reward function
    def R(self, s, a, sp):
        if goal_test(sp):
            return 10000
        else:
            return 0