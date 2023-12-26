# Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
# Date: 25/12/2023

from itertools import chain, combinations # Used to generate the powerset @see powerset(iterable).
import os, sys, argparse, re

def get_command_args() -> tuple:
    """ 
    Returns the arguments provided along the program execution.
    """
    parser = argparse.ArgumentParser(description="Abstract Argumentation Solver - A software which solves VE-CO, DC-CO, DS-CO, VE-ST, DC-ST and DS-ST problems.")
    
    # Arguments for the command.
    parser.add_argument('-f', '--file', type=str, help='The .apx file to read, which contains the Abstract Argumentation Framework information.')
    parser.add_argument('-p', '--param', type=str, help='VE-CO, DC-CO, DS-CO, VE-ST, DC-ST or DS-ST.')
    parser.add_argument('-a', '--args', type=str, help='ARG1,ARG2,...,ARGn the names of the arguments in the query set E (for VE-XX problems) or ARG (for DC-XX and DS-XX problems).')
    
    # Read args in the command.
    command_args = parser.parse_args()

    # Regular expression for arguments. Can be any sequence of letters (upper case or lower case), numbers, 
    # or the underscore symbol _, with the exception of the following sequences: "att" and "arg".
    regex_pattern = re.compile(r"^(?!att$|arg$)\w+$")

    # Get command args.
    file_name = command_args.file # Recover the file containing the Argumentation Framework information to read (.apx).
    problem_name = command_args.param # Recover the name of the problem (VE-CO, DC-CO, DS-CO...).
    args_value = set(command_args.args.split(",")) # Recover the argument set to query.

    # Checks for valid arguments. Raise a ValueError if at least one of them is not valid.
    if not all(regex_pattern.match(argument) for argument in args_value):    
        raise ValueError("Unaccepted argument(s). The name of an argument can be any sequence of letters " +
                         "(upper case or lower case), numbers, or the underscore symbol _, except the " +
                         "words 'arg' and 'att' which are reserved for defining the lines.")

    # Raise a ValueError if the number of provided arguments is not coherent with the specified problem.
    if not is_number_of_arguments_valid(args_value, problem_name):
        raise ValueError("Only one argument should be specified for the Determine-XX problems.")

    return problem_name, file_name, args_value


def is_number_of_arguments_valid(arg_set: set, param: str) -> bool:
    """ 
    Checks if the number of provided arguments is valid or not.
    Only one should be specified when using the Determine-XX problems.
    """
    if param.startswith("DC") or param.startswith("DS"):
        return not len(arg_set) != 1
    return True


def read_AF_from_file(file_path: str) -> dict:
    """
    Returns the argumentation framework (AF) read from the specified file as a dictionary.
    Key : attacking argument, Value : set of the arguments it attacks.
    """
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)

    graph = {}
        
    with open(file_path, 'r') as file:
        for line in file:
            content = line[line.find("(")+1 : line.find(")")]
            if line.startswith("arg"):
                argument = content
                graph[argument] = set()
            elif line.startswith("att"):
                attacker, attacked = content.split(',')[0], content.split(',')[1]
                graph[attacker].add(attacked)
                
    return graph


def is_admissible(arg_framework: dict, arg_set: set) -> bool:
    """ 
    Checks if the provided set is admissible, or not. 
    """
    # The empty set is always an admissible set, although never used since we cannot provide empty sets as a program argument.
    if len(arg_set) == 0: return True
    
    # The set has to be conflict-free to be admissible.
    if not is_conflict_free(arg_framework, arg_set): return False
    
    # If attacked, each argument of the set must be defended by another (from the set) for the set to be admissible.
    return all(is_defended(arg_framework, arg_set, argument) for argument in arg_set)


def is_defended(arg_framework: dict, arg_set: set, argument: str) -> bool:
    """ 
    Checks if the provided argument is defended by at least one other argument of the given set, or not. 
    """
    # Return True if at least one argument of the set defends the argument in case of an attack, and False otherwise.
    for attacker in arg_framework:
        attacked_args = arg_framework[attacker]
        if argument in attacked_args:
            if not any(attacker in arg_framework[defender] for defender in arg_set):
                return False
    return True


def is_conflict_free(arg_framework: dict, arg_set: set) -> bool:
    """
    Checks if the provided argument set is conflict-free in the argumentation framework (AF), or not.
    """
    # Return False if any argument from the set attacks another one from the set, and True otherwise
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in arg_set: return False
    return True


def powerset(iterable: set|tuple|list) -> set:
    """ 
    Returns the powerset of the given arguments. In other words, give all possible combinations of arguments as a set of sorted tuples.
    For instance, powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3).
    Inspired by the powerset recipe provided in the following documentation: https://docs.python.org/3/library/itertools.html#itertools-recipes.
    """
    s = list(iterable) 
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def is_a_complete_extension(arg_framework: dict, arg_set: set) -> bool:
    """ 
    Checks if the provided argument set is a complete extension, or not.
    """
    # The set has to be admissible to be a complete extension.
    if not is_admissible(arg_framework, arg_set): return False 
    
    # Create a set of all arguments of the framework that are not in the provided argument set.
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # Return False if at least one argument that isn't in the provided set is defended by an argument of the set, and True otherwise.
    return not any(is_defended(arg_framework, arg_set, other_arg) for other_arg in other_args)


def find_all_complete_extensions(arg_framework: dict) -> set:
    """
    Returns the set of all complete extensions of the argumentation framework.
    """
    all_complete_extensions = set()
    
    # Iterate over every possible combination of arguments in the framework,
    # and add it to the all_complete_extensions set if it is a complete extension.
    all_arguments = list(arg_framework.keys())
    for arg_set in powerset(all_arguments): # powerset() returns every combination of the provided arguments as a set of sorted tuples.
        if is_a_complete_extension(arg_framework, arg_set):
            all_complete_extensions.add(arg_set)
            
    return all_complete_extensions
    

def find_all_stable_extensions(arg_framework: dict) -> set:
    """
    Returns the set of all stable extensions of the argumentation framework.
    """
    all_stable_extensions = set()

    # Iterate over every possible combination of arguments in the framework,
    # and add it to the all_stable_extensions set if it is a stable extension.
    all_arguments = list(arg_framework.keys())
    for arg_set in powerset(all_arguments): # powerset() returns every combination of the provided arguments as a set of sorted tuples.
        if verify_stable_extension(arg_framework, arg_set):
            all_stable_extensions.add(arg_set)

    return all_stable_extensions


def verify_complete_extension(arg_framework: dict, arg_set: set) -> bool:
    """
    Determine whether the provided argument set is a complete extension of the argumentation framework, or not.
    """
    complete_extensions = find_all_complete_extensions(arg_framework)
    return tuple(sorted(arg_set)) in complete_extensions # Sort the set for the comparison to work properly. Otherwise, (A,D) != (D,A).


def decide_complete_credulous(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Credulous acceptability of the given argument with respect to σ = complete.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    complete_extensions = find_all_complete_extensions(arg_framework)
    return any(argument in complete_extension for complete_extension in complete_extensions)


def decide_complete_skeptical(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Skeptical acceptability of the given argument with respect to σ = complete.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    complete_extensions = find_all_complete_extensions(arg_framework)
    return all(argument in complete_extension for complete_extension in complete_extensions)


def verify_stable_extension(arg_framework: dict, arg_set: set) -> bool:
    """
    Determine whether the provided argument set is a stable extension of the argumentation framework, or not.
    """
    # The set has to be conflict-free to be a stable extension.
    if not is_conflict_free(arg_framework, arg_set): return False
        
    # Create a set of all arguments of the framework that are not in the provided argument set.
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # The argument set is a stable extension if all other arguments of the framework are attacked by the provided arguments.
    # arg_set is stable if all arguments in other_args are attacked.
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in other_args:
                other_args.remove(attacked_arg)

    if len(other_args) == 0: # All args were attacked, so arg_set is stable.
        return True
    return False


def decide_stable_credulous(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Credulous acceptability of the given argument with respect to σ = stable.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    stable_ext = find_all_stable_extensions(arg_framework)
    return any(argument in stable for stable in stable_ext)


def decide_stable_skeptical(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Skeptical acceptability of the given argument with respect to σ = stable.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    stable_ext = find_all_stable_extensions(arg_framework)
    return all(argument in stable for stable in stable_ext)


def is_argument_set_in_AF(arg_framework: dict, arg_set: set) -> bool:
    """
    Checks if an argument or an argument set is included in the argumentation framework, or not.
    """
    return all(argument in arg_framework.keys() for argument in arg_set)


def solve_problem(param: str, arg_framework: dict, arg_set: set) -> bool:
    """
    Returns either True (YES) or False (NO) depending on the problem for the result to be printed in main().
    """
    # Return False if at least one of the arguments in the provided set does not belong to the argumentation framework.
    if not is_argument_set_in_AF(arg_framework, arg_set): return False

    if param == "VE-CO":
        return verify_complete_extension(arg_framework, arg_set)
    elif param == "DC-CO":
        return decide_complete_credulous(arg_framework, arg_set)
    elif param == "DS-CO":
        return decide_complete_skeptical(arg_framework, arg_set)
    elif param == "VE-ST":
        return verify_stable_extension(arg_framework, arg_set)
    elif param == "DC-ST":
        return decide_stable_credulous(arg_framework, arg_set)
    elif param == "DS-ST":
        return decide_stable_skeptical(arg_framework, arg_set)
    else:
        raise ValueError("Unknown parameter.\n" +
                         "Please choose one of these : VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.")
    

def print_result(result: bool):
    """
    Prints "YES" if the provided problem result is True, and "NO" otherwise.
    """
    if result: print("YES")
    else: print("NO")


#=========================================================#
        
        
def main():
    try:
        param, file, arg_set = get_command_args() # Recover the arguments provided with the script execution.

        arg_framework = read_AF_from_file(file)

        result = solve_problem(param, arg_framework, arg_set)
        print_result(result)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

