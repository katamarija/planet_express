import pytest
import sqlite3
from delivery_contract.delivery_contract import DeliveryContract

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
    delivery_contract = DeliveryContract(external_id=123, item="Test Item", crew_size=1, crew_conditions = ["Condition 1"], destination="Test Destination")
    delivery_contract.save(cursor)

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
