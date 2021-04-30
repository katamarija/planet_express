import requests


class LocationRequester:
    @classmethod
    def get_api_response(cls, name):
        URL = "http://localhost:8000/locations"
        r = requests.get(url=URL, params={"name": name})
        data = r.json()
        return data

    # @classmethod
    # def retrieve_and_save_contract_to_db(cls, cursor=None):
    #     api_response = ContractRequester.get_api_response()
    #     DeliveryContract.create_from_api_response(api_response, cursor)
