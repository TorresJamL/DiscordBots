import discord

from bingo import *
from graphics import CardGraphic

###! IDEA ABANDONED FOR NOW
# GameData/
# |-seshid/
#   |-form_responses
#   |-instance_data 
class Game:    
    def __init__(self):
        self.data_loaded = False

        self.free_squares: dict[str, list[CardSquare]] = {}
        self.personal_squares: dict[str, list[CardSquare]] = {}
        self.random_squares: list[CardSquare] = []

        self.players: list[str] = []
        self.player_to_card: dict[str, BingoCard] = {}
        self.session_card: BingoCard = None

    def save(self):
        pass
    
    # @staticmethod
    # def postsave(func):
    #     def wrapper():
    #         func()
    #     return wrapper

    def game_start(self):
        self.generate_boards()

    def save_data_exists(self):
        pass

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

    def cross_out_sq(self, user: str, squ_coord: tuple[int]):
        self.player_to_card[user].flip_squ_state(squ_coord[0], squ_coord[1], False)

    def print_data(self):
        print(self.free_squares)
        print(self.personal_squares)
        print(self.random_squares)

def test():
    temp_dict = {
        "zingiez": {
            "Free": [],
            "Personal": [],
            "Random": []
        }
    }
    for i in range(random.randint(13, 30)):
        temp_dict['zingiez']['Free'].append(f"FreeSQ #{i}")
        temp_dict['zingiez']['Personal'].append(f"PersSQ #{i}")
        temp_dict['zingiez']['Random'].append(f"RandSQ #{i}")
    
    # resp = GameData.get_data_from_json("form_responses.json")[0]
    # F_sqs, P_sqs, R_sqs = tuple(map(
    #     lambda x : BingoCard.to_bingo_squares(x, temp_dict['zingiez'][x]), ['Free', "Personal", "Random"]))  
    # testBoard = BingoCard("zingiez")
    # testBoard.generate_board(F_sqs, P_sqs, R_sqs)

    dummyBoards = [BingoCard("zingiez1"), BingoCard("zingiez2"), BingoCard("zingiez3")]
    F_sqs, P_sqs, R_sqs = tuple(map(
        lambda x : BingoCard.to_bingo_squares(x, temp_dict['zingiez'][x]), ['Free', "Personal", "Random"]))  
    for board in dummyBoards:
        board.generate_board(F_sqs, P_sqs, R_sqs)
        print(board)

    dummyBoards[0].grid[0][4].sq_val = "OVERWRITTEN VALUE"
    dummyBoards[0].grid[0][3].sq_val = "OVERWRITTEN VALUE"
    dummyBoards[0].grid[0][2].sq_val = "OVERWRITTEN VALUE"
    dummyBoards[0].grid[0][1].sq_val = "OVERWRITTEN VALUE"
    dummyBoards[0].grid[0][0].sq_val = "OVERWRITTEN VALUE"

    dummyBoards[0].grid[0][3].state = False

    CardGraphic.generate_image(dummyBoards[0].grid)

test()