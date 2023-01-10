from dataclasses import dataclass


@dataclass
class ModuleObjectInfo:
    file_name: str
    module_object: object
    cohesion_data: list


@dataclass
class ClassObjectInfo:
    class_object: object
    class_name: str
    class_attributes: list[str]
    num_class_attrrbutes: int
    class_methods: list[object]
    num_class_methods: int


@dataclass
class FunctionObjectInfo:
    function_variables: list[str]
    num_function_variables: int
    whole_function: str
