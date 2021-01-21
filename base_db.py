import abc
import sqlite3

class BaseDB(abc.ABC):

    def reload(self, cursor=None):
        if cursor:
            select_cursor = cursor
        else:
            connection = sqlite3.connect("test.db")
            select_cursor = connection.cursor()

        reload_row = select_cursor.execute(
                f"""
                    select
                      { ",".join(self._table_columns()) }
                    from { self._table_name() }
                    where
                      pk = ( ? )
                      ;
                """
                , [self.pk]
            ).fetchone()
        for index, column in enumerate(self._table_columns()):
            setattr(self, column, reload_row[index])


    @abc.abstractmethod
    def _table_name(self):
        raise


    @abc.abstractmethod
    def _table_columns(self):
        raise
