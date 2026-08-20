"""
CS211 Project 2, 1/20/26
Name: Josh Gilliam
Credit: N/A

A bag of letters for finding anagrams.
Associates a cardinality (count) with each character
in the bag.
"""

def normalize(phrase: str) -> list[str]:
    """Normalize word or phrase to the
    sequence of letters we will try to match, discarding
    anything else, such as blanks and apostrophes.
    Return as a list of individual letters.
    """
    normalized = []
    for ch in phrase:
        if ch.isalpha():
            normalized.append(ch.lower())
    return normalized
    

class LetterBag:
    """A bag (also known as a multiset) is
    a map from keys to non-negative integers.
    A LetterBag is a bag of single character
    strings.
    """
    def __init__(self, word=""):
        """Create a LetterBag"""
        self.word = word.strip()
        normal = normalize(self.word)
        self.length = len(normal)  # Counts letters only!
        self.letters = {} # Dict should be a count of normal characters

        for ch in normal:
            if ch not in self.letters:
                self.letters[ch] = 1
            else:
                self.letters[ch] += 1

    def __len__(self):
        return self.length

    def __str__(self):
        return self.word

    def __repr__(self):
        counts = [f"{ch}:{n}" for ch, n in self.letters.items() if n > 0]
        return f'LetterBag({self.word}/[{", ".join(counts)}])'
    
    def contains(self, other: "LetterBag") -> bool:
        """Determine whether enough of each letter in
        other LetterBag are contained in this LetterBag.
        """
        for ch in other.letters:
            if ch not in self.letters:
                return False
            elif self.letters[ch] < other.letters[ch]:
                return False
        return True
    
    def copy(self) -> "LetterBag":
        """Make a copy before mutating."""
        copy_ = LetterBag()
        copy_.word = self.word
        copy_.letters = self.letters.copy() # Copied to avoid aliasing
        copy_.length = self.length
        return copy_
    
    def take(self, other: "LetterBag") -> "LetterBag":
        """Return a LetterBag after removing
        the letters in other.  Raises exception
        if any letters are not present.
        """
        bag = self.copy()
        for ch, count in other.letters.items():
            assert ch in bag.letters    # ch must be in bag.letters
            assert count <= bag.letters[ch]  # can't take letters from nothing
            bag.letters[ch] -= count
            bag.length -= count
        return bag

