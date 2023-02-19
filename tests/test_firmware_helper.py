from datetime import datetime
from unittest.mock import patch

from firmware_manager.common.firmware_helper import (
    get_all_events_for_device,
    upload_new_firmware_event,
)
from firmware_manager.db.models import Devices, FirmwareEvents

MOCK_FIRMWARE_LIST = [
    {
        "device_id": 3,
        "firmware": "1.0.1",
        "id": "510c6f50-406d-4e9c-abc4-ee69ad523014",
        "project_id": 2,
        "status": "updated",
        "timestamp": "2023-01-01T00:00:00.000000Z",
    },
    {
        "device_id": 3,
        "firmware": "1.0.2",
        "id": "579d9f43-78c7-4d96-bc2a-ec7ecc476213",
        "project_id": 2,
        "status": "updated",
        "timestamp": "2023-01-01T00:00:00.000000Z",
    },
]


def mock_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_caller():
    return Devices(id=3, project_id=2)


@patch(
    "firmware_manager.common.firmware_helper.FirmwareEvents.get_all_for_device",
    return_value=MOCK_FIRMWARE_LIST,
)
def test_get_firmware_for_device(get_all_for_device):
    result = get_all_events_for_device(3, get_caller())
    assert result == MOCK_FIRMWARE_LIST


@patch(
    "firmware_manager.common.firmware_helper.FirmwareEvents.get_all_for_device",
    return_value=[],
)
def test_get_firmware_for_device_no_events(get_all_for_device):
    result = get_all_events_for_device(3, get_caller())
    assert result is None


def test_get_firmware_for_device_no_caller():
    result = get_all_events_for_device(3, None)
    assert result is None


@patch("firmware_manager.common.firmware_helper.FirmwareEvents.save", return_value=True)
def test_upload_new_firmware_event(save):
    now = datetime.now()
    result = upload_new_firmware_event(
        firmware="1.0.0", device=get_caller(), timestamp=now, status="updated"
    )
    assert isinstance(result, FirmwareEvents)
    assert result.timestamp == now
    assert result.status == "updated"
    assert result.firmware == "1.0.0"


@patch("firmware_manager.common.firmware_helper.FirmwareEvents.save", return_value=True)
def test_upload_new_firmware_event_wrong_semver(save):
    now = datetime.now()
    result = upload_new_firmware_event(
        firmware="wrong_semver", device=get_caller(), timestamp=now, status="updated"
    )
    assert result is None
