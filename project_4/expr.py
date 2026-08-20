"""
Name: Josh Gilliam
Info: CS211 Project 4, 1/3/2026
"""

ENV: dict[str, "IntConst"] = dict()


class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")
    

class IntConst(Expr):
    """Integer constant expression"""

    def __init__(self, value: int):
        self.value = value

    def eval(self) -> "IntConst":
        return self

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"IntConst({self.value})"
    
    def __eq__(self, other: Expr):
        return isinstance(other, IntConst) and self.value == other.value


class BinOp(Expr):
    """Abstract base class for binary operations"""

    def __init__(self, left: Expr, right: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.left} {self.symbol} {self.right})"
    
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.left)}, {repr(self.right)})"
    
    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))       # Returns an IntConst despite _apply returning an int


class Plus(BinOp):
    """Expr + Expr"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="+")
    
    def _apply(self, left: int, right: int) -> int:
        return left + right
    

class Times(BinOp):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="*")

    def _apply(self, left: int, right: int) -> int:
        return left * right
    

class Minus(BinOp):
    """left - right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="-")

    def _apply(self, left: int, right: int) -> int:
        return left - right
    

class Div(BinOp):
    """left // right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="/")       # Represent div as / (for user) but math behind it //

    def _apply(self, left: int, right: int) -> int:
        return left // right
    

class Unop(Expr):
    """Abstract base class for unary operations"""

    def __init__(self, value: Expr, symbol: str="?Operation symbol undefined"):
        self.value = value
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.symbol} {self.value})"
    
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.value)})"
    
    def _apply(self, value: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.value.eval()
        return IntConst(self._apply(left_val.value))


class Abs(Unop):
    """Negation: @ value"""
    
    def __init__(self, value: Expr):
        super().__init__(value, symbol="@")

    def _apply(self, value: int) -> int:
        return abs(value)


class Neg(Unop):
    """Absolute value: ~ value"""

    def __init__(self, value: Expr):
        super().__init__(value, symbol="~")        # Needs to be a different symbol than "-" avoiding ambiguity

    def _apply(self, value: int) -> int:
        return -value
    

def env_clear():
    """Clear all variables in calculator memory"""
    ENV = dict()


class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that 
    is not in ENV
    """
    pass


class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")
        
    def assign(self, value: IntConst):
        global ENV
        ENV[self.name] = value


class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""
    
    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables! 
        self.left = left
        self.right = right

    def eval(self) -> IntConst: 
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val
    
    def __str__(self) -> str:
        return f"({self.left} = {self.right})"

    def __repr__(self) -> str:
        return f"Assign({repr(self.left)}, {repr(self.right)})"