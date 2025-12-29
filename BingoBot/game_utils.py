import json

from pathlib import Path

class ConventionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class GameruleException(Exception):
    pass

class GameData:
    @staticmethod
    def get_data_from_json(json_file_name: str) -> tuple[dict, Path]:
        if len(json_file_name) < 5:
            raise ConventionError(f"File Names should never be < 5 characters for file name: {json_file_name}")
        curr_file_dir = Path(__file__).resolve().parent
        if ".json" in json_file_name:
            form_resp_path = curr_file_dir / f"GameData/{json_file_name}"
        else:
            form_resp_path = curr_file_dir / f"GameData/{json_file_name}.json"
        
        if not Path(form_resp_path).exists():
            with open(form_resp_path, 'w+') as responses_json:
                json.dump(dict(), responses_json, indent=4)

        with open(form_resp_path, 'r') as responses_json:
            return (dict(json.load(responses_json)), form_resp_path)