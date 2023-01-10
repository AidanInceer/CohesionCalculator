import inspect
from dataclasses import dataclass
from types import MethodType

from src.parsing.data_objects import (
    ClassObjectInfo,
    FunctionObjectInfo,
    ModuleObjectInfo,
)
from src.utils.logger import logger


@dataclass
class FunctionParser:
    module_info: ModuleObjectInfo
    class_info: ClassObjectInfo
    method: MethodType

    def parse_function(self):
        function_object = getattr(self.class_info.class_object, self.method)
        whole_function = self.get_full_function(function_object)
        function_variables = list(function_object.__code__.co_varnames)

        if "self" in function_variables and len(function_variables) > 1:
            function_variables = function_variables[1:]
            num_function_variables = len(function_variables)
        elif "self" not in function_variables:
            function_variables = function_variables
            num_function_variables = len(function_variables)
        else:
            function_variables = []
            num_function_variables = 0

        func_object = FunctionObjectInfo(
            function_variables, num_function_variables, whole_function
        )
        self.create_output(func_object)

    def create_output(self, func_object: FunctionObjectInfo):
        logger.debug(f"Appending function info to output data object")
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
        self.module_info.cohesion_data.append(data)

    def get_full_function(self, function_object):
        return inspect.getsource(function_object).replace("\n", " ").strip()
