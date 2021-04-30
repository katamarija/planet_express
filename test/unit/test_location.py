"""
Adding Location
- new calculations of delivery time based on location coords
- location attr for schedule
  - starting and ending loc?
- contract attr for schedule
  - start and ending loc
- open ? do we store the location info here or not?

"""

import pytest

# import requests
from unittest.mock import MagicMock, patch
from location_requester.location_requester import LocationRequester


def test_performs_successful_get_to_endpoint():
    name = "earth"
    response = LocationRequester.get_api_response(name=name)
    assert type(response["name"]) == str
    assert type(response["coordinates"]) == dict
    assert type(response["coordinates"]["x"]) == int
    assert type(response["coordinates"]["y"]) == int
    assert type(response["coordinates"]["z"]) == int


def test_with_mocked_library():
    with patch("requests.get") as mock_method:
        name = "earth"
        response = LocationRequester.get_api_response(name=name)
        mock_method.assert_called_once_with(
            url="http://localhost:8000/locations", params={"name": "earth"}
        )
