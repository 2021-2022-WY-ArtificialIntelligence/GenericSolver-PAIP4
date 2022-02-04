import copy
import unittest
import tomli

import gpsolver
from gpsolver import SolverTrait, SolverOp, SolverData, SolverState
from debug import dprint
from genericsolver import MoveList, runsolver


class TestGeneric(unittest.TestCase):
    def test_achieve_1(self):
        with open("solve_simpledemo.toml", "rb") as infile:
            solverdata = SolverData(tomli.load(infile))
        result = runsolver(solverdata)
        self.assertIsNotNone(result)
        self.assertTrue(solverdata.goal_state <= result)

    def test_achieve_2(self):
        """Check the gpsolver.school1 problem (simple)"""
        solverdata = gpsolver.school1
        result = runsolver(solverdata)
        self.assertIsNotNone(result)
        self.assertTrue(solverdata.goal_state <= result)

    def test_achieve_3(self):
        """Check the gpsolver.school2 problem (harder)"""
        solverdata = gpsolver.school2
        result = runsolver(solverdata)
        self.assertIsNotNone(result)
        self.assertTrue(solverdata.goal_state <= result)

    def test_achieve_4(self):
        """school2 without a way to contact the shop = expect to fail"""
        solverdata = copy.copy(gpsolver.school2)
        solverdata.initial_state = solverdata.safe_trait_set({'kid at home','car needs battery','have money'})
        result = runsolver(solverdata)
        self.assertIsNone(result)
