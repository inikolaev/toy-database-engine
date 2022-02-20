from functools import cmp_to_key
from typing import Callable, Optional, Any


class Record(dict):
    def __init__(self, *args, aliases: Optional[dict[str, str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__hash = hash(tuple(self.items()))
        self.__aliases = {} if aliases is None else dict(aliases)
        self.__aliases_to_columns = {
            alias: column
            for column, alias in self.__aliases.items()
        }

    def __hash__(self):
        return self.__hash

    def __setitem__(self, key, value):
        raise NotImplemented('Record is immutable')

    def __getitem__(self, name: str) -> Optional[Any]:
        if name in self.__aliases_to_columns:
            name = self.__aliases_to_columns[name]

        record = self
        path = name.split('.')
        for item in path[:-1]:
            record = super(Record, record).get(item)

            if record is None:
                return None

        return super(Record, record).get(path[-1])

    def get(self, name: str) -> Any | None:
        return self[name]

    def __getattr__(self, name: str) -> Optional[Any]:
        return self[name]

    def __repr__(self):
        values = {
            self.__aliases.get(column, column): self.get(column)
            for column in self.columns()
        }

        return f'Record({values})'

    def columns(self) -> set[str]:
        names = set()
        for key, value in self.items():
            if isinstance(value, Record):
                for column in value.columns():
                    names.add(f'{key}.{column}')
            else:
                names.add(key)
        return names

    @staticmethod
    def from_dict(root: dict) -> 'Record':
        return Record({
            name: Record.from_dict(value) if isinstance(value, dict) else value
            for name, value in root.items()
        })

    def projection(self, columns: set[str]) -> 'Record':
        root = {}

        for name in columns:
            path = name.split('.')

            node = root
            for item in path[:-1]:
                if item not in node:
                    node[item] = {}
                node = node[item]

            node[path[-1]] = self.get(name)

        return Record.from_dict(root)


Table = set[Record]
Condition = Callable[[Record], bool]
BiCondition = Callable[[Record, Record], bool]


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


if __name__ == '__main__':
    employees = {
        create_employee(0, "Michael Scott", "Regional Manager", 100000),
        create_employee(1, "Dwight K. Schrute", "Assistant to the Regional Manager", 65000),
        create_employee(2, "Pamela Beesly", "Receptionist", 40000),
        create_employee(3, "James Halpert", "Sales", 55000),
        create_employee(4, "Stanley Hudson", "Sales", 55000)
    }

    tasks = {
        create_task(0, 0, False),
        create_task(1, 0, False),
        create_task(2, 1, True),
        create_task(3, 1, True),
        create_task(4, 1, True),
        create_task(5, 2, True),
        create_task(6, 3, False),
        create_task(7, 3, False),
        create_task(8, 3, True),
        create_task(9, 3, False)
    }

    result = sorted_employees = order_by(
        projection(
            rename(
                left_outer_join(employees, tasks, lambda left, right: left.id == right.employee_id),
                {'left.id': 'employee_id', 'left.name': 'name', 'right.id': 'task_id'}
            ),
            columns={'employee_id', 'task_id', 'name'}
        ),
        lambda left, right: left.employee_id - right.employee_id
    )

    for record in result:
        print(record.employee_id, record.task_id, record.name)
