import json


def write_to_json(data: list, filename: str) -> None:
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
