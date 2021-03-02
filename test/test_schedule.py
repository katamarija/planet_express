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

    # track schedule assignments, Fry is not on every delivery
    # future schedules - when can you schedule them again if currently unavail
