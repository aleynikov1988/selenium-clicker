from yaml import load


def get_config():
    with open('config.yaml', 'r') as outfile:
        config = load(outfile)
    return config
