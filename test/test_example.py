import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance("Hello World", str)
    assert not isinstance('10', int)
    assert isinstance(1, int)
    assert not isinstance(1, str)

def test_boolean():
    validated = True
    assert validated is True
    assert ("Hello" == 'World') is False

def test_type():
    assert type("Hello") is str
    assert type(1) is int

def test_bool():
    assert 7 > 1
    assert 1 < 7
    assert bool(1) is True
    assert bool(0) is False

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

def test_person_initialization():
    student = Student("John", "Doe", "Computer Science", 3)
    assert student.first_name == "John", "First name is not John"
    assert student.last_name == "Doe", "Last name is not Doe"
    assert student.major == "Computer Science", "Major is not Computer Science"
    assert student.years == 3

@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 3)

def test_fixture(default_student):
    assert default_student.first_name == "John", "First name is not John"
    assert default_student.last_name == "Doe", "Last name is not Doe"
    assert default_student.major == "Computer Science", "Major is not Computer Science"
    assert default_student.years == 3