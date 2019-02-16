import parser as pr
import problem as prob
import re
from itertools import combinations

answer = []

def grounding(domain_robot, problem_robot):
    pars = pr.parser2(domain_robot)
    parser = prob.problem_parser2(problem_robot)
    for i in pars.action:
        i.parameters = pop(i.parameters)
        ground_action(i.name, i.parameters, dict1(parser.object))
    for i in pars.method:
        i.parameters = pop(i.parameters)
        ground_action(i.name, i.parameters, dict1(parser.object))
        
    return answer


def dict1(list):
    obj = dict()
    for i in range(len(list)):
        if list[i].find('-') != -1:
            index = list[i].find('-')
            list1 = list[i][:index - 1]
            list2 = list[i][index + 2:]
            if obj.get(list2) == None:
                obj[list2] = []
                obj[list2].append(list1)
            else:
                obj[list2].append(list1)
    return obj

def ground_action(name, act, dict):
    room = 0
    door = 0
    pack = 0
    l1, l2, l3 = [], [], []
    for i in range(len(act)):
        if act[i] == 'Room':
            room += 1
        elif act[i] == 'Room_door':
            door += 1
        elif act[i] == 'Package':
            pack += 1
    l1 =list(combinations(dict['Package'], pack))
    l2 =list(combinations(dict['Room'], room))
    l3 = list(combinations(dict['Room_door'], door))
    for i in l1:
        for j in l2:
            for k in l3:
                print(*name, *(i + j + k + ('r',)))
                answer.append((name, ) + (i + j + k + ('r',)))


def pop(list):
    param = []
    for i in range(len(list)):
        if list[i].find('?') == -1:
            param.append(list[i])
    return param


#grounding("/Users/liza/domain_robot.pddl", "/Users/liza/problem_robot.pddl")
