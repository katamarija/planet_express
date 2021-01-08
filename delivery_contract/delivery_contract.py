class DeliveryContract:

    def __init__(self, external_id, item, crew_size, crew_conditions, destination):
        self._external_id = external_id
        self._item = item
        self._crew_size = crew_size
        self._crew_conditions = crew_conditions
        self._destination = destination
        self._pk = None

    @property
    def item(self):
        return self._item

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
