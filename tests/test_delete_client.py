"""Test functions for the delete api"""
import pytest
from fastapi import HTTPException
from app.clients.service.delete import delete_client
from app.clients.service.create import create_client
from app.clients.service.update_model import ClientUpdateModel

@pytest.mark.asyncio
async def test_delete_client_success():
    """
    Test successful deletion of a client.
    """

    client_data = ClientUpdateModel(
        age=23,
        gender="Female",
        work_experience=2,
        canada_workex=5,
    )
    result = await create_client(client_data)
    client_id = str(result['client_id'])

    # Delete the client created before
    result = await delete_client(client_id)

    # Assertions
    assert result["success"] is True
    assert result["message"] == f"Client {client_id} successfully deleted"
    assert result["client_id"] == client_id

@pytest.mark.asyncio
async def test_delete_client_not_found():
    """
    Test deletion when the client is not found in the database.
    """

    client_id = "250"
    with pytest.raises(HTTPException) as excinfo:
        await delete_client(client_id)

    # Assertions
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == f"Client with ID {client_id} not found"

@pytest.mark.asyncio
async def test_delete_client_invalid_id():
    """
    Test deletion with an invalid client_id.
    """
    client_id = "invalid_id"
    with pytest.raises(HTTPException) as excinfo:
        await delete_client(client_id)

    # Assertions
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Invalid client_id format."
