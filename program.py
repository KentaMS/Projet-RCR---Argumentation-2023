# AF_program.py

"""
Main module for the Abstract Argumentation Solver.
This module serves as the entry point for the abstract argumentation solver project. It coordinates the execution of the solver and other relevant functionalities.
To run the abstract argumentation solver, execute this module using a command prompt (cmd).
Please refer to the helper by running: "python program.py --help" to view the expected arguments.

Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
Date: 25/12/2023
"""

import sys, AF_solver

def main():
    try:
        param, file, arg_set = AF_solver.get_command_args() # Recover the arguments provided with the script execution.

        arg_framework = AF_solver.read_AF_from_file(file) # Building the argumentation framework.

        result = AF_solver.solve_problem(param, arg_framework, arg_set) # Solving problem according to the arguments of the command line.
        AF_solver.print_result(result) # Printing result

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

