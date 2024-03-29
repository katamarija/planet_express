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

save_cursor.execute(
    """
    create table if not exists schedule (
      pk integer primary key not null
      , contract_fk integer
      , depart_date text
      , delivery_date text
    );
    """
)

save_cursor.execute(
    """
    create table if not exists crew_assignment(
      crew_fk integer not null
      , schedule_fk integer not null
    );
    """
)
connection.commit()
