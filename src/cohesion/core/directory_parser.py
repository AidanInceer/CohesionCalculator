import glob
import os
from dataclasses import dataclass

from src.cohesion.core.class_parser import ClassParser
from src.utils.logger import logger


@dataclass
class DirectoryParser:
    path: str

    def parse_directory(self):
        files = [f for f in glob.glob(self.path + "**/*.py", recursive=True)]
        return files

    @staticmethod
    def module_name(file):
        return file.split("\\")[-1].split("/")[-1]
