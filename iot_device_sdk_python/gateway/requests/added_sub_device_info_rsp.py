# -*- encoding: utf-8 -*-


class AddedSubDeviceInfoRsp:
    def __init__(self):
        self._parent_device_id: str = ""
        self._node_id: str = ""
        self._device_id: str = ""
        self._name: str = ""
        self._description: str = ""
        self._manufacturer_id: str = ""
        self._model: str = ""
        self._product_id: str = ""
        self._fw_version: str = ""
        self._sw_version: str = ""
        self._status: str = ""
        self._extension_info: str = ""

    @property
    def parent_device_id(self):
        return self._parent_device_id

    @parent_device_id.setter
    def parent_device_id(self, value):
        self._parent_device_id = value

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        self._node_id = value

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def manufacturer_id(self):
        return self._manufacturer_id

    @manufacturer_id.setter
    def manufacturer_id(self, value):
        self._manufacturer_id = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def fw_version(self):
        return self._fw_version

    @fw_version.setter
    def fw_version(self, value):
        self._fw_version = value

    @property
    def sw_version(self):
        return self._sw_version

    @sw_version.setter
    def sw_version(self, value):
        self._sw_version = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def extension_info(self):
        return self._extension_info

    @extension_info.setter
    def extension_info(self, value):
        self._extension_info = value

    def to_dict(self):
        return {"parent_device_id": self._parent_device_id,
                "node_id": self._node_id,
                "device_id": self._device_id,
                "name": self._name,
                "description": self._description,
                "manufacturer_id": self._manufacturer_id,
                "model": self._model,
                "product_id": self._product_id,
                "fw_version": self._fw_version,
                "sw_version": self._sw_version,
                "status": self._status,
                "extension_info": self._extension_info}

    def convert_from_dict(self, json_dict: dict):
        json_name = ["parent_device_id", "node_id", "device_id", "name", "description", "manufacturer_id",
                     "model", "product_id", "fw_version", "sw_version", "status", "extension_info"]
        for key in json_dict.keys():
            if key not in json_name:
                continue
            if key == "parent_device_id":
                self.parent_device_id = json_dict.get(key)
            elif key == "node_id":
                self.node_id = json_dict.get(key)
            elif key == "device_id":
                self.device_id = json_dict.get(key)
            elif key == "name":
                self.name = json_dict.get(key)
            elif key == "description":
                self.description = json_dict.get(key)
            elif key == "product_id":
                self.product_id = json_dict.get(key)
            elif key == "fw_version":
                self.fw_version = json_dict.get(key)
            elif key == "sw_version":
                self.sw_version = json_dict.get(key)
            elif key == "status":
                self.status = json_dict.get(key)
            elif key == "extension_info":
                self.extension_info = json_dict.get(key)
            else:
                pass















