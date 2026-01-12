import json
import os
import logging

from functools import reduce
from pathlib import Path

utility_logger = logging.getLogger(__name__)

def deprecated(func):
    def wrapper(*args, **kwargs):
        return func(args, kwargs)
    return wrapper

class ConventionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class GameruleException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class GameData:
    @staticmethod
    def data_exists(file_name) -> bool:
        curr_file_dir = Path(__file__).resolve().parent
        data_path = curr_file_dir / f"GameData/{file_name}"
        if Path(data_path).exists():
            return True
        return False

    @staticmethod
    def verify_path_directories(p: Path) -> None:
        dir_structure = p.as_posix().split('/')

        verification_path = ""
        for i in range(len(dir_structure) - 1):
            verification_path += dir_structure[i] + '/'

            if not Path(verification_path).is_dir():
                Path(verification_path).mkdir(parents=True)
                utility_logger.info(f"Creating New Directory: {verification_path}")

    @staticmethod
    def get_data_from_json(json_file_name: str) -> tuple[dict, Path]:
        curr_file_dir = Path(__file__).resolve().parent
        if ".json" in json_file_name:
            data_path = curr_file_dir / f"GameData/{json_file_name}"
        else:
            data_path = curr_file_dir / f"GameData/{json_file_name}.json"

        GameData.verify_path_directories(data_path)

        if not Path(data_path).exists():
            with open(data_path, 'w+') as responses_json:
                json.dump(dict(), responses_json, indent=4)

        with open(data_path, 'r') as responses_json:
            return (dict(json.load(responses_json)), data_path)
        
    @staticmethod
    def store_data_to_json(json_fn: str, data: dict, override_og_data = True) -> bool:
        curr_file_dir = Path(__file__).resolve().parent
        if ".json" in json_fn:
            data_path = curr_file_dir / f"GameData/{json_fn}"
        else:
            data_path = curr_file_dir / f"GameData/{json_fn}.json"

        GameData.verify_path_directories(data_path)

        try:
            if override_og_data:
                with open(data_path, 'w+') as data_json:
                    json.dump(data, data_json, indent=4)
            elif not Path(data_path).exists():
                with open(data_path, 'w+') as data_json:
                    json.dump(data, data_json, indent=4)
        except Exception as err:
            print("Error occured while storing: \n", err)
            return False
        
        return True
