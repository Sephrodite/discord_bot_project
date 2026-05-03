import os
import json
import traceback

CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")
DEFAULT = os.getenv("REFERENCE_FILE", "reference.json")
LANGUAGES = os.getenv("LANGUAGES", "languages.json")
SPORTS = os.getenv("SPORTS", "sports.json")
ARTS = os.getenv("ARTS", "arts.json")

def load_characters(char_file=CHAR_FILE):
    try:
        with open(char_file, "r", encoding="utf-8") as file:
            characters = json.load(file)
            return characters
    except FileNotFoundError:
        return {}
    
# loads defeault statistics from an existing file
def load_default(DEFAULT):
    try:
        with open(DEFAULT, 'r') as file:
            default = json.load(file)
            return default
    except FileNotFoundError:
        print("file not found")
        return

def save_characters(characters, char_file=CHAR_FILE):
    with open(char_file, "w", encoding="utf-8") as file:
        json.dump(characters, file, indent=4)

def load_json(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("file not found")
        return

def save_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)