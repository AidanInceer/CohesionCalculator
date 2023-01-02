from dataclasses import dataclass

from cohensioncalculator.utils.logger import logger


@dataclass
class ClassParser:
    @staticmethod
    def read_file():
        with open("./data/sample2.py", "r") as f:
            data = f.readlines()
        return data

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
    def count_classes(class_groups: list[str]):
        return len(class_groups)

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
        fp = FunctionParser()
        grouped_functions = fp.group_function_rows(grouped_class)
        init_function = grouped_functions[0]
        if fp.is_header_one_line(init_function[0]):
            init_args = fp.get_init_function_args(init_function[0])
        return init_args

    def class_noinit_parser(self, grouped_class: list[str]):
        fp = FunctionParser()
        # print(grouped_class)
        function_locations = []
        for index, row in enumerate(grouped_class):
            fp.row_is_function_header(row, index, function_locations)
        first_function_definition = function_locations[0]
        arg_rows = grouped_class[1 : first_function_definition - 1]
        args = []
        for arg in arg_rows:
            cleaned_arg = arg.split(":")[0].strip()
            args.append(cleaned_arg)
        return args


@dataclass
class FunctionParser:
    @staticmethod
    def read_file():
        with open("./data/sample.py", "r") as f:
            data = f.readlines()
        return data

    @staticmethod
    def count_functions(funcs: list[str]):
        counter = 0
        for item in funcs:
            if item.startswith("def "):
                counter += 1
        return counter

    def group_function_rows(self, rows: list[str]) -> list[list]:
        func_groups = []
        split_class = []
        for index, row in enumerate(rows):
            self.row_is_function_header(row, index, split_class)
        for i, _ in enumerate(split_class):
            if i == (len(split_class) - 1):
                func_groups.append(rows[split_class[i] :])
            else:
                func_groups.append(rows[split_class[i] : split_class[i + 1]])
        return func_groups

    @staticmethod
    def row_is_function_header(row: str, index: int, split_class: list) -> None:
        if row.startswith("def ") or row.startswith("    def "):
            split_class.append(index)
        else:
            return

    @staticmethod
    def create_function_headers(file: list[str]):
        function_header = []
        for row in file:
            if row.startswith("def ") or row.startswith("    def "):
                function_header.append(row)
        return function_header

    @staticmethod
    def is_header_one_line(header: str):
        if (
            header.startswith("def ") or header.startswith("    def ")
        ) and header.endswith(":\n"):
            return True
        else:
            return False

    @staticmethod
    def count_function_args(headers: list[str]):
        for header in headers:
            raw_args = header.split("(")[1].split(")")[0]
            args = raw_args.split(",")
            output_args = []
            for arg in args:
                cleaned_arg = arg.split(":")[0].strip()
                output_args.append(cleaned_arg)
            # name = FunctionParser.get_function_name(header)
        return output_args

    @staticmethod
    def get_init_function_args(row: list[str]):

        raw_args = row.split("(")[1].split(")")[0]
        args = raw_args.split(",")
        output_args = []
        for arg in args:
            cleaned_arg = arg.split(":")[0].strip()
            output_args.append(cleaned_arg)
        output_args.remove("self")
        return output_args

    @staticmethod
    def get_function_name(header: list[str]) -> bool:
        return header.split("(")[0].split("def ")[1]
