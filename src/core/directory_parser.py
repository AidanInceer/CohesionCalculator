import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

from src.core.class_parser import ClassParser


@dataclass
class DirectoryParser:

    files = [
        f.replace("/", "\\") for f in glob.glob("./data/" + "**/*.py", recursive=True)
    ]
    thing = []
    for file in files:
        if "__init__" not in file:
            f_1 = str(os.path.splitext(file)[0])[2:].replace("\\", ".")
            mod = importlib.import_module(f_1)


@dataclass
class ModuleObjectInfo:
    file_name: str
    module_object: object
