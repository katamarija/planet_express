from base_db import BaseDB
import sqlite3


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
    def get_available_crew_member_from_db(cls, quantity, depart_date_raw, cursor=None):
        crew_members = []
        depart_date = depart_date_raw.strftime("%Y-%m-%d")
        crew_member_rows = cursor.execute(
            """
                select
                  c.pk, c.name
                from
                  crew_member c
                left join crew_assignment ca on ca.crew_fk = c.pk
                left join schedule s on s.pk = ca.schedule_fk
                where
                  s.delivery_date < ? or ca.crew_fk is null
                limit ? ;
                """,
            [depart_date, quantity],
        ).fetchall()
        for row in crew_member_rows:
            pk = row[0]
            name = row[1]
            crew_member = cls(name)
            crew_member._pk = pk
            crew_members.append(crew_member)

        return crew_members
