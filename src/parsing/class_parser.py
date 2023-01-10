from dataclasses import dataclass

from src.parsing.data_objects import ClassObjectInfo, ModuleObjectInfo
from src.parsing.function_parser import FunctionParser
from src.utils.logger import logger


@dataclass
class ClassParser:
    module_info: ModuleObjectInfo
    class_name: str
    class_object: type

    def parse_class(self):
        self.class_methods = []
        logger.info(f"Collecting class attributes and methods")
        self.cls_attrs = self.collect_class_attrs()
        for func in dir(self.class_object):
            self.is_method(func)
        self.num_cls_attrs = len(self.cls_attrs)
        self.num_cls_methods = len(self.class_methods)
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

    def collect_class_attrs(self) -> list[str]:
        try:
            class_info = dict(self.class_object.__dict__)
            class_attrs = class_info["__annotations__"].keys()
            return list(class_attrs)
        except:
            logger.warning("class has no '__annotations__' attribute")
            class_attrs = []
            return class_attrs
