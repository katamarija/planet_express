import pytest
from contract_requester.contract_requester import ContractRequester

def test_performs_successful_get_to_endpoint():
    response = ContractRequester.get_api_response()
    assert type(response["crew_requirements"]["conditions"]) == list
    assert type(response["crew_requirements"]["size"]) == int
    assert type(response["destination"]) == str
    assert type(response["id"]) == int
    assert type(response["item"]) == str
    # could add assertion / alert if the dictionary has additional key/values
