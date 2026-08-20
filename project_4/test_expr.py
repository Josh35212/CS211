"""Unit tests for expr.py"""

import unittest
from expr import *

class TestIntConst(unittest.TestCase):

    def test_eval(self):
        five = IntConst(5)
        self.assertEqual(five.eval(),IntConst(5))

    def test_str(self):
        twelve = IntConst(12)
        self.assertEqual(str(twelve), "12")

    def test_repr(self):
        forty_two = IntConst(42)
        self.assertEqual(repr(forty_two), f"IntConst(42)")


class TestPlus(unittest.TestCase):

    def test_plus_str(self):
        exp = Plus(IntConst(5), IntConst(4))
        self.assertEqual(str(exp), "(5 + 4)")

    def test_nested_str(self):
        exp = Plus(Plus(IntConst(4), IntConst(5)), IntConst(3))
        self.assertEqual(str(exp), "((4 + 5) + 3)")

    def test_repr_simple(self):
        exp = Plus(IntConst(12), IntConst(13))
        self.assertEqual(repr(exp), "Plus(IntConst(12), IntConst(13))")

    def test_repr_nested(self):
        exp = Plus(IntConst(7), Plus(IntConst(4), IntConst(2)))
        self.assertEqual(repr(exp), "Plus(IntConst(7), Plus(IntConst(4), IntConst(2)))")

    def test_addition_simple(self):
        exp = Plus(IntConst(4), IntConst(8))
        self.assertEqual(exp.eval(), IntConst(12))

    def test_additional_nested(self):
        exp = Plus(IntConst(7), Plus(IntConst(2), IntConst(3)))
        self.assertEqual(exp.eval(), IntConst(12))


class TestBinOp(unittest.TestCase):
    """Test the remainder of the binary operations"""

    def test_div(self):
        exp = Div(IntConst(7), IntConst(3))
        self.assertEqual(exp.eval(), IntConst(2))

    def test_sub(self):
        exp = Minus(IntConst(7), IntConst(3))
        self.assertEqual(exp.eval(), IntConst(4))

    def test_composed(self):
        """Putting them all together: (10 - (2 + 1)) * (4 / 2) = 14"""
        exp = Times(
            Minus(IntConst(10), Plus(IntConst(2), IntConst(1))),
            Div(IntConst(4), IntConst(2)))
        self.assertEqual(exp.eval(), IntConst(14))


class TestUnOp(unittest.TestCase):

    def test_repr_simple(self):
        exp = Abs(IntConst(5))
        self.assertEqual(repr(exp), "Abs(IntConst(5))")
        exp = Neg(IntConst(6))
        self.assertEqual(repr(exp), "Neg(IntConst(6))")

    def test_str_simple(self):
        exp = Abs(IntConst(12))
        self.assertEqual(str(exp), "(@ 12)")
        exp = Neg(IntConst(13))
        self.assertEqual(str(exp), "(~ 13)")

    def test_abs_eval(self):
        exp = Minus(IntConst(3), IntConst(5))
        self.assertEqual(exp.eval(), IntConst(-2))
        exp = Abs(exp)
        self.assertEqual(exp.eval(), IntConst(2))

    def test_neg_eval(self):
        exp = Minus(IntConst(12), IntConst(8))
        self.assertEqual(exp.eval(), IntConst(4))
        exp = Neg(exp)
        self.assertEqual(exp.eval(), IntConst(-4))

    def test_together(self):
        """Compose unary and """
        exp = Abs(Plus(IntConst(3), Neg(IntConst(12))))
        self.assertEqual(str(exp), "(@ (3 + (~ 12)))")
        self.assertEqual(exp.eval(), IntConst(9))


class TestVars(unittest.TestCase):
    def test_assign(self):
        v = Var("v")
        w = Var("w")
        exp = Assign(v, IntConst(5))
        self.assertEqual(exp.eval(), IntConst(5))
        self.assertEqual(v.eval(), IntConst(5))
        exp = Assign(w, v)
        self.assertEqual(exp.eval(), IntConst(5))
        self.assertEqual(w.eval(), IntConst(5))

    def test_assign_reps(self):
        v = Var("v")
        w = Var("w")
        exp = Assign(v, Plus(IntConst(5), w))
        self.assertEqual(str(exp), "(v = (5 + w))")
        self.assertEqual(repr(exp), "Assign(Var(v), Plus(IntConst(5), Var(w)))")
        

if __name__ == "__main__":
    unittest.main()