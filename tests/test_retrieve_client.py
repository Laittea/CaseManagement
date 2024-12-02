"""Test functions for the retrieve API"""
import pytest
from fastapi import HTTPException
from app.clients.service.retrieve import retrieve_client

# Mock database for testing
database = {
    "123": {"name": "John Doe", "email": "john@example.com"},
    "456": {"name": "Jane Smith", "email": "jane@example.com"}
}

@pytest.mark.asyncio
async def test_retrieve_client_success():
    """
    Test successful retrieval of a client.
    """
    client_id = "123"  # Ensure this ID exists in the mock database
    result = await retrieve_client(client_id)

    # Assertions
    assert result["success"] is True
    assert result["data"] == {"name": "John Doe", "email": "john@example.com"}

@pytest.mark.asyncio
async def test_retrieve_client_not_found():
    """
    Test retrieval when the client is not found in the database.
    """
    client_id = "999"  # Ensure this ID does not exist in the mock database
    with pytest.raises(HTTPException) as excinfo:
        await retrieve_client(client_id)

    # Assertions
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == f"Client with ID {client_id} not found"

@pytest.mark.asyncio
async def test_retrieve_client_invalid_id():
    """
    Test retrieval with an invalid client_id format.
    """
    client_id = ""  # Simulate an invalid ID
    with pytest.raises(HTTPException) as excinfo:
        await retrieve_client(client_id)

    # Assertions
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid client_id format."
