"""Test cases for module letter_bag.py."""
import unittest
from letter_bag import normalize
from letter_bag import LetterBag

class Test_Normalize(unittest.TestCase):
    """Normalization selects only letters and lowercases them.
    It returns a list of characters, rather than a string."""

    def test_01_normalize_plain_word(self):
        """Simplest case, input is already in normal form"""
        self.assertEqual(normalize("normal"), list("normal"))

    def test_02_skip_punc(self):
        """Omit non-letters"""
        self.assertEqual(normalize("no way! can't be"), list("nowaycantbe"))

    def test_03_lettercase(self):
        """Normalization also lower-cases everything"""
        self.assertEqual(normalize("Make It So"), list("makeitso"))

class Test_LetterBag(unittest.TestCase):
    """Test cases for the LetterBag class itself"""

    def test_01_construct_observe(self):
        """Basic smoke test of constructor"""
        bag = LetterBag("kooky!")
        # Magic observer methods
        self.assertEqual(len(bag), 5)
        self.assertEqual(str(bag), "kooky!")
        self.assertEqual(repr(bag),
                         f"LetterBag(kooky!/[k:2, o:2, y:1])")
        
    def test_02_containment(self):
        """Basic containment without modification"""
        bag = LetterBag("total")
        self.assertTrue(bag.contains(LetterBag("tat")))
        self.assertTrue(bag.contains(LetterBag("alt")))
        self.assertFalse(bag.contains(LetterBag("toll")))
        self.assertFalse(bag.contains(LetterBag("talk")))

    def test_03_take_result(self):
        """Containment before and after taking letters from bag.
        Note value semantics:  'take' has a result, not an effect.
        """
        bag = LetterBag("fluffy")
        fly = LetterBag("fly")
        self.assertTrue(bag.contains(fly))
        depleted = bag.take(fly)
        self.assertEqual(len(bag), 6)
        self.assertEqual(len(depleted), 3)
        self.assertFalse(depleted.contains(fly))
        self.assertTrue(bag.contains(fly))
        self.assertTrue(bag.contains(LetterBag("uff")))
        self.assertTrue(depleted.contains(LetterBag("uff")))

    def test_04_copy(self):
        """Copying a LetterBag allows us to explore with and
        without taking letters that make a candidate word.
        This is a modified version of test_03_take_effect.
        """
        bag = LetterBag("fluffy")
        fly = LetterBag("fly")
        self.assertTrue(bag.contains(fly))
        dup = bag.copy()
        bag = bag.take(fly)
        self.assertFalse(bag.contains(fly))
        self.assertTrue(bag.contains(LetterBag("uff")))
        self.assertTrue(dup.contains(fly))
        dup2 = bag.copy()  # Copy AFTER removing fly
        self.assertEqual(len(dup2), 3)
        self.assertEqual(len(bag), 3)
        self.assertEqual(len(dup), 6)
        self.assertFalse(dup2.contains(fly))
        self.assertTrue(dup2.contains(LetterBag("uff")))
    

if __name__ == "__main__":
    unittest.main()