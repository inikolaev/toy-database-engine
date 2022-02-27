from sql_parser import parse_sql, Select, read_conditions


def test_sql_parser():
    tokens = parse_sql('select id, name from employees, tasks inner join tasks on employee.id = tasks.employee_id where salary > 10000 and salary < 100000')
    assert tokens == [Select(
        select_list=['id', 'name'],
        select_from=['employees', 'tasks'],
        join=[('inner join', 'tasks', ('employee.id', '=', 'tasks.employee_id'))],
        where=('and', ('salary', '>', '10000'), ('salary', '<', '100000'))
    )]


def test_read_conditions():
    expression = 'a = 1 and b = 2 or c = 3 and d = 4'
    result = read_conditions(expression, 0)
    assert result == (('or', ('and', ('a', '=', '1'), ('b', '=', '2')), ('and', ('c', '=', '3'), ('d', '=', '4'))), 34)


def test_read_conditions_with_brackets():
    expression = 'a = 1 and (b = 2 or c = 3) and d = 4'
    result = read_conditions(expression, 0)
    assert result == (('and', ('a', '=', '1'), ('and', ('or', ('b', '=', '2'), ('c', '=', '3')), ('d', '=', '4'))), 36)
