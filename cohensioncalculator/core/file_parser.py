from dataclasses import dataclass

from cohensioncalculator.utils.logger import logger


@dataclass
class FileParser:
    @staticmethod
    def split_functions():
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
            if row.startswith("def "):
                function_header.append(row)
        return function_header

    @staticmethod
    def get_function_name(header: list[str]):
        return header.split("(")[0].split("def ")[1]

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
            name = FileParser.get_function_name(header)

            output_dict[f"function_{name}"] = {
                "name": name,
                "args": output_args,
                "num_args": len(output_args),
                "function_length": '_____',
                

            }

        return output_dict
