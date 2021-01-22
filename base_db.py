import abc
import sqlite3

class BaseDB(abc.ABC):

    def __init__(self):
        self._pk = None

    def reload(self, cursor=None):
        if cursor:
            select_cursor = cursor
        else:
            connection = sqlite3.connect("test.db")
            select_cursor = connection.cursor()

        reload_row = select_cursor.execute(
                f"""
                    select
                      { ",".join(self._model_attributes().keys()) }
                    from { self._table_name() }
                    where
                      pk = ( ? )
                      ;
                """
                , [self.pk]
            ).fetchone()
        for index, value in enumerate(self._model_attributes().values()):
            setattr(self, value, reload_row[index])


    def save(self, cursor=None):
        if cursor:
            save_cursor = cursor
        else:
            connection = sqlite3.connect("test.db")
            save_cursor = connection.cursor()

        set_statements = ",".join([f"{key} = ( ? )" for key in self._model_attributes().keys() ])
        values = [getattr(self, attrname) for attrname in self._model_attributes().values()]
        # a = [1, 2, 3, 4]
        # [i * 2 for i in a] => [2, 4, 6, 8]
        # [ transformation for item_variable in list/dict/enumerable]

        if self._pk:
            save_cursor.execute(
                    f"""
                        update { self._table_name() }
                        set
                          { set_statements }
                        where
                          pk = ( ? )
                        ;
                    """
                    , [*values, self.pk]
            )
        else:
            save_cursor.execute(
                    f"""
                        insert into { self._table_name() } (
                          name
                        )
                        values
                        ( ? )
                        ;
                    """
                    , [self.name]
            )

            self._pk = save_cursor.execute("SELECT last_insert_rowid();").fetchone()[0]
        if not cursor:
            connection.commit()



    @abc.abstractmethod
    def _table_name(self):
        raise


    @abc.abstractmethod
    def _model_attributes(self):
        raise
