# -*- encoding: utf-8 -*-

# Copyright (c) 2023-2024 Huawei Cloud Computing Technology Co., Ltd. All rights reserved.
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
演示MQTT 注册组秘钥方式发放（设备自注册场景）
"""

from __future__ import absolute_import
import logging
import time

from iot_device_sdk_python.client.client_conf import ClientConf
from iot_device_sdk_python.client.connect_auth_info import ConnectAuthInfo
from iot_device_sdk_python.client.request.device_message import DeviceMessage
from iot_device_sdk_python.iot_device import IotDevice


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(threadName)s - %(filename)s[%(funcName)s] - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def run():
    server_uri = "iot-bs.cn-north-4.myhuaweicloud.com"
    port = 8883
    # device_id可以自己随意命名，用一个唯一标识设备身份的ID
    device_id = "your device id"
    iot_cert_file_path = "iot cert path"
    bs_cert_path = "bs cert path"
    # 注册组秘钥
    secret = "scope secret"
    scope_id = "scopeId"

    connect_auth_info = ConnectAuthInfo()
    connect_auth_info.server_uri = server_uri
    connect_auth_info.secret = secret
    connect_auth_info.port = port
    connect_auth_info.id = device_id
    connect_auth_info.scope_id = scope_id
    connect_auth_info.bs_cert_path = bs_cert_path
    connect_auth_info.iot_cert_path = iot_cert_file_path
    connect_auth_info.auth_type = ConnectAuthInfo.SECRET_AUTH
    connect_auth_info.bs_mode = ConnectAuthInfo.BS_MODE_BOOTSTRAP_WITH_SCOPEID
    connect_auth_info.bs_message = "{\"baseStrategyKeyword\":\"1111\"}"

    client_conf = ClientConf(connect_auth_info)

    device = IotDevice(client_conf)
    if device.connect() != 0:
        logger.error("init failed")
        return
    logger.info("begin report message")
    device_message = DeviceMessage()
    device_message.content = "Hello Huawei"
    # 定时上报消息
    while True:
        device.get_client().report_device_message(device_message)
        time.sleep(10)


if __name__ == "__main__":
    run()
