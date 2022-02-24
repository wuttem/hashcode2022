#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import glob
import math

from collections import defaultdict


class SomeClass:
    __slots__ = ['int_a', 'int_b', "name", "time"]

    def __init__(self, int_a, int_b, name, time):
        self.int_a = int_a
        self.int_b = int_b
        self.name = name
        self.time = time

    def __repr__(self):
        return f'SomeClass(int_a={self.int_a}, int_b={self.int_b}, name={self.name}, time={self.time})'



class Result:
    def __init__(self, x):
        self.x = x

    def print_sol(self, ofile):
        print(self.x, file=ofile)
        # assert streets only once
        assert x


def solve(INPUT_FILE):

    # READ INPUT FILE
    with open(INPUT_FILE, "r") as f:
        first_line = f.readline().strip()
        list(f.readline().strip().split())

        solutions.append(Result(int_id, schedule, cycle_time, stw))

    with open(INPUT_FILE.replace(".txt", ".out"), "w") as of:
        print(len(solutions), file=of)
        for solution in solutions:
            solution.print_sol(of)


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        files = args[1:]
    else:
        files = glob.glob("*.txt")

    for inputfile in files:
        if "requirements.txt" in inputfile:
            continue
        solve(inputfile)
