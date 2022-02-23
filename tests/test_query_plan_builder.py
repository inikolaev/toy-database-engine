from query_plan_builder import QueryPlanBuilder, JoinType, BinaryCondition, JoinNode, ScanNode, Node, QueryPlan


def test_query_plan_builder():
    plan = (
        QueryPlanBuilder()
            .scan('employees')
            .scan('tasks')
            .join(JoinType.INNER_JOIN,
                  [BinaryCondition('id', 'employee_id', '='), BinaryCondition('id', 'task_id', '=')])
            .build()
    )
    assert plan == QueryPlan(
        JoinNode(
            JoinType.INNER_JOIN,
            ScanNode('employees'),
            ScanNode('tasks'),
            [BinaryCondition('id', 'employee_id', '='), BinaryCondition('id', 'task_id', '=')]
        )
    )
