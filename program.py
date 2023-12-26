# Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
# Date: 25/12/2023

from itertools import chain, combinations # Used to generate the powerset @see powerset(arguments)
import os, sys, argparse, re

# Get arguments in the command line
def get_command_args():
    parser = argparse.ArgumentParser(description="Abstract Argumentation Solver - A software which solves VE-CO, DC-CO, DS-CO, VE-ST, DC-ST and DS-ST problems.")
    
    # Arguments for the command
    parser.add_argument('-f', '--file', type=str, help='The .apx file to read, which contains the Abstract Argumentation Framework information.')
    parser.add_argument('-p', '--param', type=str, help='VE-CO, DC-CO, DS-CO, VE-ST, DC-ST or DS-ST.')
    parser.add_argument('-a', '--args', type=str, help='ARG1,ARG2,...,ARGn the names of the arguments in the query set E (for VE-XX problems) or ARG (for DC-XX and DS-XX problems).')
    
    # Read args in the command
    command_args = parser.parse_args()

    # Regular expression for arguments. Can be any sequence of letters (upper case or lower case), numbers, 
    # or the underscore symbol _, with the exception of the following sequences: "att" and "arg"
    regex_pattern = re.compile(r"^(?!att$|arg$)\w+$")

    # Get command args
    file_name = command_args.file # file to read (.apx)
    problem_name = command_args.param # param for the problem (VE-CO, DC-CO, DS-CO...)
    if len(command_args.args) > 1 :
        args_value = set(command_args.args.split(",")) # Set of arguments
    else:
        args_value = command_args.args # arg

    # Checks for valid arguments. Raise a ValueError if at least one of them is not
    if not all(regex_pattern.match(argument) for argument in args_value):    
        raise ValueError("Unaccepted argument(s). The name of an argument can be any sequence of letters " +
                         "(upper case or lower case), numbers, or the underscore symbol _, except the " +
                         "words 'argument' and 'att' which are reserved for defining the lines.")

    # Raise a ValueError if the number of provided arguments is not coherent with the specified problem
    if not is_number_of_arguments_valid(args_value, problem_name):
        raise ValueError("Only one argument should be specified for the Determine-XX problems.")

    return problem_name, file_name, args_value


# Checks if the number of provided arguments is valid or not (only one should be specified when using the Determine-XX problems)
def is_number_of_arguments_valid(arg_set, param):
    if param.startswith("DC") or param.startswith("DS"):
        return not len(arg_set) != 1
    return True


# Returns the argumentation framework (AF) read from the specified file as a dictionary
# key: attacking argument, value : set of the args it attacks
def read_AF_from_file(file_path):
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


# Checks if the provided set is admissible
def is_admissible(arg_framework, arg_set):

    # The empty set is always an admissible set
    if len(arg_set) == 0: return True
    
    # The set has to be conflict-free to be admissible
    if not is_conflict_free(arg_framework, arg_set): return False
    
    # If attacked, each argument of the set must be defended by another (from the set) for the set to be admissible
    return all(is_defended(arg_framework, arg_set, argument) for argument in arg_set)


# Checks if the provided argument is defended by at least one other argument of the given set
def is_defended(arg_framework, arg_set, argument):

    # Return True if at least one argument of the set defends the argument in case of an attack, and False otherwise
    for attacker in arg_framework:
        attacked_args = arg_framework[attacker]
        if argument in attacked_args:
            if not any(attacker in arg_framework[defender] for defender in arg_set):
                return False
    return True


# Checks if the provided argument set is conflict-free in the argumentation framework (AF)
def is_conflict_free(arg_framework, arg_set):

    # Return False if any argument from the set attacks another one from the set, and True otherwise
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in arg_set: return False
    return True


# Returns the powerset of the given arguments. In other words, give all possible combinations of arguments as a set of subsets.
# Inspired by the powerset recipe under the following documentation: https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(arguments):
    arg_list = list(arguments)
    return set(chain.from_iterable(combinations(arg_list, r) for r in range(len(arg_list) + 1)))


# Checks if the provided argument set is a complete extension
def is_a_complete_extension(arg_framework, arg_set):

    # The set has to be admissible to be a complete extension
    if not is_admissible(arg_framework, arg_set): return False
    
    # Create a set of all arguments of the framework that are not in the provided argument set
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # Return False if at least one argument that isn't in the provided set is defended by an argument of the set, and True otherwise
    return not any(is_defended(arg_framework, arg_set, other_arg) for other_arg in other_args)


# Returns the set of all complete extensions of the argumentation framework
def find_all_complete_extensions(arg_framework):
    all_complete_extensions = set()
    
    # Iterate over every possible combination of arguments in the framework 
    # and add it to the all_complete_extensions set if it is a complete extension
    all_arguments = arg_framework.keys()
    for arg_set in powerset(all_arguments): # powerset() returns every combination of the provided arguments
        if is_a_complete_extension(arg_framework, arg_set):
            all_complete_extensions.add(tuple(sorted(arg_set))) # Sort the set in order for the comparison to work properly in verify_complete_extension
            
    return all_complete_extensions
    

# Returns the set of all stable extensions of the argumentation framework
def find_all_stable_extensions(arg_framework):
    all_stable_extensions = set()

    # Iterate over every possible combination of arguments in the framework 
    # and add it to the all_stable_extensions set if it is a stable extension
    all_arguments = arg_framework.keys()
    for arg_set in powerset(all_arguments): # powerset() returns every combination of the provided arguments
        if verify_stable_extension(arg_framework, arg_set): # Keep the ones that are stable
            all_stable_extensions.add(tuple(sorted(arg_set)))

    return all_stable_extensions


# Determine whether the provided argument set is a complete extension of the argumentation framework or not
def verify_complete_extension(arg_framework, arg_set):
    complete_extensions = find_all_complete_extensions(arg_framework)
    return tuple(sorted(arg_set)) in complete_extensions


# Decide the Credulous acceptability of the given argument with respect to σ = complete
def decide_complete_credulous(arg_framework, argument):
    if argument == "": return True
    complete_extensions = find_all_complete_extensions(arg_framework)
    return any(argument in complete_extension for complete_extension in complete_extensions)


# Decide the Skeptical acceptability of the given argument with respect to σ = complete
def decide_complete_skeptical(arg_framework, argument):
    if argument == "": return False
    complete_extensions = find_all_complete_extensions(arg_framework)
    return all(argument in complete_extension for complete_extension in complete_extensions)


# Determine whether the provided argument set is a stable extension of the argumentation framework or not
def verify_stable_extension(arg_framework, arg_set):

    # The set has to be conflict-free to be a stable extension
    if not is_conflict_free(arg_framework, arg_set): return False
        
    # Create a set of all arguments of the framework that are not in the provided argument set
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # arg_set is stable if all args in other_args are attacked
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in other_args:
                other_args.remove(attacked_arg)

    if len(other_args) == 0: # All args were attacked, so arg_set is stable
        return True
    return False


# Decide the Credulous acceptability of the given argument with respect to σ = stable
def decide_stable_credulous(arg_framework, argument):
    stable_ext = find_all_stable_extensions(arg_framework)
    return any(argument in stable for stable in stable_ext)


# Decide the Skeptical acceptability of the given argument with respect to σ = stable
def decide_stable_skeptical(arg_framework, argument):
    stable_ext = find_all_stable_extensions(arg_framework)
    return all(argument in stable for stable in stable_ext)


# Checks if an argument or an argument set is included in the argumentation framework, or not
def is_argument_set_in_AF(arg_framework, arg_set):
    return all(argument in arg_framework.keys() for argument in arg_set)


# Returns either True (YES) or False (NO) depending on the problem
def solve_problem(param, arg_framework, arg_set):

    # Return False if at least one of the arguments in the provided set does not belong to the argumentation framework
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


#=========================================================#
        
        
def main():
    try:
        param, file, arg_set = get_command_args() # Recover the arguments provided with the script execution

        path_to_data = "./data/"
        arg_framework = read_AF_from_file(path_to_data + file)

        if solve_problem(param, arg_framework, arg_set): print("YES")
        else: print("NO")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

