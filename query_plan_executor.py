from database_engine import inner_join, left_outer_join
from models import Table
from query_plan_builder import QueryPlan, JoinNode, JoinType, ScanNode, Node


def execute_query_plan_node(plan: Node, tables: dict[str, Table]) -> Table:
    match plan:
        case JoinNode(join_type=JoinType.INNER_JOIN, left=left, right=right, conditions=conditions):
            return inner_join(
                execute_query_plan_node(left, tables),
                execute_query_plan_node(right, tables),
                lambda l, r: all(condition.get_executable_condition()(l, r) for condition in conditions)
            )
        case JoinNode(join_type=JoinType.LEFT_OUTER_JOIN, left=left, right=right, conditions=conditions):
            return left_outer_join(
                execute_query_plan_node(left, tables),
                execute_query_plan_node(right, tables),
                lambda l, r: all(condition.get_executable_condition()(l, r) for condition in conditions)
            )
        case ScanNode(table=table):
            return tables[table]
        case _:
            return set()


def execute_query_plan(plan: QueryPlan, tables: dict[str, Table]) -> Table:
    return execute_query_plan_node(plan.node, tables)
