"""Test heuristic scoring of words.
We use Scrabble scores as a proxy for a heuristic that
prioritizes both long words and words that use letters
that are relatively hard to match subsequently.  For example,
the word "quiz" should  be tried before the word "bean", because
if our anagram contains a 'q' and a 'z' we want to fill those in
as quickly as possible in the search.
"""

import unittest
import word_heuristic

class TestHeuristic(unittest.TestCase):
    """Test the scoring function of word_heuristic."""

    def test_score_jerk(self):
        self.assertEqual(word_heuristic.score("jerk"),15)

    def test_score_quiz(self):
        self.assertEqual(word_heuristic.score("quiz"), 22)

if __name__ == "__main__":
    unittest.main()