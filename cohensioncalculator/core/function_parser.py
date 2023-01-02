from dataclasses import dataclass

from cohensioncalculator.utils.logger import logger


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

    @staticmethod
    def create_function_headers(file: list[str]):
        function_header = []
        for row in file:
            if row.startswith("def ") or row.startswith("    def "):
                function_header.append(row)
        return function_header

    @staticmethod
    def is_header_one_line(header: str):
        if header.startswith("def ") and header.endswith(":"):
            return True
        else:
            return False

    @staticmethod
    def count_function_arguments(headers: list[str]):
        output_dict = {}
        for header in headers:
            raw_args = header.split("(")[1].split(")")[0]
            args = raw_args.split(",")
            output_args = []
            for arg in args:
                cleaned_arg = arg.split(":")[0]
                output_args.append(cleaned_arg)
            name = FunctionParser.get_function_name(header)
            output_dict[f"function_{name}"] = {
                "name": name,
                "args": output_args,
                "num_args": len(output_args),
                "function_length": "_____",
            }
        return output_dict

    @staticmethod
    def get_function_name(header: list[str]) -> bool:
        return header.split("(")[0].split("def ")[1]


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

    def class_arg_parser(self, grouped_class):
        if self.is_init_in_class(grouped_class):
            args = self.class_init_parser()
        else:
            args = self.class_noinit_parser()
        return args

    @staticmethod
    def is_init_in_class(grouped_class: list[str]) -> bool:
        for row in grouped_class:
            if "def __init__(self," in row:
                return True
        else:
            return False

    def class_init_parser(self):
        return "init"

    def class_noinit_parser(self):
        return "noinit"


