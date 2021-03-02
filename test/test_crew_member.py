import pytest
import sqlite3

from crew.crew_member import CrewMember


def test_init_crew_member():
    crew_member = CrewMember(name="Fry")

    assert crew_member.name == "Fry"


def test_save_new_crew_member(cursor):
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
    assert crew_member_rows[0][1] == "Fry"


def test_save_update_crew_member(cursor):
    crew_member = CrewMember(name="Fry")
    crew_member.save(cursor)
    # this is only changing the python version of the object
    crew_member.name = "Philip J. Fry"
    # same operation, but this is updating the DB to match the in memory python version of the object
    crew_member.save(cursor)

    crew_member_rows = cursor.execute(
        """
                select pk, name
                from crew_member;
            """
    ).fetchall()

    assert len(crew_member_rows) == 1
    assert crew_member_rows[0][1] == "Philip J. Fry"


def test_reload_crew_member(cursor):
    crew_member = CrewMember(name="Philip J. Fry")
    crew_member.save(cursor)
    crew_member.name = "Fry"

    crew_member.reload(cursor)

    assert crew_member.name == "Philip J. Fry"
