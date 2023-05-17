   English | [简体中文](./README_CN.md) 

# iot-device-sdk-python Development Guide
# Contents

- [SDK Version](#0)

- [About This Document](#1)

- [SDK Overview](#2)

- [Preparations](#3)

- [Uploading a Product Model and Registering a Device](#4)

- [Online Debugging](#5)

- [Device Initialization](#6)

- [Command Delivery](#7)

- [Platform Message Delivery/Device Message Reporting](#8)

- [Property Reporting/Configuration](#9)

- [Device Shadow](#10)

- [Profile-Oriented Programming](#11)

- [OTA Upgrade](#12)

- [File Upload/Download](#13)

- [Device Time Synchronization](#14)

- [Gateway and Child Device Management](#15)

- [Device Information Reporting](#16)

- [Device Log Reporting](#17)

- [Open Source Protocols](#18)

- [API Reference](./IoT-Device-SDK-Python-API文档.pdf)

- [More Documents](https://support.huaweicloud.com/intl/en-us/devg-iothub/iot_02_0178.html)

<h1 id="0">SDK Version</h1>

| version |change type|explanation|
|:--------|:---|:---|
| 1.1.2   |add new feature|add support for micropython and corresponding demo, downlonding OTA from OBS, and readme|
| 1.1.1   |add new feature|provide ability to access Huawei IoT platform, enable users to implement business scenarios such as secure access, device management, data collection, and command delivery|


<h1 id="1">About This Document</h1>

iot-device-sdk-python (SDK for short) provides abundant demo code for IoT devices to communicate with the platform and implement device, gateway, and over-the-air (OTA) services.
The SDK greatly simplifies device development and enables quick access to the platform.

This document uses the examples to describe how to use the SDK to quickly connect devices to the Huawei Cloud IoT platform via MQTT protocol.

Official website: https://www.huaweicloud.com/intl/en-us/

In the upper right corner of the Huawei Cloud official website, click **Console** to access the management console. On the top of the page, search for **IoTDA** to access the IoTDA console.

<h1 id="2">SDK Overview</h1>

The SDK is designed for embedded devices with powerful computing and storage capabilities. You can call SDK APIs to implement communication between devices and the platform. The SDK currently supports:
*  Device message reporting, property reporting, property reading and writing, and command delivery
*  OTA upgrades
*  Device authentication using secrets and certificates
*  Device shadow query
*  Gateway services, child device management, and child device message forwarding
*  Profile-oriented programming
*  Custom topics
*  File upload and download.

**SDK Directory Structure**

**iot_device_sdk_python**: SDK code

**iot_device_demo**: demo code

**iot_gateway_demo**: demo code for gateway and child device management

<h1 id="3">Preparations</h1>

*  You have installed Python 3.8.2.

*  You have installed the third-party class library paho-mqtt: 1.5.0 (mandatory).

*  You have installed the third-party class library schedule: 1.1.0 (mandatory).

*  You have installed the third-party class library requests: 2.25.1 (optional, used in the demo of gateway and child device management).

*  You have installed the third-party class library tornado: 6.1 (optional, used in the demo of gateway and child device management).


<h1 id="4">Uploading a Product Model and Registering a Device</h1>

A smoke detector product model is provided to help you understand the product model. This smoke detector can report the smoke density, temperature, humidity, and smoke alarms, and execute the ring alarm command.
The following uses the smoke detector as an example to introduce the procedures of message reporting, property reporting, and command response.

* Visit the [IoTDA product page](https://www.huaweicloud.com/intl/en-us/product/iotda.html) and click **Access Console** to go to the IoTDA console.

* View the platform access address.

   ![MD1](./doc/figure_en/MD1.png)

* View and save the MQTT device access address.

   ![MD2](./doc/figure_en/MD2.png)

* On the IoTDA console, choose **Products** in the navigation pane, and click **Create Product** in the upper right corner. On the displayed page, specify the product name, protocol, data type, manufacturer, industry, and device type, and click **OK**.

   - Select the **MQTT** protocol.

   - Select the **JSON** data format.

   ![MD3](./doc/figure_en/MD3.png)

* After the product is created, click **View** to access its details. On the **Model Definition** page, click **Import from Local** to upload the smoke detector product model [smokeDetector](https://iot-developer.obs.cn-north-4.myhuaweicloud.com:443/smokeDetector.zip).
  The following figure shows the generated product model.

  ![MD4](./doc/figure_en/MD4.png)

* In the navigation pane, choose **Devices** > **All Devices**. In the upper right corner, click **Individual Register**. On the page displayed, set device registration parameters and click **OK**.

   ![MD5](./doc/figure_en/MD5.png)

* After the device is registered, save the node ID, device ID, and secret.

<h1 id="5">Online Debugging</h1>

In the navigation pane, choose **O&M** > **Online Debug**. The **Online Debugging** page is displayed.
Command delivery and message tracing are available.

*  Click **Select Device** in the upper right corner to select a registered device.

*  Click **IoT Platform**. The message tracing result is displayed.

*  Click **Send** in the lower right corner to send the command to the device.

![MD6](./doc/figure_en/MD6.png)

<h1 id="6">Device Initialization</h1>

* Create a device.

   Secret authentication and certificate authentication are available for device access.

   * If you use port 1883 and secret authentication for device access, write the obtained device ID and secret.

   ```
       server_uri = "iot-mqtts.cn-north-4.myhuaweicloud.com"   # Change the access address to the one you saved.
       port = 1883
       device_id = "< Your DeviceId >"
       sc = "< Your Device Secret >"

       device = IotDevice()
       device.create_by_secret(server_uri=server_uri,
                               port=port,
                               device_id=device_id,
                               secret=sc)
   ```

   * If you use port 8883 and secret authentication for device access (recommended, all the demo access the platform by this method), write the obtained device ID, secret, and preset CA certificate.
     Preset certificate: **/iot_device_demo/resources/GlobalSignRSAOVSSLCA2018.crt.pem**

   ```
       server_uri = "iot-mqtts.cn-north-4.myhuaweicloud.com"   # Change the access address to the one you saved.
       port = 8883
       device_id = "< Your DeviceId >"
       sc = "< Your Device Secret >"
       # CA certificate of the IoT platform, used for server authentication.
       iot_ca_cert_path = "./resources/GlobalSignRSAOVSSLCA2018.crt.pem"

       device = IotDevice()
       device.create_by_secret(server_uri=server_uri,
                               port=port,
                               device_id=device_id,
                               secret=sc,
                               iot_cert_file=iot_ca_cert_path)
   ```

* Call the **init** function to connect the device to the platform. This is a blocking function and it returns **0** if the device and the platform are connected.

   ```
        if device.connect() != 0:
            return
   ```

* After the connection is established, the device starts to communicate with the platform. Call the **get_client** method of the **IotDevice** class to obtain the device client, which provides communication APIs related to messages, properties, and commands.
  Example:
   ```
        device.get_client().set_command_listener(...)
        device.get_client().report_device_message(...)
   ```

*  For details about the **IotDevice** class, see **/iot_device_sdk_python/iot_device.py**.

If the connection is successful, the following information is displayed in the **Message Tracing** area on the **Online Debugging** page:

![MD7](./doc/figure_en/MD7.png)

Run logs:

![MD8](./doc/figure_en/MD8.png)

<h1 id="7">Command Delivery</h1>

**/iot_device_demo/command_sample.py** is an example of processing commands delivered by the IoT platform. You can set a command listener to receive commands delivered by the platform. The callback needs to process the commands and report responses.

The **CommandSampleListener** class in the following code inherits the **CommandListener** class and implements the **on_command** method. Set the **CommandSampleListener** instance to the command listener, which is:

```
device.get_client().set_command_listener(CommandSampleListener(device))
```

When receiving a command, the device automatically calls the **on_command** method in the listener.
The command content is printed in the **on_command** method, and the response is returned to the platform.

```
class CommandSampleListener(CommandListener):
    def __init__(self, iot_device: IotDevice):
        """ Pass an IotDevice instance. """
        self.device = iot_device

    def on_command(self, request_id, service_id, command_name, paras):
        logger.info('on_command requestId: ' + request_id)
        # Process commands.
        logger.info('begin to handle command')

        """ code here """
        logger.info(str(paras))

        # Command response
        command_rsp = CommandRsp()
        command_rsp.result_code = 0
        command_rsp.response_name = command_name
        command_rsp.paras = {"content": "Hello Huawei"}
        self.device.get_client().response_command(request_id, command_rsp)


def run():
    
    < create device code here ... >
    
    # Set a listener.
    device.get_client().set_command_listener(CommandSampleListener(device))
    
    if device.connect() != 0:
        logger.error('init failed')
        return

    while True:
        time.sleep(5)
```

Run the **run** function to deliver a command to the device on the **Online Debugging** page, The code output is as follows:

![MD9](./doc/figure_en/MD9.png)

In addition, the device response to the command is displayed in the **Message Tracing** area of the **Online Debugging** page.

![MD10](./doc/figure_en/MD10.png)

<h1 id="8">Platform Message Delivery/Device Message Reporting</h1>

Message delivery is the process in which the platform delivers messages to a device. Message reporting is the process in which a device reports messages to the platform. **/iot_device_demo/message_sample.py** shows an example of message delivery/reporting.

```
class DeviceMsgListener(DeviceMessageListener):
    def on_device_message(self, message: DeviceMessage):
        print('on_device_message: ' + json.dumps(message))


def run():
    < create device code here ... >

    # Receiving messages from the platform
    device.get_client().set_device_msg_listener(DeviceMsgListener())

    if device.connect() != 0:
        logger.error('init failed')
        return

    # Scheduled messages reporting
    logger.info('begin report message')
    default_publish_listener = DefaultPublishActionListener()
    while True:
        device.get_client().report_device_message(DeviceMessage({'content': 'Hello Huawei'}),
                                                  default_publish_listener)
        time.sleep(5)
```

The **report_device_message** method reports the message to the platform. If the message is sent, the following information is displayed on the **Online Debugging** page.

![MD11](./doc/figure_en/MD11.png)

<h1 id="9">Property Reporting/Configuration</h1>

A device can report current property values to the platform. Device properties can be configured on the platform.
**/iot_device_demo/properties_sample.py** shows an example of property reporting/configuration.

<h3>Property Reporting</h3>
Devices report property data in the format defined in the product model to the platform. The platform assigns the reported data to the device shadow.


   ```
   def run():
       < create device code here ... >
   
       if device.connect() != 0:
           logger.error('init failed')
           return
   
       service_property = ServiceProperty()
       service_property.service_id = 'smokeDetector'
       service_property.properties = {'alarm': 10, 'smokeConcentration': 36, 'temperature': 64, 'humidity': 32}
       services = [service_property.to_dict()]
   
       while True:
           device.get_client().report_properties(services, DefaultPublishActionListener())
           time.sleep(5)
   ```

The preceding code implements scheduled reporting of the **alarm**, **smokeConcentration**, **temperature**, and **humidity** properties. If properties are reported, the following information is displayed on the **Online Debugging** page.

![MD12](./doc/figure_en/MD12.png)

In the navigation pane, choose **Devices** > **All Devices**, select the registered device, and click the **Device Shadow** tab to view the reported property values.

![MD13](./doc/figure_en/MD13.png)

<h3>Setting Device Properties on the Platform</h3>
If you set the **PropertySampleListener** instance as a property listener by running the following command:

```
device.get_client().set_properties_listener(PropertySampleListener(device))
```

When receiving a property read/write request, the device automatically calls the **on_property_set** or **on_property_get** method in the listener.

**on_property_set** writes properties. **on_property_get** reads properties.

In most scenarios, you can directly read the device shadow on the platform, so **on_property_get** does not need to be implemented.

To read device properties in real time, implement this method.

The configured properties are printed in the **on_property_set** method, and the response is returned to the platform.

```
class PropertySampleListener(PropertyListener):
    def __init__(self, iot_device: IotDevice):
        """ Pass an IotDevice instance. """
        self.device = iot_device

    def on_property_set(self, request_id, services: [ServiceProperty]):
        """ Traverse services. """
        for service_property in services:
            logger.info("on_property_set, service_id:" + service_property.service_id)
            """ Traverse properties. """
            for property_name in service_property.properties:
                logger.info('set property name:' + property_name)
                logger.info("set property value:" + str(service_property.properties[property_name]))
        self.device.get_client().respond_properties_set(request_id, iot_result.SUCCESS.to_dict())

    def on_property_get(self, request_id, service_id):
        pass


def run():
    < create device code here ... >
    
    device.get_client().set_properties_listener(PropertySampleListener(device))

    if device.connect() != 0:
        return
```

On the **Device Shadow** tab page, click **Configure Property** to set the desired property value.
If the desired value you set is different from the value reported by the device, the platform automatically sends the desired value to the device when it goes online. (This is the process of setting a property on the platform.)

![MD14](./doc/figure_en/MD14.png)

Run the preceding **run** function. The following information is displayed.

![MD15](./doc/figure_en/MD15.png)

<h1 id="10">Device Shadow</h1>

This is used by device to get shadow data. A device can obtain device shadow data from the platform to synchronize (modify) device properties.

**/iot_device_demo/device_shadow_sample.py** shows an example of obtaining device shadow data from the platform.

* A device obtains device shadow data from the platform.

   ```
    # Receiving responses from the platform
    device.get_client().set_device_shadow_listener(DeviceShadowSampleListener())

    if device.connect() != 0:
        logger.error('init failed')
        return

    # Obtaining device shadow data
    request_id = str(uuid.uuid1())
    device.get_client().get_device_shadow(request_id, {'service_id': 'smokeDetector'}, None)
   ```

* A device receives shadow data returned by the platform.

   ```
   class DeviceShadowSampleListener(DeviceShadowListener):
       def on_shadow(self, request_id, message):
           logger.info('on_shadow request_id: ' + request_id)
           print(message)
   ```

<h1 id="11">Profile-Oriented Programming</h1>

You can use the profile capabilities provided by the SDK to define device services. The SDK can automatically communicate with the platform to synchronize properties and call commands. Compared with directly calling client APIs to communicate with the platform, profile-oriented programming simplifies device-side code. In this way, device-side code can focus on services and does not need to implement communications with the platform. **/iot_device_demo/smoke_detector.py** shows an example of profile-oriented programming.

Define a smoke detector service class, which is inherited from the **AbstractService** class.

```
class SmokeDetectorService(AbstractService)
```

Define service properties, which must be consistent with those defined in the product model.
*  The value of **prop_name** must be the same as that of the model. **writeable** indicates whether the property can be written. **field_name** indicates the variable name. **val** indicates the property value.

```
smoke_alarm = Property(val=20, field_name="smoke_alarm", prop_name="alarm", writeable=True)
concentration = Property(val=float(32.0), field_name="concentration", prop_name="smokeConcentration", writeable=False)
humidity = Property(val=64, field_name="humidity", prop_name="humidity", writeable=False)
temperature = Property(val=float(36.0), field_name="temperature", prop_name="temperature", writeable=False)
```

Define the methods for reading and writing properties.
*  **get_***xxx* is the read method and is called by the SDK when properties are queried by the platform or reported.
*  **set_***xxx* is the write method and is called by the SDK when properties are modified on the platform. If properties are read-only, leave the **set_***xxx* method not implemented.

```
    # Naming rules of the **get**/**set** APIs: **get**_*VariableName* or **set**_*VariableName*. If the setting is valid, the SDK automatically calls these APIs.
    def get_humidity(self):
        # Simulate the action of reading data from the sensor.
        self.humidity.val = 32
        return self.humidity.val

    def set_humidity(self, humidity):
        # You do not need to implement this method for read-only fields.
        pass

    def get_temperature(self):
        # Simulate the action of reading data from the sensor.
        self.temperature.val = 64
        return self.temperature.val

    def set_temperature(self, temperature):
        # You do not need to implement this method for read-only fields.
        pass

    def get_concentration(self):
        # Simulate the action of reading data from the sensor.
        self.concentration.val = 36
        return self.concentration.val

    def set_concentration(self, concentration):
        # You do not need to implement this method for read-only fields.
        pass

    def get_smoke_alarm(self):
        return self.smoke_alarm.val

    def set_smoke_alarm(self, smoke_alarm: int):
        self.smoke_alarm.val = smoke_alarm
        if smoke_alarm == 10:
            self._logger.info("set alarm:" + str(smoke_alarm))
            self._logger.info("alarm is clear by app")
```

Define the service command. The type of input parameters and return values of the command cannot be changed. Otherwise, a runtime error occurs.

```
    def alarm(self, paras: dict):
        duration = paras.get("duration")
        self._logger.info("ringAlarm duration = " + str(duration))
        command_rsp = CommandRsp()
        command_rsp.result_code = command_rsp.SUCCESS()
        return command_rsp
```

The service is defined. For details about the code, see the **SmokeDetectorService** class in **/iot_device_demo/smoke_detector.py**. Then, create a device, register the smoke detector service, and initialize the device. When the device is connected. The smoke detector service enables scheduled property reporting.

```
class SmokeDetector:
    def __init__(self, server_uri, port, device_id, secret):
        self.server_uri = server_uri
        self.port = port
        self.device_id = device_id
        self.secret = secret

    def start(self):
        """ Create a device. """
        < create device code here ... >
        
        """ Add smoke detector service. """
        smoke_detector_service = SmokeDetectorService()
        device.add_service("smokeDetector", smoke_detector_service)
        """ Connect the device to the platform. """
        if device.connect() != 0:
            return
        
        """ Enable scheduled property reporting. """
        smoke_detector_service.enable_auto_report(5)

        """ End scheduled reporting in 20s. """
        time.sleep(20)
        smoke_detector_service.disable_auto_report()
```

If properties are reported, the following information is displayed on the **Online Debugging** page:

![MD16](./doc/figure_en/MD16.png)

On the **Online Debugging** page, send a command to the device. The profile automatically calls the **alarm** method of the **SmokeDetectorService** class. The output is as follows:

![MD17](./doc/figure_en/MD17.png)

<h1 id="12">OTA Upgrade</h1>

**/iot_device_demo/ota_sample.py** shows an example of performing OTA upgrade. The code is as follows:

```
def run():
   < create device code here ... >

    """ OTA listener settings """
    ota_service: OTAService = device.get_ota_service()
    ota_service_listener = OTASampleListener(ota_service)
    ota_service.set_ota_listener(ota_service_listener)

    if device.connect() != 0:
        return
```

**OTAService** is a service defined by the system and can be obtained using the **get_ota_service** method.
You need to implement the OTA listener. The **OTASampleListener** class in **/iot_device_demo/ota_sample.py** is an example of listener implementation. The **OTASampleListener** class inherits the **OTAListener** class and must implement the following methods:
*  **on_query_version**: receives a version query notification. This method needs to be implemented to return the current version number to the platform.
*  **on_receive_package_info**: receives the new version notification. This method needs to be implemented to download and install a package for upgrade.

<h3>Performing OTA Upgrade</h3>

1. For details about how to upgrade firmware, see [Firmware Upgrades](https://support.huaweicloud.com/intl/en-us/usermanual-iothub/iot_01_0027.html).

2. For details about how to upgrade software, see [Software Upgrades](https://support.huaweicloud.com/intl/en-us/usermanual-iothub/iot_01_0047.html).

<h1 id="13">File Upload/Download</h1>

**/iot_device_demo/file_sample.py** shows an example of uploading and downloading files.

```
def run():
    < create device code here ... >

    """ Set the file management listener. """
    file_manager: FileManagerService = device.get_file_manager_service()
    file_manager_listener = FileManagerSampleListener()
    file_manager.set_listener(file_manager_listener)

    if device.connect() != 0:
        logger.error('init failed')
        return

    """ File upload """
    upload_file_path = os.path.dirname(__file__) + r'/download/upload_test.txt'
    file_name = "upload_test.txt"
    file_manager.get_upload_url(upload_file_path=upload_file_path, file_name=file_name)

    # After 10 seconds, download the uploaded **upload_test.txt** file and save it to **download.txt**.
    time.sleep(10)

    """ File download """
    download_file_path = os.path.dirname(__file__) + r'/download/download.txt'
    file_manager.get_download_url(download_file_path=download_file_path, file_name=file_name)
```

**FileManagerService** is a service defined by the system and can be obtained using the **get_file_manager_service** method of the device. You need to implement the **FileManagerService** listener. The **FileManagerSampleListener** class in **/iot_device_demo/file_sample.py** is an example of listener implementation. The **FileManagerSampleListener** class inherits the **FileManagerListener** class and must implement the following methods:
*  **on_upload_url**: receives the file upload URL delivered by the platform.
*  **on_download_url**: receives the file download URL delivered by the platform.

For details about the file upload/download process, see [File Uploads](https://support.huaweicloud.com/intl/en-us/usermanual-iothub/iot_01_0033.html).

* Configure OBS storage on the console.

   ![MD18](./doc/figure_en/MD18.png)

* Preset the file to be uploaded. In the preceding example, the file to be uploaded is **/iot_device_demo/download/upload_test.txt**.
   Download the uploaded **upload_test.txt** file to **/iot_device_demo/download/download.txt**.

* Run the preceding commands to view the storage result in OBS.

   ![MD19](./doc/figure_en/MD19.png)

<h1 id="14">Device Time Synchronization</h1>

**/iot_device_demo/ntp_sample.py** shows an example of synchronizing device time.

```
def run():
   < create device code here ... >

    """ Set the time synchronization service. """
    time_sync_service: TimeSyncService = device.get_time_sync_service()
    time_sync_listener = TimeSyncSampleListener()
    time_sync_service.set_listener(time_sync_listener)

    if device.connect() != 0:
        logger.error('init failed')
        return

    # Request for time synchronization
    time_sync_service.request_time_sync()
```

**TimeSyncService** is a service defined by the system and can be obtained using the **get_time_sync_service** method. You need to implement the **TimeSyncListener** listener. The **TimeSyncSampleListener** class in **/iot_device_demo/ntp_sample.py** is an example of listener implementation. The **TimeSyncSampleListener** class inherits the **TimeSyncListener** class and must implement the following method:
*  **on_time_sync_response**: time synchronization response. Assume that the time when the device receives the response is **device_recv_time**. The device calculates the accurate time as follows:
        (server_recv_time + server_send_time + device_recv_time - device_send_time) / 2

<h1 id="15">Gateway and Child Device Management</h1>

For details, see [Gateways and Child Devices](https://support.huaweicloud.com/intl/en-us/usermanual-iothub/iot_01_0052.html).

The demo code for gateway and child device management is stored in **/iot_gateway_demo**. This demo demonstrates how to use a gateway to connect TCP devices to the platform. Only an MQTT connection is established between the gateway and platform. Devices communicate with the platform using the gateway information.

This demo contains two executable .py files:
**/iot_gateway_demo/string_tcp_server.py** (gateway-related code) and **/iot_gateway_demo/tcp_device.py** (TCP device-related code).


This demo demonstrates that:
1. The gateway synchronizes the child device list. When the gateway is offline, the platform cannot notify the gateway of child device addition and deletion in a timely manner.
   When the gateway goes online, the platform notifies the gateway of child device addition and deletion.
2. The gateway updates the child device status. The gateway notifies the platform that the child device status is "ONLINE".
3. The child device reports a message to IoT platform through the gateway.
4. The platform delivers a command to the child device.
5. The gateway sends a request for adding/deleting child devices.

<h3>Procedure</h3>

Run **string_tcp_server.py**. The device ID, device secret, and product ID of the gateway need to be entered. The gateway establishes a connection with the platform and synchronizes the child device list.

Run **tcp_device.py**. The child device ID needs to be entered. Enter any string in the CLI, for example, **go online**. This is the first message sent by the child device to the gateway. If the child device has been registered with the platform, the gateway instructs the platform to set the child device status to online.
If the child device is not registered with the platform, the gateway registers the child device with the platform, as shown in the following example.

Run **string_tcp_server.py**, enter the child device ID (not registered on the platform) in **tcp_device.py**, run **tcp_device.py**, and enter a string in the CLI.

![MD20](./doc/figure_en/MD20.png)

The gateway sends a request to the platform to add a child device. The created child device is displayed on the platform.

![MD21](./doc/figure_en/MD21.png)After the child device is created, enter a string in the CLI. The gateway instructs the platform to update the child device status to "ONLINE".

![MD22](./doc/figure_en/MD22.png)

![MD23](./doc/figure_en/MD23.png)

After the child device status changes to online on the platform, enter a string in the CLI. The gateway reports the message to the platform.

![MD24](./doc/figure_en/MD24.png)

If you enter **gtwdel**, the gateway sends a request to the platform to delete the child device.

![MD25](./doc/figure_en/MD25.png)

The child device is deleted from the platform.

<h1 id="16">Device Information Reporting</h1>

**/iot_device_demo/report_device_info_sample.py** shows an example of reporting device information.
Device information includes the firmware version, software version, and SDK version. Note that when a device establishes a connection with the platform for the first time, the SDK automatically reports the device information that contains only the SDK version.

```
def run():
    < create device code here ... >

    if device.connect() != 0:
        logger.error('init failed')
        return

    """ Report device information. """
    device_info = DeviceBaseInfo()
    device_info.fw_version = "v1.0"
    device_info.sw_version = "v1.0"
    device.get_client().report_device_info(device_info)
```

<h1 id="17">Device Log Reporting</h1>

The SDK automatically reports device logs in either of the following scenarios. In other scenarios, you need to report logs manually.

1. When a device establishes a connection with the platform for the first time, the SDK automatically reports the device log. Example:

    ```
    {
        "object_device_id": "6109fd1da42d680286bb1ff3_123456",
        "services": [{
         "service_id": "$log", 
         "event_type": "log_report", 
         "event_time": "2021-09-11T10:36:18Z", 
         "event_id": "", 
         "paras": {
             "timestamp": "1631327778381", 
             "type": "DEVICE_STATUS", 
             "content": "connect complete, the uri is iot-mqtts.cn-north-5.myhuaweicloud.com"
         }
        }]
    }
    ```

2. After the device reconnects to the platform, the SDK automatically reports two device logs.
   One records the timestamp when the device reconnects to the platform, and the other records the timestamp when the device is disconnected from the platform. The log format is the same as that in the preceding example.

<h1 id="18">Open Source Protocols</h1>

- In compliance with the BSD-3 open source license agreement
