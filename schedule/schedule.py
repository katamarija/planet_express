from base_db import BaseDB
from delivery_contract.delivery_contract import DeliveryContract
from crew.crew_member import CrewMember


class Schedule(BaseDB):
    def __init__(self, contract):
        super().__init__()
        self._contract = contract
        self._crew = []

    def _table_name(self):
        return "schedule"

    def _model_attributes(self):
        return {}

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

    def save(self, cursor=None):
        super().save(cursor)
        self.save_association("contract_fk", self._contract.pk, cursor)

