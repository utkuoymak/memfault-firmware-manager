import logging

from flask import request, jsonify
from flask_restful import Resource, abort
from marshmallow import ValidationError

from firmware_manager.common.auth import key_required
from firmware_manager.common.firmware_helper import (
    get_member_or_device,
    get_all_events_for_device,
    upload_new_firmware_event,
)
from firmware_manager.db.models import Devices, FirmwarePostSchema

logging.getLogger().setLevel(logging.INFO)


class Firmware(Resource):
    @key_required
    def get(self, device_id):
        logging.info("Getting firmware for device: %s", device_id)
        api_key = request.headers.get("api_key")

        caller = get_member_or_device(api_key)
        firmware_events = get_all_events_for_device(device_id, caller)
        if not firmware_events:
            return {"message": "No firmware events found"}, 404

        return jsonify([event.to_dict() for event in firmware_events])

    @key_required
    def post(self, device_id):
        logging.info("Uploading a new firmware even for device: %s", device_id)
        api_key = request.headers.get("api_key")

        caller = get_member_or_device(api_key)
        if not isinstance(caller, Devices):
            abort(403, message="Only devices can upload firmware events")

        if int(device_id) != caller.id:
            abort(403, message="Devices can only upload firmware events for themselves")

        request_data = request.json
        schema = FirmwarePostSchema()
        try:
            # Validate request body against schema data types
            body = schema.load(request_data)
            logging.info("Request body validated %s", body)
        except ValidationError as err:
            # Return message if validation fails
            return err.messages, 400

        new_event = upload_new_firmware_event(
            body["firmware"], caller, body["timestamp"], body["status"]
        )

        if not new_event:
            return {"message": "Could not upload firmware event"}, 500

        return {"message": "Firmware event uploaded successfully"}, 201
