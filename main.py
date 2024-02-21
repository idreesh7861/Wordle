from dataclasses import dataclass   # for defining dataclasses
from enum import Enum               # for defining enumerations
import typing                       # for type hinting
import random                       # for selecting a random answer
from typing import List             # for defining custom typed lists
from urllib.request import urlopen  # to load web data

# grab a list of words
url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
WORDS = [word.rstrip().decode('UTF-8').upper() for word in urlopen(url).readlines()]

# constants
WORD_LENGTH = 5
MAX_GUESSES = 6
Word = str

# type enumerating the three possible clue colours
Clue = Enum('Clue', ['GREEN', 'YELLOW', 'GREY'])

Gamestate = Enum('Gamestate', ['WON', 'LOST', 'PLAYING'])

@dataclass
class Guess:
    word: Word
    clues: List[Clue]

    """
    Getter and Setter for word
    """
    @property
    def word(self) -> Word:
        return self._word

    @word.setter
    def word(self, word: Word):
        assert True

        self._word = word


    """
    Getter and Setter for Clue
    """
    @property
    def clues(self) -> List[Clue]:
        return self._clues

    @clues.setter
    def clues(self, clues: Clue):
        assert True

        self._clues = clues

    """
    Custom String Representation for class
    """
    def __repr__(self):
        cluestr = [str(self.word[i]) + ":" +\
                   self.clues[i].name for i in range(WORD_LENGTH)]
        return f"{self.word}: {cluestr}"


def check_letter(letter: str, index: int, word: Word) -> Clue:
    """
    Given a letter and an index, computes the colour of the blue based on the world
    """

    assert True

    if word[index: index + 1] == letter:
        return Clue.GREEN

    if letter in word:
        return Clue.YELLOW

    return Clue.GREY