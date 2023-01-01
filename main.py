import pprint

from cohensioncalculator.core.file_parser import FileParser
from cohensioncalculator.utils.logger import logger

if __name__ == "__main__":
    fp = FileParser()
    split_file = fp.split_functions()
    cnt = fp.count_functions(split_file)
    headers = fp.create_function_headers(split_file)
    args = fp.count_function_arguments(headers)
    pprint.pprint(args)
