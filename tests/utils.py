from main import Record


def create_employee(id: int, name: str, position: str, salary: int) -> Record:
    return Record(id=id, name=name, position=position, salary=salary)


def create_task(id: int, employee_id: int, completed: bool) -> Record:
    return Record(id=id, employee_id=employee_id, completed=completed)