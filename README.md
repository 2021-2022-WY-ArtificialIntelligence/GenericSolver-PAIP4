# GenericSolver

Automatically runs the main file, which executes the tests in `genericsolver_test.py`.

* GitHub.
    https://github.com/2021-2022-WY-ArtificialIntelligence/GenericSolver-PAIP4.git

* ReplIt
    https://replit.com/@maueroats/GenericSolver-PAIP4#README.md
    
## Notes

* The set with no elements is `[]` not `[""]`. Do not make any sets containing the empty string.
* Produce a set of traits by using the `trait_set` function:

      solverdemo.traitset[{"red shirt", "blue pants"}]
* Find a single `SolverTrait` object by using the lookup dictionary:

      solverdemo.operation_lookup["red shirt on"]
* If you want to interact with your main file, modify the `.replit` config so it says:

      run = "python -i main.py"
      
