class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class BinOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Sum(BinOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())

class Statements():
    def __init__(self, value=False, nodes=[]):
        self.value = value
        self.children = nodes

    def eval(self):
        for i in self.children:
            i.eval()

    def add_child(self, child):
        self.children.append(child)