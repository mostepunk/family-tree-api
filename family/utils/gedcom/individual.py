from family.utils.gedcom.tag import Tag


class Individual:
    def __init__(self, id_: str = None, sex: str = None):
        self.id_ = id_
        self.tags = []
        self.sex = sex

    def __repr__(self):
        return f"Individual ITEMS: {self.__dict__}"

    def __setitem__(self, key, value):
        if "INDI" in value:
            self.set_indi(key)
        elif key == "SEX":
            self.sex = value
        else:
            self.create_tag(key, value)

    def __getitem__(self, key):
        for tag in self.tags:
            if tag.name == key:
                return tag
        raise KeyError(f"Key: {key} does not exist")

    def find_tag(self, name, value):
        """Основная проблема кроется в новой фамилии.

        1 NAME Ann /Smith/
        2 GIVN Ann
        2 SURN Smith

        1 NAME Doe
        2 TYPE MARRIED

        при первом заходе определяется как надо,
        потом создает новый тег с именем Doe,
        но на этот же тег не присваивает тип MARRIED,
        Вместо этого парсер видит второй уровень, и ищет первую попавшуюся фамилию,
        а это 1 NAME Ann /Smith/
        """
        for tag in self.tags:
            if tag.name == name and tag.value == value:
                return tag
        # raise TagNotFound(f"TagName: {name} TagValue: {value} Not Found")

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set_indi(self, key: str):
        self.id_ = key.strip("@")

    def create_tag(self, key, value):
        self.tags.append(Tag(name=key, value=value.strip("@")))

    @property
    def all_tags(self):
        return [tag.name for tag in self.tags]

    @property
    def families(self):
        return [tag.value for tag in self.tags if tag.name == "fams"]

    @property
    def family_child(self):
        for tag in self.tags:
            if tag.name == "FAMC":
                return tag.value

    @property
    def obje(self):
        return [tag.value for tag in self.tags if tag.name == "obje"]

    @property
    def b_day(self):
        b_day_dict = {"date": "unknown"}
        for tag in self.tags:
            if tag.name == "BIRT":
                b_day_dict.update(tag.__dict__)
                del b_day_dict["name"]
                del b_day_dict["value"]
        return b_day_dict
