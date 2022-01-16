# Presburger Logic Formula Solver

# Input:
The program supports taking input from command line. 

(OR) The inputs can be directly given as values to the variables: z3_formula = Z3 formula as a string
number_of_variables = Number of x_i in the given z3 formula
variables_values[]  = (i-1)th position in this array gives the coefficient of x_i 

It is assumed that z3 formula does not have any space. Also, coefficient for any variable x_i in the z3 formula is given in the form c*x_i.
Also, it is assumed that there are no extra enclosing brackets around the formula.

It is assumed that all the variables x_1, x_2...x_n are present in the givn z3 forumula.

# Output:
Gives the transition table for the automata constructed in each step of the inductive procedure. Atlast, decides whether the given input satifies the given formula or not.

The transition table contains unreachable states also.

# Description of Functions:

1) parse_input(): Parse the given Z3 formula and store it in the form of a tree.
2) post_order_traversal(root): Performs post order traversal on the constructed tree to construct the automata inductively.
3) construct_automata(form): For a given atomic formula (leaves in the tree), the relation used and the coefficients of each variable in the formula is parsed. And it calls the function to perform to construct the transition table based on the relation (<, <=, ==, >, >=) used in the formula.
4) automata_for_equal(coeff, variable): Constructs and displays the transition table for the atomic formula with '==' relation.
5) automata_for_less_than_equal(coeff, type, variable): Constructs and displays the transition table for the atomic formula with '<=' or '>' relations.
6) automata_for_less_than(coeff, type, variable): Constructs and displays the transition table for the atomic formula with '<' or '>=' relations.
7) print_automata(automata, number_of_input): Prints the automata using Pretty Table 
8) complement_automata(transition_table, variables): For a given transition table of a DFA, it returns the transition table of the complement of the given DFA.
9) intersect_automata(table1, table2, var1, var2, cur_var, coeff): For the given transition tables of the two DFAs, it returns the transition table of the intersection of the two DFAs.
10) union_automata(table1, table2, var1, var2, cur_var, coeff): For the given transition tables of the two DFAs, it returns the transition table of the union of the two DFAs.
11) decider(automata, inputs): Decides whether the given input satisfies the given formula.
