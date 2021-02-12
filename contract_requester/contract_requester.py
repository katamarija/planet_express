import requests
from delivery_contract.delivery_contract import DeliveryContract

class ContractRequester:
    # method that exists on blueprint of class, not an instance
    @classmethod
    def get_api_response(cls):
        URL = "http://localhost:5000/contracts/request/"
        r = requests.get(url = URL)
        data = r.json()
        return data

    @classmethod
    def retrieve_and_save_contract_to_db(cls, cursor=None):
        api_response = ContractRequester.get_api_response()
        DeliveryContract.create_from_api_response(api_response, cursor)
