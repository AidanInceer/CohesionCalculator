import pprint

from cohensioncalculator.core.function_parser import ClassParser, FunctionParser
from cohensioncalculator.utils.logger import logger

if __name__ == "__main__":

    # basic class parsing
    cp = ClassParser()
    rows = cp.read_file()
    class_groups = cp.group_class_rows(rows)
    num_classes = cp.count_classes(class_groups)
    for grouped_class in class_groups:
        class_name = cp.get_class_name(grouped_class)
        class_args = cp.class_init_arg_parser(grouped_class)
        print(f"name: {class_name}, class_args:{class_args}")
