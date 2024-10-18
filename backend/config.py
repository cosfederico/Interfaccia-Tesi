import os
import json
import jsonschema

def load_config(config_file='config.json'):
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except:
        raise FileNotFoundError("Config file \"" + config_file + "\" not found.")
        
    schema = {
        "type": "object",
        "properties": {
            "app": {
                "type": "object",
                "properties": {
                    "DATA_FOLDER": { "type": "string" },
                    "VIDEO_FOLDER": { "type": "string" }
                    },
                "required": ["DATA_FOLDER", "VIDEO_FOLDER"]
            },
            "empatica": {
                "type": "object",
                "properties": {
                    "BUCKET_NAME": { "type": "string" },
                    "PREFIX": { "type": "string" },
                    "PARTICIPANT_ID": { "type": "string" },
                    "ORG_ID": { "type": "string" },
                    "STUDY_ID": { "type": "string" },
                    "SAMPLE_RATE": { "type": "integer" }
                },
                "required": [
                    "BUCKET_NAME", "PREFIX", "PARTICIPANT_ID",
                    "ORG_ID", "STUDY_ID", "SAMPLE_RATE"
                ]
            }
        },
        "required": ["app", "empatica"]
    }

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