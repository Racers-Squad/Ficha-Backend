class DotDict(dict):

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dictionary: dict) -> None:
        for key, value in dictionary.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value
        super().__init__()

    def __getattr__(self, item):
        try:
            value = dict.__getitem__(self, item)
        except KeyError:
            value = None
        return value
