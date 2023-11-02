"""Parser for gedcom record."""

from __future__ import annotations

from family.utils.gedcom.individual import Individual


class GedcomParser:
    @classmethod
    def parse(cls, record: str):
        lines = record.split("\n")
        if "INDI" in lines[0]:
            return cls.parse_individual(lines)

    @classmethod
    def parse_individual(cls, record: str):
        indi = Individual()
        upper_key = None
        upper_value = None
        level = 1

        for line in record.split("\n"):
            number, key, *values = line.split()

            number = int(number)
            if isinstance(values, list):
                value = " ".join(values)
            else:
                value = values

            if number > level:
                tag = indi.find_tag(upper_key, upper_value)
                setattr(tag, key, value)

            elif number <= level:
                # для точного поиска тэгов
                upper_key = key
                upper_value = value
                indi[key] = value

        return indi
