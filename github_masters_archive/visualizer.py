#!/usr/bin/env python

# Gareth David Hunt
#

# Description: A gridworld visualiser, for use with gridworld.py generated worlds

import argparse
import random
import subprocess


import pickle
import os.path

import numpy as np

import cv2
from cv_bridge import CvBridge

from gridworld import GridWorld
from gridworld import GridSquare


def display(self, gridworld):
    print("Displaying...")
    image = np.zeros((gridworld.length * 100, gridworld.width * 100, 3), np.uint8)
    image[:, :] = (255, 255, 255)
    print("Drawing Grid")
    for i in range(0, gridworld.length):
        for k in range(0, gridworld.width):
            square = gridworld.get_grid_square(i, k)
            danger = square.get_danger()
            danger_val = int(
                (danger / 0.35) * 255.0
            )  # 0.35 is the maximum allowed danger value, so we set the square solid red if it is 0.35
        x_start = i * 100
        x_end = x_start + 99
        y_start = k * 100
        y_end = y_start + 99
        image[x_start + 10 : x_end - 10, y_start + 10 : y_end - 10] = (
            0,
            0,
            danger_val,
        )
    print("Drawing goal")
    start_x = gridworld.goal_x * 100
    end_x = start_x + 99
    start_y = gridworld.goal_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (0, 255, 0)
    print("Drawing start")
    start_x = gridworld.start_x * 100
    end_x = start_x + 99
    start_y = gridworld.start_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (255, 0, 0)
    print("Drawing current location")
    start_x = gridworld.current_x * 100
    end_x = start_x + 99
    start_y = gridworld.current_y * 100
    end_y = start_y + 99
    image[start_x + 40 : end_x - 40, start_y + 40 : end_y - 40] = (255, 255, 0)
    cv2.imshow("Gridworld", image)
    cv2.waitKey(0)


def pm_map(self, gridworld):
    print("Displaying...")
    image = np.zeros((gridworld.length * 100, gridworld.width * 100, 3), np.uint8)
    image[:, :] = (255, 255, 255)
    print("Drawing Grid")

    for i in range(0, gridworld.length):
        for k in range(0, gridworld.width):
            square = gridworld.get_grid_square(i, k)
            pm = square.movement_prob
            pm_val = int((float(pm) / 10.0) * 255.0)
            x_start = i * 100
            x_end = x_start + 99
            y_start = k * 100
            y_end = y_start + 99
            image[x_start + 10 : x_end - 10, y_start + 10 : y_end - 10] = (
                pm_val / 2,
                pm_val,
                0,
            )
    print("Drawing goal")
    start_x = gridworld.goal_x * 100
    end_x = start_x + 99
    start_y = gridworld.goal_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (0, 255, 0)
    print("Drawing start")
    start_x = gridworld.start_x * 100
    end_x = start_x + 99
    start_y = gridworld.start_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (255, 0, 0)
    print("Drawing current location")
    start_x = gridworld.start_x * 100
    end_x = start_x + 99
    start_y = gridworld.start_y * 100
    end_y = start_y + 99
    image[start_x + 40 : end_x - 40, start_y + 40 : end_y - 40] = (255, 255, 0)
    cv2.imshow("PM Values", image)
    cv2.waitKey(0)


def heatmap(self, gridworld, heatmap):
    print("Generating heatmap")
    image = np.zeros((gridworld.length * 100, gridworld.width * 100, 3), np.uint8)
    image[:, :] = (255, 255, 255)
    print("Drawing Grid")
    max_visits = np.amax(heatmap)
    for i in range(0, gridworld.length):
        for k in range(0, gridworld.width):
            visit_val = int((float(heatmap[i][k]) / max_visits) * 255.0)
            x_start = i * 100
            x_end = x_start + 99
            y_start = k * 100
            y_end = y_start + 99
            image[x_start + 10 : x_end - 10, y_start + 10 : y_end - 10] = (
                0,
                visit_val,
                visit_val,
            )
    print("Drawing goal")
    start_x = gridworld.goal_x * 100
    end_x = start_x + 99
    start_y = gridworld.goal_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (0, 255, 0)
    print("Drawing start")
    start_x = gridworld.start_x * 100
    end_x = start_x + 99
    start_y = gridworld.start_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (255, 0, 0)
    cv2.imshow("Heatmap", image)
    cv2.waitKey(0)


def runpath(self, gridworld, runpath):
    print("Runpath gen...")
    image = np.zeros((gridworld.length * 100, gridworld.width * 100, 3), np.uint8)
    image[:, :] = (0, 0, 0)
    print("Drawing Grid")
    for curr in runpath:
        path_val = 255.0
        x_start = curr[0] * 100
        x_end = x_start + 99
        y_start = curr[1] * 100
        y_end = y_start + 99
        image[x_start + 10 : x_end - 10, y_start + 10 : y_end - 10] = (
            path_val,
            path_val,
            path_val,
        )

    print("Drawing goal")
    start_x = gridworld.goal_x * 100
    end_x = start_x + 99
    start_y = gridworld.goal_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (0, 255, 0)
    print("Drawing start")
    start_x = gridworld.start_x * 100
    end_x = start_x + 99
    start_y = gridworld.start_y * 100
    end_y = start_y + 99
    image[start_x + 30 : end_x - 30, start_y + 30 : end_y - 30] = (255, 0, 0)
    cv2.imshow("Runpath", image)
    cv2.waitKey(0)


def load_gridworld(gridworld, filename):
    if os.path.isfile(filename):
        f = open(filename, "rb")
        to_load = pickle.load(f)
    else:
        print("ERROR: FAILED TO LOAD")
    return to_load


def load_other(filename):
    if os.path.isfile(filename):
        f = open(filename, "rb")
        to_load = pickle.load(f)
    else:
        print("ERROR: FAILED TO LOAD")
    return to_load


def main():
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="path to the save file")
    parser.add_argument("-H", "--heatmap", help="path to the heatmap file (optional)")
    parser.add_argument(
        "-rp", "--runpath", help="path to the runpath save file (optional)"
    )
    parser.add_argument(
        "-pm",
        "--movementprobabilities",
        help="movement probability map. 0 = no movement probability map, 1 = movement probability map",
    )
    args = vars(parser.parse_args())
    random.seed(None)
    filename = args["filename"]
    heatmap_file = args["heatmap"]
    runpath_file = args["runpath"]
    pm_arg = args["movementprobabilities"]
    if not filename:
        print("No file location provided, cannot display")
    else:
        print("Attempting to Load file...")
        gridworld = GridWorld(10, 10)
        gridworld = load_gridworld(gridworld, filename)
        display(gridworld)
        if heatmap_file:
            heatmap_data = load_other(heatmap_file)
            heatmap(gridworld, heatmap_data)
        if not runpath_file:
            runpath_data = load_other(runpath_file)
            runpath(gridworld, runpath_data)
        if pm_arg != None:
            if int(pm_arg) == 1:
                pm_map(gridworld)


if __name__ == "__main__":
    main()
