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
