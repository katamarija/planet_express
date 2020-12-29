import sqlite3

class CrewMember:

    def __init__(self, name):
        self._name = name
        self._pk = None


    @property
    def name(self):
        return self._name


    @property
    def pk(self):
        return self._pk


    def save(self, cursor=None):
        if cursor:
            save_cursor = cursor
        else:
            connection = sqlite3.connect("test.db")
            save_cursor = connection.cursor()

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
