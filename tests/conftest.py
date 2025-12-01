import pytest
import asyncio
from core.aether_conductor import AetherConductor
from core.signature import OriginMetadata, AISource

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def clean_conductor():
    """Returns a clean AetherConductor instance for each test.

    Since AetherConductor is a singleton, we need to reset its state
    between tests to ensure isolation.
    """
    # Reset the singleton instance (if possible, or just clear channels)
    # The current implementation of AetherConductor uses __new__ for singleton.
    # We can clear the state of the existing instance.

    conductor = AetherConductor()
    conductor.channels.clear()
    conductor.trust_scores = {
        AISource.HUMAN_ARCHITECT: 100,
        AISource.GEMINI_CORE: 95,
        AISource.UNKNOWN_ECHO: 10
    }
    return conductor
