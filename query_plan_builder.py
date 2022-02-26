from enum import Enum
from typing import Callable

from database_engine import Record


class Condition:
    def get_executable_condition(self) -> Callable[..., bool]:
        def condition() -> bool:
            return False

        return condition


class BinaryCondition(Condition):
    def __init__(self, left: str, right: str, operator: str):
        self.left = left
        self.right = right
        self.operator = operator

    def __eq__(self, other):
        if not isinstance(other, BinaryCondition):
            return False

        return self.left == other.left and self.right == other.right and self.operator == other.operator

    def __repr__(self):
        return f'{self.left} {self.operator} {self.right}'

    def get_executable_condition(self) -> Callable[..., bool]:
        def condition(left: Record, right: Record) -> bool:
            return left[self.left] == right[self.right]

        return condition


class Node:
    pass


class ScanNode(Node):
    def __init__(self, table: str):
        self.table = table

    def __eq__(self, other):
        if not isinstance(other, ScanNode):
            return False

        return self.table == other.table

    def __repr__(self):
        return f'Scan(table="{self.table}")'


class JoinType(Enum):
    CARTESIAN_JOIN = 'cartesian_join'
    INNER_JOIN = 'inner_join'
    LEFT_OUTER_JOIN = 'left_outer_join'


class JoinNode(Node):
    def __init__(self, join_type: JoinType, left: Node, right: Node, conditions: list[Condition]):
        self.join_type = join_type
        self.left = left
        self.right = right
        self.conditions = conditions

    def __eq__(self, other):
        if not isinstance(other, JoinNode):
            return False

        return (
            self.join_type == other.join_type
            and self.left == other.left
            and self.right == other.right
            and self.conditions == other.conditions
        )

    def __repr__(self):
        conditions = ' AND '.join([
            repr(condition) for condition in self.conditions
        ])
        return f'Join(type={self.join_type}, left={self.left}, right={self.right}, on="{conditions}")'


class QueryPlan:
    def __init__(self, node: Node):
        self.node = node

    def __eq__(self, other):
        if not isinstance(other, QueryPlan):
            return False

        return self.node == other.node

    def __repr__(self):
        return f'QueryPlan(node={self.node})'


class QueryPlanBuilder:
    def __init__(self):
        self.__stack = []

    def scan(self, table: str):
        self.__stack.append(ScanNode(table))
        return self

    def join(self, join_type: JoinType, conditions: list[Condition]):
        right = self.__stack.pop()
        left = self.__stack.pop()
        self.__stack.append(JoinNode(join_type, left, right, conditions))
        return self

    def build(self) -> QueryPlan:
        return QueryPlan(self.__stack.pop())
