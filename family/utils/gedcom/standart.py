"""
GEDCOM tags.

Add My tags from webtrees
"RIN"
"_UID"
"TYPE"
"""


GEDCOM_PROGRAM_DEFINED_TAG_MREL = "_MREL"
"""Value: `_MREL`

Relationship to a mother."""

GEDCOM_PROGRAM_DEFINED_TAG_FREL = "_FREL"
"""Value: `_FREL`

Relationship to a father."""

GEDCOM_TAG_BIRTH = "BIRT"
"""Value: `BIRT`

The event of entering into life."""

GEDCOM_TAG_BURIAL = "BURI"
"""Value: `BURI`

The event of the proper disposing of the mortal remains of a deceased person."""

GEDCOM_TAG_CENSUS = "CENS"
"""Value: `CENS`.

The event of the periodic count of the population for a designated locality, such as a national or state Census."""

GEDCOM_TAG_CHANGE = "CHAN"
"""Value: `CHAN`

Indicates a change, correction, or modification. Typically used in connection
with a `gedcom.tags.GEDCOM_TAG_DATE` to specify when a change in information occurred."""

GEDCOM_TAG_CHILD = "CHIL"
"""Value: `CHIL`

The natural, adopted, or sealed (LDS) child of a father and a mother."""

GEDCOM_TAG_CONCATENATION = "CONC"
"""Value: `CONC`

An indicator that additional data belongs to the superior value. The information from the `CONC` value is to
be connected to the value of the superior preceding line without a space and without a carriage return and/or
new line character. Values that are split for a `CONC` tag must always be split at a non-space. If the value is
split on a space the space will be lost when concatenation takes place. This is because of the treatment that
spaces get as a GEDCOM delimiter, many GEDCOM values are trimmed of trailing spaces and some systems look for
the first non-space starting after the tag to determine the beginning of the value."""

GEDCOM_TAG_CONTINUED = "CONT"
"""Value: `CONT`

An indicator that additional data belongs to the superior value. The information from the `CONT` value is to be
connected to the value of the superior preceding line with a carriage return and/or new line character.
Leading spaces could be important to the formatting of the resultant text. When importing values from `CONT` lines
the reader should assume only one delimiter character following the `CONT` tag. Assume that the rest of the leading
spaces are to be a part of the value."""

GEDCOM_TAG_DATE = "DATE"
"""Value: `DATE`

The time of an event in a calendar format."""

GEDCOM_TAG_DEATH = "DEAT"
"""Value: `DEAT`

The event when mortal life terminates."""

GEDCOM_TAG_FAMILY = "FAM"
"""Value: `FAM`.

Identifies a legal, common law, or other customary relationship of man and woman and their children,
if any, or a family created by virtue of the birth of a child to its biological father and mother."""

GEDCOM_TAG_FAMILY_CHILD = "FAMC"
"""Value: `FAMC`

Identifies the family in which an individual appears as a child."""

GEDCOM_TAG_FAMILY_SPOUSE = "FAMS"
"""Value: `FAMS`

Identifies the family in which an individual appears as a spouse."""

GEDCOM_TAG_FILE = "FILE"
"""Value: `FILE`

An information storage place that is ordered and arranged for preservation and reference."""

GEDCOM_TAG_GIVEN_NAME = "GIVN"
"""Value: `GIVN`

A given or earned name used for official identification of a person."""

GEDCOM_TAG_HUSBAND = "HUSB"
"""Value: `HUSB`

An individual in the family role of a married man or father."""

GEDCOM_TAG_INDIVIDUAL = "INDI"
"""Value: `INDI`

A person."""

GEDCOM_TAG_MARRIAGE = "MARR"
"""Value: `MARR`.

A legal, common-law, or customary event of creating a family unit of a man and a woman as husband and wife."""

GEDCOM_TAG_NAME = "NAME"
"""Value: `NAME`.

A word or combination of words used to help identify an individual, title, or other item.
More than one NAME line should be used for people who were known by multiple names."""

GEDCOM_TAG_OBJECT = "OBJE"
"""Value: `OBJE`

Pertaining to a grouping of attributes used in describing something. Usually referring to the data required
to represent a multimedia object, such an audio recording, a photograph of a person, or an image of a document."""

GEDCOM_TAG_OCCUPATION = "OCCU"
"""Value: `OCCU`

The type of work or profession of an individual."""

GEDCOM_TAG_PLACE = "PLAC"
"""Value: `PLAC`

A jurisdictional name to identify the place or location of an event."""

GEDCOM_TAG_PRIVATE = "PRIV"
"""Value: `PRIV`

Flag for private address or event."""

GEDCOM_TAG_SEX = "SEX"
"""Value: `SEX`

Indicates the sex of an individual--male or female."""

GEDCOM_TAG_SOURCE = "SOUR"
"""Value: `SOUR`

The initial or original material from which information was obtained."""

GEDCOM_TAG_SURNAME = "SURN"
"""Value: `SURN`

A family name passed on or used by members of a family."""

GEDCOM_TAG_WIFE = "WIFE"
"""Value: `WIFE`

An individual in the role as a mother and/or married woman."""
