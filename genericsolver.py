import gpsolver
from gpsolver import SolverTrait, SolverOp, SolverData, SolverState
from typing import List, Tuple, Set, FrozenSet, Optional
from debug import dprint

MoveList = List[SolverOp]

def runsolver(solverdata: SolverData) -> SolverState:
    # FIXME
    return solverdata.initial_state
