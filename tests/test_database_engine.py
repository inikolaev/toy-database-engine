from database_engine import select, create_employee, projection, rename, inner_join, left_outer_join
from models import Table, Record


def test_select_all(employees: Table):
    result = select(employees, lambda r: True)
    assert result == employees


def test_select_with_condition(employees: Table):
    result = select(employees, lambda r: r.salary > 56000)
    assert result == {
        create_employee(0, "Michael Scott", "Regional Manager", 100000),
        create_employee(1, "Dwight K. Schrute", "Assistant to the Regional Manager", 65000),
    }


def test_projection(employees: Table):
    result = projection(employees, columns={'id', 'name'})
    assert result == {
        Record(id=2, name='Pamela Beesly'),
        Record(id=1, name='Dwight K. Schrute'),
        Record(id=0, name='Michael Scott'),
        Record(id=3, name='James Halpert'),
        Record(id=4, name='Stanley Hudson'),
    }


def test_rename(employees: Table):
    result = rename(employees, columns={'id': 'employee_id'})
    assert result == {
        Record(name='Dwight K. Schrute', salary=65000, position='Assistant to the Regional Manager', id=1, aliases={'id': 'employee_id'}),
        Record(name='James Halpert', salary=55000, position='Sales', id=3, aliases={'id': 'employee_id'}),
        Record(name='Michael Scott', salary=100000, position='Regional Manager', id=0, aliases={'id': 'employee_id'}),
        Record(name='Pamela Beesly', salary=40000, position='Receptionist', id=2, aliases={'id': 'employee_id'}),
        Record(name='Stanley Hudson', salary=55000, position='Sales', id=4, aliases={'id': 'employee_id'}),
    }


def test_inner_join(employees: Table, tasks: Table):
    result = inner_join(employees, tasks, lambda e, t: e.id == t.employee_id)
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


def test_left_outer_join(employees: Table, tasks: Table):
    result = left_outer_join(employees, tasks, lambda e, t: e.id == t.employee_id)
    assert result == {
        Record(
            left=Record(id=2, name='Pamela Beesly', position='Receptionist', salary=40000), 
            right=Record(id=5, employee_id=2, completed=True)
        ),
        Record(
            left=Record(id=0, name='Michael Scott', position='Regional Manager', salary=100000), 
            right=Record(id=0, employee_id=0, completed=False)
        ),
        Record(
            left=Record(id=1, name='Dwight K. Schrute', position='Assistant to the Regional Manager', salary=65000), 
            right=Record(id=4, employee_id=1, completed=True)
        ),
        Record(
            left=Record(id=3, name='James Halpert', position='Sales', salary=55000), 
            right=Record(id=6, employee_id=3, completed=False)
        ),
        Record(
            left=Record(id=1, name='Dwight K. Schrute', position='Assistant to the Regional Manager', salary=65000), 
            right=Record(id=3, employee_id=1, completed=True)
        ),
        Record(
            left=Record(id=3, name='James Halpert', position='Sales', salary=55000), 
            right=Record(id=9, employee_id=3, completed=False)
        ),
        Record(
            left=Record(id=0, name='Michael Scott', position='Regional Manager', salary=100000), 
            right=Record(id=1, employee_id=0, completed=False)
        ),
        Record(
            left=Record(id=4, name='Stanley Hudson', position='Sales', salary=55000)
        ),
        Record(
            left=Record(id=3, name='James Halpert', position='Sales', salary=55000), 
            right=Record(id=7, employee_id=3, completed=False)
        ),
        Record(
            left=Record(id=3, name='James Halpert', position='Sales', salary=55000), 
            right=Record(id=8, employee_id=3, completed=True)
        ),
        Record(
            left=Record(id=1, name='Dwight K. Schrute', position='Assistant to the Regional Manager', salary=65000), 
            right=Record(id=2, employee_id=1, completed=True)
        )
    }
