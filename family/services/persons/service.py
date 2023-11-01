"""
0 @I500011@ INDI
1 SEX F  # M
1 BIRT
    2 DATE DD MAY YYYY
    2 PLAC City, Country

1 FAMS @F500004@  # families.f_id
1 FAMS @F500005@
1 FAMS @F500072@  # Famliy Spouse(супруг) or parent
1 FAMC @F500001@  # Family Child
1 RIN MH:I500011
1 _UID 5795183612D496A3570494EFD7953016
1 NAME Helen /Doe/
    2 GIVN Helen
    2 SURN Doe
1 NAME Malkovich
    2 TYPE MARRIED
1 OBJE @X15@  # media.m_id
1 OBJE @X16@


# Family Record
0 @F500001@ FAM
1 _UPD 25 SEP 2023 14:37:23 GMT -0500
1 HUSB @I500003@
1 WIFE @I500002@
1 CHIL @I500001@
1 CHIL @I500011@
1 RIN MH:F500001
1 _UID 5795160EBD3CADD5CCAF13441CDC7976
1 MARR
    2 TYPE CIVIL
    2 DATE 31 JUL 1982
    2 HUSB
        3 AGE 21
    2 WIFE
        3 AGE 20
    2 PLAC Street, City, Country
1 DIV
    2 DATE DD MAR YYYY
    2 PLAC Street, City, Country
"""

from loguru import logger as logging

from family.services.base import BaseService


class PersonService(BaseService):
    """Information about person in family-Tree."""

    async def info(self, person_id: str):
        async with self.uow:
            res = await self.uow.persons.get_by_id(person_id)
            logging.info(f"Found in DB: {res}")
            return res
