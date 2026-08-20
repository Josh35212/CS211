"""Configuration options for multi-word anagram finder"""


# Which word list to use.  You may want longer or shorter word lists depending
# on whether you are getting a flood or anagrams or a trickle.
DICT =   "data/ngsl.csv"           # Pretty good for more common words
# DICT = "data/wordlist.10000.txt"   # Lousy --- lots of abbreviations
# DICT = "data/1-1000.txt"           # Limited
#DICT = "data/dict.txt"               # The 40,000 word list we used for single word anagrams in CS 210
# DICT = "data/nifty-3.txt"            # From Stuart Reges' entry in Nifty Projects database
# DICT = "data/cs_sample.txt"            # Tiny list for test cases


# Some large word lists contain "words" that are almost never useful,
# especially very short words that can dominate the list.  Rather than
# clean out all the word lists, we'll create a "stop list" to always
# exclude.

STOP_LIST = set([
    "b", "c", "d", "e", "f", "g", "h", "j", "k", "l",
    "m", "n", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "ru", "ur", "su", "og", "un", "usr", "sg", "oo", "ooo", "rg",
    "ou", "gg", "o", "ro", "nr", "nu", "ng", "os", "sur", "oe", "geo",
    "eu", "oe", "seo", "er", "es", "eos", "ot", "et", "st", "ts", "ea",
    "ae", "ns", "nt", "tt", "sn", "en", "ste", "est", "soa", "sao",
    "rt", "tr", "ta", "re", "se", "ee", "tn", "fo", "ge", "gr", "fe",
    "ef", "eur", "fi", "fs", "sf", "im", "sh"
])
