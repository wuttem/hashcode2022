#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import glob
import math
import time

from collections import defaultdict
import itertools


MAX_RUNTIME = 60
max_days = 0
max_best_before = 0
max_score = 0


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

        if self.best_before > (current_day + self.days):
            score = self.score
        else:
            score = self.score - ((current_day + self.days) - self.best_before)

        max_level = 0
        for skill in self.skills:
            if skill[1] > max_level:
                max_level = skill[1]
        if max_level <= 7:
            score = score * 10

        score_per_day = score/self.days

        # todo add max level here
            

        return score_per_day


class ExecutedProject:
    def __init__(self, name, contributors):
        self.name = name
        self.contributors = contributors

    def print_sol(self, ofile):
        print(self.name, file=ofile)
        assert len(self.contributors) >= 1
        print(" ".join(self.contributors), file=ofile)


def filter_projects_by_skill(projects):
    filtered_projects = []
    for p in projects:
        print(p.name)
        print(p.skills)
        max_level = 0
        for skill in p.skills:
            if skill[1] > max_level:
                max_level = skill[1]
        print(max_level)
        if max_level <= 7:
            filtered_projects.append(p)
    return filtered_projects


def solve(INPUT_FILE):
    global max_days, max_best_before, max_score
    # READ INPUT FILE
    with open(INPUT_FILE, "r") as f:
        first_line = f.readline().strip()
        num_contr, num_pro = map(int, first_line.split(" "))

        print("Loading: {}".format(INPUT_FILE))
        print("Contributors:", num_contr)
        print("Projects:", num_pro)

        contributors = {}
        projects = []
        people_by_skill = defaultdict(dict)

        # Contributors
        for _ in range(num_contr):
            name, skill_count = f.readline().strip().split(" ")
            print(name)
            skills = {}
            for _ in range(int(skill_count)):
                sk, level = f.readline().strip().split(" ")
                skills[sk] = int(level)
                people_by_skill[sk][name] = int(level)
            contributors[name] = Contributor(name, skills)

        # Projects
        for _ in range(num_pro):
            name, days, score, best_before, roles = f.readline().strip().split(" ")
            print(name)
            skills = []
            for _ in range(int(roles)):
                sk, level = f.readline().strip().split(" ")
                skills.append((sk, int(level)))
            # normalize
            max_days = max(max_days, int(days))
            max_best_before = max(max_best_before, int(best_before))
            max_score = max(max_score, int(score))
            projects.append(Project(name, int(days), int(score), int(best_before), skills))

        # print(contributors)
        # print(projects)

    executed_projects = []

    # projects = filter_projects_by_skill(projects)

    remaining_projects = [x for x in projects]
    people_available = set([c.name for c in contributors.values()])
    all_people = set(contributors.keys())
    people_become_available = defaultdict(list)
    t1 = time.time()
    day = 0

    while remaining_projects and time.time() < t1 + MAX_RUNTIME:
        # find out whos available
        a = people_become_available[day]
        if a:
            people_available.update(a)

        # sort projects
        remaining_projects.sort(key=lambda l: l.value(day))

        for p in list(remaining_projects):
            skills_needed = p.skills

            print(p.name)
            # Team (without mentees)
            team = [None] * len(skills_needed)
            for i, (sk, level) in enumerate(skills_needed):
                print(sk)
                have_skill = [c for c,s in people_by_skill[sk].items() if s >= level]
                possible = people_available.intersection(have_skill)
                # take someone!
                if len(possible) > 0:
                    c = possible.pop() # maybe take a random person
                    team[i] = c
                    people_available.remove(c)

            # find out the skills we have in the team
            highest_skills_wo = [None] * len(skills_needed)
            for current_pos, _ in enumerate(team):
                highest_skill = defaultdict(int)
                for c in list(team[0:current_pos] + team[current_pos+1:]):
                    if c is None:
                        continue
                    contributer = contributors[c]
                    for sk, level in contributer.skills.items():
                        highest_skill[sk] = max(level, highest_skill[sk])
                highest_skills_wo[current_pos] = highest_skill
            #print(highest_skills_wo)

            # Team (mentees)
            for current_pos, (sk, level) in enumerate(skills_needed):
                have_skill = [c for c,s in people_by_skill[sk].items() if s >= level]
                if level == 1:
                    can_be_mentee = all_people - set(have_skill)
                else:
                    can_be_mentee = [c for c,s in people_by_skill[sk].items() if s == level-1]
                possible_mentees = people_available.intersection(can_be_mentee)
                mentor_levels = highest_skills_wo[current_pos]
                if mentor_levels[sk] >= level and len(possible_mentees) > 0:
                    # we can use the mentee
                    if team[current_pos] is None:
                        # free for mentee anyway
                        m = possible_mentees.pop()
                        team[current_pos] = m
                        people_available.remove(m)
                    else:
                        # there is already someone here ...
                        m = possible_mentees.pop()
                        people_available.add(team[current_pos])
                        team[current_pos] = m
                        people_available.remove(m)
                        # because we can only use one mentee we break here
                        break

            if not None in team:
                # we have a match
                print(team)
                for c in team:
                    people_become_available[day+p.days].append(c)
                executed_projects.append(ExecutedProject(p.name, team))
                remaining_projects.remove(p)
            else:
                # give them back
                people_available.update(team)

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
