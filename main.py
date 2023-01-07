import pandas as pd

from src.cohesion.core.class_parser import ClassCohesion, ClassParser
from src.cohesion.core.directory_parser import DirectoryParser
from src.cohesion.core.function_parser import FunctionParser

if __name__ == "__main__":
    path = "./data/"
    dp = DirectoryParser(path)
    directory = dp.parse_directory()
    all_data = []

    for file in directory:
        # Initalize classes
        module = dp.module_name(file)
        fp = FunctionParser(file)
        cp = ClassParser(file)
        class_cohesion = ClassCohesion(file)

        # Setup class parsing
        file_rows = cp.read_file()
        class_groups = cp.group_class_rows(file_rows)
        num_classes = cp.count_classes(class_groups)

        # Parse Class information
        for grouped_class in class_groups:
            class_name = cp.get_class_name(grouped_class)
            class_args = cp.class_init_arg_parser(grouped_class)
            num_funcs = fp.count_functions(grouped_class)
            func_names = cp.get_class_function_names(grouped_class)

            # Calculate cohesion for each class
            class_cohesion = class_cohesion.calculate(
                grouped_class, class_args, num_funcs
            )
            data = {
                "module": module,
                "name": class_name,
                "class_args": class_args,
                "class_cohesion": class_cohesion,
            }
            all_data.append(data)

    # Summarise cohesion for directory
    df = pd.DataFrame(all_data)
    print(df)

    # TODO:
    # research into cohesion more
    # multiline function/class defintion handling
    # other edge cases as they arrise
    # refactor functions
    # doc strings
    # tests
    # publish as package
    # readme
