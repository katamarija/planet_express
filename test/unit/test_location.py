import pytest

from unittest.mock import MagicMock, patch
from location_requester.location_requester import LocationRequester


def test_with_mocked_library():
    with patch("requests.get") as mock_method:
        name = "earth"
        response = LocationRequester.get_api_response(name=name)
        mock_method.assert_called_once_with(
            url="http://localhost:8000/locations", params={"name": "earth"}
        )
