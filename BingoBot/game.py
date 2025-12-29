import discord

from bingo import * # greed 
from discord.ext import commands
###
# GameData/
# |-seshid/
#   |-form_responses
#   |-instance_data 
class Game:
    __active_sessions = {} # {sesh_id : data_directory, ...}
    
    def __init__(self, guild_invoked: discord.Guild, invoker: discord.User):
        self.sesh_id: str = "" #! Game is NOT serializable, too many other components. 
                               #? Possible solution: make a dict representation of all relevant classes.
        self.sesh_data_dir = ""
        
        self.data_loaded = False

        self.free_squares: dict[str, list[CardSquare]] = {}
        self.personal_squares: dict[str, list[CardSquare]] = {}
        self.random_squares: list[CardSquare] = []

        self.players: list[str] = []
        self.player_to_card: dict[str, BingoCard] = {}
        self.session_card: BingoCard = None

    # def save(self):
    #     pass
    
    # @staticmethod
    # def postsave(func):
    #     def wrapper():
    #         func()
    #     return wrapper

    def init_sesh_id(self, guild_id: int, invoker_id: int) -> str:
        sesh_id = str(len(Game.__active_sessions)) + ":<" + hex(guild_id) + ">" + ",<" + hex(invoker_id) + ">"
        Game.__active_sessions
        return sesh_id

    def game_start(self):
        self.generate_boards()

    def generate_boards(self):
        """ Initializes player_to_card. """
        if not self.data_loaded:
            self.load_square_data()

        for player in self.players:
            p_b = BingoCard(player)
            p_b.generate_board(
                self.free_squares[player], 
                self.personal_squares[player], 
                self.random_squares)
            self.player_to_card[player] = p_b

    def load_square_data(self):
        """ Loads the user square suggestions into free, personal, and random squares.

        Raises:
            Exception: If somehow the format of the form response json is wrong.
        """
        response_dict = GameData.get_data_from_json("form_responses.json")[0] #? This will change for session IDs

        for user in response_dict:
            self.players.append(user)
            for i, (key, value) in enumerate(response_dict[user].items()):
                print(f"key: {key}\nvalue: {value}")
                match key:
                    case "Free":
                        if (self.free_squares.get(user) == None):
                            self.free_squares[user] = []
                        self.free_squares[user].extend(BingoCard.to_bingo_squares("Free", value))
                    case "Personal":
                        if (self.personal_squares.get(user) == None):
                            self.personal_squares[user] = []
                        self.personal_squares[user].extend(BingoCard.to_bingo_squares("Personal", value))
                    case "Random": 
                        self.random_squares.extend(BingoCard.to_bingo_squares("Random", value))
                    case _:
                        raise Exception(f"How'd you get here? iter: {i}")


    def print_data(self):
        print(self.free_squares)
        print(self.personal_squares)
        print(self.random_squares)
