import sys
import os

sys.path.append(os.path.join("pkg"))
from state import State

closed = [(State(0, 0), 0.0), (State(1, 1), 0.0)]

states, costs = list(map(list, zip(*closed)))

print(State(0, 0) in states)
print(State(1, 0) in states)
print(State(1, 1) in states)