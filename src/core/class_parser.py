import glob
import importlib
import inspect
import os
from dataclasses import dataclass
from types import MethodType

import pandas as pd

from src.core.data_objects import ClassObjectInfo, ModuleObjectInfo
from src.core.function_parser import FunctionParser
from src.utils.logger import logger


@dataclass
class ClassParser:
    module_info: ModuleObjectInfo
    class_name: str
    class_object: type

    def parse_class(self):
        logger.info(f"parsing Classes")
        self.class_methods = []
        self.cls_attrs = []
        for func in dir(self.class_object):
            self.is_method(func)
            self.is_class_attr(func)

        self.num_cls_attrs = len(self.cls_attrs)
        self.num_cls_methods = len(self.class_methods)

        logger.info(f"Creating class info object")
        class_info = ClassObjectInfo(
            self.class_object,
            self.class_name,
            self.cls_attrs,
            self.num_cls_attrs,
            self.class_methods,
            self.num_cls_methods,
        )
        for method in self.class_methods:
            function_parser = FunctionParser(self.module_info, class_info, method)
            logger.info(f"Parsing class functions")
            function_parser.parse_function()

    def is_method(self, func):
        if callable(getattr(self.class_object, func)) and not func.startswith("__"):
            self.class_methods.append(func)

    def is_class_attr(self, func):
        if not callable(getattr(self.class_object, func)):
            if not func.startswith("__"):
                self.cls_attrs.append(func)
