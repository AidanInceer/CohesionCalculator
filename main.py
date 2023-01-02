from src.cohesion.core.function_parser import ClassParser, FunctionParser

if __name__ == "__main__":
    module = "./data/sample.py"
    fp = FunctionParser(module)
    cp = ClassParser(module)
    rows = cp.read_file()
    class_groups = cp.group_class_rows(rows)
    num_classes = cp.count_classes(class_groups)
    print(f"============================={module}=================================")
    for grouped_class in class_groups:
        class_name = cp.get_class_name(grouped_class)
        class_args = cp.class_init_arg_parser(grouped_class)
        num_funcs = fp.count_functions(grouped_class)
        func_names = cp.get_class_function_names(grouped_class)
        class_cohesion = cp.is_class_cohesive(grouped_class, class_args, num_funcs)
        data = {
            "name": class_name,
            "class_args": class_args,
            "class_cohesion": class_cohesion,
        }
        print(data)

    # TODO:
    # research into cohesion more
    # multiline function/class defintion handling
    # other edge cases as they arrise
    # refactor functions
    # doc strings
    # refactor files
    # tests
    # publish as package
    # readme
