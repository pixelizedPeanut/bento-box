import pytest
from fastapi import status
from httpx import AsyncClient

# --- THE MEMBERS & INVENTORY API CONTRACT TABLE ---
RESOURCE_CONTRACT_CASES = [
    (
        "FETCH_ALL_INVENTORY",
        "GET",
        "/inventory/",
        None,  # No body required for GET
        status.HTTP_200_OK,
    ),
    (
        "CREATE_INVENTORY_MALFORMED",
        "POST",
        "/inventory/",
        {"wrong_field": "Misfit Box"},
        status.HTTP_422_UNPROCESSABLE_CONTENT,
    ),
    (
        "FETCH_ALL_MEMBERS",
        "GET",
        "/members/",
        None,
        status.HTTP_200_OK,
    ),
]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "scenario, method, path, payload, expected_status", RESOURCE_CONTRACT_CASES
)
async def test_resource_api_contracts(
    client: AsyncClient,
    scenario: str,
    method: str,
    path: str,
    payload: dict | None,
    expected_status: int,
):
    """
    Living Documentation: Enforces the network contract for browsing and creating entities.
    """
    # 1. Fire the asynchronous network request depending on whether a payload exists
    response = await client.request(method, path, json=payload)

    # 2. Verify the response status matches the API agreement exactly
    assert response.status_code == expected_status, (
        f"Scenario '{scenario}' failed. Got body: {response.json()}"
    )

    # 3. Contract Check: Validate that successful list retrievals return a JSON array
    if expected_status == status.HTTP_200_OK:
        assert isinstance(response.json(), list), f"Expected list layout for {scenario}"
