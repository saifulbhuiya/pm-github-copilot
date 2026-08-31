import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_endpoint():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from API"}


def test_get_board_endpoint():
    response = client.get("/api/boards/user")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "cards" in data
    assert len(data["columns"]) == 5


def test_card_crud_lifecycle():
    # 1. Create a card
    create_res = client.post(
        "/api/cards",
        json={"column_id": 1, "title": "Test Integration Card", "details": "Integration details"}
    )
    assert create_res.status_code == 200
    card_data = create_res.json()
    card_id = int(card_data["id"])
    assert card_data["title"] == "Test Integration Card"

    # 2. Move the card to column 2
    move_res = client.put(f"/api/cards/{card_id}", json={"column_id": 2, "position": 0})
    assert move_res.status_code == 200
    assert move_res.json() == {"success": True}

    # 3. Delete the card
    del_res = client.delete(f"/api/cards/{card_id}")
    assert del_res.status_code == 200
    assert del_res.json() == {"success": True}


def test_rename_column_endpoint():
    res = client.put("/api/columns/1", json={"title": "Backlog Updated"})
    assert res.status_code == 200
    assert res.json() == {"success": True}

    # Revert title
    revert_res = client.put("/api/columns/1", json={"title": "Backlog"})
    assert revert_res.status_code == 200


def test_ai_chat_endpoint():
    response = client.post("/api/ai/chat", json={"message": "create test task in Backlog"})
    assert response.status_code == 200
    data = response.json()
    assert "action" in data
    assert "summary" in data
