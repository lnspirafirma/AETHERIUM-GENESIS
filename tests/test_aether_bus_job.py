import pytest
import asyncio
from core.aether_conductor import conductor

@pytest.mark.asyncio
async def test_job_registry_lifecycle():
    # 1. Register Job
    intent = {"id": "JOB-001", "task": "Test Job"}
    job_id = await conductor.register_job(intent)
    assert job_id == "JOB-001"

    # 2. Check Initial Status
    status_data = await conductor.get_job_status(job_id)
    assert status_data["status"] == "INTENT_GENERATED"
    assert len(status_data["history"]) == 1

    # 3. Update Status
    success = await conductor.update_job_status(job_id, "PROCESSING", "Started processing")
    assert success is True

    # 4. Check Updated Status
    status_data = await conductor.get_job_status(job_id)
    assert status_data["status"] == "PROCESSING"
    assert len(status_data["history"]) == 2
    assert status_data["history"][-1]["note"] == "Started processing"

@pytest.mark.asyncio
async def test_job_registry_concurrency():
    # Test concurrent updates to ensure lock works
    job_id = await conductor.register_job({"id": "JOB-CONCURRENT"})

    async def update_task(i):
        await conductor.update_job_status(job_id, f"STEP_{i}")

    await asyncio.gather(*(update_task(i) for i in range(10)))

    status_data = await conductor.get_job_status(job_id)
    # The final status is indeterminate, but history length should be 1 (init) + 10 (updates) = 11
    assert len(status_data["history"]) == 11
