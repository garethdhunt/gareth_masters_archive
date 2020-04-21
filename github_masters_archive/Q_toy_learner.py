#!/usr/bin/env python

# Gareth David Hunt
#

# Description: Stanard Q learner for gridworld.py

import random
import subprocess
import pickle
import os.path


import numpy as np
import math
import copy


class Learner(object):
    learning_rate = 0.1  # alpha
    discount_factor = 0.5  # gamma
    epsilon = 0.1
    q_table = np.zeros([100, 4])
    visit_table = np.zeros([100, 4])
    neg_rewards = True

    def __init__(self):
        print "Initing Q Learner"
        random.seed(None)

    def set_q_table(self, new_q_table):
        self.q_table = new_q_table

    def learn(self, gridworld, x, y, action):
        state_loc = x + y * 10
        old_value = self.q_table[state_loc, action]
        next_x = gridworld.current_x
        next_y = gridworld.current_y
        next_state = next_x + 10 * next_y
        next_max = np.max(self.q_table[next_state])
        if gridworld.success:
            reward = 15
        elif (gridworld.failure) and (self.neg_rewards):
            reward = -15
        else:
            reward = 0
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (
            reward + self.discount_factor * next_max
        )
        self.q_table[state_loc, action] = new_value
        self.visit_table[state_loc, action] = self.visit_table[state_loc, action] + 1

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def choose_action(self, gridworld):  # softmax
        x = gridworld.current_x
        y = gridworld.current_y
        state_loc = x + y * 10
        directions = self.q_table[state_loc]
        probabilities = self.softmax(directions)
        action = -1
        i = 0
        found_action = False
        rand_action = random.random()  # Choose a random number between 0 and 1...
        while (i < 4) and (
            found_action == False
        ):  # ...which is used to pick the action with the probablity of the post softmax value
            if rand_action < probabilities[i]:
                action = i
                found_action = True
            rand_action = rand_action - probabilities[i]
            i = i + 1
        return action

    def choose_action_epsilon_greedy(self, gridworld):  # epsilon_greedy
        x = gridworld.current_x
        y = gridworld.current_y
        state_loc = x + y * 10
        if random.uniform(0, 1) < self.epsilon:
            action = random.randint(0, 3)
        else:
            action = np.argmax(self.q_table[state_loc])
        return action

    def export_policy(self, gridworld):
        state_list = np.zeros([10, 10])
        for i in range(0, 10):
            for k in range(0, 10):
                for j in range(0, 4):
                    direction = gridworld.test_move(i, k, j)
                    x = direction.x
                    y = direction.y
                    state_loc = i + 10 * k
                    state_list[x][y] = state_list[x][y] + self.q_table[state_loc, j]
        for i in range(0, 10):
            for j in range(0, 10):
                if gridworld.isGoalAdjacent(i, k):
                    state_list[i][k] = state_list[i][k] / 3
                else:
                    state_list[i][k] = state_list[i][k] / 4
        return state_list
