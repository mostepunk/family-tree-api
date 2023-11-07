################################################################################
# Этот запрос формирует дерево от персоны к предкам по прямой линии.

# | I1 | John Silver    | I2 | Mother of John  |
# | I1 | John Silver    | I3 | Father of John  |
# | I2 | Mother of John | I4 | Grandba of John |
# | I2 | Mother of John | I5 | Grandpa of John |
# | I3 | Father of John | I6 | Grandba of John |
# | I3 | Father of John | I7 | Grandpa of John |


direct = """
    with recursive fam as (
        select
            i.i_id as child,
            REGEXP_SUBSTR(i.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            parents.l_from as parent,
            REGEXP_SUBSTR(parent_family.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i
        left join link ch_to_fam on
            i.i_id = ch_to_fam.l_from
         and ch_to_fam.l_type = 'FAMC'
        left join link parents on
            ch_to_fam.l_to = parents.l_to
         and parents.l_type = 'FAMS'
        left join individuals parent_family on
            parents.l_from = parent_family.i_id
        where i.i_id = '{root_person_id}'
    union
        select
            i2.i_id as child,
            REGEXP_SUBSTR(i2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            parents2.l_from as parent,
            REGEXP_SUBSTR(parent_family2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i2
        left join link ch_to_fam2 on
            i2.i_id = ch_to_fam2.l_from
         and ch_to_fam2.l_type = 'FAMC'
        left join link parents2 on
            ch_to_fam2.l_to = parents2.l_to
         and parents2.l_type = 'FAMS'
        left join individuals parent_family2 on
            parents2.l_from = parent_family2.i_id
        join fam on fam.parent = i2.i_id
    )
    select * from fam
"""


################################################################################
# Этот запрос формирует дерево от персоны к предкам по прямой линии.
# Но при этом захватывает родных братьев и сестер

# | I1 | John Silver    | I2 | Mother of John  |
# | I1 | John Silver    | I3 | Father of John  |
# | I1 | John Silver    | I8 | Sister of John  |
# | I2 | Mother of John | I4 | Grandba of John |
# | I2 | Mother of John | I5 | Grandpa of John |
# | I3 | Father of John | I6 | Grandba of John |
# | I3 | Father of John | I7 | Grandpa of John |
# | I8 | Sister of John | I2 | Mother of John  |
# | I8 | Sister of John | I3 | Father of John  |

with_brothers_and_sisters = """
    with recursive fam as (NAME
        select
            i.i_id as child,
            REGEXP_SUBSTR(i.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            parents.l_from as parent, parents.l_type,
            REGEXP_SUBSTR(parent_family.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i
        left join link ch_to_fam on
            i.i_id = ch_to_fam.l_from
         and ch_to_fam.l_type = 'FAMC'
        left join link parents on
            ch_to_fam.l_to = parents.l_to
        and parents.l_from != i.i_id
        left join individuals parent_family on
            parents.l_from = parent_family.i_id
        where i.i_id = '{root_person_id}'
    union
        select
            i2.i_id as child,
            REGEXP_SUBSTR(i2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            parents2.l_from as parent, parents2.l_type,
            REGEXP_SUBSTR(parent_family2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i2
        left join link ch_to_fam2 on
            i2.i_id = ch_to_fam2.l_from
         and ch_to_fam2.l_type = 'FAMC'
        left join link parents2 on
            ch_to_fam2.l_to = parents2.l_to
        and parents2.l_from != i2.i_id
        left join individuals parent_family2 on
            parents2.l_from = parent_family2.i_id
        join fam on fam.parent = i2.i_id
    )
    select * from fam
"""


################################################################################
# Этот запрос формирует дерево от персоны к предкам по прямой линии,
# захватывает родных братьев и сестер и детей
# Чтобы в связях не запутаться я добавил доп колонки:

# | I1 | John Silver | FAMC | I2 | FAMS | Mother of John |
# | I1 | John Silver | FAMC | I3 | FAMS | Father of John |
# | I1 | John Silver | FAMC | I4 | FAMC | Sister of John |
# | I1 | John Silver | FAMS | I5 | FAMS | Wife of John   |
# | I1 | John Silver | FAMS | I6 | FAMC | Son of John    |

# FAMC FAMS: Parent to son
# FAMS FAMC: Son to parent
# FAMC FAMC: Brother to sister
# FAMS FAMS: Husband to Wife

full_tree = """
    with recursive fam as (
        select
            1 AS "level",
            i.i_id as child,
            REGEXP_SUBSTR(i.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            ch_to_fam.l_type as child_to_family,
            parents.l_from as parent,
            parents.l_type as family_to_parent,
            REGEXP_SUBSTR(parent_family.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i
        left join link ch_to_fam on
            i.i_id = ch_to_fam.l_from
        join link parents on
            ch_to_fam.l_to = parents.l_to
        and parents.l_from != i.i_id
        and ch_to_fam.l_type != 'SOUR'
        left join individuals parent_family on
            parents.l_from = parent_family.i_id
        where i.i_id = '{root_person_id}'
    union
        select
            fam.level + 1 as "level",
            i2.i_id as child,
            REGEXP_SUBSTR(i2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as child_name,
            ch_to_fam2.l_type,
            parents2.l_from as parent,
            parents2.l_type as family_to_parent,
            REGEXP_SUBSTR(parent_family2.i_gedcom, 'NAME ([/\w+/].*[/\w+]/)') as parent_name
        from individuals i2
        left join link ch_to_fam2 on
            i2.i_id = ch_to_fam2.l_from
        join link parents2 on
            ch_to_fam2.l_to = parents2.l_to
         and parents2.l_from != i2.i_id
         and ch_to_fam2.l_type != 'SOUR'
        left join individuals parent_family2 on
            parents2.l_from = parent_family2.i_id
        join fam on fam.parent = i2.i_id
    )
    select * from fam
"""
