import pytest
from fastapi import status
from httpx import AsyncClient

# --- THE CLEAN API CONTRACT TABLE ---
# Front-end engineers can read this block alone to understand the entire route logic.
BOOKING_CONTRACT_CASES = [
    (
        "SUCCESS_PATH",
        "POST",
        "/book",
        {"member_id": "2", "inventory_id": "1"},
        status.HTTP_201_CREATED,
    ),
    (
        "MEMBER_LIMIT_EXCEEDED",
        "POST",
        "/book",
        {"member_id": "1", "inventory_id": "1"},
        status.HTTP_400_BAD_REQUEST,
    ),
    (
        "ITEM_OUT_OF_STOCK",
        "POST",
        "/book",
        {"member_id": "5", "inventory_id": "6"},
        status.HTTP_400_BAD_REQUEST,
    ),
    (
        "MALFORMED_PAYLOAD",
        "POST",
        "/book",
        {"wrong_payload_key": "some_value"},
        status.HTTP_422_UNPROCESSABLE_CONTENT,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "scenario, method, path, payload, expected_status", BOOKING_CONTRACT_CASES
)
async def test_booking_api_contract(
    client: AsyncClient,
    setup_contract_fixtures,  # Hidden helper that maps strings to database states
    scenario: str,
    method: str,
    path: str,
    payload: dict,
    expected_status: int,
):
    """
    Living Documentation: Verifies that the endpoint respects the network structural design.
    """
    # 1. Translate placeholder string keys inside the test matrix into live database UUIDs
    real_payload = setup_contract_fixtures(payload)

    # 2. Fire Request using the exact method, endpoint, and payload from the table above
    response = await client.request(method, path, json=real_payload)

    # 3. Enforce the status boundary rule
    assert response.status_code == expected_status, (
        f"Scenario '{scenario}' failed. Got body: {response.json()}"
    )
