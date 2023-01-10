from src.parsing.directory_parser import DirectoryParser
import pandas as pd

if __name__ == "__main__":
    path = "./data/"
    directory_parser = DirectoryParser(path)
    directory_parser.parse_directory()
    output_data = directory_parser.cohesion_data_to_df()
    print(output_data)
