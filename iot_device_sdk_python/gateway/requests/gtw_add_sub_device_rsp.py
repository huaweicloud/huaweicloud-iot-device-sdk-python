# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from typing import List

from iot_device_sdk_python.gateway.requests.added_sub_device_info_rsp import AddedSubDeviceInfoRsp
from iot_device_sdk_python.gateway.requests.add_sub_device_failed_reason import AddSubDeviceFailedReason


class GtwAddSubDeviceRsp:
    def __init__(self):
        self._successful_devices: List[AddedSubDeviceInfoRsp] = []
        self._add_sub_device_failed_reasons: List[AddSubDeviceFailedReason] = []

    @property
    def successful_devices(self):
        return self._successful_devices

    @successful_devices.setter
    def successful_devices(self, value):
        self._successful_devices = value

    @property
    def add_sub_device_failed_reasons(self):
        return self._add_sub_device_failed_reasons

    @add_sub_device_failed_reasons.setter
    def add_sub_device_failed_reasons(self, value):
        self._add_sub_device_failed_reasons = value

    def to_dict(self):
        return {"successful_devices": self._successful_devices,
                "failed_devices": self._add_sub_device_failed_reasons}













