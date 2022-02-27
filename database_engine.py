from functools import cmp_to_key
from typing import Callable

from models import Table, Condition, Record, BiCondition


def select(table: Table, predicate: Condition) -> Table:
    return Table(filter(predicate, table))


def projection(table: Table, columns: set[str]) -> Table:
    return Table(map(lambda r: r.projection(columns), table))


def rename(table: Table, columns: dict[str, str]) -> Table:
    """
    Function to rename columns. Doesn't work with nested records yet.
    """
    return Table(map(lambda r: Record(**r, aliases=columns), table))


def union(left: Table, right: Table) -> Table:
    return left | right


def difference(left: Table, right: Table) -> Table:
    return left - right


def cross_join(left: Table, right: Table) -> Table:
    return {
        Record(left=left_record, right=right_record)
        for left_record in left
        for right_record in right
    }


def inner_join(left: Table, right: Table, condition: BiCondition) -> Table:
    return select(cross_join(left, right), lambda r: condition(r.left, r.right))


def left_outer_join(left: Table, right: Table, condition: BiCondition) -> Table:
    all_records = cross_join(left, right)
    matching_records = select(all_records, lambda r: condition(r.left, r.right))

    non_matching_records = difference(
        projection(all_records, columns={'left'}),
        projection(matching_records, columns={'left'})
    )

    return union(
        matching_records,
        non_matching_records
    )


def order_by(table: Table, comparator: Callable[[Record, Record], int]) -> list[Record]:
    return sorted(table, key=cmp_to_key(comparator))


def create_employee(id: int, name: str, position: str, salary: int) -> Record:
    return Record(id=id, name=name, position=position, salary=salary)


def create_task(id: int, employee_id: int, completed: bool) -> Record:
    return Record(id=id, employee_id=employee_id, completed=completed)
