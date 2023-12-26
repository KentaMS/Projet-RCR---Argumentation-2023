from itertools import chain, combinations # Used to generate the powerset @see powerset(arguments)
import os, sys, argparse, re

# Get arguments in the command line
def get_command_args():
    parser = argparse.ArgumentParser(description="Abstract Argumentation Solver - A software which solves VE-CO, DC-CO, DS-CO, VE-ST, DC-ST, DS-ST problems.")
    
    # Arguments for the command
    parser.add_argument('-p', '--param', type=str, help='VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.')
    parser.add_argument('-f', '--file', type=str, help='File.apx to read (Describe an Argumentation Framework AF).')
    parser.add_argument('-a', '--args', type=str, help='ARG1,ARG2,...,ARGn the names of the arguments in the query set S (for VE-XX problems) or ARG (for DC-XX or DS-XX problems).')
    
    # Read args in the command
    command_args = parser.parse_args()

    # regular expression for arguments (any sequence of letters (upper case or lower case), numbers, or the underscore symbole _)
    regex_pattern = re.compile(r"^(?!att$|arg$)[a-zA-Z0-9_]+$")

    # Get command args
    param_value = command_args.param # param for the problem (VE-CO, DC-CO, DS-CO...)
    file_value = command_args.file # file to read (.txt)
    if len(command_args.args) > 1 :
        args_value = set(command_args.args.split(",")) # set of args
    else:
        args_value = command_args.args # arg

    # Checks valid arguments
    for argument in args_value:
        if not regex_pattern.match(argument):
            print("Unaccepted argument(s)) Remember, the name of an argument can be any sequence of letters (upper case or lower case), numbers, or the underscore symbole _, except the words argument and att which are reserved for defining the lines.")
            sys.exit(1)

    check_number_of_arguments(args_value, param_value)

    return param_value, file_value, args_value


# Checks if the number of provided arguments is valid (Only one should be given when using the determine problems)
def check_number_of_arguments(arg_set, param):
    if(param.startswith("DC") or param.startswith("DS")):
        if len(arg_set) != 1:
            print("Only one argument should be specified for the determine problems.")
            sys.exit(1)


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
def powerset(arguments):
    s = list(arguments)
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


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
            all_complete_extensions.add(tuple(arg_set))
            
    return all_complete_extensions
    

# Returns the set of all stable extensions of the argumentation framework
def find_all_stable_extensions(arg_framework):
    all_stable_extensions = set()

    # Iterate over every possible combination of arguments in the framework 
    # and add it to the all_stable_extensions set if it is a stable extension
    all_arguments = arg_framework.keys()
    for arg_set in powerset(all_arguments): # powerset() returns every combination of the provided arguments
        if verify_stable_extension(arg_framework, arg_set): # Keep the ones that are stable
            all_stable_extensions.add(tuple(arg_set))

    return all_stable_extensions


# Determine whether the provided argument set is a complete extension of the argumentation framework or not
def verify_complete_extension(arg_framework, arg_set):
    complete_extensions = find_all_complete_extensions(arg_framework)
    return tuple(arg_set) in complete_extensions


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
    # Check if arg_set is conflict free
    if not is_conflict_free(arg_framework, arg_set):
        return False

    # arg_set is stable if all args in others_args are attacked
    others_args = {argument for argument in arg_framework.keys() if argument not in arg_set} # set of others args

    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in others_args:
                others_args.remove(attacked_arg)

    if len(others_args) == 0: # All args were attacked, then arg_set is stable
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


# Returns either YES or NO depending on the problem
def solve_problem(param, arg_framework, arg_set):

    # Return NO if at least one of the arguments in the provided set does not belong to the argumentation framework
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
        print("Error : Unknown parameter.")
        print("Please choose one of these : VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.")
        sys.exit(1)


#=========================================================#
        
        
def main():
    param, file, arg_set = get_command_args() # Recover the arguments provided with the script execution
    path_to_data = "./data/"
    arg_framework = read_AF_from_file(path_to_data + file)
    if solve_problem(param, arg_framework, arg_set): print("YES")
    else: print("NO")

if __name__ == '__main__':
    main()

