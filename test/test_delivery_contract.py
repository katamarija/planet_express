import pytest
import sqlite3
from delivery_contract.delivery_contract import DeliveryContract

@pytest.fixture
def contract_api_response():
    return {
            "id": 1,
            "item": "Test Item",
            "crew_requirements": {
                "size": 1,
                "conditions": [],
                },
            "destination": "Test Destination",
            }

def test_init_delivery_contract():
    delivery_contract = DeliveryContract(external_id=123, item="Test Item", crew_size=1, crew_conditions = ["Condition 1"], destination="Test Destination")

    assert delivery_contract.external_id == 123
    assert delivery_contract.item == "Test Item"
    assert delivery_contract.crew_size == 1
    assert delivery_contract.crew_conditions == ["Condition 1"]
    assert delivery_contract.destination == "Test Destination"


def test_save_new_delivery_contract():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    # instance of class DeliveryContract
    delivery_contract = DeliveryContract(external_id=123, item="Test Item", crew_size=1, crew_conditions = ["Condition 1"], destination="Test Destination")
    # calling an instance method
    delivery_contract.save(cursor)
    # class method
    # DeliveryContract.method()

    assert type(delivery_contract.pk) is int

    delivery_contract_rows = cursor.execute(
            """
                select pk, external_id, item, crew_size, destination
                from delivery_contract;
            """
    ).fetchall()

    assert len(delivery_contract_rows) == 1
    assert delivery_contract.pk == delivery_contract_rows[0][0]
    assert delivery_contract_rows[0][1]  == 123
    assert delivery_contract_rows[0][2]  == "Test Item"
    assert delivery_contract_rows[0][3]  == 1
    assert delivery_contract_rows[0][4]  == "Test Destination"

def test_save_update_delivery_contract():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    delivery_contract = DeliveryContract(external_id=123, item="Test Item", crew_size=1, crew_conditions = ["Condition 1"], destination="Test Destination")
    delivery_contract.save(cursor)
    delivery_contract.item = "Testing Item"

    delivery_contract.save(cursor)

    delivery_contract_rows = cursor.execute(
            """
                select pk, external_id, item, crew_size, destination
                from delivery_contract;
            """
    ).fetchall()

    assert len(delivery_contract_rows) == 1
    assert delivery_contract_rows[0][2]  == "Testing Item"

def test_reload_delivery_contract():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    delivery_contract = DeliveryContract(external_id=123, item="Test Item", crew_size=1, crew_conditions = ["Condition 1"], destination="Test Destination")
    delivery_contract.save(cursor)
    delivery_contract.item = "Testing Item"

    delivery_contract.reload(cursor)

    assert delivery_contract.item == "Test Item"

def test_new_delivery_contract_via_api_response(contract_api_response):
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    delivery_contract = DeliveryContract.create_from_api_response(contract_api_response, cursor)

    delivery_contract_rows = cursor.execute(
            """
                select pk, external_id, item, crew_size, destination
                from delivery_contract;
            """
    ).fetchall()

    assert delivery_contract.external_id == 1
    assert delivery_contract.item == "Test Item"
    assert delivery_contract.crew_size == 1
    assert delivery_contract.crew_conditions == []
    assert delivery_contract.destination == "Test Destination"

    assert len(delivery_contract_rows) == 1
    assert delivery_contract.pk == delivery_contract_rows[0][0]
    assert delivery_contract_rows[0][1]  == 1
    assert delivery_contract_rows[0][2]  == "Test Item"
    assert delivery_contract_rows[0][3]  == 1
    assert delivery_contract_rows[0][4]  == "Test Destination"
