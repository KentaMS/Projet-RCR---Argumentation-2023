# AF_util.py

"""
This file contains utility methods for solving problems related to Argumentation Frameworks (AF).

Authors: Latif YAYA, Nassim LATTAB, Kentaro SAUCE
Creation Date: 25/12/2023
"""

from itertools import chain, combinations # Used to generate the powerset @see powerset(iterable).

def is_number_of_arguments_valid(arg_set: set, param: str) -> bool:
    """ 
    Checks if the number of provided arguments is valid or not.
    Only one should be specified when using the Determine-XX problems.
    """
    if param.startswith("DC") or param.startswith("DS"):
        return not len(arg_set) != 1
    return True


def is_argument_set_in_AF(arg_framework: dict, arg_set: set) -> bool:
    """
    Checks if an argument or an argument set is included in the argumentation framework, or not.
    """
    return all(argument in arg_framework.keys() for argument in arg_set)
    
    
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

def powerset(iterable: set|tuple|list) -> set:
    """ 
    Returns the powerset of the given arguments. In other words, give all possible combinations of arguments as a set of sorted tuples.
    For instance, powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3).
    Inspired by the powerset recipe provided in the following documentation: https://docs.python.org/3/library/itertools.html#itertools-recipes.
    """
    s = list(iterable) 
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))