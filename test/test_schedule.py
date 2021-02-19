import pytest
from delivery_contract.delivery_contract import DeliveryContract
from crew.crew_member import CrewMember
from schedule.schedule import Schedule


def test_init_schedule():
    delivery_contract = DeliveryContract(
        external_id=123,
        item="Test Item",
        crew_size=1,
        crew_conditions=["Condition 1"],
        destination="Test Destination",
    )
    schedule = Schedule(delivery_contract)

    assert schedule.contract == delivery_contract
    assert type(schedule.crew) is list
    assert len(schedule.crew) == 1
    assert isinstance(schedule.crew[0], CrewMember)
