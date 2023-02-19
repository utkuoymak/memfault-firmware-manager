import logging
from datetime import datetime
from typing import Union

import semver

from firmware_manager.db.models import Devices, Member, FirmwareEvents


def get_member_or_device(api_key: str):
    """
    Figure out if the API key belongs to a member or a device
    :param api_key: API key
    :return: Member or device
    """
    device = Devices.find_by_api_key(api_key)
    if device is None:
        return Member.find_by_api_key(api_key)
    return device


def get_all_events_for_device(device_id: int, caller: Union[Member, Devices]):
    """
    Get all firmware events for a device
    :param caller: Caller member or device
    :param device_id: Device ID
    :return: List of firmware events
    """
    if not caller:
        logging.info("No caller present")
        return None
    events = FirmwareEvents.get_all_for_device(device_id, caller.project_id)
    if not events:
        logging.info(
            "No firmware events found for device %s, or caller doesnt have permissions for the project",
            device_id,
        )
        return None

    return events


def upload_new_firmware_event(
    firmware: str,
    device: Devices,
    timestamp: datetime = datetime.now(),
    status: str = "updated",
):
    """
    Upload a new firmware event
    :param status: status of the firmware event
    :param timestamp: timestamp from the request if exists
    :param firmware: Firmware version
    :param device: Device
    :return: Firmware event
    """

    try:
        semver.VersionInfo.parse(firmware)
    except ValueError:
        logging.error(
            "Could not parse firmware version %s. Not semver compliant", firmware
        )
        return None

    new_event = FirmwareEvents(
        device=device,
        firmware=firmware,
        status=status,
        timestamp=timestamp,
        project_id=device.project_id,
    )
    new_event.save()
    logging.info(f"Created new firmware event {new_event.id}")

    return new_event
