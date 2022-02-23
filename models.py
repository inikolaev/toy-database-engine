from typing import Optional, Any, Callable


class Record(dict):
    def __init__(self, *args, aliases: Optional[dict[str, str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__hash = hash(tuple(sorted(self.items())))
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
