class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[key] for key in d.keys() if not key.startswith("_")]

    @classmethod
    def key_choices(cls):
        d = cls.__dict__
        return [{key: d[key]} for key in d.keys() if not key.startswith("_")]

    @classmethod
    def choices_dict(cls):
        d = cls.__dict__
        return {key: d[key] for key in d.keys() if not key.startswith("_")}

    @classmethod
    def options(cls):
        d = cls.__dict__
        return [
            dict(label=d[key], value=key)
            for key in d.keys()
            if not key.startswith("__")
        ]

    @classmethod
    def keys(cls):
        d = cls.__dict__
        return [key for key in d.keys() if not key.startswith("_")]
