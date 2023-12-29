# AF_solver.py

"""
This file implements an Abstract Argumentation Solver.
The solver allows users to pose some problems related to Argumentation Frameworks (AF) using a command prompt (cmd) and provides responses 'YES' or 'NO' accordingly.

Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
Creation Date: 25/12/2023
"""

import os, sys, argparse, re, AF_util, AF_extensions

def get_command_args() -> tuple:
    """ 
    Returns the arguments provided along the program execution.
    """
    parser = argparse.ArgumentParser(description="Abstract Argumentation Solver - A software which solves VE-CO, DC-CO, DS-CO, VE-ST, DC-ST and DS-ST problems.")
    
    # Arguments for the command.
    parser.add_argument('-f', '--file', type=str, help='The .apx file to read, which contains the Abstract Argumentation Framework information.')
    parser.add_argument('-p', '--problem', type=str, help='VE-CO, DC-CO, DS-CO, VE-ST, DC-ST or DS-ST.')
    parser.add_argument('-a', '--arguments', type=str, nargs='?', help='ARG1,ARG2,...,ARGn the names of the arguments in the query set E (for VE-XX problems) or ARG (for DC-XX and DS-XX problems). '
                        'Use without any value or leave it out to test an empty set as an argument.')
    
    # Read args in the command.
    command_args = parser.parse_args()

    # Regular expression for arguments. Can be any sequence of letters (upper case or lower case), numbers, 
    # or the underscore symbol _, with the exception of the following sequences: "att" and "arg".
    regex_pattern = re.compile(r"^(?!att$|arg$)\w+$")

    # Get command args.
    file_name = command_args.file # Recover the file containing the Argumentation Framework information to read (.apx).
    problem_name = command_args.problem # Recover the name of the problem (VE-CO, DC-CO, DS-CO...).
    
    args_value = "" if command_args.arguments is None else set(command_args.arguments.split(","))

    # Checks for valid arguments. Raise a ValueError if at least one of them is not valid.
    if not all(regex_pattern.match(argument) for argument in args_value):    
        raise ValueError("Unaccepted argument(s). The name of an argument can be any sequence of letters " +
                         "(upper case or lower case), numbers, or the underscore symbol _, except the " +
                         "words 'arg' and 'att' which are reserved for defining the lines.")

    # Raise a ValueError if the number of provided arguments is not coherent with the specified problem.
    if not AF_util.is_number_of_arguments_valid(args_value, problem_name):
        raise ValueError("Only one argument should be specified for the Determine-XX problems.")

    return problem_name, file_name, args_value


def read_AF_from_file(file_path: str) -> dict:
    """
    Returns the argumentation framework (AF) read from the specified file as a dictionary.
    Key : attacking argument, Value : set of the arguments it attacks.
    """
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)

    graph = {}
    # Regular expression for arguments. 
    # Each argument is defined in a line of the form "arg(name_argument)." 
    # Each attack is defined in a line of the form "att(name_argument_1,name_argument_2)."
    regex_pattern = re.compile(r'^(arg\(\w+\)|att\(\w+,\w+\))\.$')

    with open(file_path, 'r') as file:
        for line in file:
            # Checks for valid syntax for the representation of the AF in the text file. Raise a ValueError if at least one of them is not valid.
            if not regex_pattern.match(line):
                raise ValueError("Unaccepted argument or attack for the representation of the AF in the text file.\n"+ 
                                "Each argument must be defined in a line of the form 'arg(name_argument).'\n"+
                                "Each attack must be defined in a line of the form 'att(name_argument_1,name_argument_2).'.")
            content = line[line.find("(")+1 : line.find(")")]
            if line.startswith("arg"):
                argument = content
                graph[argument] = set()
            elif line.startswith("att"):
                attacker, attacked = content.split(',')[0], content.split(',')[1]
                if not attacker in graph.keys():
                    raise ValueError("One of the attacker is not part of the arguments. All arguments must be defined before attacks.")
                graph[attacker].add(attacked)
                
    return graph


def solve_problem(problem: str, arg_framework: dict, arg_set: set) -> bool:
    """
    Returns either True (YES) or False (NO) depending on the problem for the result to be printed in main().
    """
    # Return False if at least one of the arguments in the provided set does not belong to the argumentation framework.
    if not AF_util.is_argument_set_in_AF(arg_framework, arg_set): return False

    if problem == "VE-CO":
        return  AF_extensions.verify_complete_extension(arg_framework, arg_set)
    elif problem == "DC-CO":
        return  AF_extensions.decide_complete_credulous(arg_framework, arg_set)
    elif problem == "DS-CO":
        return  AF_extensions.decide_complete_skeptical(arg_framework, arg_set)
    elif problem == "VE-ST":
        return  AF_extensions.verify_stable_extension(arg_framework, arg_set)
    elif problem == "DC-ST":
        return  AF_extensions.decide_stable_credulous(arg_framework, arg_set)
    elif problem == "DS-ST":
        return  AF_extensions.decide_stable_skeptical(arg_framework, arg_set)
    else:
        raise ValueError("Unknown parameter.\n" +
                         "Please choose one of these : VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.")


def print_result(result: bool):
    """
    Prints "YES" if the provided problem result is True, and "NO" otherwise.
    """
    if result: print("YES")
    else: print("NO")                         