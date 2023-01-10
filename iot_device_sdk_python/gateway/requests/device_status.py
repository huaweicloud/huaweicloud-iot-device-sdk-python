# -*- encoding: utf-8 -*-


class DeviceStatus:
    def __init__(self):
        self._device_id: str = ""
        self._status: str = ""

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def to_dict(self):
        return {"device_id": self._device_id, "status": self._status}

    def convert_from_dict(self, json_dict: dict):
        json_name = ["device_id", "status"]
        for key in json_dict.keys():
            if key not in json_name:
                continue
            if key == "device_id":
                self.device_id = json_dict.get(key)
            elif key == "status":
                self.status = json_dict.get(key)
            else:
                pass







