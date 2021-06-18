import math
import datetime
from base_db import BaseDB
from delivery_contract.delivery_contract import DeliveryContract
from location_requester.location_requester import LocationRequester
from crew.crew_member import CrewMember


class Schedule(BaseDB):
    DEFAULT_DEPART_DATE = datetime.date(3000, 1, 1)
    DEFAULT_SPEED = 1
    DEFAULT_ORIGIN = "earth"

    def __init__(self, contract):
        super().__init__()
        self._contract = contract
        self._crew = []
        self._depart_date = self.DEFAULT_DEPART_DATE
        self._delivery_date = self._calculate_delivery_date()

    def _table_name(self):
        return "schedule"

    def _model_attributes(self):
        return {"depart_date": "_depart_date", "delivery_date": "_delivery_date"}

    def _calculate_delivery_date(self):
        """
        return a date
        distance = sqrt((x1 - x2)**2 + (y1-y2)**2 + (z1 - z2)**2)
        """
        origin = self.DEFAULT_ORIGIN
        origin_coords = LocationRequester.get_api_response(origin)["coordinates"]
        x1 = origin_coords["x"]
        y1 = origin_coords["y"]
        z1 = origin_coords["z"]

        destination = self.contract.destination
        destination_coords = LocationRequester.get_api_response(destination)[
            "coordinates"
        ]
        x2 = destination_coords["x"]
        y2 = destination_coords["y"]
        z2 = destination_coords["z"]

        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        speed = self.DEFAULT_SPEED
        delivery_date = self._depart_date + datetime.timedelta(days=(distance / speed))
        return delivery_date

    @property
    def contract(self):
        return self._contract

    @property
    def crew(self):
        return self._crew

    @property
    def delivery_date(self):
        return self._delivery_date

    def assign_crew(self, cursor=None):
        crew_size = self._contract.crew_size
        crew_members = CrewMember.get_available_crew_member_from_db(
            crew_size, self._depart_date, cursor
        )
        # conditions but ignore for now
        self._crew = crew_members

    def save(self, cursor=None):
        super().save(cursor)
        self.save_association("contract_fk", self._contract.pk, cursor)
        # use in memory crew objects from assign_crew, get their pks and then insert into crew_assignment table
        for crew in self.crew:
            self.save_many_to_many_association(
                "crew_assignment",
                ["schedule_fk", "crew_fk"],
                [self.pk, crew.pk],
                cursor,
            )
