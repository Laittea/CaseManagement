"""Test functions for the update API"""
import pytest
from fastapi import HTTPException
from app.clients.service.update import update_client

@pytest.mark.asyncio
async def test_update_client_success():
    """Test successful update of a client."""
    client_id = "61"
    update_data = {
        "age": 32,
        "work_experience": 7,
        "canada_workex": 3,
        "level_of_schooling": "Master's degree",
        "fluent_english": "Yes",
        "currently_employed": "Yes",
        "housing": "Homeowner"
    }
    result = await update_client(client_id, update_data)

    # Assertions
    assert result["success"] is True
    assert result["message"] == f"Client {client_id} successfully updated"
    assert result["client_id"] == client_id

@pytest.mark.asyncio
async def test_update_client_not_found():
    """Test update when the client is not found in the database."""
    client_id = "250"
    update_data = {
        "age": 45
    }
    with pytest.raises(HTTPException) as excinfo:
        await update_client(client_id, update_data)

    # Assertions
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Client with ID {client_id} not found"

@pytest.mark.asyncio
async def test_update_client_invalid_id():
    """Test update with an invalid client_id."""
    client_id = "invalid_id"
    update_data = {
        "age": 29
    }
    with pytest.raises(HTTPException) as excinfo:
        await update_client(client_id, update_data)

    # Assertions
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid client_id format."