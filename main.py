import pprint

from cohensioncalculator.core.function_parser import ClassParser, FunctionParser
from cohensioncalculator.utils.logger import logger

if __name__ == "__main__":
    # basic function parsing
    fp = FunctionParser()
    split_file = fp.read_file()
    cnt = fp.count_functions(split_file)
    headers = fp.create_function_headers(split_file)
    args = fp.count_function_arguments(headers)

    # basic class parsing
    cp = ClassParser()
    rows = cp.read_file()
    class_groups = cp.group_class_rows(rows)
    [print(i) for i in class_groups]
    counter = cp.count_classes(rows)
    for row in rows:
        cp.get_class_name(row)
