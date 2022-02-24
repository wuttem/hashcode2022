#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import glob
import math
import time

from collections import defaultdict
import itertools
import pandas as pd


MAX_RUNTIME = 10
max_days, max_best_before, max_score = None


class Contributor:
    __slots__ = ['name', 'skill_count', "skills"]

    def __init__(self, name, skills):
        self.name = name
        self.skill_count = len(skills)
        self.skills = skills

    def __repr__(self):
        return f'Contributor(name={self.name}, skill_count={self.skill_count})'


class Project:
    __slots__ = ['name', 'days', "score", "best_before", "skills", "roles"]

    def __init__(self, name, days, score, best_before, skills):
        self.name = name
        self.days = days
        self.score = score
        self.best_before = best_before
        self.skills = skills
        self.roles = len(skills)

    def __repr__(self):
        return f'Project(name={self.name}, days={self.days}, score={self.score}, best_before={self.best_before}, roles={self.roles})'

    def value(self, current_day=0):
        global max_days, max_best_before, max_score
        if max_days is not None:
            days_weight = float(self.days)/float(max_days)
        else:
            days_weight = float(self.days)

        if self.best_before < current_day + self.days:
            best_before_weight = 1
        else:
            best_before_weight = 0
        #     best_before_weight = float(self.best_before - current_day)/float(max_best_before)
        # else:
        #     days_weight = float(self.best_before)

        if max_score is not None:
            score_weight = float(self.score)/float(max_score)
        else:
            score_weight = float(self.score)


class ExecutedProject:
    def __init__(self, name, contributors):
        self.name = name
        self.contributors = contributors

    def print_sol(self, ofile):
        print(self.name, file=ofile)
        assert len(self.contributors) >= 1
        print(" ".join(self.contributors), file=ofile)

def to_table_format(INPUT_FILE, contributors, projects):
    skills = [list(contributor.skills.keys()) for contributor in contributors]
    all_skills = set(list(itertools.chain(*skills)))
    contributor_skill_dict = {}
    contributor_skill_dict["name"] = []
    for skill in all_skills:
        contributor_skill_dict[skill] = []
    for c in contributors:
        contributor_skill_dict["name"].append(c.name)
        for skill in all_skills:
            contributor_skill_dict[skill].append(c.skills.get(skill,0))

    project_skill_dict = {}
    project_skill_dict["name"] = []
    project_skill_dict["score"] = []
    project_skill_dict["best_before"] = []
    project_skill_dict["roles"] = []
    for skill in all_skills:
        project_skill_dict[skill] = []
    for p in projects:
        project_skill_dict["name"].append(p.name)
        project_skill_dict["score"].append(p.score)
        project_skill_dict["roles"].append(p.roles)
        project_skill_dict["best_before"].append(p.best_before)
        for skill in all_skills:
            project_skill_dict[skill].append(p.skills.get(skill, 0))

    
    project_skill_dict
    contributor_skill_dict
    pandas_projects = pd.DataFrame(project_skill_dict)
    pandas_contributors = pd.DataFrame(contributor_skill_dict)

    pandas_projects.to_csv(INPUT_FILE + "_projects.csv")
    pandas_contributors.to_csv(INPUT_FILE + "_contributors.csv")
    print(pandas_projects)
    print(pandas_contributors)



def project_value(p)


def solve(INPUT_FILE):
    # READ INPUT FILE
    with open(INPUT_FILE, "r") as f:
        first_line = f.readline().strip()
        num_contr, num_pro = map(int, first_line.split(" "))

        print("Loading: {}".format(INPUT_FILE))
        print("Contributors:", num_contr)
        print("Projects:", num_pro)

        contributors = []
        projects = []

        # Contributors
        for _ in range(num_contr):
            name, skill_count = f.readline().strip().split(" ")
            print(name)
            skills = {}
            for _ in range(int(skill_count)):
                sk, level = f.readline().strip().split(" ")
                skills[sk] = level
            contributors.append(Contributor(name, skills))

        # Projects
        for _ in range(num_pro):
            name, days, score, best_before, roles = f.readline().strip().split(" ")
            print(name)
            skills = {}
            for _ in range(int(roles)):
                sk, level = f.readline().strip().split(" ")
                skills[sk] = level
            projects.append(Project(name, int(days), int(score), int(best_before), skills))

        # print(contributors)
        # print(projects)
        to_table_format(INPUT_FILE, contributors, projects)


    executed_projects = []
    remaining_projects = projects
    t1 = time.time()
    day = 0


    while remaining_projects and time.time() < t1 + MAX_RUNTIME:



        day += 1




    # Print Result to File
    with open(INPUT_FILE.replace(".txt", ".out"), "w") as of:
        print(len(executed_projects), file=of)
        for proj in executed_projects:
            proj.print_sol(of)



if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        files = args[1:]
    else:
        files = glob.glob("*.txt")

    for inputfile in files:
        if "requirements.txt" in inputfile:
            continue
        if ".out" in inputfile:
            continue
        solve(inputfile)
