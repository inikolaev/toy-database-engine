from database_engine import create_task, create_employee, order_by, projection, rename, left_outer_join

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
