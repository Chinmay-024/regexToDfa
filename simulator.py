import json
import sys

dfa = {}

def load_dfa():
    global dfa
    with open(sys.argv[1], 'r') as inpjson:
        dfa = json.loads(inpjson.read())

def dfs(dfa, current_state, visited_states, exp ,index):
    if index == len(exp):
        if current_state in dfa['final_states']:
            return True
        else:
            return False
        
    letter = exp[index]   
    transitions = [t[2] for t in dfa['transition_function'] if t[0] == current_state and t[1] == letter]
    
    for state in transitions:
            if dfs(dfa, state, visited_states,exp,index+1):
                return True
    return False

if __name__ == "__main__":
    load_dfa()
    while(1):
        status = input("Do you want to enter a string? (y/n)")
        if status == "n":
            break
        else:
            exp = input("Enter a string: ")
            current_state = dfa['start_states'][0]
            visited_states = []
            ans = dfs(dfa, current_state, visited_states, exp, 0)
            if ans:
                print("String satisfies regex pattern")
            else:
                print("String doesn't satisfy regex pattern")


