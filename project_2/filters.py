"""Filter overlong lists of anagrams to include only those that
are deemed interesting in some way.
"""

import logging
logging.basicConfig()
log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
def filter_only_unique(raw: list[list[str]]) -> list[list[str]]:
    """Given a list like
        dance case it
        stead can ice
        ice cat end as
    return just
        dance case it
        ice cat end as
    i.e., phrases with no duplicates among them.
    This may be preferred for VERY long lists of anagram phrases,
    but may filter useful words from shorter lists.
    """
    log.info(">>> filter_only_unique")
    seen = set()
    filtered = []
    for phrase in raw:
        dups = False
        for word in phrase.split():
            if word in seen:
                dups = True
                break
        if not dups:
            filtered.append(phrase)
            for word in phrase.split():
                seen.add(word)
    return filtered

def filter_some_unique(raw: list[list[str]]) -> list[list[str]]:
    """Produce phrases that 'cover' the unique words, i.e., each
    phrase introduces at least one word that hasn't appeared before.
    """
    log.info(">>> filter_some_unique")
    seen = set()
    filtered = []
    for phrase in raw:
        log.debug("Phrase {phrase} splits into {phrase.split()}")
        words = phrase.split()
        for word in words:
            log.debug(f"Word: {word}")
            if word not in seen:
                filtered.append(phrase)
                for word in words:
                    seen.add(word)
                break
    return filtered

def filter_unique_words(raw: list[list[str]]) -> list[str]:
    """Return a list of distinct words (not phrases) that appear in some
    phrase.
    """
    log.info(">>> filter_unique_words")
    seen = set()
    filtered = []
    for phrase in raw:
        log.debug(f"Phrase: {phrase}")
        for word in phrase.split():
            log.debug(f"Word: {word}")
            if word not in seen:
                log.debug(f"First time seeing: {word}")
                seen.add(word)
                filtered.append(word)
    return filtered