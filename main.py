from dataclasses import dataclass  # for defining dataclasses
from enum import Enum  # for defining enumerations
import typing  # for type hinting
import random  # for selecting a random answer
from typing import List  # for defining custom typed lists
from urllib.request import urlopen  # to load web data

# grab a list of words

url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
WORDS = [word.rstrip().decode('UTF-8').upper() for word in urlopen(url).readlines()]

# constants

WORD_LENGTH = 5
MAX_GUESSES = 6
Word = str


# type enumerating the three possible clue colours

class Clue(Enum):
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    GREY = 'GREY'


class Gamestate(Enum):
    WON = 'WON'
    LOST = 'LOST'
    PLAYING = 'PLAYING'


# Hint is defined as a single alphabetic uppercase character
class Hint:
    def __init__(self, hint):

        # Ensures a string

        if not isinstance(hint, str):
            raise TypeError("Hint must be a string")

        # Ensures a single character

        if len(hint) != 1:
            raise ValueError("Hint must be a single character")

        # Ensures is alphabetic and upper

        if not hint.isalpha() or not hint.isupper():
            raise ValueError("Hint must be a single uppercase letter A-Z")

        # Sets hint to hint
        self.hint = hint

    def __str__(self): return self.hint


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
        assert isinstance(word, Word), "Word must be of type word"

        self._word = word

    """
    Getter and Setter for Clue
    """

    @property
    def clues(self) -> List[Clue]:
        return self._clues

    @clues.setter
    def clues(self, clues: Clue):
        assert isinstance(clues, list)

        self._clues = clues

    """
    Custom String Representation for class
    """

    def __repr__(self):
        cluestr = [str(self.word[i]) + ":" + \
                   self.clues[i].name for i in range(WORD_LENGTH)]
        return f"{self.word}: {cluestr}"


def check_letter(letter: str, index: int, word: Word) -> Clue:
    """
    Given a letter and an index, computes the colour of the clue based on the word
    """

    assert isinstance(index, int) and \
           isinstance(letter, str) and \
           isinstance(word, Word) and \
           0 <= index <= WORD_LENGTH and \
           len(word) == WORD_LENGTH, "pre-check_letter failed"

    if word[index: index + 1] == letter:
        return Clue.GREEN

    if letter in word:
        return Clue.YELLOW

    return Clue.GREY


def check_guess(word: Word, guess: Word) -> List[Clue]:
    """
    Given the answer and a guess compute the list of clues corresponding to each letter
    """
    assert isinstance(word, Word) and \
           isinstance(guess, Word) and \
           len(guess) == WORD_LENGTH and \
           len(word) == WORD_LENGTH, "pre-check_guess failed"

    clues = []
    for index, letter in enumerate(guess):
        clues.append(check_letter(guess[index: index + 1], index, word))

    return clues


class Game:
    answer: Word
    guesses: List[Guess]
    gstate: Gamestate

    def __init__(self, answer="STOUT"):
        # Game Constructor
        self.answer = answer
        self.guesses = []
        self.gstate = Gamestate.PLAYING

    def make_guess(self, word: Word):
        """
        Make a guess at the wordle
        """
        assert self.gstate == Gamestate.PLAYING and \
               isinstance(word, Word) and \
               len(word) == WORD_LENGTH and \
               word.upper() in WORDS, "make-guess assertion failed"

        word = word.upper()
        guess = Guess(word, check_guess(self.answer, word))
        self.guesses.append(guess)

        if not (Clue.YELLOW in guess.clues or Clue.GREY in guess.clues):
            self.gstate = Gamestate.WON

        if len(self.guesses) == 6:
            self.gstate = Gamestate.LOST

    def print_state(self):
        """
        Print the current state of the game
        """
        for guess in self.guesses: print(guess)
        if self.gstate == Gamestate.WON:
            print(f"You Won! You took {len(self.guesses)} guesses.")
        elif self.gstate == Gamestate.LOST:
            print(f"You lost! The answer was: {self.answer}")
        else:
            print(f"Guess the wordle, you have {MAX_GUESSES - len(self.guesses)} guesses remaining")

    def game_over(self) -> bool:
        """
        Yields true if the game is over, otherwise false
        """
        return self.gstate == Gamestate.WON or self.gstate == Gamestate.LOST

    def reset(self):
        """
        Reset the game by picking a new word, clearing the guesses
        and setting the state back to playing
        """
        assert self.game_over(), "Cannot reset, game in play"
        self.answer = random.choice(WORDS)
        self.guesses = []
        self.gstate = Gamestate.PLAYING

    def print_hint(self):
        lst = []
        for letter in self.answer:
            lst.append(letter)

        hint = Hint(random.choice(lst))
        print("HINT: The letter {0} is at position {1} in the word.".format(hint, lst.index(str(hint)) + 1))


def test():

    # Test cases to be included here

    print(check_letter("S", 0, "STOUT"))  # Expected Output: CLUE.GREEN
    print(check_letter("S", 3, "STOUT"))  # Expected Output: CLUE.YELLOW
    print(check_letter("Z", 0, "STOUT"))  # Expected Output: CLUE.GREY

    print(check_guess("STAND", "STOUT"))
    # Expected Output: [<Clue.GREEN: 1>, <Clue.GREEN: 1>, <Clue.GREY: 3>, <Clue.GREY: 3>, <Clue.YELLOW: 2>]

    try:
        hint1 = Hint('A')
        print(hint1)  # Output: A

        hint2 = Hint('AB')  # ValueError: Hint must be a single character
    except ValueError as e:
        print(e)

    pass


game = Game()

# test()

game.gstate = Gamestate.WON

# Reset game to reset word from default

game.reset()
while game.gstate == Gamestate.PLAYING:
    game.print_state()
    Input = "TEST"

    while Input.upper() not in WORDS:
        Input = input("Please enter a valid word\n")
        if Input.upper() == "HINT":
            game.print_state()
            game.print_hint()

    game.make_guess(Input)

game.print_state()
