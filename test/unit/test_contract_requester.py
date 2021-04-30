import pytest
import sqlite3
from unittest.mock import MagicMock, patch
from contract_requester.contract_requester import ContractRequester


def test_retrieve_and_save_contract_to_db(cursor):
    with patch("requests.get") as mock_method:
        # r_mock = MagicMock()
        # r_mock.json.return_value = {
        #     "id": 486769,
        #     "item": "'Please Don't Drink The Emperor' Sign",
        #     "crew_requirements": {
        #         "size": 5,
        #         "conditions": [],
        #     },
        #     "destination": "Trisol",
        # }
        # mock_method.return_value = r_mock

        mock_method.return_value.json.return_value = {
            "id": 486769,
            "item": "'Please Don't Drink The Emperor' Sign",
            "crew_requirements": {
                "size": 5,
                "conditions": [],
            },
            "destination": "Trisol",
        }

        ContractRequester.retrieve_and_save_contract_to_db(cursor)
        mock_method.assert_called_once_with(
            url="http://localhost:8000/contracts/request/"
        )

    delivery_contract_rows = cursor.execute(
        """
                select pk, external_id, item, crew_size, destination
                from delivery_contract;
            """
    ).fetchall()

    assert len(delivery_contract_rows) == 1
