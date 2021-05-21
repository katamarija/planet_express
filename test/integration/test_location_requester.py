import pytest
from location_requester.location_requester import LocationRequester


def test_performs_successful_get_to_endpoint():
    name = "earth"
    response = LocationRequester.get_api_response(name=name)
    assert type(response["name"]) == str
    assert type(response["coordinates"]) == dict
    assert type(response["coordinates"]["x"]) == int
    assert type(response["coordinates"]["y"]) == int
    assert type(response["coordinates"]["z"]) == int
