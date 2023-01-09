# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from typing import List

from iot_device_sdk_python.client.request.service_property import ServiceProperty


class DeviceProperty:
    """
    设备属性
    """
    def __init__(self):
        self._device_id: str = ""
        self._services: List[ServiceProperty] = []

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def services(self):
        return self._services

    @services.setter
    def services(self, value):
        self._services = value

    def to_dict(self):
        service_list = list()
        for service in self._services:
            service_list.append(service.to_dict())
        return {"device_id": self._device_id, "services": service_list}


