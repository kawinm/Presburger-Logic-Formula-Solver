import sys
from z3 import *
from itertools import product
from math import ceil
from prettytable import PrettyTable

class Node:
    def __init__(self):
        self.formula = ''
        self.left_child = None
        self.right_child = None
        self.automata = None
        self.variables = None
        self.coeff = None

    def set_formula(self, formula):
        self.formula = formula

    def set_left_child(self, left):
        self.left_child = left

    def set_right_child(self, right):
        self.right_child = right

    def post_order_traversal(self, root):
        if root == None:
            return 
        self.post_order_traversal(root.left_child)
        self.post_order_traversal(root.right_child)
        print(root.formula)
        if root.left_child == None and root.right_child == None:
            root.automata, root.variables, root.coeff = construct_automata(root.formula)
        elif root.formula == 'Not' and root.left_child != None and root.right_child == None:
            root.automata = complement_automata(root.left_child.automata)
            root.variables = root.left_child.variables[:]
            print(root.variables)
            root.coeff = root.left_child.coeff
        elif root.formula == 'And' and root.left_child != None and root.right_child != None:
            root.variables = root.left_child.variables[:]
            root.coeff = root.left_child.coeff[:]

            for i in range(len(root.variables)):
                if root.variables[i] == 0 and root.right_child.variables[i] == 1:
                    root.variables[i] = 1
                    root.coeff[i] = root.right_child.coeff[i]

            root.automata = intersect_automata(root.left_child.automata, root.right_child.automata, root.left_child.variables, root.right_child.variables, root.variables, root.coeff)
        elif root.formula == 'Or' and root.left_child != None and root.right_child != None:
            self.variables = root.left_child.variables[:]
            root.coeff = root.left_child.coeff[:]

            for i in range(len(root.variables)):
                if root.variables[i] == 0 and root.right_child.variables[i] == 1:
                    root.variables[i] = 1
                    root.coeff[i] = root.right_child.coeff[i]

            root.automata = union_automata(root.left_child.automata, root.right_child.automata, root.left_child.variables, root.right_child.variables, root.variables, root.coeff)

def union_automata(table1, table2, var1, var2, cur_var, coeff):

    print(var1)
    
    states1 = [i for i in table1]
    states2 = [i for i in table2]

    automata = {}
    visited = []

    position_of_input_1 = []
    position_of_input_2 = []

    num_of_input = 0
    for i in range(1,len(cur_var)):
        if cur_var[i] == 1:
            num_of_input += 1
        if var1[i] == 1:
            position_of_input_1.append(num_of_input-1)
        if var2[i] == 1:
            position_of_input_2.append(num_of_input-1)
    
    print(position_of_input_1,position_of_input_2, var1, var2, cur_var)

    for states in product(states1, states2):
        if 'D' in states[0] or 'D' in states[1]:
            continue
        if 'I' in states[0] and 'I' in states[1]:
            init = 'I'
        else:
            init = ''
        if 'F' in states[0] or 'F' in states[1]:
            final = 'F'
        else:
            final = ''

        cur_state1 = []
        for i in states[0]:
            if i == 'I' or i == 'F':
                break 
            elif i == '<' or i == '>':
                continue
            cur_state1.append(i)
        cur_state1 = "".join(cur_state1)

        cur_state2 = []
        for i in states[1]:
            if i == 'I' or i == 'F':
                break 
            elif i == '<' or i == '>':
                continue
            cur_state2.append(i)
        cur_state2 = "".join(cur_state2)

        cur_state3 = '<' + cur_state1 + ',' +cur_state2 +'>' + init + final 

        perm = product(['0','1'], repeat=num_of_input)

        automata[cur_state3] = {}

        for input in list(perm):
            input1 = []
            for pos in position_of_input_1:
                input1.append(input[pos])
            input1 = "".join(input1)

            input2 = []
            for pos in position_of_input_2:
                input2.append(input[pos])
            input2 = "".join(input2)

            trans1 = table1[states[0]][input1]
            trans2 = table2[states[1]][input2]

            transition1 = []
            for i in str(trans1):
                if i == '<' or i == '>':
                    continue
                transition1.append(i)
            transition1 = "".join(transition1)

            transition2 = []
            for i in str(trans2):
                if i == '<' or i == '>':
                    continue
                transition2.append(i)
            transition2 = "".join(transition2)

            trans3 = '<' + transition1 + ',' + transition2 + '>'
            automata[cur_state3]["".join(input)] = trans3


    print(automata)
    return automata


def intersect_automata(table1, table2, var1, var2, cur_var, coeff):

    print(var1)
    
    states1 = [i for i in table1]
    states2 = [i for i in table2]

    automata = {}
    visited = []

    position_of_input_1 = []
    position_of_input_2 = []

    num_of_input = 0
    for i in range(1,len(cur_var)):
        if cur_var[i] == 1:
            num_of_input += 1
        if var1[i] == 1:
            position_of_input_1.append(num_of_input-1)
        if var2[i] == 1:
            position_of_input_2.append(num_of_input-1)
    
    print(position_of_input_1,position_of_input_2, var1, var2, cur_var)

    for states in product(states1, states2):
        if 'D' in states[0] or 'D' in states[1]:
            continue
        if 'I' in states[0] and 'I' in states[1]:
            init = 'I'
        else:
            init = ''
        if 'F' in states[0] and 'F' in states[1]:
            final = 'F'
        else:
            final = ''

        cur_state1 = []
        for i in states[0]:
            if i == 'I' or i == 'F':
                break 
            elif i == '<' or i == '>':
                continue
            cur_state1.append(i)
        cur_state1 = "".join(cur_state1)

        cur_state2 = []
        for i in states[1]:
            if i == 'I' or i == 'F':
                break 
            elif i == '<' or i == '>':
                continue
            cur_state2.append(i)
        cur_state2 = "".join(cur_state2)

        cur_state3 = '<' + cur_state1 + ',' +cur_state2 +'>' + init + final 

        perm = product(['0','1'], repeat=num_of_input)

        automata[cur_state3] = {}

        for input in list(perm):
            input1 = []
            for pos in position_of_input_1:
                input1.append(input[pos])
            input1 = "".join(input1)

            input2 = []
            for pos in position_of_input_2:
                input2.append(input[pos])
            input2 = "".join(input2)

            trans1 = table1[states[0]][input1]
            trans2 = table2[states[1]][input2]

            transition1 = []
            for i in str(trans1):
                if i == '<' or i == '>':
                    continue
                transition1.append(i)
            transition1 = "".join(transition1)

            transition2 = []
            for i in str(trans2):
                if i == '<' or i == '>':
                    continue
                transition2.append(i)
            transition2 = "".join(transition2)

            trans3 = '<' + transition1 + ',' + transition2 + '>'
            automata[cur_state3]["".join(input)] = trans3


    print(automata)
    return automata


def complement_automata(transition_table):

    automata = {}

    for i in transition_table.items():
        if 'F' in i[0] :
            automata[i[0][:-1]] = i[1]
        elif 'D' in i[0]:
            automata[i[0]] = i[1]
        else:
            automata[i[0]+'F'] = i[1]

    print(automata)
    return automata

def automata_for_equal(coeff):
    start_state = [coeff[0]]
    states = []
    states.append(start_state[0])

    weights = []
    for i in coeff:
        if i != 0:
            weights.append(i)
    
    print(weights)
    
    number_of_input = len(weights)

    transition_table = {}

    i = 0
    n = len(states)
    while i < n:
        perm = product([0,1], repeat=number_of_input-1)

        if states[i] in transition_table:
            i+=1
            continue

        transition_table[states[i]] = {}

        for input in list(perm):
            
            c = 0
            for theta in range(0,len(input)):
                c += input[theta] * weights[theta+1]
            
            c = states[i] - c 

            if c % 2 == 0:
                c= c //2
                transition_table[states[i]]["".join(map(str,input))] = c
                if c not in transition_table:
                    states.append(c)
            else:
                transition_table[states[i]]["".join(map(str,input))] = 'D' 
        i+= 1
        n = len(states)
    #print(transition_table)

    x = PrettyTable()

    header = [""]
    perm = product([0,1], repeat=number_of_input-1)
    for input in perm:
        header.append("".join(map(str,input)))
    
    x.field_names = header

    automata = {}

    initial = 0
    for i in transition_table.items():
        if initial == 0:
            row = [str(i[0])+'I']
            if i[0] == 0:
                row[0] = row[0] + 'F'
            initial = 1
        else:
            row = [str(i[0])]
            if i[0] == 0:
                row[0] = row[0] + 'F'
        for j in i[1].items():
            row.append(j[1])
        x.add_row(row)
        automata[row[0]] = i[1] 
    error_state = ['D']*(2**(number_of_input-1) + 1)

    automata['D'] = {}
    perm = product([0,1], repeat=number_of_input-1)
    for input in perm:
        automata['D']["".join(map(str,input))] = 'D'
    x.add_row(error_state)

    #print(x)

    return automata, x

def automata_for_less_than_equal(coeff, type):
    start_state = [coeff[0]]
    states = []
    states.append(start_state[0])

    weights = []
    for i in coeff:
        if i != 0:
            weights.append(i)
    
    print(weights)
    
    number_of_input = len(weights)

    transition_table = {}

    i = 0
    n = len(states)
    while i < n:
        perm = product([0,1], repeat=number_of_input-1)

        if states[i] in transition_table:
            i+=1
            continue

        transition_table[states[i]] = {}

        for input in list(perm):
            
            c = 0
            for theta in range(0,len(input)):
                c += input[theta] * weights[theta+1]
            
            c = states[i] - c 

            c= c //2
            transition_table[states[i]]["".join(map(str,input))] = c
            if c not in transition_table:
                states.append(c)
        i+= 1
        n = len(states)
    #print(transition_table)

    x = PrettyTable()

    header = [""]
    perm = product([0,1], repeat=number_of_input-1)
    for input in perm:
        header.append("".join(map(str,input)))
    
    x.field_names = header

    automata = {}
    initial = 0
    for i in transition_table.items():
        if initial == 0:
            row = [str(i[0])+'I']
            if type == 0 and i[0] >= 0:
                row[0] = row[0] + 'F'
            elif type == 1 and i[0] < 0:
                row[0] = row[0] + 'F'
            initial = 1
        else:
            row = [str(i[0])]
            if type == 0 and i[0] >= 0:
                row[0] = row[0] + 'F'
            elif type == 1 and i[0] < 0:
                row[0] = row[0] + 'F'
        for j in i[1].items():
            row.append(j[1])
        x.add_row(row)
        automata[row[0]] = i[1] 

    #print(x)

    return automata, x

def automata_for_less_than(coeff, type):
    start_state = [coeff[0]]
    states = []
    states.append(start_state[0])

    weights = []
    for i in coeff:
        if i != 0:
            weights.append(i)
    
    print(weights)
    
    number_of_input = len(weights)

    transition_table = {}

    i = 0
    n = len(states)
    while i < n:
        perm = product([0,1], repeat=3) #number_of_input)

        if states[i] in transition_table:
            i+=1
            continue

        transition_table[states[i]] = {}

        for input in list(perm):
            
            c = 0
            for theta in range(0,len(input)):
                c += input[theta] * weights[theta+1]
            
            c = states[i] - c 

            c= ceil(c / 2)
            transition_table[states[i]]["".join(map(str,input))] = c
            if c not in transition_table:
                states.append(c)
        i+= 1
        n = len(states)
    #print(transition_table)

    x = PrettyTable()

    header = [""]
    perm = product([0,1], repeat=number_of_input-1)
    for input in perm:
        header.append("".join(map(str,input)))
    
    automata = {}
    x.field_names = header
    initial = 0
    for i in transition_table.items():
        if initial == 0:
            row = [str(i[0])+'I']
            if type == 0 and i[0] > 0:
                row[0] = row[0] + 'F'
            elif type == 1 and i[0] <= 0:
                row[0] = row[0] + 'F'
            initial = 1
        else:
            row = [str(i[0])]
            if type == 0 and i[0] > 0:
                row[0] = row[0] + 'F'
            elif type == 1 and i[0] <= 0:
                row[0] = row[0] + 'F'
        for j in i[1].items():
            row.append(j[1])
        x.add_row(row)
        automata[row[0]] = i[1] 

    #print(x)

    return automata, x

def construct_automata(form):
    relation = ''

    r1 = -1
    l2 = -1
    for i in range(len(form)):
        if form[i] == "=":
            if form[i+1] == "=":
                relation = 1            # ==
                r1 = i-1
                l2 = i+2
            break
        elif form[i] == "<":
            if form[i+1] == "=":
                relation = 2            # <=
                r1 = i-1
                l2 = i+2
            else:
                relation = 3            # <
                r1 = i-1
                l2 = i+1
            break
        elif form[i] == ">":
            if form[i+1] == "=":
                relation = 4            # >=
                r1 = i-1
                l2 = i+2
            else:
                relation = 5            # >
                r1 = i-1
                l2 = i+1
            break
    
    coeff = [0]*(number_of_variables+1)
    variable = [0]*(number_of_variables+1) # n = number of var

    a = form[0:r1+1].split('+')
    for i in a:
        if '*' in i:
            b = i.split('*')
            var = int(b[1][1:])
            coeff[var] += int(b[0])
            variable[var] = 1
        else:
            try:
                coeff[0] -= int(i)
                variable[0] = 1
            except:
                var = int(i[1:])
                coeff[var] += 1
                variable[var] = 1
    print(relation, coeff, variable)

    a = form[l2:].split('+')
    for i in a:
        if '*' in i:
            b = i.split('*')
            var = int(b[1][1:])
            coeff[var] -= int(b[0])
            variable[var] = 1
        else:
            try:
                coeff[0] += int(i)
                variable[0] = 1
            except:
                var = int(i[1:])
                coeff[var] -= 1
                variable[var] = 1
    print(relation, coeff, variable)

    if relation == 1:
        automata, table = automata_for_equal(coeff)
    elif relation == 2:
        automata, table = automata_for_less_than_equal(coeff, 0)
    elif relation == 5:
        automata, table = automata_for_less_than_equal(coeff, 1)
    elif relation == 3:
        automata, table = automata_for_less_than(coeff, 0)
    else:
        automata, table = automata_for_less_than(coeff, 1)

    print(form, automata)
    print(table)

    return automata, variable, coeff

        


def parse_input(input, root):
    n = len(input)

    if n == 0:
        return 0
    
    if input[0] == 'A' and input[:3] == 'And':
        d = 1
        root.set_formula('And')
        print(root.formula)

        left_child = Node()
        root.set_left_child(left_child)

        right_start = parse_input(input[4:], left_child)
        print(d, 'r', right_start)
        right_child = Node()
        root.set_right_child(right_child)
        input_ends = parse_input(input[right_start+4:], right_child)
        print(d, input_ends)
        return input_ends + right_start + 4
    elif input[0] == 'O' and input[:2] == 'Or':
        d = 2
        root.set_formula('Or')
        print(root.formula)

        left_child = Node()
        root.set_left_child(left_child)

        right_start = parse_input(input[3:], left_child)
        print(d, 'r', right_start)
        right_child = Node()
        root.set_right_child(right_child)
        input_ends = parse_input(input[right_start+3:], right_child)
        print(d, input_ends)
        
        return input_ends + right_start + 3
    elif input[0] == 'N' and input[:3] == 'Not':
        d = 3
        root.set_formula('Not')
        print(root.formula)

        left_child = Node()
        root.set_left_child(left_child)

        right_start = parse_input(input[4:], left_child)
        print(d, 'r', right_start)
        return right_start + 4
    else:
        l = 0
        for i in range(n):
            if input[i] == ',':
                root.set_formula(input[l:i])
                print(root.formula)
                return i+1
            elif input[i] == ')':
                root.set_formula(input[l:i])
                print(root.formula)
                if i == n-1:
                    return i + 1
                return i + 2
        root.set_formula(input[l:])
        print(root.formula)
        return n




number_of_variables = int(sys.argv[2])

print("First Argument is",sys.argv[1])

root = Node()
parse_input(sys.argv[1], root)

root.post_order_traversal(root)

