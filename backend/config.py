import os
import json
import jsonschema

def load_config(config_file='config.json', schema_file='schema.json'):
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("Config file \"" + config_file + "\" not found.")
       
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError("Config file \"" + schema_file + "\" not found.")

    try:
        jsonschema.validate(config, schema=schema)
    except Exception as e:
        print("Invalid config file:", e)
        print("\nPlease refer to the following schema:")
        print(json.dumps(schema, indent=2))
        quit()

    DATA_FOLDER = config['app']['DATA_FOLDER']
    VIDEO_FOLDER = config['app']['VIDEO_FOLDER']
    PARTICIPANT_ID = config['empatica']['PARTICIPANT_ID']

    if not os.path.isdir(DATA_FOLDER):
        raise NotADirectoryError("The specified data folder in config.json is not a valid directory.")

    if not os.path.isdir(VIDEO_FOLDER):
        raise NotADirectoryError("The specified video folder in config.json is not a valid directory.")

    if len(PARTICIPANT_ID) > 10 or not (PARTICIPANT_ID.isupper() or PARTICIPANT_ID.isdigit()):
        raise ValueError("A Participant ID can have up to 10 characters and can only include upper-case letters and numbers. Found: \"" + PARTICIPANT_ID + "\"")

    return config