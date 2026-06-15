import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def client():
    """Provides the async HTTP client for hitting the API routes."""
    # Using ASGITransport is the standard way to test FastAPI apps with HTTPX
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def setup_contract_fixtures():
    """
    Since your test IDs ('1', '2') already align with your data,
    this helper just passes the payload straight through.
    """

    def _bypass_translation(payload):
        return payload

    return _bypass_translation


@pytest.fixture
def anyio_backend():
    """Instructs AnyIO to use the standard asyncio loop backend."""
    return "asyncio"
