# Conversion from NFA to DFA
import json
import sys
from graphviz import Digraph

dfa = {}
final_dfa = {}
nfa = {}
nfa_states = []
dfa_states = []

def get_power_set(nfa_st):
    powerset = [[]]
    for i in nfa_st:
        for sub in powerset:
            powerset = powerset + [list(sub) + [i]]
    return powerset

def load_nfa():
    global nfa
    with open(sys.argv[1], 'r') as inpjson:
        nfa = json.loads(inpjson.read())

def out_dfa():
    global final_dfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(final_dfa, indent = 4))

def generate_transition_graph(transition_function):
    global final_dfa
    start_states = final_dfa['start_states']
    graph = Digraph(format='png')

    for transition in transition_function:
        start_state, letter, end_state = transition
        graph.node(start_state, shape='circle')
        graph.node(end_state, shape='doublecircle' if end_state in final_dfa['final_states'] else 'circle')
        graph.edge(start_state, end_state, label=letter)

    if len(start_states) == 1:
        start_state = start_states[0]
        graph.node('', shape='none')
        graph.edge('', start_state, label='start')

    return graph

if __name__ == "__main__":
    load_nfa()

    dfa['states'] = []
    dfa['letters'] = nfa['letters']
    dfa['transition_function'] = []

    final_dfa['states'] = []
    final_dfa['letters'] = nfa['letters']

    for state in nfa['states']:
        nfa_states.append(state)

    dfa_states = get_power_set(nfa_states)


    dfa['states'] = []
    for states in dfa_states:
        temp = []
        for state in states:
            temp.append(state)
        dfa['states'].append(temp)

    for states in dfa_states:
        for letter in nfa['letters']:
            q_to = []
            for state in states:
                for val in nfa['transition_function']:
                    start = val[0]
                    inp = val[1]
                    end = val[2]
                    if state == start and letter == inp:
                        if end not in q_to:
                            q_to.append(end)
            q_states = []
            for i in states:
                q_states.append(i)
            dfa['transition_function'].append([q_states, letter, q_to])

    dfa['start_states'] = []
    final_dfa['start_states']= []
    final_dfa['final_states']= []
    final_dfa['transition_function']= []
    for state in nfa['start_states']:
        dfa['start_states'].append([state])
    dfa['final_states'] = []
    for states in dfa['states']:
        for state in states:
            if state in nfa['final_states'] and states not in dfa['final_states']:
                dfa['final_states'].append(states)

    for state in dfa['states']:
        st=''.join(state)
        final_dfa['states'].append(st)

    for state in dfa['start_states']:
        st=''.join(state)
        final_dfa['start_states'].append(st)

    for state in dfa['final_states']:
        st=''.join(state)
        final_dfa['final_states'].append(st)

    for transition in dfa['transition_function']:
        start_state, letter, end_state = transition
        ss=''.join(start_state)
        l=''.join(letter)
        es=''.join(end_state)
        if ss=='' or l=='' or es=='':
            continue
        final_dfa['transition_function'].append([ss,l,es])

    graph = generate_transition_graph(final_dfa["transition_function"])
    graph.render(filename='transition_graph', view=True)

    out_dfa()


