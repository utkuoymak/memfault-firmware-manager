import functools
import logging

from flask import request

from firmware_manager.common.firmware_helper import get_member_or_device


def is_valid(api_key):
    caller = get_member_or_device(api_key)
    return True if caller else False


def key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Get API key from request
        logging.info(f"Checking API key for request {request}")
        if request.headers.get("api_key"):
            api_key = request.headers.get("api_key")
        else:
            return {"message": "No API key provided in headers"}, 403

        # Check if API key is correct and valid
        if is_valid(api_key):
            logging.info("API key is valid")
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403

    return decorator
