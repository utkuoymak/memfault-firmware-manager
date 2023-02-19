import logging
import uuid
from datetime import datetime
from marshmallow import Schema, fields

from .database import db


class Member(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    keys = db.relationship("MembershipApiKey", back_populates="owner")

    @classmethod
    def find_by_api_key(cls, api_key):
        return (
            cls.query.join(MembershipApiKey)
            .filter(MembershipApiKey.secret_key == api_key)
            .first()
        )


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    members = db.relationship("Member", backref="project")
    firmware_events = db.relationship("FirmwareEvents")


class MembershipApiKey(db.Model):
    __tablename__ = "membership_api_keys"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secret_key = db.Column(db.String, unique=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("memberships.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    owner = db.relationship("Member", back_populates="keys")


class Devices(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    current_firmware = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    project = db.relationship("Project", backref="devices")
    keys = db.relationship("DeviceApiKeys", back_populates="device")
    firmware_events = db.relationship("FirmwareEvents", backref="device")

    @classmethod
    def find_by_api_key(cls, api_key):
        return (
            cls.query.join(DeviceApiKeys)
            .filter(DeviceApiKeys.secret_key == api_key)
            .first()
        )


class DeviceApiKeys(db.Model):
    __tablename__ = "device_api_keys"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secret_key = db.Column(db.String, unique=True, index=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    device = db.relationship("Devices")


class FirmwareEvents(db.Model):
    __tablename__ = "firmware_events"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    firmware = db.Column(db.String, index=True)
    status = db.Column(db.String, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": str(self.id),
            "device_id": self.device_id,
            "firmware": self.firmware,
            "status": self.status,
            "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            if isinstance(self.timestamp, datetime)
            else self.timestamp,
            "project_id": self.project_id,
        }

    @classmethod
    def get_all_for_device(cls, device_id: int, project_id: int = None):
        """
        Get all firmware events for a given device. If project_id is provided,
        only return firmware events for that project.

        :param device_id: int
        :param project_id: int
        :return: List of FirmwareEvents
        """
        if project_id:
            return cls.query.filter_by(device_id=device_id, project_id=project_id).all()
        return cls.query.filter_by(device_id=device_id).all()


class FirmwarePostSchema(Schema):
    firmware = fields.String(required=True)
    timestamp = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ")
    status = fields.String(required=True)
