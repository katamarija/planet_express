import pytest
import sqlite3
from crew.crew_member import CrewMember

@pytest.fixture
def cursor():
    connection = sqlite3.connect("test.db")
    yield connection.cursor()
    connection.rollback()

@pytest.fixture
def fry(cursor):
    return CrewMember(name="Fry").save(cursor)

@pytest.fixture
def leela(cursor):
    return CrewMember(name="Leela").save(cursor)
