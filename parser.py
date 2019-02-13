Name_file = "/Users/liza/domain01.pddl";
import re
import copy

def get_requirements(line):
    line = line.strip('(').strip(')')
    line = line.split()
    return line[1:]


def get_types(count):
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
            break;
    return lines[index:end + 1]


class Action:
    def __init__(self, name, parameters, precondition, effect):
        Action.name = name
        Action.parameters = parameters
        Action.precondition = precondition
        Action.effect = effect


def get_actions(lines):
    action = []
    param = []
    precond = []
    effect = []
    name = lines[0].split()
    name = name[1:]
    lines[1] = re.sub('[)(-]', '', lines[1])
    param = lines[1].split()
    param = param[1:]
    for i in range(len(lines)):
        if lines[i].find(':precondition') != -1:
            end = i;
            brackets = 0;
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
                    break;
        elif lines[i].find(':effect') != -1:
            end = i;
            brackets = 0;
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
                    break;
    action.append(Action(name, param, precond, effect))
    for j in action:
       print('Name:', j.name)
       print('Parameters:', j.parameters)
       print('Precondition:', j.precondition)
       print('Effect:', j.effect, '\n')

class Method:
    def __init__(self, name, parameters, task, subtask, ordering):
        Method.name = name
        Method.parameters = parameters
        Method.task = task
        Method.subtask = subtask
        Method.ordering = ordering


def get_methods(lines):
    name, param, task, subtask, ord = [], [], [], [], []
    methods = []
    name = lines[0].split()
    name = name[1:]
    lines[1] = re.sub('[)(-]', '', lines[1])
    param = lines[1].split()
    param = param[1:]
    for i in range(len(lines)):
        if lines[i].find(':task') != -1:
            lines[i] = re.sub('[)(:]', '', lines[i][5:])
            task.append(lines[i])
            #lines[i] = lines[i].split()
            #for j in range(1, len(lines[i])):
                #task.append(lines[i][j])
        elif lines[i].find(':subtask') != -1:
            end = i;
            brackets = 0;
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
                    break;
        elif lines[i].find(':ordering') != -1:
            lines[i + 2] = re.sub('[)(]', '', lines[i + 2])
            i = i + 2
            while lines[i] != ')':
                lines[i] = re.sub('[)(]', '', lines[i])
                ord.append(lines[i])
                i += 1

    methods.append(Method(name, param, task, subtask, ord))
    for i in methods:
        print('Name:', i.name)
        print('Parameters:', i.parameters)
        print('Task:', i.task)
        print('Subtask', i.subtask)
        print('Ordering:', i.ordering, '\n')

class Task:
    def __init__(self, name, parameters):
        Task.name = name
        Task.parameters = parameters

def get_tasks(text):
    name = text[0].split()
    name = name[1:]
    param = []
    Tasks = []
    text[1] = re.sub('[)(-]', '', text[1])
    param = text[1].split()
    param = param[1:]
    Tasks.append(Task(name, param))
    for i in Tasks:
        print('Name:', i.name)
        print('Parameters:', i.parameters, '\n')





class Domain:
    def __init__(self, name: object, requirements: object, type: object, predicate: object, task: object = None):
        Domain.name = name
        Domain.requirements = requirements
        Domain.types = type
        Domain.predicate = predicate
        Domain.task = task


def parser(Name_file):
    a = []
    first, second = '', '';
    fifth, actions, third, fourth, part = [], [], [], [], [];
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]

    for i in range(len(lines)):
        if (lines[i].find('domain') != -1):
            lines[i] = lines[i].strip('(').strip(')')
            lines[i] = lines[i].split();
            first = lines[0][2].split();
        elif (lines[i].find(':requirements') != -1):
            second = get_requirements(lines[i]);
        elif (lines[i].find(':types') != -1):
            third = get_types(i)
        elif (lines[i].find(':predicates') != -1):
            fifth = get_predicate(get_part(i, Name_file))
    Domain(first, second, third, fifth)

def print_answer():
    with open(Name_file) as infile:
        lines = [line.strip() for line in infile]
    print('Domain name:', Domain.name)
    print('-----------')
    print('Requirements:', Domain.requirements)
    print('-------------')
    print('Types:', Domain.types)
    print('------')
    print('Predicetes:', Domain.predicate)
    print('-----------')
    print('Tasks:')
    print('-------')
    for i in range(len(lines)):
        if (lines[i].find('(:task') != -1):
            get_tasks(get_part(i, Name_file))
    print('Actions:')
    print('--------')
    for i in range(len(lines)):
        if (lines[i].find('(:action') != -1):
            get_actions(get_part(i, Name_file))
    print('Methods:')
    print('--------')
    for i in range(len(lines)):
        if (lines[i]).find('(:method') != -1:
            get_methods(get_part(i, Name_file))


parser(Name_file);
print_answer();
