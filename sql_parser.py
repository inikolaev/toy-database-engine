import re


class Keyword:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Keyword):
            return False

        return self.value == other.value

    def __repr__(self):
        return f'Keyword(value="{self.value}")'


class Literal:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False

        return self.value == other.value

    def __repr__(self):
        return f'Literal(value="{self.value}")'


class Select:
    def __init__(
        self,
        select_list: list[str],
        select_from: list[str],
        join: list[tuple[str, str, list]],
        where: list[tuple[str, str, str]]
    ):
        self.select_list = select_list
        self.select_from = select_from
        self.join = join
        self.where = where

    def __eq__(self, other):
        if not isinstance(other, Select):
            return False

        return (
            self.select_list == other.select_list
            and self.select_from == other.select_from
            and self.join == other.join
            and self.where == other.where
        )

    def __repr__(self):
        return f'Select(select_list={self.select_list}, select_from={self.select_from}, join={self.join}, where={self.where})'


class InvalidTokenError(Exception):
    pass


Tokens = list[Keyword | Literal | Select]


def parse_sql(s: str) -> Tokens:
    position = skip_white_spaces(s, 0)
    select, position = read_query(s, position)
    return [select]


def skip_white_spaces(s: str, position: int) -> int:
    while position < len(s) and s[position] in (' ', '\t', '\n', '\r'):
        position += 1
    return position


def read_query(s: str, position: int) -> tuple[Select, int]:
    _, position = read_keyword('select', s, position)
    select_list, position = read_list(s, position)
    _, position = read_keyword('from', s, position)
    select_from, position = read_list(s, position)
    join, position = read_joins(s, position)
    where, position = read_where(s, position)
    return Select(select_list=select_list, select_from=select_from, join=join, where=where), position


def read_list(s: str, position: int) -> tuple[list, int]:
    items = []
    while position < len(s):
        value, position = read_until_separator(s, position)
        items.append(value)
        position = skip_white_spaces(s, position)
        if position >= len(s) or s[position] != ',':
            break
        position += 1
        position = skip_white_spaces(s, position)

    position = skip_white_spaces(s, position)
    return items, position


def read_until(values: list[str], s: str, position: int) -> tuple[str, int]:
    start = position
    while position < len(s):
        found_value = any(s[position:].lower().startswith(value) for value in values)
        if found_value:
            break

        position += 1

    return s[start:position], position


def read_until_white_space(s: str, position: int) -> tuple[str, int]:
    value, position = read_until([' ', '\t', '\n', '\r'], s, position)
    position = skip_white_spaces(s, position)
    return value, position


def read_until_separator(s: str, position: int) -> tuple[str, int]:
    return read_until([',', ' ', '\t', '\n', '\r'], s, position)


def read_keyword(keyword: str, s: str, position: int) -> tuple[Keyword, int]:
    t = s[position:].lower()
    if t.startswith(keyword):
        position = skip_white_spaces(s, position + len(keyword))
        return Keyword(keyword), position

    raise InvalidTokenError(f'Invalid token at position {position}: expected keyword "{keyword}"')


def read_keywords(keywords: list[str], s: str, position: int) -> tuple[Keyword, int]:
    s = s[position:].lower()

    for keyword in keywords:
        if s.startswith(keyword):
            return Keyword(keyword), position + len(keyword)

    raise InvalidTokenError(f'Invalid token at position {position}: expected keywords "{keywords}"')


def read_literal(s: str, position: int) -> tuple[Literal, int]:
    start = position
    while position < len(s) and s[position] not in (' ', '\t', '\n', '\r'):
        position += 1

    return Literal(s[start:position]), position


def read_joins(s: str, position: int) -> tuple[list, int]:
    joins = []
    while position < len(s):
        position = skip_white_spaces(s, position)
        if re.match(r'^left\s+outer\s+join\s+', s[position:], re.IGNORECASE) is not None:
            join, position = read_left_outer_join(s, position)
        elif re.match(r'^inner\s+join\s+', s[position:], re.IGNORECASE) is not None:
            join, position = read_inner_join(s, position)
        elif re.match(r'^join\s+', s[position:], re.IGNORECASE) is not None:
            join, position = read_join(s, position)
        else:
            break

        joins.extend(join)

    position = skip_white_spaces(s, position)
    return joins, position


def read_left_outer_join(s: str, position: int) -> tuple[list, int]:
    _, position = read_keyword('left', s, position)
    _, position = read_keyword('outer', s, position)
    _, position = read_keyword('join', s, position)
    table, position = read_until_white_space(s, position)
    _, position = read_keyword('on', s, position)
    conditions, position = read_conditions(s, position)
    return [('left outer join', table, conditions)], position


def read_inner_join(s: str, position: int) -> tuple[list, int]:
    _, position = read_keyword('inner', s, position)
    _, position = read_keyword('join', s, position)
    value, position = read_until_white_space(s, position)
    _, position = read_keyword('on', s, position)
    conditions, position = read_conditions(s, position)
    return [('inner join', value, conditions)], position


def read_join(s: str, position: int) -> tuple[list, int]:
    _, position = read_keyword('join', s, position)
    value, position = read_until_white_space(s, position)
    _, position = read_keyword('on', s, position)
    conditions, position = read_conditions(s, position)
    return [('join', value, conditions)], position


def read_where(s: str, position: int) -> tuple[list, int]:
    if not s[position:].lower().startswith('where'):
        return [], position

    _, position = read_keyword('where', s, position)
    conditions, position = read_conditions(s, position)

    return conditions, position


def read_conditions(s: str, position: int) -> tuple[list, int]:
    conditions = []
    while position < len(s):
        left, position = read_until_white_space(s, position)
        operator, position = read_until_white_space(s, position)
        right, position = read_until_white_space(s, position)

        conditions.append((left, operator, right))

        if not any(s[position:].lower().startswith(op) for op in ('and',)):
            break

        keyword, position = read_keyword('and', s, position)

    position = skip_white_spaces(s, position)
    return conditions, position

