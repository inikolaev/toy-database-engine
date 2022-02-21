import pytest

from main import Record, Table
from tests.utils import create_employee, create_task


@pytest.fixture
def employees() -> Table:
    return {
        create_employee(0, "Michael Scott", "Regional Manager", 100000),
        create_employee(1, "Dwight K. Schrute", "Assistant to the Regional Manager", 65000),
        create_employee(2, "Pamela Beesly", "Receptionist", 40000),
        create_employee(3, "James Halpert", "Sales", 55000),
        create_employee(4, "Stanley Hudson", "Sales", 55000)
    }


@pytest.fixture
def tasks() -> Table:
    return {
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