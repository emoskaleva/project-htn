action = []
Name_file = "/Users/liza/domain-htn.hddl";
import re
class Action:
    def __init__(self, name, parameters, precondition, effect):
        Action.name = name
        Action.parameters = parameters
        Action.precondition = precondition
        Action.effect = effect


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
    #return get_actions(lines[index:end + 1])

def get_actions(lines):
    param = []
    precond = []
    effect = []
    name = lines[0].strip('(:action').split()
    for i in range(len(lines)):
        if lines[i].find(':parameters') != -1:
            lines[i] = lines[i].strip('(').strip(')').strip(':parameters')
            lines[i] = lines[i].split()
            for j in range(len(lines[i])):
                param.append(lines[i][j]);
        elif lines[i].find(':precondition') != -1:
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
                    for j in range(len(lines[i + 1:end])):
                        precond.append(lines[i + 1:end][j])
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
                    for j in range(len(lines[i + 1:end])):
                        effect.append(lines[i + 1:end][j])
                    for k in range(len(effect)):
                        effect[k] = re.sub('[)(]', '', effect[k])
                    break;

    return Action(name, param, precond, effect)
    #print(Action.name)
    #print(Action.parameters)



class Domain:
    def __init__(self, name: object, requirements: object, type: object, predicate: object, action: object, task: object = None, method: object = None):
        Domain.name = name
        Domain.requirements = requirements
        Domain.types = type
        Domain.action = action
        Domain.predicate = predicate
        Domain.task = task
        Domain.method = method



def parser(Name_file):
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
        elif (lines[i].find('(:action') != -1):
            #part = get_part(i, Name_file)
             actions = get_part(i, Name_file)
             fourth.append(get_actions(actions))
             #print(Action.name)
             #print(Action.parameters)
        elif (lines[i].find('(:method') != -1):
             sixth = get_method(get_part(i, Name_file))
    Domain(first, second, third, fifth, fourth)
def print_answer():
    print('Domain name:', Domain.name, '\n')
    print('Requirements:', Domain.requirements, '\n')
    print('Types:', Domain.types, '\n')
    print('Predicetes:', Domain.predicate, '\n')
    print('Actions:')
    for action in Domain.action:
        print('Name:', action.name)
        print('Parameters:', action.parameters)
        print('Precondition: ', action.precondition)
        print('Effect: ', action.effect, '\n')



parser(Name_file);
print_answer();