# Writes to a given file for errors 
import json
import os
def write_to(filename, what_to_write):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = [data]
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    data.append(what_to_write)
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)