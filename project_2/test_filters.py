"""Test cases for the filters we apply to lists of anagrams"""

import unittest
import filters

class TestFilterSomeUnique(unittest.TestCase):
    """Test function filter_some_unique, which
    should select phrases such that each phrase introduces
    at least one word that has not appeared before in the
    list of phrases.
    """

    def test_word_cover(self):
        """Phrases that "cover" all the unique words"""
        before = ["dance case it",  # First use all three
                  "stead can ice",  # First use all three
                  "ice case stead", # Redundant
                  "ice cat end as",  # "cat" and "as" are new
                  "case stead end" # Redundant
                  ]
        expect = ["dance case it",  # First use all three
                  "stead can ice",  # First use all three
                  "ice cat end as"  # "cat" and "as" are new
                  ]
        self.assertListEqual(filters.filter_some_unique(before), expect)


class TestFilterOnlyUnique(unittest.TestCase):
    """Test function filter_only_unique, which
    should select phrases with NO words in common.
    """

    def test_disjoint_phrases(self):
        """Completely disjoint phrases"""
        before = ["dance case it",  # First use all three
                  "stead can ice",  # First use all three
                  "ice case stead",  # Redundant
                  "ice cat end as",  # overlap "ice"
                  "case stead end"  # overlap "stead" and "case"
                  ]
        expect = ["dance case it",  # First use all three
                  "stead can ice",  # First use all three
                  ]
        self.assertListEqual(filters.filter_only_unique(before), expect)

class TestFilterUniqueWords(unittest.TestCase):

    def test_unique_words(self):
        """List of unique words, rather than anagrammatic phrases"""
        before = ["dance case it",  # First use all three
                  "stead can ice",  # First use all three
                  "ice case stead",  # Redundant
                  "ice cat end as",  # "as" is new
                  "case stead end"  # Redundant
                  ]
        expect = ["dance", "case", "it", "stead", "can", "ice",
                  "cat", "end", "as"]
        self.assertListEqual(filters.filter_unique_words(before), expect)

if __name__ == "__main__":
    unittest.main()
