"""Test functions for the create api"""
import pytest
from fastapi import HTTPException
from app.clients.service.create import create_client
from app.clients.service.update_model import ClientUpdateModel

# Create Client Tests
@pytest.mark.asyncio
async def test_create_client_success():
    """Test successful client creation."""
    client_data = ClientUpdateModel(
        age=30,
        gender="Male",
        work_experience=5,
        canada_workex=3,
        fluent_english="Yes",
        level_of_schooling="Bachelor's",
        currently_employed="Yes"
    )

    result = await create_client(client_data)

    # Assertions
    assert result["success"] is True
    assert "Client successfully created with ID" in result["message"]
    assert "client_id" in result

@pytest.mark.asyncio
async def test_create_client_missing_required_fields():
    """Test client creation with insufficient data."""
    # Create a client model with minimal or missing required fields
    client_data = ClientUpdateModel()

    with pytest.raises(HTTPException) as excinfo:
        await create_client(client_data)

    # Assertions
    assert excinfo.value.status_code == 500
