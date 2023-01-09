# -*- encoding: utf-8 -*-


class ScanSubDeviceNotify:
    """
    扫描子设备通知（暂未使用）
    """
    def __init__(self):
        self._protocol: str = ""
        self._channel: str = ""
        self._parent: str = ""
        self._settings = None

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value














