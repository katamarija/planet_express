from datetime import date
import pytest
import sqlite3

from unittest.mock import MagicMock, patch
from delivery_contract.delivery_contract import DeliveryContract
from crew.crew_member import CrewMember
from schedule.schedule import Schedule


def test_init_schedule(cursor, fry, leela):
    with patch(
        "location_requester.location_requester.LocationRequester.get_api_response"
    ) as mock_method:
        delivery_contract = DeliveryContract(
            external_id=123,
            item="Test Item",
            crew_size=2,
            crew_conditions=["Condition 1"],
            destination="mars",
        )

        def side_effect_func(location):
            test_coords = {
                "earth": {"coordinates": {"x": 0, "y": 0, "z": 0}},
                "mars": {"coordinates": {"x": 2, "y": 2, "z": 3}},
            }
            return test_coords[location]

        mock_method.side_effect = side_effect_func

        schedule = Schedule(delivery_contract)
        schedule.assign_crew(cursor)

    assert schedule.contract == delivery_contract
    assert type(schedule.crew) is list
    assert len(schedule.crew) == 2
    assert isinstance(schedule.crew[0], CrewMember)
    assert isinstance(schedule.crew[1], CrewMember)
    assert type(schedule.delivery_date) is date
    assert schedule.delivery_date.strftime("%d/%m/%Y") == "05/01/3000"


def test_schedule_with_crew_saved(cursor, fry, leela):
    with patch(
        "location_requester.location_requester.LocationRequester.get_api_response"
    ) as mock_method:
        delivery_contract = DeliveryContract(
            external_id=123,
            item="Test Item",
            crew_size=2,
            crew_conditions=["Condition 1"],
            destination="the moon",
        )

        delivery_contract.save(cursor)
        schedule = Schedule(delivery_contract)

    schedule.assign_crew(cursor)
    schedule.save(cursor)

    assert type(schedule.pk) is int
    schedule_rows = cursor.execute(
        """
            select pk, contract_fk, depart_date, delivery_date
            from schedule;
        """
    ).fetchall()

    assert len(schedule_rows) == 1
    assert type(schedule_rows[0][0]) is int
    assert schedule_rows[0][1] == delivery_contract.pk
    assert len(schedule.crew) == 2
    assert schedule_rows[0][2] == "3000-01-01"
    assert schedule_rows[0][3] == "3000-01-02"

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


def test_assign_crew_to_simultaneous_contracts(cursor, fry, leela, zoidberg):
    with patch(
        "location_requester.location_requester.LocationRequester.get_api_response"
    ) as mock_method:
        delivery_contract = DeliveryContract(
            external_id=123,
            item="Test Item",
            crew_size=1,
            crew_conditions=["Condition 1"],
            destination="the moon",
        )

        delivery_contract.save(cursor)
        schedule_moon = Schedule(delivery_contract)

    with patch(
        "location_requester.location_requester.LocationRequester.get_api_response"
    ) as mock_method:
        delivery_contract = DeliveryContract(
            external_id=456,
            item="Test Item",
            crew_size=2,
            crew_conditions=["Condition 1"],
            destination="mars",
        )

        delivery_contract.save(cursor)
        schedule_mars = Schedule(delivery_contract)

    schedule_moon.assign_crew(cursor)
    schedule_moon.save(cursor)
    schedule_mars.assign_crew(cursor)
    schedule_mars.save(cursor)

    assert schedule_moon.crew[0].pk != schedule_mars.crew[0].pk
    assert schedule_moon.crew[0].pk != schedule_mars.crew[1].pk
