from dataclasses import dataclass


@dataclass
class FileParser:

    def split_functions():
        with open('data/sample.py','r') as f:
            data = f.readlines()
        
        return data