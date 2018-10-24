from yaml import load
from random import choice


def _get_config(name):
    with open('./config/{0}.yaml'.format(name), 'r') as outfile:
        config = load(outfile)
    return config

def get_general():
    return _get_config('general')

def get_proxy(lang):
    proxy = _get_config('lang-proxy')

    if proxy[lang]:
        return proxy[lang]

    return None

def get_links(linksType):
    config = _get_config('links')

    if config[linksType]:
        return config[linksType]

    return None

def get_batch(name):
    config = _get_config('batch')
    batch = config[name]

    if batch:
        if batch['lang']:
            batch['proxy'] = get_proxy(batch['lang'])

        if batch['deviceType'] == 'mobile':
            device = _get_config('device-type')
            batch['mobile'] = choice(device['mobile'])
        else:
            batch['mobile'] = None

        if batch['linksType']:
            batch['links'] = get_links(batch['linksType'])

        return batch

    return None 
