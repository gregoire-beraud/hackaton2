"""
toying around the MOTUS game
"""

from pathlib import Path
from itertools import islice
from functools import reduce
from enum import Enum, auto

"""
auto can be used in place of a value. If used, the Enum machinery will call an Enum's _generate_next_value_() to get an appropriate value. For Enum and IntEnum that appropriate value will be the last value plus one; for Flag and IntFlag it will be the first power-of-two greater than the highest value; for StrEnum it will be the lower-cased version of the member's name. Care must be taken if mixing auto() with manually specified values.

auto instances are only resolved when at the top level of an assignment:

    FIRST = auto() will work (auto() is replaced with 1);

    SECOND = auto(), -2 will work (auto is replaced with 2, so 2, -2 is used to create the SECOND enum member;

    THREE = [auto(), -3] will not work (<auto instance>, -3 is used to create the THREE enum member)

"""

from colorama import Back, Style, Fore


# on Enums: see https://docs.python.org/3/howto/enum.html
class Color(Enum):
    """
    the codes for creating an answer
    """

    RED = auto()  # full match
    YELLOW = auto()  # exists in another location
    BLUE = auto()  # not in word at all


    def outline(self, message: str):
        """
        a string colored with that color
        """
        if self.name == "RED":
            beg, end = Back.RED, Style.RESET_ALL
        elif self.name == "YELLOW":
            beg, end = Back.YELLOW, Style.RESET_ALL
        elif self.name == "BLUE":
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
        return "".join(
            color.outline(f"{char}") for char, color in zip(self.word, self.answer)
        )

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
            char for char, color in zip(self.word, self.answer) if color != Color.BLUE
        }
        apparently_not_there = {
            char for char, color in zip(self.word, self.answer) if color == Color.BLUE
        }
        return apparently_not_there - definitely_there
    
    def success(self, mot) -> bool:
        return self.word == mot


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
        return "".join(
            color.outline(f"{char}") for char, color in zip(self.word, [Color.BLUE]*(len(self)))
        )

    def __len__(self):
        return len(self.word)

    def attempt(self, typed: str) -> Attempt:
    
        if len(self) != len(typed):
            raise ValueError(f"length mismatch {len(self)} != {len(typed)}")
        # first pass is to spot exact matches
        red_indices = {
            index for index, (ct, ch) in enumerate(zip(typed, self.word))
            if ct == ch}

        typed_sans_r = list(typed)
        for i in red_indices:
            typed_sans_r[i] = "0"
        typed_sans_r = "".join(typed_sans_r)
        #print(typed_sans_r)

        hidden_sans_r = list(self.word)
        for i in red_indices:
            hidden_sans_r[i] = "0"
        hidden_sans_r = "".join(hidden_sans_r)
        #print(hidden_sans_r)

        yellow_indices = set()
        for index, ct in enumerate(typed_sans_r):
            if index not in red_indices and ct in hidden_sans_r:
                yellow_indices.add(index)
                hidden_sans_r = hidden_sans_r.replace(ct, "0", 1)

        # fill the result
        result = []
        for i in range(len(self)):
            if i in red_indices:
                result.append(Color.RED)
            elif i in yellow_indices:
                result.append(Color.YELLOW)
            else:
                result.append(Color.BLUE)
        return Attempt(typed, Answer(*result))
    
    def indice_lettre(self, attempts: Attempts) -> str:
        """
        Révèle une lettre bien placée que le joueur n'a pas encore trouvée.
        """
        found = set()
        
        # Regarder toutes les lettres que le joueur a déjà trouvées (RED)
        for attempt in attempts:
            for i, color in enumerate(attempt.answer.colors):
                if color == Color.RED:
                    found.add(i)  # On marque la position comme découverte

        # Trouver une lettre encore cachée
        for i, letter in enumerate(self.word):
            if i not in found:
                return f"Indice : La {i+1}ᵉ lettre est '{letter}'."

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

    def sample_of_length(self, length) -> str:
        """
        for convenience, returns one word of length length
        """
        # we have already the logic to extract all words, so just take
        # the first one using islice, because all_words_of_length())
        # returns an iterator, so we cannot use regular [] here
        # also, nicely handle the case where length is too large
        # and there is not word of that length
        try:
            return next(islice(self.all_words_of_length(length), None, 1))
        except StopIteration:
            pass

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
            set(),
        )
        comb = {
            word
            for word in self.all_words_of_length(length)
            if not (set(word) & set(absent_chars))
        }

        def match(candidate):
            # does a candidate word yield the same answers
            # as the ones provided in parameter ?
            return all(
                Hidden(candidate).attempt(attempt.word) == attempt
                for attempt in attempts
            )

        return {word for word in comb if match(word)}


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
        return "".join(Color.RED.outline(x) for x in hidden)

    print(f"with hidden word : {_hidden(hidden)}")
    print(f"   you would get : {Hidden(hidden).attempt(word)}")
    print(f"         because : {Hidden(word).attempt(hidden)}")
