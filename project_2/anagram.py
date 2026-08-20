"""
CS211 Project 2, 1/20/26
Name: Josh Gilliam
Credit: 
    - Chatgpt mapped out the necessity for using the str() method from letter_bag.py, line 61
    - Chatgpt introduced/explained how the .join() method works, line 65

Find anagrams (potentially multi-word) for a word or phrase.
"""

import config
import io
from letter_bag import LetterBag 
import argparse
import columns
import word_heuristic
import filters

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def read_word_list(f: io.TextIOBase) -> list[str]:
    """Reads list of words, exactly as-is except
    for stripping off leading and trailing whitespace
    including newlines.
    """
    words = []
    for word in f:
        clean_word = word.strip()
        if clean_word in config.STOP_LIST:
            continue
        words.append(clean_word)
    return words

def search(letters: LetterBag,
           candidates: list[LetterBag],
           limit: int=500,
           seed: str="") -> list[str]:
    """Returns a list of anagrams for letters, where
     each anagram is constructed from entries in the
     candidates list.
     """

    result = []

    # List of candidates, limit, and result list are visible to the
    # nexted function, and need not be passed to it.

    def _search(letters: LetterBag,  # The letters we can draw from
                pos: int,            # Position in list of word list letterbags
                phrase: list[str]    # The phrase we are building
                ):
        """Recursive function has the effect of adding phrases to result"""
        if len(result) >= limit:  # prevents potential recursion errors
            return
        for i in range(pos, len(candidates)):
            if letters.contains(candidates[i]):
                new_phrase = phrase.copy()      # must create a copy, don't modify original
                new_phrase.append(str(candidates[i]))
                new_letters = letters.take(candidates[i])

                if len(new_letters) == 0:
                    result.append(" ".join(new_phrase))
                else:
                    _search(new_letters, i + 1, new_phrase)
                
    # Initiate a single search at position 0 with an empty phrase,
    # after seeding if appropriate
    phrase = []
    if seed:
        phrase.append(seed)
        lb_seed = LetterBag(seed)
        letters = letters.take(lb_seed)
    _search(letters,  0, phrase)
    return result
    
def cli() -> argparse.Namespace:
    """Command line interface"""
    parser = argparse.ArgumentParser("Search for multi-word anagrams")
    parser.add_argument("phrase", type=str)
    parser.add_argument("--words",
                        action='store_true',
                        help="List of words that could appear in a multi-word anagram")
    parser.add_argument("--seed", type=str, default="",
                        help="Just anagrams that include this seed word or phrase",
                        nargs="?")
    parser.add_argument("--cover",
                        action='store_true',
                        help="Just anagrams with at least one distinct word")
    parser.add_argument("--disjoint",
                        action='store_true',
                        help="Just anagrams that have no words in common")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Stop after discovering this many anagrams (before filtering)",
                        nargs="?")
    args = parser.parse_args()
    return args

def main():
    """Search for multi-word anagrams."""
    args = cli()  # Command line interface
    bag = LetterBag(args.phrase)
    words = read_word_list(open(config.DICT, "r"))
    # Preferably explore long candidate words with infrequent letters.
    words.sort(key=word_heuristic.score,reverse=True)
    candidates = [LetterBag(word) for word in words]
    # Filter words that can't be built
    candidates = [cand for cand in candidates if bag.contains(cand)]
    seed = args.seed
    anagrams = search(bag, candidates, seed=seed, limit=args.limit)
    if args.words:
        ### Only distinct words found in the anagrams
        filtered = filters.filter_unique_words(anagrams)
    elif args.disjoint:
        ### Only phrases that don't repeat any words from seen phrases
        filtered = filters.filter_only_unique(anagrams)
    elif args.cover:
        ### Only phrases that introduce at least one new word
        filtered = filters.filter_some_unique(anagrams)
    else:
        filtered = anagrams
    columnized = columns.columns(filtered, col_width=len(args.phrase)+5)
    print(columnized)

if __name__ == "__main__":
    main()