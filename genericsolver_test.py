import copy
import unittest
import tomli

import gpsolver
from gpsolver import SolverTrait, SolverOp, SolverData, SolverState
from debug import *
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
        """school3 is school2 (broken car) without a way to contact the shop = expect to fail"""
        solverdata = copy.copy(gpsolver.school1)
        solverdata.initial_state = solverdata.safe_trait_set({'kid at home','car needs battery','have money'})
        result = runsolver(solverdata)
        self.assertIsNone(result)

    def test_achieve_5(self):
        """school4 is school1 but wants you to end up with money = expect to fail"""
        dprint(f"goals: {gpsolver.school4.goal_state}")
        result = runsolver(gpsolver.school4)
        self.assertIsNone(result)

    @unittest.skip("Fails with a huge stack trace")
    def test_achieve_6(self):
        """school5 get to school with an extra circular action trying to get the phone number"""
        solverdata = gpsolver.school5
        result = runsolver(solverdata)
        self.assertIsNone(result)
