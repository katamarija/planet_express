from delivery_contract.delivery_contract import DeliveryContract
from crew.crew_member import CrewMember


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

    def assign_crew(self, cursor=None):
        crew_size = self._contract.crew_size
        crew_members = CrewMember.get_crew_members_from_db(crew_size, cursor)
        # conditions but ignore for now
        self._crew = crew_members
