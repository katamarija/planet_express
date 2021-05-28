import pytest
import sqlite3
from crew.crew_member import CrewMember
from delivery_contract.delivery_contract import DeliveryContract


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


@pytest.fixture
def delivery_contract():
    return DeliveryContract(
        external_id=123,
        item="Test Item",
        crew_size=1,
        crew_conditions=["Condition 1"],
        destination="Test Destination",
    )
