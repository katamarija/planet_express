import requests

class ContractRequester:
    # method that exists on blueprint of class, not an instance
    @classmethod
    def get_api_response(cls):
        URL = "http://localhost:5000/contracts/request/"
        r = requests.get(url = URL)
        data = r.json()
        return data

    # stubs or mocks next time!!
    # contract object save and into DB
