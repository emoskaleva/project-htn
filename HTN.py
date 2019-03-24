import parser as pr
import problem as prob
import grounding as ground
import re
import random

ans = []
inits = []
oper = list()
prec = []
tasks = list()
Methods = []
T1 = []


class HTN_planner():
    def precedents(self, goal, init, effect):
        effect = [x for x in effect if x]
        for j in range(len(init)):
            init[j] = re.sub('[?]', '', init[j])
        with open("prec.pddl", "a") as f:
            f.write(':Name\n' + goal + 2 * '\n')
            f.write(':Init\n')
            for i in range(len(init)):
                f.write(init[i] + '\n')
            f.write('\n:Effect\n')
            for i in range(len(effect)):
                f.write(effect[i] + '\n')
            f.write('\n')


        f.close()

    def pls(self, name, param):
        full_name = list()
        full_name.append(name)
        for i in range(len(param)):
            full_name.append(param[i])
        full_name = ' '.join(full_name)
        return full_name

    def change(self, effect, init, prec):
        init = [item for item in init if item not in prec]
        for i in range(len(effect)):
            init.append(effect[i])
        return init

    def htn(self, T, oper, init, task, gr_m, gr, gr_pr):
        global ans, Methods, inits
        list1 = []
        Actions = []
        Decomposition = []
        if len(T) == 0:
            return 0
        name = T[0].split()[0]
        if name in oper or name in prec:
            inits = []
            for r in gr:
                if name == r.name:
                    list1 = r.precond
                    if all(z in init for z in list1) == True:
                        list1 = self.pls(r.name, r.param)
                        Actions.append(list1)
            for r in gr_pr:
                if name == r.name:
                    list1 = r.precond
                    if all(z in init for z in list1) == True:
                        list1 = self.pls(r.name, r.param)
                        Actions.append(list1)
            if Actions == []:
                return 0
            secure_random = random.SystemRandom()
            action_ch = secure_random.choice(Actions)
            for a in gr:
                if a.name == action_ch.split()[0] and a.param == action_ch.split()[1:]:
                    init = self.change(a.effect, init, a.precond)
            inits = init
            T.pop(0)
            again = self.htn(T1, oper, init, task, gr_m, gr, gr_pr)
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
                            list2 = self.pls(k.name, k.param)
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
                kl = 0
                T.pop(0)
                T.reverse()
                again = self.htn(T1, oper, init, task, gr_m, gr, gr_pr)
                if again == -1:
                    return -1

    def function(self, domain_robot, problem_robot, precends):
        # domain_robot = "domain_robot.pddl"
        # problem_robot = "problem_robot.pddl"
        pars = pr.parser2(domain_robot)
        gr = ground.grounding_actions(domain_robot, problem_robot)
        gr_m = ground.grounding_methods(domain_robot, problem_robot)
        gr_pr = ground.grounding_precend(precends, problem_robot)
        pr_parser = prob.problem_parser2(problem_robot)
        for i in pars.action:
            oper.append(*i.name)
        for i in pars.task:
            tasks.append(*i.name)
        for i in gr_pr:
            if i.name not in prec:
                prec.append(i.name)
        T = pr_parser.goal
        T = T.split()
        T = ' '.join(T)
        T1.append(T)
        init = pr_parser.init
        for i in range(len(init)):
            inits.append(init[i])
        for j in range(len(inits)):
            inits[j] = re.sub('[?]', '', inits[j])
        self.htn(T1, oper, inits, tasks, gr_m, gr, gr_pr)
        self.precedents(T, init, inits)
        ans.reverse()
        print("Цель:\n",T)
        print("\n")
        print("Начальное состояние:")
        for i in range(len(init)):
            print(init[i])
        print("\n")
        print("Конечное состояние:")
        for i in range(len(inits)):
            print(inits[i])
        print("\n")
        print("План:")
        for i in range(len(ans)):
            print(ans[i])
        return ans


#answer(T1, oper, inits, tasks)
#planner = HTN_planner()
#print(planner.function("domain_robot.pddl", "problem_robot.pddl", "prec.pddl"))