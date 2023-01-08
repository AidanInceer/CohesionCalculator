import glob
import importlib
import inspect
import os
from dataclasses import dataclass

import pandas as pd

from src.core.class_parser import ClassParser
from src.core.directory_parser import DirectoryParser
from src.core.function_parser import FunctionParser

if __name__ == "__main__":
    abs_file_path = input("Input the absolute path for your project: ")
    parser_directory = DirectoryParser()
