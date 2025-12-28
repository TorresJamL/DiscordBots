# Each bingo card has squares for the free space, personal goal spaces, and just random event spaces
## Personal goals are guaranteed to be on your own card
##* They can also appear on the MAIN bingo card, but only 1 personal goal from each person
## Random event spaces are just there, they can be any event POSSIBLE within the year
## Free spaces are always the middle square on the bingo grid. They should be near GUARANTEED to happen
##! PEOPLE CAN CURRENTLY SUBMIT MULTIPLE FREE SPACES, HANDLING OF THIS MIGHT NEED RECONSIDERING

# The main bingo card should be bigger than the individual player cards. 
## Player cards should be 5x5
## Main card should be anywhere from 7x7 to 11x11 although currently I believe 7x7 to be optimal.
# I have not decided whether the win conditions for a bingo card should the same as traditionally or
#-have the player cards play by stricter win conditions than the main card.
## Tradition win is 5 squares in a line crossed out. 
## Strict rules is the entire board must be complete
##? I doubt playing by strict rules will feel good, but for the 5x5 board it *might* work. 

# Player cards naturally should be private, but if a player wants to show his card to someone else, they should be able to.

# TODO - by December 30 #
# Bingo card class
## This should hold a grid of squares and the player who owns this card.
##? Grid implementation might end up being a hassle. For now, it should be a 2D array.
##* Random squares are universal to all playing cards. So the game class will have to hold a Game-Scope collection of the squares.
##? Personal Goals are iffy, changing the form to ask whether they'd like the goal to appear on the main board might be the play
##?-but I can't say I like that from the developer side of things.
# Bingo card square class
## This should hold the type of square and the value it should hold. (Basically a bad struct)
# Game class
## This is technically unnecessary, but having a game class means multiple instances of the game can happen at once.
## All of the discord interactions should be held in this class
### Reminder - Players should have the power to make their board visible when prompting to see it. 

# All of these can be in one file. If it becomes messy, i'll organize them.

from game_utils import GameruleException, GameData
from dataclasses import dataclass
import random
### Format for 5x5 ###
#* R P P P R
#* P R R R P
#* P R F R P
#* P R R R P
#* R P P P R
### Format for 5x5 ###
@dataclass
class CardSquare:
    sq_type: str
    sq_val: str
    state: bool

class BingoCard:
    def __init__(self, owner: str, is_individual:bool = True, n:int = 5):
        if n % 2 == 0: 
            raise GameruleException(f"n must be odd. Caught: n = {n}")
        self.owner = owner
        self.is_individual = is_individual
        self.n = n

        self.grid = [None] * n

    @staticmethod
    def to_bingo_squares(sq_type:str, sq_vals:list):
        return list(map(lambda val : CardSquare(sq_type, val, True), sq_vals[:]))

    def generate_board(
            self, 
            p_squares:list[CardSquare], 
            r_squares:list[CardSquare], 
            f_squares:list[CardSquare]):
        """_summary_

        Args:
            p_squares (list[CardSquare]): _description_
            r_squares (list[CardSquare]): _description_
            f_squares (list[CardSquare]): _description_

        Raises:
            GameruleException: _description_
            GameruleException: _description_
        """
        if len(p_squares) + len(r_squares) + 1 < self.n **2:
            raise GameruleException(f"Not enough squares for user:{self.owner}'s bingo card.")
        
        if self.n == 5:
            priority_format_5x5 = [
                ['R', 'P', 'P', 'P', 'R'],
                ['P', 'R', 'R', 'R', 'P'],
                ['P', 'R', 'F', 'R', 'P'],
                ['P', 'R', 'R', 'R', 'P'],
                ['R', 'P', 'P', 'P', 'R'],
            ]
            def __create_square(i:int, j:int, L: list, M:list):
                """Changes grid @ (i, j) to a random item in L, if L is empty: choose a random item from M."""
                if L:
                    self.grid[i][j] = random.choice(L)
                    L.remove(self.grid[i][j])
                else:
                    self.grid[i][j] = random.choice(M)
                    M.remove(self.grid[i][j])

            p = p_squares[:]
            r = r_squares[:]
            f = f_squares[:]
            for i in range(5):
                for j in range(5):
                    match priority_format_5x5[i][j]:
                        case 'P':
                            __create_square(i, j, p, r)
                        case 'R':
                            __create_square(i, j, r, p)
                        case 'F':
                            if f: self.grid[i][j] = random.choice(f)
                            else: raise GameruleException("No Free Squares Provided.")
        else:
            squares = p_squares[:] + r_squares[:]
            for i in range(self.n):
                for j in range(self.n):
                    if i == self.n // 2 and j == self.n // 2:
                        self.grid[i][j] = random.choice(f_squares)

    def load_card(self):
        """Generates a bingo card from an pre-existing format."""
        pass

def test():
    resp = GameData.get_data_from_json("form_responses.json")[0]
    sqs = BingoCard.to_bingo_squares(resp['zingiez'])

test()