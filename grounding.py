import parser as pr
import problem as prob
import re
import itertools
from itertools import permutations, combinations
import copy

answer = []


class Action:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect



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

    return obj  # возвращает словарь тип-объект из проблемы



def dict2(dict1, param):
    dict3 = dict()
    for i in range(len(param)):
        for key, value in dict1.items():
            for q in range(len(dict1[key])):
                if dict1[key][q] == param[i]:
                    if dict3.get(key) == None:
                        dict3[key] = []
                        dict3[key].append(param[i])
                    else:
                        dict3[key].append(param[i])
    return dict3


def get_prec_effect(dict1, prec, dict2):
    pr = copy.deepcopy(prec)
    for i in range(len(pr)):
        pr[i] = pr[i].split()
        for k in range(len(pr[i])):
            for key in dict2.keys():
                for q in range(len(dict2[key])):
                    if pr[i][k] == dict2[key][q]:
                        pr[i][k] = dict1[key][q]
                        break
        pr[i] = ' '.join(pr[i])

    return pr


class Precend:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect


def grounding_precend(file, problem):
    list4 = []
    prec = pr.parser_precend(file)
    parser = prob.problem_parser2(problem)
    for i in prec:
        list4.append(ground_precend(i.name, i.parameters, dict1(parser.object), i.precond, i.effect))
    list4 = list(itertools.chain(*list4))
    return list4


def ground_precend(name, param, dict1, precond, effect):
    room, door, obj = 0, 0, 0
    answer = []
    dict3 = dict()
    for i in range(len(param)):
        if param[i] in dict1['Room']:
            room += 1
        if param[i] in dict1['Room_door']:
            door += 1
        if param[i] in dict1['Package']:
            obj += 1
    l1 = list(permutations(dict1['Package'], obj))
    l2 = list(permutations(dict1['Room'], room))
    l3 = list(permutations(dict1['Room_door'], door))
    for i in l1:
        for j in l2:
            for k in l3:
                parameters = list(j + k + ('r',) + i)
                dict3 = dict2(dict1, parameters)  # словарь тип - обьект для каждого заграундинного действия
                prec = get_prec_effect(dict3, precond, dict1)
                eff = get_prec_effect(dict3, effect, dict1)
                answer.append(Precend(name, parameters, prec, eff))
    return answer




grounding_precend("prec.pddl", "problem_robot.pddl")
def grounding_actions(domain_robot, problem_robot):
    pars = pr.parser2(domain_robot)
    list3 = []
    parser = prob.problem_parser2(problem_robot)
    for i in pars.action:
        i.parameters = pop(i.parameters)
        effect = i.effect
        prec = i.precondition
        for j in range(len(prec)):
            prec[j] = re.sub('[?]', '', prec[j])
        for k in range(len(effect)):
            effect[k] = re.sub('[?]', '', effect[k])
        list3.append(ground_action(i.name, i.parameters, i.param2, dict1(parser.object), prec, effect)) # param2 (домен)
    list3 = list(itertools.chain(*list3))  # возвращает список из списка списков
    return list3

def grounding_methods(domain_robot, problem_robot):
    pars = pr.parser2(domain_robot)
    list4 = []
    parser = prob.problem_parser2(problem_robot)
    for i in pars.method:
        precond = i.precond
        subtask = i.subtask
        i.parameters = pop(i.parameters)
        for j in range(len(precond)):
            precond[j] = re.sub('[?]', '', precond[j])
        for k in range(len(subtask)):
            subtask[k] = re.sub('[?]', '', subtask[k])
        list4.append(ground_methods(i.name, i.parameters, i.param2, dict1(parser.object), precond, subtask, i.task, i.ordering))
    list4 = list(itertools.chain(*list4))
    return list4


class Methods:
    def __init__(self, name, param, task, subtask, prec, ord=None):
        self.name = name
        self.param = param
        self.task = task
        self.subtask = subtask
        self.prec = prec
        self.ord = ord


def ground_methods(name, parameters, param2, dict, prec, subtask, task, ordering):
    room = 0
    door = 0
    pack = 0
    param = []
    answer2 = []
    name = name[0]
    l1, l2, l3 = [], [], []
    for i in range(len(parameters)):
        if parameters[i] == 'Room':
            room += 1
        elif parameters[i] == 'Room_door':
            door += 1
        elif parameters[i] == 'Package':
            pack += 1
    l1 = list(combinations(dict['Package'], pack))
    l2 = list(combinations(dict['Room'], room))
    l3 = list(combinations(dict['Room_door'], door))
    for i in l1:
        for j in l2:
            for k in l3:
                param = list(i + ('r',) + j + k)
                dict3 = dict2(dict, param)  # словарь тип - обьект для каждого заграундинного действия
                prec = get_prec_effect(dict3, prec, dict1(param2))
                subtask = get_prec_effect(dict3, subtask, dict1(param2))
                task = get_prec_effect(dict3, task, dict1(param2))
                answer2.append(Methods(name, param, task, subtask, prec))
    return answer2


def ground_action(name, act, parameters, dict, precond, effect):
    room = 0
    door = 0
    pack = 0
    param = []
    answer1 = []
    name = name[0]
    l1, l2, l3 = [], [], []
    for i in range(len(act)):
        if act[i] == 'Room':
            room += 1
        elif act[i] == 'Room_door':
            door += 1
        elif act[i] == 'Package':
            pack += 1
    l1 =list(permutations(dict['Package'], pack))
    l2 =list(permutations(dict['Room'], room))
    l3 = list(permutations(dict['Room_door'], door))
    for i in l1:
        for j in l2:
            for k in l3:
                param = list(i + ('r',) + j + k)  # граундинг всевозможных действий, возвращает список только объектов
                dict3 = dict2(dict, param) # словарь тип - обьект для каждого заграундинного действия
                eff = get_prec_effect(dict3, effect, dict1(parameters))
                prec = get_prec_effect(dict3, precond, dict1(parameters))
                answer1.append(Action(name, param, prec, eff))
    return answer1


def pop(list):   #возвращает вместо параметра только тип объектов для каждого действия
    param = []
    for i in range(len(list)):
        if list[i].find('?') == -1:
            param.append(list[i])
    return param



#grounding_actions("/Users/liza/Downloads/project-htn-master-5/domain_robot.pddl", "/Users/liza/Downloads/project-htn-master-5/problem_robot.pddl")
#grounding_methods("/Users/liza/Downloads/project-htn-master-5/domain_robot.pddl", "/Users/liza/Downloads/project-htn-master-5/problem_robot.pddl")