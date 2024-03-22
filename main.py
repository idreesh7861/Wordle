from dataclasses import dataclass  # for defining dataclasses
from enum import Enum  # for defining enumerations
import typing  # for type hinting
import random  # for selecting a random answer
from typing import List  # for defining custom typed lists
from urllib.error import URLError  # For catching URLError
from urllib.request import urlopen  # to load web data
from colorama import Fore  # For coloring text for hints
import time  # For adding delays in code

# grab a list of words

url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
try:
    WORDS = [word.rstrip().decode('UTF-8').upper() for word in urlopen(url).readlines()]
    setWords = set(WORDS)
except URLError as e:
    print("Internet Connection Error: {0}".format(e))
    print("Exiting...")
    quit()

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
class Hint:
    # Hint is defined as a single alphabetic uppercase character
    def __init__(self, hint):
        assert isinstance(hint, str) and \
            len(hint) == 1 and \
            hint.isalpha() and \
            hint.isupper(), "pre-hint assertion failed"

        # Sets hint to inputted value
        self.hint = hint

    def __str__(self):
        return self.hint


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
        # cluestr = [str(self.word[i]) + ":" +
        #            self.clues[i].name for i in range(WORD_LENGTH)]
        # return f"{self.word}: {cluestr}"
        colordict = {
            Clue.GREY: Fore.WHITE,
            Clue.YELLOW: Fore.YELLOW,
            Clue.GREEN: Fore.GREEN
        }
        cluestr = ""
        for i in range(WORD_LENGTH):
            cluestr += colordict[self.clues[i]] + self.word[i]
        cluestr += Fore.RESET
        return cluestr


def check_letter(letter: str, index: int, word: Word) -> Clue:
    """
    Given a letter and an index, computes the colour of the clue based on the word
    ORIGINAL IMPLEMENTATION
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


def check_green(letter: str, index: int, word: Word, char_count: dict) -> [Clue, dict]:
    if word[index: index + 1] == letter:
        char_count[letter] -= 1
        return Clue.GREEN, char_count

    return Clue.GREY, char_count


def check_yellow(letter: str, word: Word, char_count: dict) -> [Clue, dict]:
    if letter in word and char_count[letter] != 0:
        char_count[letter] -= 1
        return Clue.YELLOW, char_count

    return None, char_count


def check_guess(word: Word, guess: Word) -> List[Clue]:
    """
    Given the answer and a guess compute the list of clues corresponding to each letter
    """

    assert isinstance(word, Word) and \
           isinstance(guess, Word) and \
           len(guess) == WORD_LENGTH and \
           len(word) == WORD_LENGTH, "pre-check_guess failed"

    # Create a dictionary with a char count
    char_count = {}
    for char in word:
        if char in char_count.keys():
            char_count[char] += 1
        else:
            char_count[char] = 1

    clues = [Clue.GREY for i in range(WORD_LENGTH)]

    # Check Green

    for index, letter in enumerate(guess):
        clues[index], char_count = check_green(letter, index, word, char_count)

    # Check Yellow

    for index, letter in enumerate(guess):
        temp, char_count = check_yellow(letter, word, char_count)
        if temp is not None:
            clues[index] = temp

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
        for guess in self.guesses:
            print(guess)

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
        print("HINT: The letter {0} is the {1} letter in the word.".format(
            hint, numbers_to_ordinal(lst.index(str(hint)))))


def numbers_to_ordinal(number: int) -> str:
    assert isinstance(number, int) and 0 <= number <= 4
    match number:
        case 0:
            return "1st"
        case 1:
            return "2nd"
        case 2:
            return "3rd"
        case 3:
            return "4th"
        case 4:
            return "5th"
        case _:
            return "Error Occurred"


def playgame():
    game = Game()

    game.gstate = Gamestate.WON

    # Reset game to reset word from default

    game.reset()
    while game.gstate == Gamestate.PLAYING:
        game.print_state()
        Input = "TEST"

        while Input.upper() not in setWords:
            if Input.upper() == "HINT":
                game.print_state()
                game.print_hint()
            Input = input("Please enter a valid word\n")

        game.make_guess(Input)

    game.print_state()
    pass


def playHardMode():
    game = Game()
    game.gstate = Gamestate.WON

    # Reset game to reset word from default

    game.reset()

    while game.gstate == Gamestate.PLAYING:
        game.print_state()
        Input = "TEST"
        while Input.upper() not in setWords:
            # HARD MODE CODE
            #
            Input = input("HARDMODE: Please enter a valid word using all clues provided\n")
            Input = Input.upper()

            if Input == "HINT":
                game.print_state()
                game.print_hint()

            if Input in setWords:
                if len(game.guesses) != 0:
                    index = -1
                    for clue in game.guesses[len(game.guesses) - 1].clues:
                        index += 1
                        if clue == Clue.GREEN and Input[index] != game.guesses[len(game.guesses) - 1].word[index]:
                            Input = "TEST"
                            break

                        if clue == Clue.YELLOW and game.guesses[len(game.guesses) - 1].word[index] not in Input:
                            Input = "TEST"
                            break

        game.make_guess(Input)

    game.print_state()
    pass


def test():
    print(check_letter("S", 0, "STOUT"))  # Expected Output: CLUE.GREEN
    print(check_letter("S", 3, "STOUT"))  # Expected Output: CLUE.YELLOW
    print(check_letter("Z", 0, "STOUT"))  # Expected Output: CLUE.GREY

    print(check_guess("STAND", "STOUT"))
    # Expected Output: [<Clue.GREEN>, <Clue.GREEN>, <Clue.GREY>, <Clue.GREY>, <Clue.GREY>]

    try:
        hint1 = Hint('A')
        print(hint1)  # Expected Output: A

        hint2 = Hint('AB')  # Expected Output: Hint must be a single character
        print(hint2)
    except ValueError as error:
        print(error)

    try:
        hint3 = Hint('a')
        print(hint3)
    except ValueError as error:
        print(error)  # Expected Output: Hint must be a single uppercase letter A-Z

    input("\nPress the enter key to continue...")
    pass


def menu():
    """
    Function to print and navigate menu
    """
    while True:
        # Print Menu Options
        print("""
        1) Play Game
        2) Hard Mode
        3) Tests
        4) Quit
        """)
        try:
            # Accept user input to navigate menu
            int_input = int(input("Enter your choice: "))

            match int_input:
                case 1:
                    # Regular Game Mode
                    playgame()
                case 2:
                    # Hard Mode
                    playHardMode()
                case 3:
                    # Test Scenarios
                    test()
                case 4:
                    # Quit
                    quit()
                case _:
                    # If other numbers are entered
                    print("Invalid Entry")
                    time.sleep(1)
        except ValueError:
            # If input by user is not a number
            print("Invalid Entry")
            time.sleep(1)


def main():
    menu()


if __name__ == "__main__":
    main()
