import tomli
import unittest

from gpsolver import SolverTrait, SolverOp, SolverData, sl, school1, school2

# First use: choose package -> install "tomli" 

print(sl.dump())

print(sl.traits)

print("TRAITS")
for x in sl.traits:
  print(x.name)

print(sl.initial_state)
for op in sl.operations:
  print(f"  name: {op.name}")
  print(f"  add: {op.add}")
  print(f"  remove: {op.remove}")
  print(f"  precond: {op.precond}")
  print()


with open("solve_simpledemo.toml","rb") as f:
    simpledemo = SolverData(tomli.load(f))

print(f"Loaded: {simpledemo.title}")

## attempt to apply "a->b"
## add lookup for next time

state = simpledemo.initial_state
print(f"Start state: {state}")
#for op in simpledemo.operations:
#  if op.name == "a->b":

op = simpledemo.operation_lookup['a->b']
newstate = op.apply(state)

print(f"End state: {newstate}")

print(f"this is a problem? no")
print(f"how about this one? {newstate}")

## This is how you run test cases in replit
unittest.main(module='genericsolver_test')

