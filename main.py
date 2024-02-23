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
        cluestr = [str(self.word[i]) + ":" + \
                   self.clues[i].name for i in range(WORD_LENGTH)]
        return f"{self.word}: {cluestr}"


def check_letter(letter: str, index: int, word: Word) -> Clue:
    """
    Given a letter and an index, computes the colour of the blue based on the word
    """

    assert True

    if word[index: index + 1] == letter:
        return Clue.GREEN

    if letter in word:
        return Clue.YELLOW

    return Clue.GREY


def check_guess(word: Word, guess: Word) -> List[Clue]:
    """
    Given the answer and a guess
    compute the list of clues correspsonding to each letter
    """
    assert True
    clues = []
    for index in range(6):
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
        assert True

        word = word.upper()
        guess = Guess(word, check_guess(self.answer, word))
        self.guesses.append(guess)

        won = True
        for results in guess.clues:
            if results == Clue.YELLOW or results == Clue.GREY:
                won = False
        
        if won == True:
            self.gstate = Gamestate.WON
        
        if len(self.guesses) == 6:
            self.gstate = Gamestate.LOST


    def print_state(self):
        """
        Print the current state of the game
        """
        for guess in self.guesses: print(guess)
        if self.gstate == Gamestate.WON: print(f"You Won! You took {len(self.guesses)} guesses.")
        elif self.gstate == Gamestate.LOST: print(f"You lost! The answer was: {self.answer}")
        else: print(f"Guess the wordle, you have {MAX_GUESSES - len(self.guesses)} guesses remaining")

    def game_over(self) -> bool:
        """
        Yields true if the game is over, otherwise false
        :return:
        """
        return self.gstate == Gamestate.WON or self.gstate == Gamestate.LOST

    def reset(self):
        """
        Reset the game by picking a new word, clearing the guesses
        and setting hte state back to playing
        :return:
        """
        assert self.game_over(), "Cannot reset, game in play"
        self.answer = random.choice(WORDS)
        self.guesses = []
        self.gstate = Gamestate.PLAYING

game = Game()
game.gstate = Gamestate.WON
game.reset()
while (game.gstate == Gamestate.PLAYING):
    game.print_state()
    Input = input()
    game.make_guess(Input)

game.print_state()