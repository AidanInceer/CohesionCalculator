class BasicOne:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

    def mult1(self):
        return self.a * self.b

    def sub1(self):
        return self.a - self.b

    def sub2(self):
        return self.b + self.a


class BasicTwo:
    a: int
    b: int

    def mult1(self):
        return self.a * self.b

    def sub1(self):
        return self.a - self.b

    def sub2(self):
        return self.b + self.a


class BasicThree:
    a: int
    b: int

    def mult1(self):
        return self.a * self.b

    def sub1(self):
        return self.a - self.b

    def sub2(self):
        return self.b + self.a
