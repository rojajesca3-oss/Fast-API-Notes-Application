import pytest

@pytest.mark.asyncio
async def test_create_note(async_client):
    response = await async_client.post(
        "/api/v1/notes/",
        json={"title": "Test Note", "content": "This is comprehensive content."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is comprehensive content."
    assert "id" in data

@pytest.mark.asyncio
async def test_get_note_by_id(async_client):
    # Setup - Create note first
    create_res = await async_client.post(
        "/api/v1/notes/",
        json={"title": "Find Me", "content": "Lookup criteria content."}
    )
    note_id = create_res.json()["id"]

    # Action
    response = await async_client.get(f"/api/v1/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"

@pytest.mark.asyncio
async def test_note_not_found(async_client):
    response = await async_client.get("/api/v1/notes/non-existent-uuid")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_note(async_client):
    create_res = await async_client.post(
        "/api/v1/notes/",
        json={"title": "Delete Me", "content": "Will be expunged."}
    )
    note_id = create_res.json()["id"]

    delete_res = await async_client.delete(f"/api/v1/notes/{note_id}")
    assert delete_res.status_code == 204

    get_res = await async_client.get(f"/api/v1/notes/{note_id}")
    assert get_res.status_code == 404