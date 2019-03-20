import parser as pr
import problem as prob
import grounding as ground
import re
import itertools
import random

ans = []
inits = []
oper = list()
tasks = list()
Methods = []
T1 = []

def function(domain_robot, problem_robot):
    #domain_robot = "domain_robot.pddl"
    #problem_robot = "problem_robot.pddl"
    pars = pr.parser2(domain_robot)
    gr = ground.grounding_actions(domain_robot, problem_robot)
    gr_m = ground.grounding_methods(domain_robot, problem_robot)
    pr_parser = prob.problem_parser2(problem_robot)
    for i in pars.action:
        oper.append(*i.name)
    for i in pars.task:
        tasks.append(*i.name)
    T = pr_parser.goal
    T = T.split()
    T = ' '.join(T)
    T1.append(T)
    init = pr_parser.init
    for i in range(len(init)):
        inits.append(init[i])
    for j in range(len(inits)):
        inits[j] = re.sub('[?]', '', inits[j])
    answer(T1, oper, inits, tasks, gr_m, gr)


def pls(name, param):
    full_name = list()
    full_name.append(name)
    for i in range(len(param)):
        full_name.append(param[i])
    full_name = ' '.join(full_name)
    return full_name


def change(effect, init, prec):
    init = [item for item in init if item not in prec]
    for i in range(len(effect)):
        init.append(effect[i])
    return init


def htn(T, oper, init, task, gr_m, gr):
    global ans, Methods
    list1 = []
    Actions = []
    Decomposition = []
    if len(T) == 0:
        return 0
    name = T[0].split()[0]
    if name in oper:
        for r in gr:
            if name == r.name:
                list1 = r.precond
                if all(z in init for z in list1) == True:
                    list1 = pls(r.name, r.param)
                    Actions.append(list1)
        if Actions == []:
            return 0
        secure_random = random.SystemRandom()
        action_ch = secure_random.choice(Actions)
        for a in gr:
            if a.name == action_ch.split()[0] and a.param == action_ch.split()[1:]:
                init = change(a.effect, init, a.precond)
        T.pop(0)
        again = htn(T1, oper, init, task, gr_m, gr)
        if again == -1:
            return -1
        ans.append(action_ch)
    else:
        if name in task:
            name1 = T[0]
            for k in gr_m:
                if name1 == k.task[0]:
                    list2 = k.prec
                    if all(z in init for z in list2) == True:
                        list2 = pls(k.name, k.param)
                        Methods.append(list2)
                        subtask = k.subtask
                        for j in range(len(subtask)):
                            subtask[j] = subtask[j][6:]
                        Decomposition.append(subtask)
            if Decomposition == []:
                return 0
            secure_random = random.SystemRandom()
            decomp_ch = secure_random.choice(Decomposition)
            for k in gr_m:
                if k.subtask == decomp_ch:
                    k.subtask.reverse()
                    for e in range(len(subtask)):
                        T.append(subtask[e])
            T.pop(0)
            T.reverse()
            again = htn(T1, oper, init, task, gr_m, gr)
            if again == -1:
                return -1


def answer(T1, oper, inits, tasks, gr_m, gr):
    htn(T1, oper, inits, tasks, gr_m, gr)
    ans.reverse()
    print(ans)

#answer(T1, oper, inits, tasks)