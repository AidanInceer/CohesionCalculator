from dataclasses import dataclass

from src.cohesion.core.function_parser import FunctionParser
from src.utils.logger import logger


@dataclass
class ClassParser:
    module: str

    ##### Core methods ######
    def read_file(self):
        with open(self.module, "r") as f:
            data = f.readlines()
        return data

    @staticmethod
    def count_classes(class_groups: list[str]):
        return len(class_groups)

    def group_class_rows(self, rows: list[str]) -> list[list]:
        class_groups = []
        split_file = []
        for index, row in enumerate(rows):
            self.row_is_class_header(row, index, split_file)
        for i, _ in enumerate(split_file):
            if i == (len(split_file) - 1):
                class_groups.append(rows[split_file[i] :])
            else:
                class_groups.append(rows[split_file[i] : split_file[i + 1]])
        return class_groups

    @staticmethod
    def row_is_class_header(row: str, index: int, split_file: list) -> None:
        if row.startswith("class "):
            split_file.append(index)
        else:
            return

    @staticmethod
    def get_class_name(grouped_class: list[str]) -> bool:
        header = grouped_class[0]
        return header.split(" ")[1].split(":")[0]

    ##### Init Parser ######
    def class_init_arg_parser(self, grouped_class):
        if self.is_init_in_class(grouped_class):
            args = self.class_init_parser(grouped_class)
        else:
            args = self.class_noinit_parser(grouped_class)
        return args

    @staticmethod
    def is_init_in_class(grouped_class: list[str]) -> bool:
        for row in grouped_class:
            if "def __init__(self," in row:
                return True
        else:
            return False

    def class_init_parser(self, grouped_class):
        fp = FunctionParser(self.module)
        grouped_functions = fp.group_function_rows(grouped_class)
        init_function = grouped_functions[0]
        if fp.is_header_one_line(init_function[0]):
            init_args = fp.get_init_function_args(init_function[0])
        return init_args

    def class_noinit_parser(self, grouped_class: list[str]):
        fp = FunctionParser(self.module)
        function_locations = []
        for index, row in enumerate(grouped_class):
            fp.row_is_function_header(row, index, function_locations)
        first_function_definition = function_locations[0]
        arg_rows = grouped_class[1 : first_function_definition - 1]
        args = []
        for arg in arg_rows:
            cleaned_arg = arg.split(":")[0].strip()
            if cleaned_arg != "":
                args.append(cleaned_arg)
        return args

    ##### Class Cohesion ######
    def get_class_function_names(self, grouped_class):
        fp = FunctionParser(self.module)
        class_functions = fp.group_function_rows(grouped_class)
        class_function_names = []
        for func in class_functions:
            func_header = func[0]
            if "__init__" not in func_header:
                function_name = fp.get_function_name(func_header)
                class_function_names.append(function_name)
        return class_function_names

    def is_class_cohesive(
        self, grouped_class: list[str], class_args: list[str], num_funcs: int
    ):
        fp = FunctionParser(self.module)
        num_args = len(class_args)
        func_args = []
        for arg in class_args:
            instance_args = "self." + arg
            func_args.append(instance_args)
        class_functions = fp.group_function_rows(grouped_class)
        all_funcs_cohesion = []
        for func in class_functions:
            func_cohesion = self.calc_function_cohesion(func, func_args)
            all_funcs_cohesion.append(func_cohesion)

        if num_args != 0:
            cohesion = sum(all_funcs_cohesion) / (num_args * num_funcs)
            cohesion = round(cohesion, 2)
            return cohesion
        else:
            return None

    def calc_function_cohesion(self, func, func_args):
        counter = 0
        for arg in func_args:
            for row in func:
                if arg in row:
                    counter += 1
        return counter
