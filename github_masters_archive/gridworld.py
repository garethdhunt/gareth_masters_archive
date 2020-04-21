#!/usr/bin/env python

# Gareth David Hunt
#

# Description: A simple gridworld environment with risks

import random
import struct

import math

import pickle
import os.path

import Queue

import numpy as np


class GridSquare:
    x = 1
    y = 1
    movement_prob = 1
    danger_percentage = 0.1
    rubble = 1
    water = 1
    pits = 1

    def __init__(self):
        self.movement_prob = random.randint(1, 10)
        self.danger_percentage = random.uniform(0.03, 0.35)

    def set_danger(self, danger):
        self.danger_percentage = danger

    def get_danger(self):
        return self.danger_percentage

    def fail_check(self):
        randnum = random.random()
        if randnum > actual_danger:
            fail = False
        else:
            fail = True
        return fail

    def successful_move(self):
        randnum = random.randint(0, 10)
        if randnum <= self.movement_prob:
            success_move = True
        else:
            success_move = False
        return success_move

    def set_pm(self, new_pm):
        self.movement_prob = new_pm


class GridWorld:
    length = 10
    width = 10
    start_x = 9
    start_y = 9
    current_x = 9
    current_y = 9
    goal_x = 1
    goal_y = 1
    success = False
    failure = False
    last_x = 9
    last_y = 9
    absolute_zero = True
    gridworld = []

    def __init__(self, x_size, y_size):
        print("Initializing gridworld")
        if x_size < 6:
            print("Length must be at 6")
            x_size = 6
        if y_size < 6:
            print("Width must be at least 6")
            y_size = 6
        self.start_x = random.randint(0, x_size - 1)
        self.start_y = random.randint(0, y_size - 1)
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.last_x = self.current_x
        self.last_y = self.current_y
        self.goal_x = random.randint(0, x_size - 1)
        self.goal_y = random.randint(0, y_size - 1)
        while (abs(self.goal_x - self.start_x) < 3) and (
            abs(self.goal_y - self.start_y) < 3
        ):  # ensure the start and goal aren't on top of each other
            self.goal_x = random.randint(0, x_size - 1)
            self.goal_y = random.randint(0, y_size - 1)
        self.gridworld = [[GridSquare() for x in range(x_size)] for y in range(y_size)]
        self.length = x_size
        self.width = y_size
        for i in range(0, x_size):
            for k in range(0, y_size):
                self.gridworld[i][k].x = i
                self.gridworld[i][k].y = k

    def move(self, action):
        result = 0  # 1 means success, -1 means failure
        self.last_x = self.current_x
        self.last_y = self.current_y
        if action == 0:
            print("Action: UP")
            self.current_x = self.current_x - 1
            if self.current_x < 0:
                self.current_x = 0
        elif action == 1:
            print("Action: RIGHT")
            self.current_y = self.current_y - 1
            if self.current_y < 0:
                self.current_y = 0
        elif action == 2:
            print("Action: DOWN")
            self.current_x = self.current_x + 1
            if self.current_x >= self.length:
                self.current_x = self.length - 1
        elif action == 3:
            print("Action: LEFT")
            self.current_y = self.current_y + 1
            if self.current_y >= self.width:
                self.current_y = self.width - 1
        else:
            print("!!!!!!!!!!!!!!!!!!!!")
            print("ERROR: invalid action")
            print("!!!!!!!!!!!!!!!!!!!!")
        print("Current location: ", self.current_x, ", ", self.current_y)
        if (self.current_y == self.goal_y) and (self.current_x == self.goal_x):
            self.success = True
            for i in range(1, 10):
                print("SUCCESS")
        else:
            current_grid = self.gridworld[self.current_x][self.current_y]
            self.failure = current_grid.fail_check()

    def finished(self):
        return self.success or self.failure

    def reset(self):
        self.success = False
        self.failure = False
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.last_x = self.start_x
        self.last_y = self.last_y

    def get_grid_square(self, x, y):
        return self.gridworld[x][y]

    def get_state(self):
        return self.gridworld[self.current_x][self.current_y]
