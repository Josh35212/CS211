"""Test of code that spreads a long list of strings
into multiple columns.  It's not sophisticated, but
it makes dealing with a long list of anagrams a little
less annoying.
"""

import unittest
import columns

def explain_text_diff(desc: str, s1: str, s2: str):
    """Helper function for diagnosing failed tests.  How do the multi-line texts differ?"""
    s1_lines = s1.split('\n')
    s2_lines = s2.split('\n')
    print(f"\n*** Comparing columnized output for ***{desc}***")
    print(f"S1 is {len(s1)} characters in {len(s1_lines)} lines")
    print(f"S2 is {len(s2)} characters in {len(s2_lines)} lines")
    print("Line by line:")
    for i in range(min(len(s1_lines), len(s2_lines))):
        print( "   012345678901234567890123456789012345678901234567890")
        print(f"{i}: |{s1_lines[i]}|")
        print(f"{i}: |{s2_lines[i]}|")
    print(f"*** End of comparison for ***{desc}***")


class TestColumns(unittest.TestCase):
    """Various column and line lengths to check columnization of the same text"""

    def test_01_fives_in_fives(self):
        """Chunks of 5 characters, in columns of width 5, should jam together"""
        sample = ["12345", "12345", "12345",
                  "12345", "12345", "12345",
                  "12345"]
        expect = "12345     12345     12345\n12345     12345     12345\n12345"
        columnized = columns.columns(sample, line_length=25)
        self.assertEqual(columnized, expect)

    def test_02_three_in_fives(self):
        """Chunks of 3 characters, in columns of width 5, should space nicely"""
        sample = ["123", "123", "123",
                  "123", "123", "123",
                  "123"]
        expect = "123  123  123  123\n123  123  123"
        columnized = columns.columns(sample, line_length=18)
        self.assertEqual(columnized, expect)

    def test_03_uneven(self):
        """Some chunks that exceed a column"""
        sample = ["1234567", "123", "123", "1234567", "123"]
        expect = "1234567   123  123\n1234567   123"
        columnized = columns.columns(sample, line_length=25)
        self.assertEqual(columnized, expect)





if __name__ == '__main__':
    unittest.main()


