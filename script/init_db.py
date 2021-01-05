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
connection.commit()
