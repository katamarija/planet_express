from datetime import datetime
import pytest
import sqlite3

from delivery_contract.delivery_contract import DeliveryContract
from crew.crew_member import CrewMember
from schedule.schedule import Schedule


def test_init_schedule(cursor, fry, leela):
    delivery_contract = DeliveryContract(
        external_id=123,
        item="Test Item",
        crew_size=2,
        crew_conditions=["Condition 1"],
        destination="Test Destination",
    )
    schedule = Schedule(delivery_contract)
    schedule.assign_crew(cursor)

    assert schedule.contract == delivery_contract
    assert type(schedule.crew) is list
    assert len(schedule.crew) == 2
    assert isinstance(schedule.crew[0], CrewMember)
    assert isinstance(schedule.crew[1], CrewMember)
    assert type(schedule.delivery_date) is datetime


def test_schedule_with_crew_saved(cursor, fry, leela):
    delivery_contract = DeliveryContract(
        external_id=123,
        item="Test Item",
        crew_size=2,
        crew_conditions=["Condition 1"],
        destination="Test Destination",
    )
    delivery_contract.save(cursor)
    schedule = Schedule(delivery_contract)
    schedule.assign_crew(cursor)
    schedule.save(cursor)

    assert type(schedule.pk) is int
    schedule_rows = cursor.execute(
        """
            select pk, contract_fk
            from schedule;
        """
    ).fetchall()

    assert len(schedule_rows) == 1
    assert type(schedule_rows[0][0]) is int
    assert schedule_rows[0][1] == delivery_contract.pk
    assert len(schedule.crew) == 2

    crew_assignments = cursor.execute(
        """
            select crew_fk
            from crew_assignment
            where schedule_fk = ( ? )
            order by crew_fk;
        """,
        [schedule.pk],
    ).fetchall()
    crew_results = [result[0] for result in crew_assignments]

    assert crew_results == sorted(crew.pk for crew in schedule.crew)
