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
        file_split_by_class = []
        for index, row in enumerate(rows):
            if self.row_is_class_header(row):
                file_split_by_class.append(index)
        max_len = len(file_split_by_class) - 1
        for i, j in enumerate(file_split_by_class):
            if i == max_len:
                class_groups.append(rows[file_split_by_class[i] :])
            else:
                class_groups.append(
                    rows[file_split_by_class[i] : file_split_by_class[i + 1]]
                )
        return class_groups

    @staticmethod
    def count_classes(funcs: list[str]):
        counter = 0
        for item in funcs:
            if item.startswith("class "):
                counter += 1
        return counter

    @staticmethod
    def row_is_class_header(row: str):
        if row.startswith("class "):
            return True
        else:
            return False

    @staticmethod
    def get_class_name(row: str) -> bool:
        if row.startswith("class "):
            return row.split(" ")[1].split(":")[0]

    def class_arg_parser():
        pass

    def class_init_parser():
        pass

    def class_noinit_parser():
        pass
