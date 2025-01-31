"""
toying around the MOTUS game
"""

from pathlib import Path
from itertools import islice
from functools import reduce
from enum import Enum, auto
from typing import Optional
"""
auto can be used in place of a value. If used, the Enum machinery will call an Enum's _generate_next_value_() to get an appropriate value. For Enum and IntEnum that appropriate value will be the last value plus one; for Flag and IntFlag it will be the first power-of-two greater than the highest value; for StrEnum it will be the lower-cased version of the member's name. Care must be taken if mixing auto() with manually specified values.

auto instances are only resolved when at the top level of an assignment:

    FIRST = auto() will work (auto() is replaced with 1);

    SECOND = auto(), -2 will work (auto is replaced with 2, so 2, -2 is used to create the SECOND enum member;

    THREE = [auto(), -3] will not work (<auto instance>, -3 is used to create the THREE enum member)

"""

from colorama import Back, Style

# on Enums: see https://docs.python.org/3/howto/enum.html
class Color(Enum):
    """
    the codes for creating an answer
    """

    RED = auto()     # full match
    YELLOW = auto()  # exists in another location
    BLUE = auto()   # not in word at all

    def outline(self, message: str):
        """
        a string colored with that color
        """
        if self.name == "RED":
            beg, end = Back.RED, Style.RESET_ALL
        elif self.name == "YELLOW":
            beg, end = Back.YELLOW, Style.RESET_ALL
        else:
            beg, end = Back.BLUE, Style.RESET_ALL
        return f"{beg} {message} {end} "
    
    def __eq__(self, other):
        # surprisingly this is required...
        return self.name == other.name


# shortcuts
R, Y, B = Color.RED, Color.YELLOW, Color.BLUE


class Answer:
    """
    primarily an ordered tuple of colors
    """
    def __init__(self, *colors: Color):
        # no need to transform into tuple
        self.colors = colors

    def __eq__(self, other):
        return self.colors == other.colors

    def __iter__(self):
        return iter(self.colors)

    def right(self):
        """
        is it a right answer ?
        """
        return all(x == Color.RED for x in self.colors)


class Attempt:
    """
    record the fact that you get an answer for a word
    """
    def __init__(self, word: str, answer: Answer):
        self.word = word
        self.answer = answer

    def __repr__(self):
        return "".join(color.outline(char)for char, color in zip(self.word, self.answer))

    def __iter__(self):
        """
        allows to unpack e.g.
        word, answer = attempt
        """
        yield self.word
        yield self.answer

    def __len__(self):
        return len(self.word)

    def __eq__(self, other):
        return self.answer == other.answer

    def absent_chars(self):
        """
        returns a set of chars that are only marked BLUE
        so we know they are not in the hidden word
        """
        # but of course we must be a little careful
        definitely_there = {
            char for char, color in zip(self.word, self.answer)
            if color != Color.BLUE
        }
        apparently_not_there = {
            char for char, color in zip(self.word, self.answer)
            if color == Color.BLUE
        }
        return apparently_not_there - definitely_there


# define this alias for type hinting
Attempts = list[Attempt]


class Hidden:

    """
    models the hidden word, and provide the algorithm to compare
    a typed word with the hidden one
    """
    def __init__(self, word: str):
        self.word = word

    def __repr__(self):
        return f"Hidden({self.word})"

    def __len__(self):
        return len(self.word)

    def attempt(self, typed: str) -> Attempt:
        """
        compares the typed answer with the hidden word
        and returns an Attempt object that summarizes the result

        there is a subtlety with chars appearing several times,
        so a few examples:

        | hidden | typed | result | comment |
        | ABC    | AAA   | RBB    | a single match |
        | ABCA   | AAAA  | RBBR   | two matches    |
        | ABCA   | AAAY  | RBYB   | one exact match and one partial |

        this version is clearly broken and you job is to fix it
        """
        if len(self) != len(typed):
            raise ValueError(f"length mismatch {len(self)} != {len(typed)}")
        # first pass is to spot exact matches
        red_indices = {
            index for index, (ct, ch) in enumerate(zip(typed, self.word))
            if ct == ch}
        restants_hidden = [ch for index, ch in enumerate(self.word) if index not in red_indices]
        restants_typed = [ct for index, ct in enumerate(typed) if index not in red_indices]

        yellow_indices = set()
    
        for index, char in enumerate(restants_typed):
            if char in restants_hidden:
                restants_hidden[restants_hidden.index(char)] = ''  
                yellow_indices.add(index)  
        result = []
        for i in range(len(self)):
            if i in red_indices:
                result.append(Color.RED)
            elif i in yellow_indices:
                result.append(Color.YELLOW)
            else:
                result.append(Color.BLUE)
        return Attempt(typed, Answer(*result))


class Dictionary:

    """
    primarily a set of words
    """

    def __init__(self, filename):
        self.filename = filename
        with Path(self.filename).open(encoding="utf-8") as feed:
            self.words = {line.strip().lower() for line in feed}

    def __contains__(self, word: str):
        return word.lower() in self.words

    def __iter__(self):
        return iter(self.words)

    def all_words_of_length(self, length: int):
        """
        iterator on all words of that length
        """
        for word in self:
            if len(word) == length:
                yield word

    def sample_of_length(self, length: int) -> Optional[str]:
        """
        For convenience, returns one word of length 'length'.
        If no word of that length exists, returns None.
        """
        try:
            return next(islice(self.all_words_of_length(length), None, 1))
        except StopIteration:
            return None

    def compatible_words(self, attempts: Attempts, length) -> set[str]:
        """
        given what has been tried so far (the attempts)
        returns the words that could fit
        """
        # it is the caller's responsability to ensure all the attempts
        # have the same length, and that it matches length
        # this is so that one can call this function with an empty list
        # of attempts

        # first we rule out all words that have any of the
        # chars that we know for sure are not present
        # this is a union of sets
        absent_chars = reduce(
            lambda s1, s2: s1 | s2,
            (attempt.absent_chars() for attempt in attempts),
            set()
        )
        comb = {
            word for word in self.all_words_of_length(length)
            if not (set(word) & set(absent_chars))
        }
        def match(candidate):
            # does a candidate word yield the same answers
            # as the ones provided in parameter ?
            return all(
                Hidden(candidate).attempt(attempt.word) == attempt
                for attempt in attempts)

        return { word for word in comb if match(word) }


# ignore this code, that is useful only to produce
# illustrations for the README.md file
def show_example(hidden, word) -> None:
    """
    print the explanation of the results obtained with these words
    """
    def _hidden(hidden) -> str:
        """
        helper function to display a hidden word with the same spacing
        as the attempts
        """
        return "".join(
            Color.RED.outline(x) for x in hidden
        )

    print(f"with hidden word : {_hidden(hidden)}")
    print(f"   you would get : {Hidden(hidden).attempt(word)}")
    print(f"         because : {Hidden(word).attempt(hidden)}")

