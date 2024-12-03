"""
This module contains tests for the client update functionality in the FastAPI application.
"""

from unittest.mock import AsyncMock
from datetime import date, datetime
from bson import ObjectId
from fastapi import HTTPException
import pytest
from app.clients.schema import ClientUpdate
from app.clients.router import update_client
from app.database import clients_collection


@pytest.mark.asyncio
async def test_update_client():
    """
    Test the update_client function to ensure it correctly updates a client's information.
    """
    # Prepare test data
    original_client_id = str(ObjectId())
    original_client_data = {
        "_id": ObjectId(original_client_id),
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "date_of_birth": date(1990, 1, 1),
        "address": "123 Main St",
        "phone": "123-456-7890"
    }

    # Prepare update data
    client_update = ClientUpdate(
        first_name="Jane",
        last_name="Doee",
        email="jane.doee@example.com",
        date_of_birth=datetime.combine(date(1991, 2, 2), datetime.min.time()),
        address="456 Elm St",
        phone="098-765-4321"
    )

    clients_collection.find_one = AsyncMock(return_value=original_client_data)
    clients_collection.update_one = AsyncMock()

    # Call the update method
    updated_client = await update_client(original_client_id, client_update)

    # Update the mock to return the updated data
    updated_client_data = original_client_data.copy()
    updated_client_data.update(client_update.dict())
    updated_client_data["_id"] = ObjectId(original_client_id) # Restore the original _id

    clients_collection.find_one = AsyncMock(return_value=updated_client_data)

    # Call the update method again to get the updated client
    updated_client = await update_client(original_client_id, client_update)

    # Assertions
    assert updated_client["first_name"] == "Jane"
    assert updated_client["last_name"] == "Doee"
    assert updated_client["email"] == "jane.doee@example.com"
    assert updated_client["date_of_birth"] == datetime(1991, 2, 2).date()
    assert updated_client["address"] == "456 Elm St"
    assert updated_client["phone"] == "098-765-4321"

@pytest.mark.asyncio
async def test_update_client_not_found():
    """
    Test the update_client function to ensure it raises an HTTPException 
    when the client is not found.
    """
    # Prepare test data
    non_existent_client_id = str(ObjectId())

    # Mock the find_one method to return None
    clients_collection.find_one = AsyncMock(return_value=None)

    # Prepare update data
    client_update = ClientUpdate(
        first_name="John Updated",
        last_name="Doe"
    )

    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await update_client(non_existent_client_id, client_update)

    # Additional assertion on the exception
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Client not found"
