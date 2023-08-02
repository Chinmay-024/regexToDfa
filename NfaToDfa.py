import json
import sys
from graphviz import Digraph

final_dfa = {}
nfa = {}

def dfs(nfa, current_state, visited_states):
    visited_states.add(current_state)
    
    transitions = [t[2] for t in nfa['transition_function'] if t[0] == current_state]
    for state in transitions:
        if state not in visited_states:
            dfs(nfa, state, visited_states)

def remove_dead_states(nfa):
    reachable_states = set()
    dfs(nfa, nfa['start_states'][0], reachable_states)

    nfa['states'] = [state for state in nfa['states'] if state in reachable_states]
    nfa['transition_function'] = [t for t in nfa['transition_function'] if t[0] in reachable_states and t[2] in reachable_states]
    nfa['final_states'] = [f_state for f_state in nfa['final_states'] if f_state in reachable_states]

    return nfa

def nfaTOdfa(nfa):
    dfa = {}
    dfa["letters"] = nfa["letters"]
    dfa["transition_function"] = []
    dfa["start_states"] = nfa["start_states"]

    transition_function = []
    state_queue = []
    a = []
    a.append(nfa['start_states'][0])
    state_queue.append(a)
    print(state_queue)
    visited = []
    while(len(state_queue)>0):
        cur_state = state_queue.pop()
        if cur_state in list(visited):
            continue
        else:
            for letter in list(nfa['letters']):
                next_state = set()
                for state in cur_state:
                    for transition in nfa['transition_function']:
                        if state == transition[0] and letter == transition[1]:
                            next_state.add(transition[2])
                if len(list(next_state)):
                    transition_function.append([cur_state, letter, sorted(next_state)])
                    state_queue.append(sorted(next_state))
                    
            visited.append(cur_state)
    dfa['transition_function']=transition_function
    dfa['states']=visited
    final_state = []
    nfa_finalstates = set(nfa["final_states"])
    # print(nfa_finalstates)

    for state in visited:
        set_state = set(state)
        p = set_state.intersection(nfa_finalstates)
        print(state, " -> ", nfa_finalstates)
        if len(p):
            final_state.append(state)
    print(final_state)
    dfa['final_states'] = final_state

    final_dfa['states'] = []
    final_dfa['letters'] = nfa['letters']
    final_dfa['start_states']= []
    final_dfa['final_states']= []
    final_dfa['transition_function']= []
    
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

    graph = generate_transition_graph(final_dfa)
    graph.render(filename='transition_graph', view=True)
    # print(dfa)
    # print(final_dfa)

def out_dfa():
    global final_dfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(final_dfa, indent = 4))

def generate_transition_graph(nfa):
    start_states = nfa['start_states']
    transition_function = nfa['transition_function']
    graph = Digraph(format='png')

    for transition in transition_function:
        start_state, letter, end_state = transition
        graph.node(start_state, shape='doublecircle' if start_state in nfa['final_states'] else 'circle')
        graph.node(end_state, shape='doublecircle' if end_state in nfa['final_states'] else 'circle')
        graph.edge(start_state, end_state, label=letter)

    if len(start_states) == 1:
        start_state = start_states[0]
        graph.node('', shape='none')
        graph.edge('', start_state, label='start')

    return graph

def load_nfa():
    global nfa
    with open(sys.argv[1], 'r') as inpjson:
        nfa = json.loads(inpjson.read())

# Main program
if __name__ == "__main__":
    load_nfa()
    nfa = remove_dead_states(nfa)
    nfaTOdfa(nfa)
    # print(json.dumps(final_dfa, indent=4))
    out_dfa()
    graph = generate_transition_graph(nfa)
    graph.render(filename='transition_graph1', view=True)
