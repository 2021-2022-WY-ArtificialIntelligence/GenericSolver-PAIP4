from dataclasses import dataclass
from typing import List, Tuple, Set, FrozenSet
import unittest
import tomli
import copy

@dataclass(frozen=True)
class SolverTrait():
    name: str
    def __repr__(self):
        return self.name

SolverState = FrozenSet[SolverTrait]
# also works but easier to mess up --> Set[SolverTrait]

@dataclass(frozen=True)
class SolverOp():
    name: str
    precond: SolverState
    add: SolverState
    remove: SolverState

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"[Op: {self.name} with preconditions {self.precond}, adding {self.add} and removing {self.remove}"

    @staticmethod
    def read_str(s: str) -> 'SolverOp':
        name_s, prereq_1, gain_1, lose_1 = s.strip().split()

    # Do not include
    def apply(self, state: SolverState) -> SolverState:
        if not self.precond <= state:
            raise ValueError(f"cannot apply {self.name} to state {state}")
        return (state - self.remove) | self.add

class SolverTest(unittest.TestCase):
    def test_simple_1(self):
        """Check the basic functioning of SolverTrait, SolverState, and SolverOp."""
        a = SolverTrait("a")
        b = SolverTrait("b")
        c = SolverTrait("c")
        op = SolverOp("a->b", {a,c}, {b}, {a})
        original = {a,c}
        result = op.apply(original)
        self.assertEqual(result, {b,c})


"""## Data file format, first draft
# TRAITS 5
student
graduate
poor
employed
wealthy
BMW
# OPERATIONS 4
study {student} {graduate} {student}
jobsearch {graduate} {employed} {}
work {employed} {wealthy} {}
splurge {wealthy} {BMW} {wealthy}
# INITIAL STATE 2
student
poor
# GOAL STATE 2
employed 
BMW
"""

student_life_txt = """
title = "Student Life Example"

traits = ["student", "graduate", "poor", "employed", "wealthy", "BMW", "yacht"]
initial_state = ["student", "poor"]
goal_state = ["BMW", "employed"]

[[operations]]
name = "study"
precond = ["student"]
add = ["graduate"]
remove = ["student"]

[[operations]]
name = "jobsearch"
precond = ["graduate"]
add = ["employed"]
remove = []

[[operations]]
name = "work"
precond = ["employed"]
add = ["wealthy"]
remove = []

[[operations]]
name = "splurge"
precond = ["wealthy"]
add = ["BMW","yacht"]
remove = ["wealthy"]

"""

class SolverData():
    def safe_trait_set(self, xs):
        try:
            return frozenset(self.trait_lookup[x] for x in xs)
        except KeyError as k:
            raise ValueError(f'unknown trait "{k.args[0]}", possible causes: misspelling or not defined in traits') from k
    def __init__(self, kv):
        """Keys required: 'traits', 'initial_state', 'goal_state', 'operations'."""
        self.title =  kv['title'] if 'title' in kv else "UNTITLED"
        self.trait_lookup = {t : SolverTrait(t) for t in kv['traits']}
        self.traits = self.trait_lookup.values()
        self.initial_state = self.safe_trait_set(kv['initial_state'])
        self.goal_state =  self.safe_trait_set(kv['goal_state'])
        self.operations = [SolverOp(name=op['name'],
                                    precond=self.safe_trait_set(op['precond']),
                                    add=self.safe_trait_set(op['add']),
                                    remove=self.safe_trait_set(op['remove']))
                           for op in kv['operations']]
        self.operation_lookup = {op.name: op for op in self.operations}
        self.trait_set = self.safe_trait_set # legacy already?


    def dump(self):
        def commalist(xs):
            return ",".join(list(map(lambda x: f'"{x.name}"', xs)))

        out = [f'title="{self.title}"']
        traits = commalist(self.traits)
        out.append(f'traits=[{traits}]')

        initial_states = commalist(self.initial_state)
        out.append(f'initial_state=[{initial_states}]')

        goal_states = commalist(self.goal_state)
        out.append(f'goal_state=[{goal_states}]')

        for op in self.operations:
            out.extend(['[[operations]]',
                        f'name="{op.name}"',
                        f'precond=[{commalist(op.precond)}]',
                        f'add=[{commalist(op.add)}]',
                        f'remove=[{commalist(op.remove)}]'
                       ])
        return '\n'.join(out)

class TestSolverData(unittest.TestCase):
    def setUp(self) -> None:
        student_life_1 = tomli.loads(student_life_txt)
        self.student_life = SolverData(student_life_1)

    def test_read_1(self):
        self.assertEqual(self.student_life.trait_set({'poor','student'}),
                         self.student_life.initial_state)
        self.assertEqual(self.student_life.trait_set({'employed','BMW'}),
                         self.student_life.goal_state)
    def test_mistake_1(self):
        """Verify that using unknown traits raises an error."""

        undelared_trait = """
title = "test_mistake_1"
traits = ["A","B","C","D"]
initial_state = ["A", "B"]
goal_state = ["A", "D"]
[[operations]]
name = "eee"
precond = ["A","B"]
add = ["C","F"]
remove = ["B"]
"""
        # Should throw Value Error
        def thunk():
            SolverData(tomli.loads(undelared_trait))
        self.assertRaises(ValueError, thunk)

sl = SolverData(tomli.loads(student_life_txt))

simpledemo = """
title="simple demo"
initial_state=["sandwich","cookie"]
[[traits]]
name="sandwich"
[[traits]]
name="milk"
[[traits]]
name="cookie"
"""

d = tomli.loads(simpledemo)

with open("solve_toschool.toml","rb") as f:
    school1 = SolverData(tomli.load(f))

school2 = copy.copy(school1)
school2.title = "Get to school, harder version"
school2.initial_state = school2.safe_trait_set({'kid at home', 'car needs battery', 'have money', 'have internet'})

school3 = copy.copy(school1)
school3.title = "Get to school, impossible version, should fail"
school3.initial_state = school3.safe_trait_set({'kid at home','car needs battery','have money'})

