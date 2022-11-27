import os
import yaml
import numpy as np

def load_user_config(user_file="_lamd.yml", directory="."):
    filename = os.path.join(os.path.expandvars(directory), user_file)
    conf = {}
    if os.path.exists(filename):
        with open(filename) as file:
            conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf

def load_config():
    default_file = os.path.join(os.path.dirname(__file__), "defaults.yml")
    local_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "machine.yml"))
    user_file = '_lamd.yml'

    conf = {}

    if os.path.exists(default_file):
        with open(default_file) as file:
            conf.update(yaml.load(file, Loader=yaml.FullLoader))

    if os.path.exists(local_file):
        with open(local_file) as file:
            conf.update(yaml.load(file, Loader=yaml.FullLoader))

    conf.update(load_user_config(user_file))

    if conf=={}:
        raise ValueError(
            "No configuration file found at either "
            + user_file
            + " or "
            + local_file
            + " or "
            + default_file
            + "."
        )

    for key, item in conf.items():
        if item is str:
            conf[key] = os.path.expandvars(item)

    if "logging" in conf:
        if not "level" in conf["logging"]:
            conf["logging"]["level"] = 20

        if not "filename" in conf["logging"]:
            conf["logging"]["filename"] = "lamd.log"
    else:
        conf["logging"] = {"level": 20, "filename": "lamd.log"}
    return conf

config = load_config()

