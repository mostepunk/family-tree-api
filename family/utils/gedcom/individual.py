from family.utils.gedcom.standart import (
    GEDCOM_TAG_BIRTH,
    GEDCOM_TAG_FAMILY_CHILD,
    GEDCOM_TAG_FAMILY_SPOUSE,
    GEDCOM_TAG_GIVEN_NAME,
    GEDCOM_TAG_INDIVIDUAL,
    GEDCOM_TAG_MARRIED_TYPE,
    GEDCOM_TAG_NAME,
    GEDCOM_TAG_OBJECT,
    GEDCOM_TAG_SURNAME,
)
from family.utils.gedcom.tag import Tag


class Individual:
    def __init__(self, id_: str = None, sex: str = None):
        self.id_ = id_
        self.tags = []
        self.sex = sex

    def __repr__(self):
        return f"Individual ITEMS: {self.__dict__}"

    def __setitem__(self, key, value):
        if GEDCOM_TAG_INDIVIDUAL in value:
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

    def tags_by_name(self, tag_name: str) -> list[Tag]:
        return [tag for tag in self.tags if tag.name == tag_name]

    @property
    def all_tags(self):
        return [tag.name for tag in self.tags]

    @property
    def families(self):
        return [tag.value for tag in self.tags if tag.name == GEDCOM_TAG_FAMILY_SPOUSE]

    @property
    def family_child(self):
        return [tag.value for tag in self.tags if tag.name == GEDCOM_TAG_FAMILY_CHILD]

    @property
    def obje(self):
        return [tag.value for tag in self.tags if tag.name == GEDCOM_TAG_OBJECT]

    @property
    def b_day(self) -> dict[str, str]:
        """Парисит день рождения из GEDCOM записи в пригодный для web вид.

        Возможно надо пересмотреть алгоритм.
        """
        b_day_dict = {"DATE": "unknown"}
        for tag in self.tags:
            if tag.name == GEDCOM_TAG_BIRTH:
                b_day_dict.update(tag.dict())

                if not b_day_dict.get("value"):
                    del b_day_dict["value"]

        formatted_dict = {}
        for key, value in b_day_dict.items():
            if value == "Y":
                value = True
            key = key.lower()
            formatted_dict[key] = value

        return formatted_dict

    @property
    def name(self):
        pers_name = {
            "name": None,
            "given_surn": None,
            "marriage_surn": None,
        }
        for tag in self.tags_by_name(GEDCOM_TAG_NAME):
            name = tag.get(GEDCOM_TAG_GIVEN_NAME)
            surname = tag.get(GEDCOM_TAG_SURNAME)
            type_ = tag.get("TYPE")

            if type_:
                pers_name[type_.lower()] = tag.dict()
                if type_ == GEDCOM_TAG_MARRIED_TYPE and surname is not None:
                    pers_name["marriage_surn"] = surname

            if name and pers_name.get("name") is None:
                pers_name["name"] = name

            if (
                surname
                and type_ != GEDCOM_TAG_MARRIED_TYPE
                and pers_name.get("given_surn") is None
            ):
                pers_name["given_surn"] = surname

        return pers_name
