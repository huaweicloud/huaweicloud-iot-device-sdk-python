# -*- encoding: utf-8 -*-

# Copyright (c) 2020-2023 Huawei Cloud Computing Technology Co., Ltd. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from typing import Optional


class OTAPackageInfoV2:
    def __init__(self):
        self._url: str = ""
        self._version: str = ""
        self._expires: Optional[int] = None

    @property
    def url(self):
        """
        软固件包下载地址
        """
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def version(self):
        """
        软固件包版本号
        """
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def expires(self):
        """
        access_token的超期时间
        """
        return self._expires

    @expires.setter
    def expires(self, value):
        self._expires = value

    def to_dict(self):
        return {"url": self._url, "version": self._version, "expires": self._expires}

    def convert_from_dict(self, json_dict: dict):
        json_name = ["url", "version", "expires"]
        for key in json_dict.keys():
            if key not in json_name:
                continue
            if key == "url":
                self.url = json_dict.get(key)
            elif key == "version":
                self.version = json_dict.get(key)
            elif key == "expires":
                self.expires = json_dict.get(key)
            else:
                pass

