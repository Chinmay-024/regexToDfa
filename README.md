
# Conversion from Regex to DFA

One script converts a regular expression (regex) into a Non-Deterministic Finite Automaton (NFA) and saves the NFA in JSON format. It also generates a graph representation of the NFA using Graphviz. Then another script converts epsilon NFA to NFA. Third one converts NFA to DFA and finally we minimize DFA






## Commands


To install library for getting graph

```bash
  pip install graphviz
```

To convert regex to epsilon nfa
```bash
  python3 regexToEnfa.py output.json
```

Note that while generating output.json it converts epsilon to \u03b5 as epsilon symbol gets converted to escape format in json. But while reading in python it will automatically convert to epsilon.

To convert epsilon nfa to nfa
```bash
  python3 regexToEnfa.py output.json nfa.json
``` 

Similarly for rest


## Screenshots

![App Screenshot](https://drive.google.com/uc?export=view&id=1FGmZ3PwHf9cfNvDQSc9NJs2LV-6vYneV)
epsilon-NFA for *a+b*

![App Screenshot](https://drive.google.com/uc?export=view&id=1LaINOhHhHkgSNZ-HvzOr00TUJEaemHId)
NFA for *a+b*

Json file will also get automatically generated along with this while running the code which contains transitions.