"""TDD Red: Tests for player name feature (all should fail initially)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestPlayerNameInput:
    """Start screen must have a player name input field."""

    def test_start_screen_has_name_input(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert 'name="player_name"' in response.text

    def test_start_screen_input_has_placeholder(self, client: TestClient):
        response = client.get("/")
        assert "placeholder" in response.text
        # Should have some hint about entering a name
        assert "name" in response.text.lower()


class TestPlayerNamePersistsOnBoard:
    """Player name submitted at /start must appear on the game board."""

    def test_start_with_name_shows_name_on_board(self, client: TestClient):
        client.get("/")
        response = client.post("/start", data={"player_name": "Alice"})
        assert response.status_code == 200
        assert "Alice" in response.text

    def test_start_with_different_name_shows_that_name(self, client: TestClient):
        client.get("/")
        response = client.post("/start", data={"player_name": "Bob"})
        assert response.status_code == 200
        assert "Bob" in response.text

    def test_name_persists_after_toggle(self, client: TestClient):
        client.get("/")
        client.post("/start", data={"player_name": "Carol"})
        response = client.post("/toggle/0")
        assert response.status_code == 200
        assert "Carol" in response.text

    def test_name_persists_after_dismiss_modal(self, client: TestClient):
        client.get("/")
        client.post("/start", data={"player_name": "Dave"})
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "Dave" in response.text


class TestPlayerNameEdgeCases:
    """Edge cases for player name handling."""

    def test_start_without_name_still_works(self, client: TestClient):
        """Submitting no name should not crash — board still renders."""
        client.get("/")
        response = client.post("/start", data={})
        assert response.status_code == 200
        assert "FREE" in response.text

    def test_start_with_empty_name_still_works(self, client: TestClient):
        client.get("/")
        response = client.post("/start", data={"player_name": ""})
        assert response.status_code == 200
        assert "FREE" in response.text

    def test_name_resets_after_reset_game(self, client: TestClient):
        """After reset, the start screen shows the name input again."""
        client.get("/")
        client.post("/start", data={"player_name": "Eve"})
        response = client.post("/reset")
        assert response.status_code == 200
        # Start screen is returned — should have the name input field again
        assert 'name="player_name"' in response.text
