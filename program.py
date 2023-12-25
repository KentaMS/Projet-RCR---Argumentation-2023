import os, sys, argparse

def get_command_args():
    parser = argparse.ArgumentParser(description="Abstract Argumentation Solver - A software which solves VE-CO, DC-CO, DS-CO, VE-ST, DC-ST, DS-ST problems.")
    
    # Arguments for the command
    parser.add_argument('-p', '--param', type=str, help='VE-CO or DC-CO or DS-CO or VE-ST or DC-ST or DS-ST.')
    parser.add_argument('-f', '--file', type=str, help='File.apx to read (Describe an Argumentation Framework AF).')
    parser.add_argument('-a', '--args', type=str, help='ARG1,ARG2,...,ARGn the names of the arguments in the query set S (for VE-XX problems) or ARG (for DC-XX or DS-XX problems).')
    
    # Read args in the command
    args = parser.parse_args()

    # Get args
    param_value = args.param # param for the method (VE-CO, DC-CO, DS-CO...)
    file_value = args.file # file to read (.txt)
    args_value = set(args.args.upper().split(",")) # arg or set of args

    # Check arguments (to delete later !!!)
    print(f"Parameter : {param_value}")
    print(f"File : {file_value}")
    print(f"Arguments : {args_value}")

    return param_value, file_value, args_value


def read_data_from_directory(path_to_data):
    AF_dictionary = {}
    complete_dictionary = {}
    stable_dictionary = {}
    
    for file_name in os.listdir(path_to_data):
        graph_name = file_name.split('_')[1].split('.')[0].upper()
        
        if ".apx" in file_name:
            AF_dictionary[graph_name] = read_AF_from_file(path_to_data, file_name)
        elif "co.txt" in file_name:
            complete_dictionary[graph_name] = read_co_from_file(path_to_data, file_name)
        elif "st.txt" in file_name:
            stable_dictionary[graph_name] = read_st_from_file(path_to_data, file_name)
            
                    
    return AF_dictionary, complete_dictionary, stable_dictionary

# Read and create the AF from the file as a dictionnary (key: attacking arg, value : set of the args it attacks)
def read_AF_from_file(path, file_name):
    file_path = path + file_name

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


def get_arguments_from_line(line):
    if "None of them" not in line:
        return line.strip().split(',')
    return []
    
def read_co_from_file(path, file_name):
    co = {
        "Complete extensions": [],
        "Skeptically accepted arguments": [],
        "Credulously accepted arguments": []
    }
    
    with open(path + file_name, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if "[" in line:
                extensions = line[line.find("[")+1 : line.find("]")].split(',')
                co["Complete extensions"] += [extensions]
            if "Skeptically accepted arguments:" in line:
                skep = get_arguments_from_line(lines[i + 1])
                co["Skeptically accepted arguments"] = skep
            if "Credulously accepted arguments:" in line:
                cred = get_arguments_from_line(lines[i + 1])
                co["Credulously accepted arguments"] = cred
        
    return co

def read_st_from_file(path, file_name):
    st = {
        "Stable extensions": [],
        "Skeptically accepted arguments": [],
        "Credulously accepted arguments": []
    }
    
    with open(path + file_name, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if "[" in line:
                extensions = line[line.find("[")+1 : line.find("]")].split(',')
                st["Stable extensions"] += [extensions]
            if "Skeptically accepted arguments:" in line:
                skep = get_arguments_from_line(lines[i + 1])
                st["Skeptically accepted arguments"] = skep
            if "Credulously accepted arguments:" in line:
                cred = get_arguments_from_line(lines[i + 1])
                st["Credulously accepted arguments"] = cred
        
    return st

#=========================================================#

# Determine if the set S = arg_set is conflit_free in the AF arg_framework
def is_conflict_free(arg_framework, arg_set):

    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if(attacked_arg in arg_set):
                return False
    return True

def verify_complete_extension(arg_framework, arg_set):
    return True

def decide_complete_credulous(arg_framework, arg_set):
    return True

def decide_complete_skeptical(arg_framework, arg_set):
    return True

def verify_stable_extension(arg_framework, arg_set):

    # Check if arg_set is conflict free
    if(not(is_conflict_free(arg_framework, arg_set))):
        return False

    # arg_set is stable if all args in others_args are attacked
    others_args = {arg for arg in set(arg_framework.keys()) if arg not in arg_set} # set of others args
    for current_arg in arg_set:
        for attacked_arg in arg_framework[current_arg]:
            if(attacked_arg in others_args):
                others_args.remove(attacked_arg)

    if(len(others_args)==0): # All args were attacked, then arg_set is stable
        return True
    return False

def decide_stable_credulous(arg_framework, arg_set):
    return True

def decide_stable_skeptical(arg_framework, arg_set):
    return True

# Returns either YES or NO depending on the problem
def solve_methode(param, arg_framework, arg_set):
    
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
    arg_framework = read_AF_from_file(path_to_data, file)
    print(arg_framework)
    print(solve_methode(param, arg_framework, arg_set))

    # graphs, co, st = read_data_from_directory(path_to_data)
    # print(graphs)
    # print(co)
    # print(st)

if __name__ == '__main__':
    main()

