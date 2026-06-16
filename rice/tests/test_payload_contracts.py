import pytest
from fastapi import status
from httpx import AsyncClient

# --- THE LIVING FIELD SPECIFICATION CONTRACT ---
# This table explicitly defines the structural keys the FE team relies on.
PAYLOAD_CONTRACT_CASES = [
    (
        "FETCH_INVENTORY_SCHEMA",
        "GET",
        "/inventory/",
        None,
        status.HTTP_200_OK,
        [
            "id",
            "title",
            "remaining_count",
        ],  # Every item in the list MUST have these keys
    ),
    (
        "FETCH_MEMBERS_SCHEMA",
        "GET",
        "/members/",
        None,
        status.HTTP_200_OK,
        ["id", "name", "surname", "booking_count"],  # Member model wire contract
    ),
    (
        "FETCH_ALL_BOOKINGS",
        "GET",
        "/bookings/",
        None,
        status.HTTP_200_OK,
        [
            "booking_ref",
            "member_id",
            "inventory_id",
            "created_at",
            "status",
        ],
    ),
    # currently canceled as the db gets generated in flight
    # and we don't have a script to esure the booking with the
    # reference actually exists
    # keeping the test for documentation purposes
    # (
    #     "CANCEL_EXISTING_BOOKING",
    #     "POST",
    #     "/cancel",
    #     {"booking_ref": "CNCG-A40A26E9"},
    #     status.HTTP_200_OK,
    #     ["message", "booking_ref", "status"],
    # ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "scenario, method, path, payload, expected_status, expected_keys",
    PAYLOAD_CONTRACT_CASES,
)
async def test_api_payload_structures(
    client: AsyncClient,
    scenario: str,
    method: str,
    path: str,
    payload: dict | None,
    expected_status: int,
    expected_keys: list[str],
):
    """
    Structural Guardrail: Locks down field names so backend changes don't break the frontend.
    """
    # 1. Dispatch the network call
    response = await client.request(method, path, json=payload)
    assert response.status_code == expected_status

    response_data = response.json()

    # 2. Extract a sample object to test structural integrity
    # If the endpoint returns a list (like GET /members/), pick the first item to evaluate keys.
    if isinstance(response_data, list):
        # If the DB is completely empty during the test run, skip structural checks safely
        if len(response_data) == 0:
            pytest.skip(
                f"Skipping key validation for {scenario} because database returned an empty list."
            )
        target_object = response_data[0]
    else:
        target_object = response_data

    # 3. Assert that every required frontend key exists in the backend response
    for key in expected_keys:
        assert key in target_object, (
            f"❌ SHIFTING SANDS DETECTED in '{scenario}'!\n"
            f"The frontend expects the key '{key}', but it was missing from the backend response.\n"
            f"Actual response shape: {list(target_object.keys())}"
        )
