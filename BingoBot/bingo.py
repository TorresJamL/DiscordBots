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

import discord

### Format for 5x5 ###
#* R P P P R
#* P R R R P
#* P R F R P
#* P R R R P
#* R P P P R
### Format for 5x5 ###

class BingoCard:
    def __init__(self, owner: str, is_individual:bool = True, ):
        self.bingo_grid = []

class CardSquare:
    """ A class to represent a singular square on a bingo card.

    Parameters
    -------------
    sq_type: :class:`str`
        The type of the square: 
        
        .. Free:: The middle square of a bingo card.
        .. Personal:: A person goal square of a bingo card.
        .. Random:: Any random event square of a bingo card.

    sq_val: :class:`str`
        The contents of the square.

    user_of_origin: Optional[:class:`str` | :class:`discord.User` | :class:`discord.Member`]
        The discord user that created the square.
        
        .. useless:: Only meant to be used for debugging purposes.
    """
    def __init__(self, sq_type, sq_val, user_of_origin = None):
        self.type = sq_type
        self.val = sq_val
        self.state = True
        self.__og_user = user_of_origin

    def get_origin(self):
        return self.__og_user
    
    def __str__(self):
        return self.val
    
    def __eq__(self, other):
        return self.type == other.type and self.val == other.val
