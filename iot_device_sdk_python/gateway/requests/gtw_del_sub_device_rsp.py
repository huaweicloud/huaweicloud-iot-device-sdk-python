# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from typing import List

from iot_device_sdk_python.gateway.requests.del_sub_device_failed_reason import DelSubDeviceFailedReason


class GtwDelSubDeviceRsp:
    def __init__(self):
        self._successful_devices: List[str] = []
        self._failed_devices: List[DelSubDeviceFailedReason] = []

    @property
    def successful_devices(self):
        return self._successful_devices

    @successful_devices.setter
    def successful_devices(self, value):
        self._successful_devices = value

    @property
    def failed_devices(self):
        return self._failed_devices

    @failed_devices.setter
    def failed_devices(self, value):
        self._failed_devices = value

    def to_dict(self):
        return {"successful_devices": self._successful_devices,
                "failed_devices": self._failed_devices}















