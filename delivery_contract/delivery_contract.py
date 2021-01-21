from base_db import BaseDB

class DeliveryContract(BaseDB):

    def __init__(self, external_id, item, crew_size, crew_conditions, destination):
        self._external_id = external_id
        self._item = item
        self._crew_size = crew_size
        self._crew_conditions = crew_conditions
        self._destination = destination
        self._pk = None

    def _table_name(self):
        return 'delivery_contract'

    def _table_columns(self):
        return ['external_id', 'item', 'crew_size', 'destination']

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def destination(self):
        return self._destination

    @property
    def external_id(self):
        return self._external_id

    @property
    def crew_size(self):
        return self._crew_size

    @property
    def crew_conditions(self):
        return self._crew_conditions

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
            update = save_cursor.execute(
                    """
                        update delivery_contract
                        set
                          external_id = ( ? )
                          , item = ( ? )
                          , crew_size = ( ? )
                          , destination = ( ? )
                        where
                          pk = ( ? )
                        ;
                    """
                    , [self.external_id, self.item, self.crew_size, self.destination, self.pk]
            )
        else:
            new_save = save_cursor.execute(
                    """
                        insert into delivery_contract (
                          external_id
                          , item
                          , crew_size
                          , destination
                        )
                        values
                        ( ?,?,?,? )
                        ;
                    """
                    , [self.external_id, self.item, self.crew_size, self.destination]
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
    #     delivery_contract_reload = select_cursor.execute(
    #             """
    #                 select pk, external_id, item, crew_size, destination
    #                 from delivery_contract
    #                 where
    #                   pk = ( ? )
    #                 ;
    #             """
    #             , [self.pk]
    #         ).fetchone()
    #     self._external_id = delivery_contract_reload[1]
    #     self._item = delivery_contract_reload[2]
    #     self._crew_size = delivery_contract_reload[3]
    #     self._destination = delivery_contract_reload[4]
