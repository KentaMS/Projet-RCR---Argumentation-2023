from itertools import chain, combinations # Used to generate the powerset @see powerset(arguments)
import os

# Returns the argumentation framework (AF) read from the specified file
def read_AF_from_file(path, file_name):
    graph = {}
        
    with open(path + file_name, 'r') as file:
        for line in file:
            content = line[line.find("(")+1 : line.find(")")]
            if "arg" in line:
                argument = content
                graph[argument] = set()
            elif "att" in line:
                attack = content.split(',')
                graph[attack[0]].add(attack[1])
                
    return graph



# Checks if the provided argument set is conflict-free
def is_conflict_free(arg_framework, arg_set):

    # Return False if any argument from the set attacks another one from the set, and True otherwise
    for attacker in arg_set:
        for attacked in arg_set:
            if attacked in arg_framework[attacker]: return False
    return True


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
    
# Returns the powerset of the given arguments. In other words, give all possible combinations of arguments as a set of subsets.
def powerset(arguments):
    s = list(arguments)
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


# Checks if the provided argument set is a complete extension of the argumentation framework or not
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

#=========================================================#
