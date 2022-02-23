import pytest

from models import Table, Record
from query_plan_builder import QueryPlanBuilder, JoinType, BinaryCondition
from query_plan_executor import execute_query_plan
from tests.utils import create_employee, create_task


@pytest.fixture
def tables() -> dict[str, Table]:
    return {
        'employees': {
            create_employee(0, "Michael Scott", "Regional Manager", 100000),
            create_employee(1, "Dwight K. Schrute", "Assistant to the Regional Manager", 65000),
            create_employee(2, "Pamela Beesly", "Receptionist", 40000),
            create_employee(3, "James Halpert", "Sales", 55000),
            create_employee(4, "Stanley Hudson", "Sales", 55000)
        },
        'tasks': {
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
    }


def test_query_plan_executor(tables: dict[str, Table]):
    plan = (
        QueryPlanBuilder()
            .scan('employees')
            .scan('tasks')
            .join(JoinType.INNER_JOIN,
                  [BinaryCondition('id', 'employee_id', '=')])
            .build()
    )

    result = execute_query_plan(plan, tables)
    assert result == {
        Record(
            left=Record({'salary': 55000, 'id': 3, 'position': 'Sales', 'name': 'James Halpert'}),
            right=Record({'employee_id': 3, 'id': 6, 'completed': False})
        ),
         Record(
             left=Record({'salary': 100000, 'id': 0, 'position': 'Regional Manager', 'name': 'Michael Scott'}),
             right=Record({'employee_id': 0, 'id': 1, 'completed': False})
         ),
         Record(
             left=Record({'salary': 65000, 'id': 1, 'position': 'Assistant to the Regional Manager', 'name': 'Dwight K. Schrute'}),
             right=Record({'employee_id': 1, 'id': 3, 'completed': True})
         ),
        Record(
            left=Record({'salary': 65000, 'id': 1, 'position': 'Assistant to the Regional Manager', 'name': 'Dwight K. Schrute'}),
            right=Record({'employee_id': 1, 'id': 4, 'completed': True})
        ),
        Record(
            left=Record({'salary': 100000, 'id': 0, 'position': 'Regional Manager', 'name': 'Michael Scott'}),
            right=Record({'employee_id': 0, 'id': 0, 'completed': False})
        ),
        Record(
            left=Record({'salary': 65000, 'id': 1, 'position': 'Assistant to the Regional Manager', 'name': 'Dwight K. Schrute'}),
            right=Record({'employee_id': 1, 'id': 2, 'completed': True})
        ),
        Record(
            left=Record({'salary': 40000, 'id': 2, 'position': 'Receptionist', 'name': 'Pamela Beesly'}),
            right=Record({'employee_id': 2, 'id': 5, 'completed': True})
        ),
        Record(
            left=Record({'salary': 55000, 'id': 3, 'position': 'Sales', 'name': 'James Halpert'}),
            right=Record({'employee_id': 3, 'id': 9, 'completed': False})
        ),
        Record(
            left=Record({'salary': 55000, 'id': 3, 'position': 'Sales', 'name': 'James Halpert'}),
            right=Record({'employee_id': 3, 'id': 8, 'completed': True})
        ),
        Record(
            left=Record({'salary': 55000, 'id': 3, 'position': 'Sales', 'name': 'James Halpert'}),
            right=Record({'employee_id': 3, 'id': 7, 'completed': False})
        )
    }