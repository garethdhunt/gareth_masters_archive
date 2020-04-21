#!/usr/bin/env python

# Gareth David Hunt
#

# Description: A Risk sensitive learning system


import random
import math

import pickle
import os.path


import numpy as np
import logging


from copy import copy

import gridworld

import dist_state


class Learner(object):
    state_list = []
    gridworld = gridworld.GridWorld(10, 10)
    action_list = []
    K_exploit = 1.0
    discount_factor = 0.9
    learning_rate = 0.1

    def __init__(self, gridworld):
        print("Initializing learner")
        self.gridworld = gridworld

    def learn(self, gridworld, x, y, action):
        print("Learning...")
        if gridworld.success:
            base_reward = 31
        elif gridworld.failure:
            base_reward = 1
        else:
            base_reward = 16
        next_states = identify_action_values(
            self.state_list, gridworld, gridworld.x, gridworld.y
        )
        next_max = np.max(next_states)
        new_reward = base_reward + self.discount_factor * next_max

        dist_state_no = find_state(self.state_list, x, y, action)
        dist_state = state_list[dist_state_no]
        dist_state.visits = dist_state.visits + 1
        if gridworld.failure:
            dist_state.failures = dist_state.failures + 1

        # Q Value
        dist_state.pos_estimate = (
            1.0 - self.learning_rate
        ) * dist_state.pos_estimate + self.learning_rate * new_reward
        # Proportion of failures
        dist_state.risk_estimate = 10000.0 * (
            float(dist_state.failures) / float(dist_state.visits)
        )

        # The positive certainty is determined by a sigmoid function
        pos_k = 0.005
        pos_xzero = 500
        dist_state.pos_certainty = 1 / (
            1 + math.exp(-pos_k * (dist_state.visits - pos_xzero))
        )

        # The  risk certainty is determined by the higher of two Sigmoids
        # Accounting for the possibility that the state is so safe it never encounters failures
        neg_k = 0.01
        neg_xzero = 10
        danger_conf = 1 / (1 + math.exp(-neg_k * (dist_state.failures - neg_xzero)))
        skep_k = 0.0025
        skep_xzero = 1000
        skep_conf = 1 / (1 + math.exp(-skep_k * (dist_state.visits - skep_xzero)))
        dist_state.neg_confidence = max(danger_conf, skep_conf)

        self.state_list[dist_state_no] = dist_state
        return state_list

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def choose_novel_action(self):
        print("Choosing novel action")
        best_action = 0
        curr_state = self.action_list[0]
        reward_list = [0, 0, 0, 0]
        for i in self.action_list:
            curr_state = i
            curr_reward = (
                (1.1 - curr_state.neg_confidence)
                + (1.1 - curr_state.pos_certainty)
                + (1.1 - curr_state.risk_certainty)
                * self.K_explore
                * curr_state.risk_estimate
                + (1.1 - curr_state.pos_certainty) * curr_state.pos_estimate
            )
            reward_list[action_num] = curr_reward

        probabilities = self.softmax(reward_list)

        best_action = -1
        i = 0
        found_action = False
        rand_action = random.random()
        while (i < 4) and (found_action == False):  # softmax action selection
            if rand_action < probabilities[i]:
                best_action = i
                found_action = True
            rand_action = rand_action - probabilities[i]
            i = i + 1
        if (best_action < 0) or (best_action > 3):
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            print("Error: selector is choosing out of bounds action")
            print("Action: ", best_action)
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            raise ValueError("An invalid action was chosen")
        return best_action

    def choose_best_action(self):
        print("Choosing best action")
        best_action = 0
        reward_list = [0, 0, 0, 0]
        for i in self.action_list:
            curr_state = i
            curr_reward = (
                curr_state.neg_confidence
                * curr_state.pos_certainty
                * curr_state.pos_estimate
                * self.K_exploit
            ) / (curr_state.risk_estimate + 1.0)
            reward_list[action_num] = curr_reward
        probabilities = self.softmax(reward_list)
        best_action = -1
        i = 0
        found_action = False
        rand_action = random.random()
        while (i < 4) and (found_action == False):  # softmax action selection
            if rand_action < probabilities[i]:
                best_action = i
                found_action = True
            rand_action = rand_action - probabilities[i]
            i = i + 1

        if (best_action < 0) or (best_action > 3):
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            print("Error: selector is choosing out of bounds action")
            print("Action: ", best_action)
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            raise ValueError("An invalid action was chosen")
        return best_action

    def choose_action(self, mode):
        if mode == 0:
            action = self.choose_novel_action()
        elif mode == 1:
            action = self.choose_best_action()
        else:
            print("Error: Invalid action mode specified (choose novel (0) or best (1))")
        return action
