import json


def load_config(file_name):

    with open(file_name, "r") as f:
        return json.load(f)


config = load_config("config.json")

if config["temperature"] > 0.5:
    print("creative mode")
else:
    print("stable mode")