# -*-coding:utf-8-*-

from __future__ import absolute_import
from typing import Optional, Dict
import ssl
import threading
import os
import time
import logging
import traceback

import paho.mqtt.client as mqtt

from iot_device_sdk_python.client.connect_auth_info import ConnectAuthInfo
from iot_device_sdk_python.client.mqtt_connect_conf import MqttConnectConf
from iot_device_sdk_python.transport.action_listener import ActionListener
from iot_device_sdk_python.transport.connection import Connection
from iot_device_sdk_python.transport.raw_message import RawMessage
from iot_device_sdk_python.transport.raw_message_listener import RawMessageListener
from iot_device_sdk_python.utils.iot_util import get_client_id, sha256_mac
from iot_device_sdk_python.devicelog.listener.default_conn_log_listener import DefaultConnLogListener
from iot_device_sdk_python.devicelog.listener.default_conn_action_log_listener import DefaultConnActionLogListener


class MqttConnection(Connection):
    """
    mqtt连接
    """
    _logger = logging.getLogger(__name__)
    MQTT_THREAD_NAME = "MqttThread"
    CONNECT_TYPE = "0"

    def __init__(self, connect_auth_info: ConnectAuthInfo, mqtt_connect_conf: MqttConnectConf,
                 raw_msg_listener: RawMessageListener):
        # 配置对象
        self.__connect_auth_info = connect_auth_info
        self.__mqtt_connect_conf = mqtt_connect_conf

        # self._raw_msg_listener是一个DeviceClient实例
        self.__raw_msg_listener = raw_msg_listener

        self.__paho_client: Optional[mqtt.Client] = None

        # connect_result_code仅用在初次建链时返回结果码给DeviceClient
        # connect_result_code在connect()方法和_on_connect()方法中设值
        self.__connect_result_code = -1

        # 发布监听器集合，mid -> listener
        self.__publish_listener_dict: Dict[int, ActionListener] = dict()

        self.__connect_listener: Optional[DefaultConnLogListener] = None
        self.__connect_action_listener: Optional[DefaultConnActionLogListener] = None

    def connect(self):
        try:
            if self.__connect_auth_info.bs_mode == ConnectAuthInfo.BS_MODE_DIRECT_CONNECT or \
                    self.__connect_auth_info.bs_mode == ConnectAuthInfo.BS_MODE_STANDARD_BOOTSTRAP:
                client_id = get_client_id(device_id=self.__connect_auth_info.id,
                                          psw_sig_type=self.__connect_auth_info.check_timestamp)
            else:
                # 自注册方式
                if self.__connect_auth_info.scope_id is not None:
                    client_id = self.__connect_auth_info.id + "_" + self.CONNECT_TYPE + "_" \
                                + self.__connect_auth_info.scope_id
                else:
                    raise ValueError("scope_id is None when bs_mode is BS_MODE_BOOTSTRAP_WITH_SCOPEID")

            try:
                # clean_session设为True，此时代理将在断开连接时删除有关此客户端的所有信息。
                # 如果为False，则客户端是持久客户端，当客户端断开连接时，订阅信息和排队消息将被保留。
                self.__paho_client = mqtt.Client(client_id=client_id, clean_session=True)
            except Exception as e:
                # mqtt_client实例创建失败就直接抛出异常
                raise Exception("create mqtt.Client() failed").with_traceback(
                    e.__traceback__)

            if self.__connect_auth_info.auth_type == ConnectAuthInfo.SECRET_AUTH:
                # 密码加密
                password = sha256_mac(self.__connect_auth_info.secret)
                # 设置用户名和密码
                self.__paho_client.username_pw_set(self.__connect_auth_info.id, password)
            elif self.__connect_auth_info.auth_type == ConnectAuthInfo.X509_AUTH:
                # 使用x509证书接入，不需要密码
                self.__paho_client.username_pw_set(self.__connect_auth_info.id)
            else:
                self._logger.error("invalid auth_type.")
                raise Exception("auth_type is invalid.")

            # 设置断链后自动reconnect的间隔。从1s开始，每重连失败一次翻倍，最大间隔为2min
            self.__paho_client.reconnect_delay_set(min_delay=1, max_delay=120)
            # 设置回调方法: on_connect, on_disconnect, on_publish, on_message
            self._set_callback()

            if self.__connect_auth_info.port == 8883:
                # SSL
                try:
                    self._mqtt_with_ssl_connect_config()
                except Exception as e:
                    # 无法加载用于SSL连接的ca证书就直接抛出异常
                    raise Exception("set ssl connect config failed").with_traceback(
                        e.__traceback__)
            else:
                # port: 1883
                pass

            # 开始建链
            self._logger.info("try to connect to %s:%s", self.__connect_auth_info.server_uri,
                              str(self.__connect_auth_info.port))

            # connect()方法是阻塞的
            # 如果不能访问平台（比如：无法连接到服务器），connect()方法会直接抛出错误；
            rc = self.__paho_client.connect(host=self.__connect_auth_info.server_uri,
                                            port=self.__connect_auth_info.port,
                                            keepalive=self.__mqtt_connect_conf.keep_alive_time)

            if rc == 0:
                # loop_forever()直到客户端调用disconnect()时才会返回，它会自动处理断链重连。
                # loop_forever()的三个参数分别是：timeout, max_packets(Not currently used), retry_first_connection
                threading.Thread(target=self.__paho_client.loop_forever,
                                 args=(self.__mqtt_connect_conf.timeout, 1, False),
                                 name=self.MQTT_THREAD_NAME).start()
            # 默认等待1s，确保有足够时间建链
            time.sleep(1)

            if self.__connect_action_listener is not None and self.is_connected():
                self.__connect_action_listener.on_success(token=rc)
        except Exception as e:
            self._logger.error("MqttConnection connect error, traceback: %s", traceback.format_exc())
            self.__connect_result_code = -1
            if self.__connect_action_listener is not None:
                # 记录建链失败的原因
                self.__connect_action_listener.on_failure(token=-1, err=e)

        # 判断是否已连接到平台
        is_connected = self.__paho_client.is_connected()
        return 0 if is_connected else self.__connect_result_code

    def _mqtt_with_ssl_connect_config(self):
        """
        mqtts连接证书设置，使用8883端口接入时需要执行配置
        """
        if not os.path.isfile(self.__connect_auth_info.iot_cert_path):
            # ca证书不存在，抛出错误
            raise ValueError("ssl certification path error")

        if self.__connect_auth_info.auth_type == ConnectAuthInfo.X509_AUTH:
            if self.__connect_auth_info.cert_path is not None and self.__connect_auth_info.key_path is not None:
                # TODO 当前的paho-mqtt暂不支持传入证书密码key_password
                self.__paho_client.tls_set(ca_certs=self.__connect_auth_info.iot_cert_path,
                                           certfile=self.__connect_auth_info.cert_path,
                                           keyfile=self.__connect_auth_info.key_path,
                                           tls_version=ssl.PROTOCOL_TLSv1_2)
            else:
                raise ValueError("x509 pem or key is None")
        else:
            # ca_certs为ca证书存放路径
            self.__paho_client.tls_set(ca_certs=self.__connect_auth_info.iot_cert_path,
                                       tls_version=ssl.PROTOCOL_TLSv1_2)
        # 设置为True表示不用验证主机名
        self.__paho_client.tls_insecure_set(True)

    def _set_callback(self):
        """
        设置回调方法
        """

        # 当平台响应连接请求时，执行self._on_connect()
        self.__paho_client.on_connect = self._on_connect
        # 当与平台断开连接时，执行self._on_disconnect()
        self.__paho_client.on_disconnect = self._on_disconnect
        # 当成功当成功发布一个消息到平台后，执行self._on_publish()。
        # 对于Qos级别为1和2的消息，这意味着已经完成了与代理的握手。
        # 对于Qos级别为0的消息，这只意味着消息离开了客户端
        self.__paho_client.on_publish = self._on_publish
        # 当接收到一个原始消息时，执行self._on_message()
        self.__paho_client.on_message = self._on_message

    def publish_message(self, raw_message: RawMessage, message_publish_listener: Optional[ActionListener] = None):
        """
        Args:
            raw_message:                 原始数据
            message_publish_listener:    监听器，可以为None
        """
        # rc: return code
        # mid: message id
        try:
            message_info: mqtt.MQTTMessageInfo = self.__paho_client.publish(raw_message.topic, raw_message.payload,
                                                                            raw_message.qos)

            self._logger.info("publish message, rc= %s, mid= %s, topic= %s, msg= %s",
                              str(message_info.rc), str(message_info.mid),
                              raw_message.topic, str(raw_message.payload))

            if message_info.rc != mqtt.MQTT_ERR_SUCCESS:
                if message_publish_listener is not None and isinstance(message_publish_listener, ActionListener):
                    message_publish_listener.on_failure(
                        "publish message failed, rc= %s, mid= %s" % (
                            str(message_info.rc), str(message_info.mid)), None)

            if message_publish_listener is not None and isinstance(message_publish_listener, ActionListener):
                if message_info.mid not in self.__publish_listener_dict.keys():
                    self.__publish_listener_dict[message_info.mid] = message_publish_listener
        except Exception as e:
            self._logger.error("publish message failed, traceback: %s", traceback.format_exc())
            if message_publish_listener is not None and isinstance(message_publish_listener, ActionListener):
                message_publish_listener.on_failure(
                    "publish message failed, qos= %s, topic= %s, msg= %s" % (
                        str(raw_message.qos), raw_message.topic, str(raw_message.payload)), e)

    def close(self):
        """
        关闭连接
        """
        if self.__paho_client.is_connected():
            try:
                self.__paho_client.disconnect()
                self._logger.info("MqttConnection close")
            except Exception as e:
                self._logger.error("_paho_client.disconnect() failed, Exception: %s", str(e))
                self._logger.error("_paho_client.disconnect() failed, traceback: %s", traceback.format_exc())
        else:
            pass

    def is_connected(self):
        if self.__paho_client is None:
            return False
        return self.__paho_client.is_connected()

    def set_connect_listener(self, connect_listener):
        self.__connect_listener = connect_listener

    def set_connect_action_listener(self, connect_action_listener):
        self.__connect_action_listener = connect_action_listener

    def subscribe_topic(self, topic: str, qos: int):
        """
        订阅自定义topic

        Args:
            topic: 自定义的topic
            qos:   qos
        """
        try:
            self.__paho_client.subscribe(topic, qos)
        except Exception as e:
            self._logger.error("subscribe_topic failed, Exception: %s", str(e))
            self._logger.error("subscribe_topic failed, traceback: %s", traceback.format_exc())

    def _on_connect(self, client, userdata, flags, rc):
        """
        当平台响应连接请求时，执行此函数
        :param client:      the client instance for this callback
        :param userdata:    the private user data as set in Client() or userdata_set()
        :param flags:       response flags sent by the broker. a dict
        :param rc:          the connection result
                            The value of rc indicates success or not:
                                0: Connection successful
                                1: Connection refused - incorrect protocol version
                                2: Connection refused - invalid client identifier
                                3: Connection refused - server unavailable
                                4: Connection refused - bad username or password
                                5: Connection refused - not authorised
                                6-255: Currently unused.
        """
        self.__connect_result_code = rc

        if rc == 0:
            self._logger.info("connect success. address: %s", self.__connect_auth_info.server_uri)
            if self.__connect_listener is not None:
                self.__connect_listener.connect_complete(False, self.__connect_auth_info.server_uri)
        else:
            if rc == 4:
                # 只有当用户名或密码错误，才不进行自动重连。
                # 如果这里不使用disconnect()方法，那么loop_forever会一直进行重连。
                self.__paho_client.disconnect()
            self._logger.error("connected with result code %s", str(rc))

    def _on_disconnect(self, client, userdata, rc):
        """
        当与平台断开连接时，执行此函数
        :param client:      the client instance for this callback
        :param userdata:    the private user data as set in Client() or userdata_set()
        :param rc:          the disconnection result.
                            如果是0，那么就是paho_client主动调用disconnect()方法断开连接。
                            如果是其他，那么可能是网络错误。
        """
        if self.__connect_listener is not None:
            self.__connect_listener.connection_lost(str(rc))
        self._logger.error("disconnected with result code %s", str(rc))

    def _on_publish(self, client, userdata, mid: int):
        """
        当成功发布一个消息到平台后，执行此函数
        :param client:      the client instance for this callback
        :param userdata:    the private user data as set in Client() or userdata_set()
        :param mid:         message id
        """
        if mid in self.__publish_listener_dict.keys():
            message_publish_listener: ActionListener = self.__publish_listener_dict.get(mid)
            if message_publish_listener is not None and isinstance(message_publish_listener, ActionListener):
                message_publish_listener.on_success(message="publish message success, mid = %s" % str(mid))

            self.__publish_listener_dict.pop(mid)
        else:
            # 没有设置发布监听器
            pass

    def _on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        """
        当接收到一个原始消息时，自动执行此回调方法
        :param client:      the client instance for this callback
        :param userdata:    the private user data as set in Client() or userdata_set()
        :param msg:         message id
        """
        try:
            self._logger.info("receive message, topic = %s, msg = %s", msg.topic, str(msg.payload))
            raw_msg = RawMessage(msg.topic, msg.payload, msg.qos)
            # 这里实际是调用DeviceClient实例中的on_message_received方法
            self.__raw_msg_listener.on_message_received(raw_msg)
        except Exception as e:
            self._logger.error(e)

    def _get_paho_client(self):
        return self.__paho_client
