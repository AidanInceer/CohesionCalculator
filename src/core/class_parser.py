import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

from src.core.directory_parser import ModuleObjectInfo
from src.core.function_parser import FunctionParser


@dataclass
class ClassParser:

    module_info: ModuleObjectInfo

    def parse_class(self):
        for class_name, obj in inspect.getmembers(self.module_info.module_object):
            if inspect.isclass(obj):
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


@dataclass
class ClassObjectInfo:
    class_object: object
    class_name: str
    class_attributes: list[str]
    num_class_attrrbutes: int
    class_methods: list[object]
    num_class_methods: int
