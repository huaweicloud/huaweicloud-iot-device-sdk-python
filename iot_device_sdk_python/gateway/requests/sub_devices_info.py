# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from typing import List

from iot_device_sdk_python.gateway.requests.device_info import DeviceInfo


class SubDevicesInfo:
    """
    子设备信息
    """
    def __init__(self):
        self._devices: List[DeviceInfo] = []
        self._version: int = 0

    @property
    def devices(self):
        return self._devices

    @devices.setter
    def devices(self, value):
        self._devices = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value















