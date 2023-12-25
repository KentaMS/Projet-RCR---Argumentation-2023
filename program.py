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
    param_value = command_args.param # param for the method (VE-CO, DC-CO, DS-CO...)
    file_value = command_args.file # file to read (.txt)
    if len(command_args.args) > 1 :
        args_value = set(command_args.args.split(",")) # set of args
    else:
        args_value = command_args.args # arg

    # Checks valid arguments
    for arg in args_value:
        if not regex_pattern.match(arg):
            print("Unaccepted argument(s)) Remember, the name of an argument can be any sequence of letters (upper case or lower case), numbers, or the underscore symbole _, except the words arg and att which are reserved for defining the lines.")
            sys.exit(1)

    check_number_of_arguments(args_value, param_value)

    return param_value, file_value, args_value


# Checks if the number of provided arguments is valid (Only one should be given when using the determine methods)
def check_number_of_arguments(arg_set, param):
    if(param.startswith("DC") or param.startswith("DS")):
        if len(arg_set) != 1:
            print("Only one argument should be specified for the determine methods.")
            sys.exit(1)


# Read and create the AF from the file as a dictionnary (key: attacking arg, value : set of the args it attacks)
def read_AF_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)

    graph = {}
        
    with open(file_path, 'r') as file:
        for line in file:
            content = line[line.find("(")+1 : line.find(")")]
            if "arg" in line:
                argument = content
                graph[argument] = set()
            elif "att" in line:
                attacker, attacked = content.split(',')[0], content.split(',')[1]
                graph[attacker].add(attacked)
                
    return graph


# Checks if the set S = arg_set is conflit_free in the AF arg_framework
def is_conflict_free(arg_framework, arg_set):

    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if(attacked_arg in arg_set):
                return False
    return True


# Generate a list of all sets combinations from an AF
def generate_combinations(arg_framework):
    
    if len(arg_framework) == 0: # Halting case
        return [set()]
    # Generate recursively all combinations without the first element
    combinations_without_first = generate_combinations(arg_framework[1:])
    # Add the first element to each combinations generated
    combinations_with_first = [{arg_framework[0]} | combination for combination in combinations_without_first]
    # Combine both sets lists 
    all_combinations = combinations_with_first + combinations_without_first
    return all_combinations
    

# Find every stable extensions in arg_framework
def find_all_stable_extensions(arg_framework):
    args = list(arg_framework.keys())
    all_combinations = generate_combinations(args) # Get all argument sets  

    stable_ext = set()
    for arg_set in all_combinations:
        if verify_stable_extension(arg_framework, arg_set): # Keep the ones that are stable
            stable_ext.add(tuple(arg_set))

    return stable_ext


def verify_complete_extension(arg_framework, arg_set):
    return True


def decide_complete_credulous(arg_framework, arg_set):
    return True


def decide_complete_skeptical(arg_framework, arg_set):
    return True


# Determine whether S is a stable extension of arg_framework
def verify_stable_extension(arg_framework, arg_set):
    # Check if arg_set is conflict free
    if not is_conflict_free(arg_framework, arg_set):
        return False

    # arg_set is stable if all args in others_args are attacked
    others_args = {arg for arg in arg_framework.keys() if arg not in arg_set} # set of others args
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if attacked_arg in others_args:
                others_args.remove(attacked_arg)

    if len(others_args) == 0: # All args were attacked, then arg_set is stable
        return True
    return False


# Determine whether arg belongs to some stable extension of arg_framework
def decide_stable_credulous(arg_framework, arg):
    stable_ext = find_all_stable_extensions(arg_framework)
    return any(arg in stable for stable in stable_ext)


# Determine whether arg belongs to every stable extension of arg_framework
def decide_stable_skeptical(arg_framework, arg):
    stable_ext = find_all_stable_extensions(arg_framework)
    return all(arg in stable for stable in stable_ext)


# Checks if an argument or an argument set is included in the argumentation framework, or not
def is_argument_set_in_AF(arg_framework, arg_set):
    return all(arg in arg_framework.keys() for arg in arg_set)


# Returns either YES or NO depending on the problem
def solve_methode(param, arg_framework, arg_set):
    if not is_argument_set_in_AF(arg_framework, arg_set): return False

    if(param == "VE-CO"):
        return verify_complete_extension(arg_framework, arg_set)
    elif(param == "DC-CO"):
        return decide_complete_credulous(arg_framework, arg_set)
    elif(param == "DS-CO"):
        return decide_complete_skeptical(arg_framework, arg_set)
    elif(param == "VE-ST"):
        return verify_stable_extension(arg_framework, arg_set)
    elif(param == "DC-ST"):
        return decide_stable_credulous(arg_framework, arg_set)
    elif(param == "DS-ST"):
        return decide_stable_skeptical(arg_framework, arg_set)
    else:
        print("Error : Unknown parameter.")
        print("Please choose one of these : VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.")
        sys.exit(1)

#=========================================================#
def main():
    param, file, arg_set = get_command_args() # args recovery
    path_to_data = "./data/"
    arg_framework = read_AF_from_file(path_to_data+file)
    if solve_methode(param, arg_framework, arg_set) == True:
        print("YES")
    else:
        print("NO")

if __name__ == '__main__':
    main()

