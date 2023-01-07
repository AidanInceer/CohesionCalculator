import glob
import inspect
import os
import pprint
import sys
from dataclasses import dataclass
from os import path


@dataclass
class HelloWorld:
    what_world: str
    caps: str

    def print_h1(self, first: str):
        if self.caps == "True":
            output = (first + " " + self.what_world).upper()
        else:
            output = first + " " + self.what_world
        return output

    def print_h2(self, second: str):
        if self.caps == "True":
            output = (second + " " + self.what_world).upper()
        else:
            output = second + " " + self.what_world
        return output

    def print_h3(self, third: str):
        if self.caps == "True":
            output = (third + " " + self.what_world).upper()
        else:
            output = third + " " + self.what_world
        return output


@dataclass
class AaBbCc:
    def dothing(self, a, b):
        return a + b

    def dothing2(self, a, b):
        return a + b


files = [f.replace("\\", "/") for f in glob.glob("./data/" + "**/*.py", recursive=True)]
for file in files:
    print(os.path.join("", file))
    with open(file, "r") as f:
        for name, obj in inspect.getmembers(sys.modules[__name__]):

            if inspect.isclass(obj):
                print("========================")
                print(f"name: {name}")
                method_list = []
                attr_list = []
                for func in dir(obj):
                    if callable(getattr(obj, func)) and not func.startswith("__"):
                        method_list.append(func)
                    if (
                        getattr(obj, func)
                        and not func.startswith("__")
                        and not callable(getattr(obj, func))
                    ):
                        attr_list.append(func)

                print("class attributes: ", attr_list)
                print("num class attributes: ", len(method_list))
                print("methods: ", method_list)
                print("num attributes: ", len(method_list))
                for method in method_list:
                    func = getattr(obj, method)
                    all_stuff = inspect.getsource(func).replace("\n", " ").strip()
                    print(all_stuff)
                    varnames = func.__code__.co_varnames
                    print(varnames)
