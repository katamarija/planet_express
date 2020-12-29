import pytest
import sqlite3

from crew.crew_member import CrewMember

def test_init_crew_member():
    crew_member = CrewMember(name="Fry")

    assert crew_member.name == "Fry"

def test_save_crew_member():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    crew_member = CrewMember(name="Fry")
    crew_member.save(cursor)

    assert type(crew_member.pk) is int
    assert crew_member.name == "Fry"

    crew_member_rows = cursor.execute(
            """
                select pk, name
                from crew_member;
            """
    ).fetchall()

    assert len(crew_member_rows) == 1
    assert type(crew_member_rows[0][0]) is int
    assert crew_member_rows[0][1]  == "Fry"
