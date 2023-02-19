from unittest.mock import patch

import pytest

from firmware_manager.app import create_app
from firmware_manager.db.models import FirmwareEvents
from tests.test_firmware_helper import get_caller, MOCK_FIRMWARE_LIST


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            with patch("firmware_manager.db.database.db", return_value=True):
                yield client


def test_get_firmware_no_api_key(client):
    response = client.get("/firmware/1")
    assert response.status_code == 403


@patch(
    "firmware_manager.resources.firmware.get_member_or_device",
    return_value=get_caller(),
)
@patch(
    "firmware_manager.resources.firmware.get_all_events_for_device",
    return_value=[FirmwareEvents(**event) for event in MOCK_FIRMWARE_LIST],
)
def test_get_firmware(get_all_events_for_device, get_member_or_device, client):
    with patch("firmware_manager.common.auth.is_valid", return_value=True):
        # Add 'api_key' to headers and make request
        response = client.get("/firmware/1", headers={"api_key": "test"})
    assert response.status_code == 200
    assert response.json == MOCK_FIRMWARE_LIST
