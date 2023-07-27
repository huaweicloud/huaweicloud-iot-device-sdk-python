# -*- encoding: utf-8 -*-

# Copyright (c) 2020-2022 Huawei Cloud Computing Technology Co., Ltd. All rights reserved.
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

"""
演示如何直接使用DeviceClient获取影子数据
"""

from typing import List
import time
import uuid
import logging

from iot_device_sdk_python.client.client_conf import ClientConf
from iot_device_sdk_python.client.connect_auth_info import ConnectAuthInfo
from iot_device_sdk_python.client.listener.device_shadow_listener import DeviceShadowListener
from iot_device_sdk_python.client.request.shadow_data import ShadowData
from iot_device_sdk_python.iot_device import IotDevice


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(threadName)s - %(filename)s[%(funcName)s] - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DeviceShadowSampleListener(DeviceShadowListener):
    """
    实现影子数据下发监听器的一个例子
    """
    def on_shadow_get(self, request_id: str, object_device_id: str, shadow: List[ShadowData]):
        """
        处理平台下发的设备影子数据
        :param request_id:  请求id
        :param object_device_id:    设备id
        :param shadow:     dict
        """
        logger.info("on_shadow_get request_id: " + request_id)
        logger.info("on_shadow_get device_id: " + object_device_id)
        print("shadow service_id: " + shadow[0].service_id)
        print("shadow desired properties: " + str(shadow[0].desired.properties))
        print("shadow reported properties: " + str(shadow[0].reported.properties))


def run():
    # 替换为真正的接入地址、device id和密钥，参考readme_CN.md中“上传产品模型并注册设备”
    server_uri = "access address"
    port = 8883
    device_id = "your device id"
    secret = "your device secret"
    iot_ca_cert_path = "./resources/GlobalSignRSAOVSSLCA2018.crt.pem"

    connect_auth_info = ConnectAuthInfo()
    connect_auth_info.server_uri = server_uri
    connect_auth_info.port = port
    connect_auth_info.id = device_id
    connect_auth_info.secret = secret
    connect_auth_info.iot_cert_path = iot_ca_cert_path
    connect_auth_info.bs_mode = ConnectAuthInfo.BS_MODE_DIRECT_CONNECT

    client_conf = ClientConf(connect_auth_info)

    device = IotDevice(client_conf)

    # 接收平台下行响应
    device.get_client().set_device_shadow_listener(DeviceShadowSampleListener())

    if device.connect() != 0:
        logger.error("init failed")
        return

    logger.info("begin get shadow")
    # 设备侧获取平台的设备影子数据
    request_id = str(uuid.uuid1())
    device.get_client().get_device_shadow(request_id, "smokeDetector")
    while True:
        time.sleep(5)


if __name__ == "__main__":
    run()
