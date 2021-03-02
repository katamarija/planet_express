import pytest
import sqlite3
from contract_requester.contract_requester import ContractRequester


def test_performs_successful_get_to_endpoint():
    response = ContractRequester.get_api_response()
    assert type(response["crew_requirements"]["conditions"]) == list
    assert type(response["crew_requirements"]["size"]) == int
    assert type(response["destination"]) == str
    assert type(response["id"]) == int
    assert type(response["item"]) == str
    # could add assertion / alert if the dictionary has additional key/values


def test_retrieve_and_save_contract_to_db(cursor):
    ContractRequester.retrieve_and_save_contract_to_db(cursor)

    delivery_contract_rows = cursor.execute(
        """
                select pk, external_id, item, crew_size, destination
                from delivery_contract;
            """
    ).fetchall()

    assert len(delivery_contract_rows) == 1
