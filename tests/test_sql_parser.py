from sql_parser import parse_sql, Select


def test_sql_parser():
    tokens = parse_sql('select id, name from employees, tasks inner join tasks on employee.id = tasks.employee_id where salary > 10000 and salary < 100000')
    assert tokens == [Select(
        select_list=['id', 'name'],
        select_from=['employees', 'tasks'],
        join=[('inner join', 'tasks', [('employee.id', '=', 'tasks.employee_id')])],
        where=[('salary', '>', '10000'), ('salary', '<', '100000')]
    )]
