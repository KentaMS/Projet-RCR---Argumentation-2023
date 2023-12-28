# AF_extensions.py

"""
This file contains methods for computing extensions in an Argumentation Framework (AF).
An Argumentation Framework is a formal structure used to represent and evaluate arguments in argumentative reasoning.
Extensions in an AF are sets of arguments that satisfy certain properties, such as stability or completness.
The methods provided in this file allow the calculation of different extensions in a given AF.

Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
Creation Date: 25/12/2023
"""

import AF_util

def is_conflict_free(arg_framework: dict, arg_set: set) -> bool:
    """
    Checks if the provided argument set is conflict-free in the argumentation framework (AF), or not.
    """
    # Return False if any argument from the set attacks another one from the set, and True otherwise
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in arg_set: return False
    return True

def is_admissible(arg_framework: dict, arg_set: set) -> bool:
    """ 
    Checks if the provided set is admissible, or not. 
    """
    # The empty set is always an admissible set, although never used since we cannot provide empty sets as a program argument.
    if len(arg_set) == 0: return True
    
    # The set has to be conflict-free to be admissible.
    if not is_conflict_free(arg_framework, arg_set): return False
    
    # If attacked, each argument of the set must be defended by another (from the set) for the set to be admissible.
    return all(AF_util.is_defended(arg_framework, arg_set, argument) for argument in arg_set)

def find_all_sigma_extensions(arg_framework: dict, semantics: str) -> set:
    """
    Returns the set of all σ extensions of the argumentation framework.
    """
    all_sigma_extensions = set()
    
    # Iterate over every possible combination of arguments in the framework,
    # and add it to the all_sigma_extensions set if it is an extension with respect to the semantics σ.
    all_arguments = list(arg_framework.keys())
    if semantics == "COMPLETE":
        for arg_set in AF_util.powerset(all_arguments): # powerset() returns every combination of the provided arguments as a set of sorted tuples.
            if verify_complete_extension(arg_framework, arg_set):
                all_sigma_extensions.add(arg_set)
    elif semantics == "STABLE":
        for arg_set in AF_util.powerset(all_arguments):
            if verify_stable_extension(arg_framework, arg_set):
                all_sigma_extensions.add(arg_set)

    return all_sigma_extensions


def verify_complete_extension(arg_framework: dict, arg_set: set) -> bool:
    """
    Determine whether the provided argument set is a complete extension of the argumentation framework, or not.
    """
    # The set has to be admissible to be a complete extension.
    if not is_admissible(arg_framework, arg_set): return False 
    
    # Create a set of all arguments of the framework that are not in the provided argument set.
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # Return False if at least one argument that isn't in the provided set is defended by an argument of the set, and True otherwise.
    return not any(AF_util.is_defended(arg_framework, arg_set, other_arg) for other_arg in other_args)


def verify_stable_extension(arg_framework: dict, arg_set: set) -> bool:
    """
    Determine whether the provided argument set is a stable extension of the argumentation framework, or not.
    """
    # The set has to be conflict-free to be a stable extension.
    if not is_conflict_free(arg_framework, arg_set): return False
        
    # Create a set of all arguments of the framework that are not in the provided argument set.
    other_args = {argument for argument in arg_framework.keys() if argument not in arg_set}

    # The argument set is a stable extension if all other arguments of the framework are attacked by the provided arguments.
    # Then it is not stable if at least one of the other arguments is never attacked.
    never_attacked = True
    for other_arg in other_args:
        for arg in arg_set:
            if other_arg in arg_framework[arg]:
                never_attacked = False
        if never_attacked:
            return False
        never_attacked = True
    return True


def decide_complete_credulous(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Credulous acceptability of the given argument with respect to σ = complete.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    complete_extensions = find_all_sigma_extensions(arg_framework, "COMPLETE")
    return any(argument in complete_extension for complete_extension in complete_extensions)


def decide_complete_skeptical(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Skeptical acceptability of the given argument with respect to σ = complete.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    complete_extensions = find_all_sigma_extensions(arg_framework, "COMPLETE")
    return all(argument in complete_extension for complete_extension in complete_extensions)


def decide_stable_credulous(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Credulous acceptability of the given argument with respect to σ = stable.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    stable_ext = find_all_sigma_extensions(arg_framework, "STABLE")
    return any(argument in stable for stable in stable_ext)


def decide_stable_skeptical(arg_framework: dict, arg_set: set) -> bool:
    """
    Decide the Skeptical acceptability of the given argument with respect to σ = stable.
    """
    argument = list(arg_set)[0] # Recover the only provided argument.
    stable_ext = find_all_sigma_extensions(arg_framework, "STABLE")
    return all(argument in stable for stable in stable_ext)
    