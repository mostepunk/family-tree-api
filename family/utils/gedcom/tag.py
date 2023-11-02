class Tag:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __setitem__(self, name, value):
        self.name = name
        self.value = value

    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        raise KeyError(f"Value: {name} does not exist")

    def __repr__(self):
        return f"Tag: {self.__dict__}"

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def update(self, name, value):
        setattr(self, name, value)

    def dict(self):
        tag_dict = {}
        for key, value in self.__dict__.items():
            if key in ("name", "TYPE"):
                continue
            tag_dict[key] = value
        return tag_dict
