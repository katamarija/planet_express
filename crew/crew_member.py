from base_db import BaseDB
import sqlite3

class CrewMember(BaseDB):

    def __init__(self, name):
        super().__init__()
        self._name = name

    def _table_name(self):
        return 'crew_member'

    def _model_attributes(self):
        return {'name':'_name'}

    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        self._name = name


    @property
    def pk(self):
        return self._pk


    # def save(self, cursor=None):
    #     if cursor:
    #         save_cursor = cursor
    #     else:
    #         connection = sqlite3.connect("test.db")
    #         save_cursor = connection.cursor()
    #
    #     if self._pk:
    #         crew_member_update = save_cursor.execute(
    #                 """
    #                     update crew_member
    #                     set name = ( ? )
    #                     where
    #                       pk = ( ? )
    #                     ;
    #                 """
    #                 , [self.name, self.pk]
    #         )
    #     else:
    #         crew_member_rows = save_cursor.execute(
    #                 """
    #                     insert into crew_member ( name )
    #                     values
    #                     ( ? )
    #                     ;
    #                 """
    #                 , [self.name]
    #         )
    #
    #         self._pk = save_cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
    #     if not cursor:
    #         connection.commit()
