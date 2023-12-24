import os

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

def read_AF_from_file(path, file_name):
    graph = {}
        
    with open(path + file_name, 'r') as file:
        for line in file:
            content = line[line.find("(")+1 : line.find(")")]
            if "arg" in line:
                argument = content
                graph[argument] = []
            elif "att" in line:
                attack = content.split(',')
                graph[attack[0]] += [attack[1]]
                
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

path_to_data = "./data/"

graphs, co, st = read_data_from_directory(path_to_data)
print(graphs, co, st)

