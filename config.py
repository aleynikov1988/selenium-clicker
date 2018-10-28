import yaml
import os.path


class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader.include)

def _get_config(name):
    with open('./config/{0}.yaml'.format(name), 'r') as outfile:
        config = yaml.load(outfile, Loader)

    return config

def get_general():
    return _get_config('general')

def get_batch(name):
    config = _get_config('batch')
    batch = None

    try:
        batch = config[name]
    except KeyError:
        pass

    return batch