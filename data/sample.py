def is_dict(object: str | list | dict) -> bool:
    return isinstance(object, dict)


def is_list(object: str | list | dict) -> bool:
    return isinstance(object, list)


def summer(a: int, b: int, c: int) -> bool:
    return a + b + c


class BasicOne:
    a: int
    b: str

    def mult1(self):
        return self.a * self.b

    def sum2(self, c):
        return self.a + self.b

    def sum3(self, c):
        return self.a + self.b + c


class BasicTwo:
    a: int
    b: str
    def __init__(self) -> None:
        pass

    def mult1(self):
        return self.a * self.b

    def sub1(self):
        return self.a - self.b

    def sub2(self):
        return self.b + self.a
