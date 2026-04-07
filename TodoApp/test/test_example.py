import pytest


def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)


def test_boolean():
    validated = True

    assert validated is True
    assert ("hello" == "world") is False


def test_type():
    assert type("Hello" is str)
    assert type("World" is not int)


def test_greater_and_less_then():
    assert 1 > 0
    assert 1 < 2


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]

    assert 1 in num_list
    assert 1 not in any_list
    assert all(num_list)
    assert not any(any_list)


class Student:
    def __init__(self, first_name, last_name, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


def test_person_creation():
    p = Student("John", "Doe", "Computer Science", 4)

    assert p.first_name == "John", "First name should be John"
    assert p.last_name == "Doe", "Last name should be Doe"
    assert p.major == "Computer Science"
    assert p.years == 4


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 4)


def test_person_initialization(default_student):
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Computer Science"
    assert default_student.years == 4
