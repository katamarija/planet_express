from base_db import BaseDB
import sqlite3
import datetime


class CrewMember(BaseDB):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def _table_name(self):
        return "crew_member"

    def _model_attributes(self):
        return {"name": "_name"}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def get_available_crew_member_from_db(cls, quantity, cursor=None):
        crew_members = []

        crew_member_rows = cursor.execute(
            """
                select
                  c.pk, c.name, max(s.delivery_date) as max_delivery_date
                from crew_member c
                left join crew_assignment ca on ca.crew_fk = c.pk
                left join schedule s on s.pk = ca.schedule_fk
                group by 1, 2
                order by s.delivery_date asc
                limit ? ;
            """,
            [quantity],
        ).fetchall()
        for row in crew_member_rows:
            pk = row[0]
            name = row[1]

            crew_member = cls(name)
            crew_member._pk = pk
            crew_members.append(crew_member)

        crew_available_dates = [
            datetime.datetime.strptime(row[2], "%Y-%m-%d") if row[2] != None else None
            for row in crew_member_rows
        ]

        available_dates_filtered = list(filter(None, crew_available_dates))
        if len(available_dates_filtered) == 0:
            return crew_members, None
        return crew_members, max(available_dates_filtered)
