from dataclasses import dataclass

from src.utils.logger import logger


@dataclass
class FunctionParser:
    module: str

    def read_file(self):
        with open(self.module, "r") as f:
            data = f.readlines()
        return data

    @staticmethod
    def count_functions(funcs: list[str]) -> int:
        counter = 0
        for row in funcs:
            if (
                row.startswith("def ") or row.startswith("    def ")
            ) and "__init__" not in row:
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
