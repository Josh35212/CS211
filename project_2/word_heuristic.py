"""Heuristic scoring of dictionary words for finding multi-word anagrams.
A phrase may have a very large number of (multi-word) anagrams.  Since we
may cut off the search before enumerating all of them, we would like to enumerate
"better" anagrams earlier in the search.

We would also like to minimize time
wasted on searches that cannot lead to a good anagram.  For example,
if the phrase to be anagrammed includes a J, we should try to include
words that have a J early in the search.
"""

"""Scrabble letter scores are a decent approximation of infrequency."""
POINTS_TO_LETTERS = {1: "aeioulnstr",
                     2: "dg",
                     3: "bcmp",
                     4: "fhvwy",
                     5: "k",
                     8: "jx",
                     10: "qz"}

# Map letters to points once at initiation
LETTERS_TO_POINTS = { }
for value,letters in POINTS_TO_LETTERS.items():
    for letter in letters:
        LETTERS_TO_POINTS[letter] = value



def score(word: str) -> int:
    """ Heuristic value based on length of normalized_word, with extra credit for
    infrequently appearing letters, is approximated by Scrabble score
    for the normalized_word.  It is just the sum of the scores of the
    individual letters.
    """
    sum = 0
    for letter in word.lower():   # Converts "17 Crows"
        if letter.islower():      # Ignores non-letters, we score "crows"
            sum += LETTERS_TO_POINTS[letter]
    return sum


