import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

from src.parsing.class_parser import ClassParser
from src.parsing.data_objects import ModuleObjectInfo
from src.utils.logger import logger


@dataclass
class DirectoryParser:
    directory_path: str

    def parse_directory(self) -> list[str]:
        self.files = [
            f.replace("/", "\\")
            for f in glob.glob(self.directory_path + "**/*.py", recursive=True)
        ]
        logger.info("collected formatted directory files")
        self.parse_files()

    def parse_files(self) -> None:
        self.cohesion_data = []
        for file in self.files:
            if "__init__" not in file:
                formatted_file = str(os.path.splitext(file)[0])[2:].replace("\\", ".")
                logger.info(f"Parsing Module: {formatted_file}")
                module = importlib.import_module(formatted_file)
                module_info = ModuleObjectInfo(
                    formatted_file,
                    module,
                    self.cohesion_data,
                )

                self.parse_module(module_info)

    def parse_module(self, module_info: ModuleObjectInfo) -> None:
        for class_name, class_object in inspect.getmembers(module_info.module_object):
            if inspect.isclass(class_object):
                logger.info(f"Parsing Class: {class_name}")
                class_parser = ClassParser(module_info, class_name, class_object)
                class_parser.parse_class()

    def cohesion_data_to_df(self) -> list[dict]:
        df = pd.DataFrame(self.cohesion_data)
        return df
