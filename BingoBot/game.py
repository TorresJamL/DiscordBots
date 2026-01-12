import logging

from typing import Optional
from functools import reduce
from dataclasses import asdict
from bingo import *
from graphics import CardGraphic

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
game_logger = logging.getLogger(__name__)

class Game():    
    def __init__(self, guild_id: int):
        self.is_setup_phase = True
        self.guid = guild_id

        self.free_squares: dict[str, list[CardSquare]] = {}
        self.personal_squares: dict[str, list[CardSquare]] = {}
        self.random_squares: list[CardSquare] = []
        self.players: list[str] = []

        self.player_to_card: dict[str, BingoCard] = {}
        self.session_card: BingoCard = None # TODO

    def save(self):
        save_dict = {
            "in_setup_phase" : self.is_setup_phase,
            "global_data" : {
                "Free" : {user: [asdict(card_sq) for card_sq in sqs] for (user, sqs) in self.free_squares.items()},
                "Personal" : {user: [asdict(card_sq) for card_sq in sqs] for (user, sqs) in self.personal_squares.items()},
                "Random" : [asdict(card_sq) for card_sq in self.random_squares],
                "Players" : self.players
            },
            "player_data" : {}
        }

        # Player Data
        for k, v in self.player_to_card.items():
            grid_ref = v.grid
            for i in range(len(grid_ref)):
                for j in range(len(grid_ref)):
                    if not save_dict["player_data"].get(k): # k not exist :(
                        save_dict["player_data"][k] = []
                    save_dict["player_data"][k].append([grid_ref[i][j].sq_val, [i, j]])
        
        was_save_successful = GameData.store_data_to_json(f"{self.guid}\\game_inst_data.json", save_dict)

        game_logger.info(f"Save Success State: {was_save_successful}")

        return was_save_successful 

    def load(self):
        data_dict = GameData.get_data_from_json(f"{self.guid}\\game_inst_data.json")[0]
        self.is_setup_phase = data_dict["in_setup_phase"]
        try:
            for (sq_type, values) in data_dict["global_data"].items():
                match sq_type:
                    case "Free":
                        for (user, sqs) in values.items():
                            if (self.free_squares.get(user) == None):
                                self.free_squares[user] = []
                            self.free_squares[user].extend(BingoCard.to_bingo_squares("Free", [(sq["sq_val"], sq["state"]) for sq in sqs]))
                    case "Personal":
                        for (user, sqs) in values.items():
                            if (self.personal_squares.get(user) == None):
                                self.personal_squares[user] = []
                            self.personal_squares[user].extend(BingoCard.to_bingo_squares("Personal", [(sq["sq_val"], sq["state"]) for sq in sqs]))
                    case "Random": 
                        self.random_squares.extend(BingoCard.to_bingo_squares("Random", [(sq["sq_val"], sq["state"]) for sq in values]))
                    case "Players":
                        self.players.extend(values)    
                    case _:
                        raise Exception(f"How'd you get here? Encountered default case during loading...")
        
            for (user, rough_data) in data_dict["player_data"].items():
                if user != str(self.guid):
                    self.player_to_card[user] = BingoCard(user)
                    self.player_to_card[user].load_card(
                        rough_data, 
                        self.free_squares[user], 
                        self.personal_squares[user], 
                        self.random_squares)
                else:
                    self.player_to_card[user] = BingoCard(user, is_individual=False, n = 7)
                    self.player_to_card[user].load_card(
                        rough_data, 
                        reduce(lambda x, y: x + y, self.free_squares.values()), 
                        reduce(lambda x, y: x + y, self.personal_squares.values()), 
                        self.random_squares)
        except Exception as err:
            print(err)
            game_logger.error(f"[load] {err}")
            return (False, err)
            
        game_logger.info("Data Finished Loading")
        return (True,)
        
    def postsave(func):
        def wrapper(self, *args, **kwargs):
            game_logger.info(f"Autosaving...")
            res = func(self, *args, **kwargs)
            self.save()
            game_logger.info(f"Autosaving... Complete!")
            return res
        return wrapper

    def game_start(self) -> tuple[bool, Optional[Exception | GameruleException | None]]:
        game_logger.info(f"Data Verification Processing")
        data_exists = GameData.data_exists(f"{self.guid}\\game_inst_data.json") 
        game_logger.info(f"Exists = {data_exists}")

        inst_data_len = 0
        try:
            inst_data_len = (reduce(lambda x, y: len(x) + len(y), self.free_squares.values()) +
                            reduce(lambda x, y: len(x) + len(y), self.personal_squares.values()) +
                            len(self.random_squares))
        except TypeError as TE_err:
            game_logger.warning(f"[game_start] {TE_err}")

        if data_exists and inst_data_len == 0: 
            return self.load()
        else:
            return self.generate_boards()

    @postsave
    def generate_boards(self):
        """ Initializes player_to_card. """
        if len(self.free_squares) == 0 and len(self.personal_squares) == 0 and len(self.random_squares) == 0:
            self.load_square_data()

        self.players.append(str(self.guid))
        for player in self.players:
            p_b = BingoCard(player) if player != str(self.guid) else BingoCard(player, False, 7)
            try:
                if player != str(self.guid):
                    p_b.generate_board(
                        self.free_squares[player], 
                        self.personal_squares[player], 
                        self.random_squares)
                else:
                    p_b.generate_board(
                        reduce(lambda x, y: x + y, self.free_squares.values()), 
                        reduce(lambda x, y: x + y, self.personal_squares.values()), 
                        self.random_squares)
                self.player_to_card[player] = p_b
            except GameruleException as GE_err:
                game_logger.error(f"Gamerule Exception: {GE_err}, has occured. Setting all data to default.")
                self.free_squares = {}
                self.personal_squares = {}
                self.random_squares = []

                self.player_to_card = {}
                game_logger.info(f"Data defaulted. Exiting...")
                return (False, GE_err)
        
        game_logger.info("Generated Boards...")
        return (True,)

    def load_square_data(self):
        """ Loads the user square suggestions into free, personal, and random squares.

        Raises:
            Exception: If somehow the format of the form response json is wrong.
        """
        response_dict = GameData.get_data_from_json(f"{self.guid}\\form_responses.json")[0] #? This will change for session IDs

        for user in response_dict:
            self.players.append(user)
            for i, (key, value) in enumerate(response_dict[user].items()):
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

    @postsave
    def cross_out_sq(self, user: str, squ_coord: tuple[int]):
        self.player_to_card[user].flip_squ_state(squ_coord[0], squ_coord[1], False)
        return self.player_to_card[user].win_check()

    def create_card_img(self, user: str):
        CardGraphic.generate_image(self.player_to_card[user].grid, user)

    def __str__(self):
        return ("free squares: " + str(self.free_squares) + "\n" + 
                "personal squares: " + str(self.personal_squares) + "\n" + 
                "random squares: " + str(self.random_squares) + "\n" + 
                "players: " + str(self.players) + "\n" + 
                "player to card: " + str(self.player_to_card))
    
    def print_data(self):
        print(self.free_squares)
        print(self.personal_squares)
        print(self.random_squares)
        print(self.players)
        print(self.player_to_card)
