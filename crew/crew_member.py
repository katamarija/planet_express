from base_db import BaseDB
import sqlite3

class CrewMember(BaseDB):

    def __init__(self, name):
        self._name = name
        self._pk = None


    def _table_name(self):
        return 'crew_member'

    def _table_columns(self):
        return ['name']

    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        self._name = name


    @property
    def pk(self):
        return self._pk


    def save(self, cursor=None):
        if cursor:
            save_cursor = cursor
        else:
            connection = sqlite3.connect("test.db")
            save_cursor = connection.cursor()

        if self._pk:
            crew_member_update = save_cursor.execute(
                    """
                        update crew_member
                        set name = ( ? )
                        where
                          pk = ( ? )
                        ;
                    """
                    , [self.name, self.pk]
            )
        else:
            crew_member_rows = save_cursor.execute(
                    """
                        insert into crew_member ( name )
                        values
                        ( ? )
                        ;
                    """
                    , [self.name]
            )

            self._pk = save_cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
        if not cursor:
            connection.commit()

    # def reload(self, cursor=None):
    #     if cursor:
    #         select_cursor = cursor
    #     else:
    #         connection = sqlite3.connect("test.db")
    #         select_cursor = connection.cursor()
    #
    #     crew_member_reload = select_cursor.execute(
    #             """
    #                 select pk, name
    #                 from crew_member
    #                 where
    #                   pk = ( ? )
    #                   ;
    #             """
    #             , [self.pk]
    #         ).fetchone()
    #     self.name = crew_member_reload[1]
