Name_file = "/Users/liza/Downloads/project-htn-master-5/domain_robot.pddl"
name = "prec.pddl"
import re
import itertools

def get_requirements(line):
    line = line.strip('(').strip(')')
    line = line.split()
    return line[1:]


def get_types(Name_file, count):
    a = []
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]
    for i in range(count + 1, len(lines)):
        if (lines[i].find(')') == -1):
            a.append(lines[i])
        else:
            break
    return a

def get_predicate(text):
    predicates = []
    for i in range(1, len(text)):
        predicates.append(text[i])
    for i in range(len(predicates)):
        predicates[i] = re.sub('[)(]', '', predicates[i])
    return predicates


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
            break
    return lines[index:end + 1]

def get_part2(index, file):
    with open(file) as infile:
        lines = [line.strip() for line in infile]
    end = index
    for i in range(index + 1, len(lines)):
        if lines[i] is "":
            end = i
            break
    return lines[index + 1:end]


class Action:
    def __init__(self, name, parameters, precondition, effect, param2):
        self.name = name
        self.parameters = parameters
        self.precondition = precondition
        self.effect = effect
        self.param2 = param2


def get_actions(lines):
    param = []
    precond = []
    param2 = []
    effect = []
    actions = []
    name = lines[0].split()
    name = name[1:]
    lines[1] = re.sub('[)(]', '', lines[1])
    param2 = lines[1].split('?')
    param2 = [i.replace('  ', '') for i in param2]
    param2 = param2[1:]
    lines[1] = re.sub('[-]', '', lines[1])
    param = lines[1].split()
    param = param[1:]
    for i in range(len(lines)):
        if lines[i].find(':precondition') != -1:
            end = i
            brackets = 0
            for ir in range(i + 1, len(lines)):
                end += 1
                for j in range(len(lines[ir])):
                    if lines[ir][j] == '(':
                        brackets += 1
                    elif lines[ir][j] == ')':
                        brackets -= 1
                if brackets == 0:
                    for j in range(len(lines[i + 2:end])):
                        precond.append(lines[i + 2:end][j])
                    for i in range(len(precond)):
                        precond[i] = re.sub('[)(]', '', precond[i])
                    break
        elif lines[i].find(':effect') != -1:
            end = i
            brackets = 0
            for ir in range(i + 1, len(lines)):
                end += 1
                for j in range(len(lines[ir])):
                    if lines[ir][j] == '(':
                        brackets += 1
                    elif lines[ir][j] == ')':
                        brackets -= 1
                if brackets == 0:
                    for j in range(len(lines[i + 2:end])):
                        effect.append(lines[i + 2:end][j])
                    for k in range(len(effect)):
                        effect[k] = re.sub('[)(]', '', effect[k])
                    break
    actions = Action(name, param, precond, effect, param2)
    #for i in actions:
        #print(i.name, i.parameters)
    return actions

    #for j in action:
       #print('Name:', j.name)
       #print('Parametes:', j.parameters)
       #print('Precondition:', j.precondition)
       #print('Effect:', j.effect, '\n')

class Method:
    def __init__(self, name, parameters, param2, task, precond, subtask, ordering):
        self.name = name
        self.parameters = parameters
        self.param2 = param2
        self.task = task
        self.precond = precond
        self.subtask = subtask
        self.ordering = ordering


def get_methods(lines):
    name, param, task, subtask, ord, precond = [], [], [], [], [], []
    methods = []
    name = lines[0].split()
    name = name[1:]
    lines[1] = re.sub('[)(]', '', lines[1])
    param2 = lines[1].split('?')
    param2 = [i.replace('  ', '') for i in param2]
    param2 = param2[1:]
    lines[1] = re.sub('[-]', '', lines[1])
    param = lines[1].split()
    param = param[1:]
    for i in range(len(lines)):
        if lines[i].find(':task') != -1:
            lines[i] = re.sub('[)?(:]', '', lines[i][5:])
            task.append(lines[i])
        elif lines[i].find(':subtask') != -1:
            end = i
            brackets = 0
            for ir in range(i + 1, len(lines)):
                end += 1
                for j in range(len(lines[ir])):
                    if lines[ir][j] == '(':
                        brackets += 1
                    elif lines[ir][j] == ')':
                        brackets -= 1
                if brackets == 0:
                    for j in range(len(lines[i + 2:end])):
                        subtask.append(lines[i + 2:end][j])
                    for k in range(len(subtask)):
                        subtask[k] = re.sub('[)(]', '', subtask[k])
                    break
        elif lines[i].find(':precondition') != -1:
            end = i
            brackets = 0
            for ir in range(i + 1, len(lines)):
                end += 1
                for j in range(len(lines[ir])):
                    if lines[ir][j] == '(':
                        brackets += 1
                    elif lines[ir][j] == ')':
                        brackets -= 1
                if brackets == 0:
                    for j in range(len(lines[i + 2:end])):
                        precond.append(lines[i + 2:end][j])
                    for i in range(len(precond)):
                        precond[i] = re.sub('[)(]', '', precond[i])
                    break
        elif lines[i].find(':ordering') != -1:
            lines[i + 2] = re.sub('[)(]', '', lines[i + 2])
            i = i + 2
            while lines[i] != ')':
                lines[i] = re.sub('[)(]', '', lines[i])
                ord.append(lines[i])
                i += 1

    methods = Method(name, param, param2, task, precond, subtask, ord)
    return methods

    #for i in methods:
        #print('Name:', i.name)
        #print('Parameters:', i.parameters)
        #print('Task:', i.task)
        #print('Subtask', i.subtask)
        #print('Ordering:', i.ordering, '\n')

class Task:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

def get_tasks(text):
    name = text[0].split()
    name = name[1:]
    param = []
    Tasks = []
    text[1] = re.sub('[()-]', '', text[1])
    param = text[1].split()
    param = param[1:]
    Tasks = Task(name, param)
    return Tasks



class Domain:
    def __init__(self, name: object, requirements: object, type: object, action, predicate: object, method, task):
        self.name = name
        self.requirements = requirements
        self.types = type
        self.action = action
        self.predicate = predicate
        self.method = method
        self.task = task

def parser2(Name_file):
    a = []
    actions = []
    first, second = '', ''
    fifth, actions, third, fourth, part, sixth, tasks = [], [], [], [], [], [], []
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]

    for i in range(len(lines)):
        if (lines[i].find('domain') != -1):
            lines[i] = lines[i].strip('(').strip(')')
            lines[i] = lines[i].split()
            first = lines[0][2].split()
        elif (lines[i].find(':requirements') != -1):
            second = get_requirements(lines[i]);
        elif (lines[i].find(':types') != -1):
            third = get_types(Name_file, i)
        elif (lines[i].find('(:action') != -1):
            actions.append(get_actions(get_part(i, Name_file)))
        elif (lines[i].find(':predicates') != -1):
            fifth.append(get_predicate(get_part(i, Name_file)))
        elif (lines[i].find(':method') != -1):
            sixth.append(get_methods(get_part(i, Name_file)))
        elif (lines[i].find('(:task') != -1):
            tasks.append(get_tasks(get_part(i, Name_file)))
    domain = Domain(first, second, third, actions, fifth, sixth, tasks)
    #for i in domain.action:
        #print(i.name, i.parameters)
    return domain


class Precend:
    def __init__(self, name, parameters, precond, effect):
        self.name = name
        self.parameters = parameters
        self.precond = precond
        self.effect = effect

def parser_precend(name):
    Name, param, precond, effect, precend = [], [], [], [], []
    with open(name) as infile:
        lines = [line.strip() for line in infile]
    for i in range(len(lines)):
        if (lines[i].find(':Name') != -1):
            lines[i] = lines[i].split()
            Name = lines[i + 1].split()[0]
            param = lines[i + 1].split()[1:]
        elif (lines[i].find(':Init') != -1):
            precond.append(get_part2(i, name))
            precond = list(itertools.chain(*precond))
        elif (lines[i].find(':Effect') != -1):
            effect.append(get_part2(i, name))
            effect = list(itertools.chain(*effect))
            precend.append(Precend(Name, param, precond, effect))
            precond = []
            effect = []
    return precend


#parser_precend(name)
def parser(Name_file):
    a = []
    actions = []
    first, second = '', ''
    fifth, actions, third, fourth, part, sixth = [], [], [], [], [], []
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]

    for i in range(len(lines)):
        if (lines[i].find('domain') != -1):
            lines[i] = lines[i].strip('(').strip(')')
            lines[i] = lines[i].split()
            first = lines[0][2].split()
        elif (lines[i].find(':requirements') != -1):
            second = get_requirements(lines[i])
        elif (lines[i].find(':types') != -1):
            third = get_types(Name_file, i)
        elif (lines[i].find('(:action') != -1):
            actions.append(get_actions(get_part(i, Name_file)))
        elif (lines[i].find(':predicates') != -1):
            fifth.append(get_predicate(get_part(i, Name_file)))
        elif (lines[i].find(':method') != -1):
            sixth.append(get_methods(get_part(i, Name_file)))
    domain = Domain(first, second, third, actions, fifth, sixth)
    print('Domain name:', domain.name)
    print('-----------')
    print('Requirements:', domain.requirements)
    print('-------------')
    print('Types:', domain.types)
    print('------')
    print('Predicetes:', domain.predicate)
    print('-----------')
    for i in domain.action:
        print('Name: ', i.name)
        print('Parameters', i.parameters)
        print('Precondition', i.precondition)
        print('Effects:', i.effect, '\n')
    for j in domain.method:
        print('Name:', j.name)
        print('Parameters', j.parameters)
        print('Task:', j.task)
        print('Subtask:', j.subtask)
        print('Ordering:', j.ordering, '\n')
    return domain

#parser2(Name_file)
