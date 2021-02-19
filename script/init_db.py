import sqlite3

connection = sqlite3.connect("test.db")
save_cursor = connection.cursor()

save_cursor.execute(
    """
        create table if not exists crew_member (
          pk integer primary key not null
          , name text not null
        );
        """
)

save_cursor.execute(
    """
        create table if not exists delivery_contract (
          pk integer primary key not null
          , external_id integer not null
          , item text not null
          , crew_size integer not null
          , destination text not null
        );
        """
)

connection.commit()
