import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

files = [f.replace("/", "\\") for f in glob.glob("./data/" + "**/*.py", recursive=True)]
thing = []
for file in files:
    if "__init__" not in file:
        f_1 = str(os.path.splitext(file)[0])[2:].replace("\\", ".")
        mod = importlib.import_module(f_1)

        for class_name, obj in inspect.getmembers(mod):

            if inspect.isclass(obj):
                # print(dir(obj))
                class_methods = []
                cls_attrs = []
                for func in dir(obj):
                    if callable(getattr(obj, func)) and not func.startswith("__"):
                        class_methods.append(func)
                    if (
                        getattr(obj, func)
                        and not func.startswith("__")
                        and not callable(getattr(obj, func))
                    ):
                        cls_attrs.append(func)
                num_cls_attrs = len(cls_attrs)
                num_cls_methods = len(class_methods)

                for method in class_methods:
                    func = getattr(obj, method)
                    str_function = inspect.getsource(func).replace("\n", " ").strip()
                    function_variables = list(func.__code__.co_varnames)
                    print(type(function_variables))
                    if "self" in function_variables and len(function_variables) == 1:
                        function_variables = []
                        print(type(function_variables))
                    if "self" in function_variables and len(function_variables) > 1:
                        function_variables = function_variables.remove("self")
                        print(type(function_variables))

                    num_function_variables = len(function_variables)

                    data = {
                        "file_name": file,
                        "class_name": class_name,
                        "class_attributes": cls_attrs,
                        "num_class_attributes": num_cls_attrs,
                        "class_methods": class_methods,
                        "num_class_methods": num_cls_methods,
                        "function_variables": function_variables,
                        "num_function_variables": num_function_variables,
                        "string_function": str_function,
                    }
                    thing.append(data)
output = pd.DataFrame(thing)
print(output)
