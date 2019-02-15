Name_file = "/Users/liza/problem_robot.pddl";
import re

obj = []


def get_part(index, file):
    with open(file) as infile:
        lines = [line.strip() for line in infile]
    end = index
    brackets = 1
    for i in range(index + 1, len(lines)):
        end += 1
        for j in range(len(lines[i])):
            if lines[i][j] == '(':
                brackets += 1
            elif lines[i][j] == ')':
                brackets -= 1
        if brackets == 0:
            break;
    return lines[index:end + 1]


def get_objects(text):
    objects = []
    for i in range(1, len(text) - 1):
        objects.append(text[i])
    for i in range(len(objects)):
        objects[i] = re.sub('[)(]', '', objects[i])
    return objects


def get_init(text):
    init = []
    for i in range(1, len(text) - 1):
        init.append(text[i])
    for i in range(len(init)):
        init[i] = re.sub('[)(]', '', init[i])
    return init


class Problem_object:
    def __init__(self, object, init, goal):
        self.object = object
        self.init = init
        self.goal = goal

def problem_parser2(Name_file):
    obj, inits, goals = [], [], []
    Name_problem, Name_domain, goal = [], [], []
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]
    lines[0] = re.sub('[)(-]', '', lines[0])
    lines[1] = re.sub('[)(-]', '', lines[1])
    Name_problem = lines[0].split()
    Name_problem = Name_problem[2:]
    Name_domain = lines[1].split()
    Name_domain = Name_domain[1:]
    for i in range(len(lines)):
        if (lines[i].find('(:objects') != -1):
            obj = get_objects(get_part(i, Name_file))
    for i in range(len(lines)):
        if (lines[i].find('(:init') != -1):
            inits = get_init(get_part(i, Name_file))
    for i in range(len(lines)):
        if (lines[i].find('(:goal') != -1):
            lines[i + 1] = re.sub('[)(-]', '', lines[i + 1])
            goal = lines[i + 1].split()
    objects = Problem_object(obj, inits, goal)
    return objects


def problem_parser(Name_file):
    obj, inits, goals = [], [], []
    Name_problem, Name_domain, goal = [], [], []
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]
    lines[0] = re.sub('[)(-]', '', lines[0])
    lines[1] = re.sub('[)(-]', '', lines[1])
    Name_problem = lines[0].split()
    Name_problem = Name_problem[2:]
    Name_domain = lines[1].split()
    Name_domain = Name_domain[1:]
    print('Name_problem:')
    print(Name_problem)
    print('Domain_problem:')
    print(Name_domain)
    for i in range(len(lines)):
        if (lines[i].find('(:objects') != -1):
            obj = get_objects(get_part(i, Name_file))
    for i in range(len(lines)):
        if (lines[i].find('(:init') != -1):
            inits = get_init(get_part(i, Name_file))
    for i in range(len(lines)):
        if (lines[i].find('(:goal') != -1):
            lines[i + 1] = re.sub('[)(-]', '', lines[i + 1])
            goal = lines[i + 1].split()
    objects = Problem_object(obj, inits, goal)
    print(objects.object)
    print(objects.init)
    print(objects.goal)
    return objects

#problem_parser(Name_file);
