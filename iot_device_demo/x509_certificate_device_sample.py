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
使用x509证书进行认证例子
"""
import time
import logging

from iot_device_sdk_python.client.client_conf import ClientConf
from iot_device_sdk_python.client.connect_auth_info import ConnectAuthInfo
from iot_device_sdk_python.client.listener.default_publish_action_listener import DefaultPublishActionListener
from iot_device_sdk_python.client.request.device_message import DeviceMessage
from iot_device_sdk_python.iot_device import IotDevice


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(threadName)s - %(filename)s[%(funcName)s] - %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def run():
    # 替换为真正的接入地址、device id、证书、和key
    server_uri = "access address"
    port = 8883
    device_id = "your device id"
    iot_ca_cert_path = "./resources/GlobalSignRSAOVSSLCA2018.crt.pem"
    cert_path = "x509证书的pem"
    key_path = "x509证书的key"

    connect_auth_info = ConnectAuthInfo()
    connect_auth_info.server_uri = server_uri
    connect_auth_info.port = port
    connect_auth_info.id = device_id
    connect_auth_info.auth_type = ConnectAuthInfo.X509_AUTH
    connect_auth_info.cert_path = cert_path
    connect_auth_info.key_path = key_path
    connect_auth_info.iot_cert_path = iot_ca_cert_path
    connect_auth_info.bs_mode = ConnectAuthInfo.BS_MODE_DIRECT_CONNECT

    client_conf = ClientConf(connect_auth_info)

    device = IotDevice(client_conf)

    if device.connect() != 0:
        logger.error("init failed")
        return

    logger.info("begin report message")
    default_publish_listener = DefaultPublishActionListener()
    device_message = DeviceMessage()
    device_message.content = "Hello Huawei"
    # 定时上报消息
    while True:
        device.get_client().report_device_message(device_message,
                                                  default_publish_listener)
        time.sleep(5)


if __name__ == "__main__":
    run()
