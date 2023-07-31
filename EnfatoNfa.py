from graphviz import Digraph
import sys
import json

def epsilon_closure(state, epsilon_transitions):
    closure = set()
    stack = [state]
    while stack:
        current_state = stack.pop()
        closure.add(current_state)
        for transition in epsilon_transitions:
            if transition[0] == current_state and transition[1] == 'ε' and transition[2] not in closure:
                stack.append(transition[2])
    return closure

def convert_epsilon_nfa_to_nfa(epsilon_nfa):
    epsilon_transitions = [(src, letter, dest) for src, letter, dest in epsilon_nfa['transition_function'] if letter == 'ε']

    # Calculate epsilon closures for all states
    epsilon_closures = {state: epsilon_closure(state, epsilon_transitions) for state in epsilon_nfa['states']}
    # print(epsilon_closure)
    for state in epsilon_nfa['states']:
        print(f"Epsilon closure of {state}: {epsilon_closures[state]}")
    # Construct the new NFA
    global nfa
    nfa = {
        'states': sorted(list(epsilon_nfa["states"])),
        'alphabet': [letter for letter in epsilon_nfa['letters'] if letter != 'ε'],
        'transition_function': [],
        'start_states': epsilon_nfa['start_states'],
        'final_states': set(epsilon_nfa['final_states'])
    }

    for state in sorted(list(epsilon_nfa["states"])):
        for letter in nfa['alphabet']:
            target_states = epsilon_closures[state]
            print(state, " -> ",letter," - ",target_states," - ")
            input_states = set()
            ans_states = set()
            for t_state in list(target_states):
                for transition in epsilon_nfa['transition_function']:
                    if transition[0] == t_state and transition[1] == letter:
                        input_states.add(transition[2])
                        print(input_states,"-> ","add")


            print(input_states)

            for i_state in input_states:
                ans_states=ans_states.union(set(epsilon_closures[i_state]))
            for a_state in ans_states:
                nfa['transition_function'].append((state, letter, a_state))
    for state in epsilon_nfa['states']:
        if(len(epsilon_closures[state].intersection(set(nfa['final_states'])))>0):
            nfa['final_states'].add(state)


    print(nfa)
    final_nfa={
        'states': (list(nfa["states"])),
        'letters': [letter for letter in epsilon_nfa['letters'] if letter != 'ε'],
        'transition_function': nfa['transition_function'],
        'start_states': list(nfa['start_states']),
        'final_states': list(nfa['final_states'])
    }
    graph = generate_transition_graph()
    graph.render(filename='transition_graph_nfa', view=True)
    output_nfa(final_nfa)
    return final_nfa

def output_nfa(final_nfa):
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(final_nfa, indent = 4))

def generate_transition_graph():
    global nfa
    transition_function = nfa['transition_function']
    start_states = nfa['start_states']
    graph = Digraph(format='png')

    for transition in transition_function:
        start_state, letter, end_state = transition
        graph.node(start_state, shape='circle')
        graph.node(end_state, shape='doublecircle' if end_state in nfa['final_states'] else 'circle')
        graph.edge(start_state, end_state, label=letter)

    if len(start_states) == 1:
        start_state = start_states[0]
        graph.node('', shape='none')
        graph.edge('', start_state, label='start')

    return graph

# Example epsilon-NFA

with open(sys.argv[1], 'r') as inpjson:
        epsilon_nfa = json.loads(inpjson.read())

# Convert epsilon-NFA to NFA
nfa = convert_epsilon_nfa_to_nfa(epsilon_nfa)
print(nfa)
