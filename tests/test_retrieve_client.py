"""Test functions for the retrieve api"""
import pytest
from fastapi import HTTPException
from app.clients.service.retrieve import retrieve_client, check_valid_input, search_clients
from app.clients.service.update_model import ClientUpdateModel

# Retrieve Client Tests
@pytest.mark.asyncio
async def test_retrieve_client_success():
    """Test successful retrieval of a client."""
    client_id = "123"

    result = await retrieve_client(client_id)

    # Assertions
    assert isinstance(result, dict)
    assert "client_id" in result
    assert result["client_id"] == int(client_id)

# Retrieve Client Tests
@pytest.mark.asyncio
async def test_search_client_success():
    """Test successful retrieval of a client."""
    client_data = ClientUpdateModel(
        age=30,
        housing="None"
    )

    with pytest.raises(HTTPException) as excinfo:
        await search_clients(client_data)

    # Assertions
    assert excinfo.value.status_code == 404

@pytest.mark.asyncio
async def test_retrieve_client_not_found():
    """Test retrieval of a non-existent client."""
    client_id = "999999"  # An ID that should not exist in the database

    with pytest.raises(HTTPException) as excinfo:
        await retrieve_client(client_id)

    # Assertions
    assert excinfo.value.status_code == 404
    assert f"Client with ID {client_id} not found" in excinfo.value.detail

@pytest.mark.asyncio
async def test_retrieve_client_invalid_id():
    """Test retrieval with an invalid client ID format."""
    invalid_client_ids = ["abc", "12.3", "-45", ""]

    for client_id in invalid_client_ids:
        with pytest.raises(HTTPException) as excinfo:
            check_valid_input(client_id)

        # Assertions
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "Invalid client_id format."
