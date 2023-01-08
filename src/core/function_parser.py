import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

from src.core.class_parser import ClassObjectInfo
from src.core.directory_parser import ModuleObjectInfo


@dataclass
class FunctionObjectInfo:
    function_variables: list[str]
    num_function_variables: int
    whole_function: str


@dataclass
class FunctionParser:
    module_info: ModuleObjectInfo
    class_info: ClassObjectInfo

    def parse_function(self):
        for method in self.class_info.class_methods:
            func = getattr(self.class_info.class_object, method)
            whole_function = inspect.getsource(func).replace("\n", " ").strip()
            function_variables = list(func.__code__.co_varnames)
            if "self" in function_variables and len(function_variables) == 1:
                function_variables = []
            if "self" in function_variables and len(function_variables) > 1:
                function_variables = function_variables.remove("self")
            num_function_variables = len(function_variables)
            func_obj = FunctionObjectInfo(
                function_variables, num_function_variables, whole_function
            )

    def create_output(self, func_object: FunctionObjectInfo):
        data = {
            "file_name": self.module_info.file_name,
            "class_name": self.class_info.class_name,
            "class_attributes": self.class_info.class_attributes,
            "num_class_attributes": self.class_info.num_class_attrrbutes,
            "class_methods": self.class_info.class_methods,
            "num_class_methods": self.class_info.num_class_methods,
            "function_variables": func_object.function_variables,
            "num_function_variables": func_object.num_function_variables,
            "string_function": func_object.whole_function,
        }
        return data
