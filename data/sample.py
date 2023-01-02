def is_dict(object: str | list | dict) -> bool:
    return isinstance(object, dict)


def is_list(object: str | list | dict) -> bool:
    return isinstance(object, list)


def summer(a: int, b: int, c: int) -> bool:
    return a + b + c


class BasicOne:
    a: int
    b: str

    def mult1(self):
        return self.a * self.b

    def sum2(self, c):
        return self.a + self.b

    def sum3(self, c):
        return self.a + self.b + c


class BasicTwo:
    a: int
    b: str

    def __init__(self) -> None:
        pass

    def mult1(self):
        return self.a * self.b

    def sub1(self):
        return self.a - self.b

    def sub2(self):
        return self.b + self.a


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


class ClassParser:
    module: str

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

    def is_class_cohesive(self, grp: list[str], cls_args: list[str], num_func: int):
        fp = FunctionParser(self.module)
        num_args = len(cls_args)
        func_args = []
        for arg in cls_args:
            instance_args = "self." + arg
            func_args.append(instance_args)

        class_functions = fp.group_function_rows(grp)
        all_funcs_cohesion = []
        for func in class_functions:
            func_cohesion = self.calc_function_cohesion(func, func_args, num_args)
            all_funcs_cohesion.append(func_cohesion)
        cohesion = sum(all_funcs_cohesion) / (num_args * num_func)
        cohesion = round(cohesion, 2)
        return cohesion

    def calc_function_cohesion(self, func, func_args, num_args):

        counter = 0
        for arg in func_args:
            for row in func:
                if arg in row:
                    counter += 1

        return counter
