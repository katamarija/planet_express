from delivery_contract.delivery_contract import DeliveryContract


class Schedule:
    def __init__(self, contract):
        self._contract = contract
        self._crew = []

    @property
    def contract(self):
        return self._contract

    @property
    def crew(self):
        return self._crew


    def assign_crew(self):
        # contract.crew_size
        # crewmembers
        # self._crew =
        # Get number of crew needed from contract, then assign the crew from DB to the schedule,
        # Need to be the crewmembers, not just a number!
