from http_client import SyncClient, AsyncClient
from config import ClearBladeConfig
import os
from exceptions import UnConfiguredEnvironment
import json

class Device():
    """
    Data class for Clearblade Device
    """
    #TODO: find a better way to construct the Device object. I dont like so much parameter in a constructor
    def __init__(self, id: str = None, name: str = None, num_id: str=None,
                 credentials: list=[], last_heartbeat_time: str = None, last_event_time: str = None,
                 last_state_time: str = None, last_config_ack_time: str = None,
                 last_config_send_time: str = None, blocked: bool = False,
                 last_error_time: str = None, last_error_status_code: dict = {"code":None, "message":""},
                 config: dict = {"cloudUpdateTime":None, "version":""} ,
                 state: dict = {"updateTime":None, "binaryData":None},
                 log_level: str = "NONE", meta_data: dict = {}, gateway_config : dict = {}  ) -> None:

        self._id = id
        self._name = name
        self._num_id = num_id
        self._credentials = credentials
        self._last_heartbeat_time = last_heartbeat_time
        self._last_event_time = last_event_time
        self._last_state_time = last_state_time
        self._last_config_ack_time = last_config_ack_time
        self._last_config_send_time = last_config_send_time
        self._blocked = blocked
        self._last_error_time = last_error_time
        self._last_error_status_code = last_error_status_code
        self._config = config
        self._state =  state
        self._log_level = log_level
        self._meta_data = meta_data
        self._gateway_config = gateway_config

    @staticmethod
    def from_json(json):
        return Device(id= json['id'], name= json['name'], num_id= json['numId'],
                      credentials= json['credentials'], last_heartbeat_time= json['lastHeartbeatTime'],
                      last_event_time= json['lastEventTime'], last_state_time= json['lastStateTime'],
                      last_config_ack_time= json['lastConfigAckTime'], last_config_send_time= json['lastConfigSendTime'],
                      blocked= json['blocked'], last_error_time= json['lastErrorTime'],
                      last_error_status_code= json['lastErrorStatus'], config= json['config'],
                      state= json['state'], log_level= json['logLevel'], meta_data= json['metadata'],
                      gateway_config= json['gatewayConfig'])

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def num_id(self):
        return self._num_id

    @property
    def credentials(self):
        return self._credentials

    @property
    def last_error_status(self):
        return self._last_error_status_code

    @property
    def config(self):
        return self._config

    @property
    def state(self):
        return self._state

    @property
    def log_level(self):
        return self._log_level

    @property
    def meta_data(self):
        return self._meta_data

    @property
    def gateway_config(self):
        return self._gateway_config

    @property
    def log_level(self):
        return self._log_level

#classes to mock googles request & response

class Request():
    def __init__(self, name) -> None:
        self._name = name

    @property
    def name(self):
        return self._name

class SendCommandToDeviceRequest(Request):
    def __init__(self, name: str = None,
                binary_data: bytes = None,
                subfolder: str = None) -> None:
        super().__init__(name)
        self._binary_data = binary_data
        self._subfolder = subfolder

    @property
    def binary_data(self):
        return self._binary_data

    @property
    def sub_folder(self):
        return self._subfolder

class CreateDeviceRequest(Request):
    def __init__(self, name: str = None,
                       device: Device = None) -> None:
        super().__init__(name)
        self._device = device

    @property
    def device(self):
        return self._device

class ModifyCloudToDeviceConfigRequest(Request):
    def __init__(self, name:str = None ,
                 version_to_update: int = -1,
                 binary_data: bytes = None) -> None:
        super().__init__(name)
        self._version_to_update = version_to_update
        self._binary_data = binary_data

    @property
    def version_to_update(self):
        return self._version_to_update

    @property
    def binary_data(self):
        return self._binary_data

class DeviceConfig(Request):
    def __init__(self, name,
                 version,
                 cloud_ack_time,
                 device_ack_time,
                 binary_data) -> None:
        super().__init__(name)
        self._version = version
        self._cloud_ack_time = cloud_ack_time
        self._device_ack_time = device_ack_time
        self._binary_data = binary_data

    def version(self):
        return self._version

    def cloud_ack_time(self):
        return self._cloud_ack_time

    def device_ack_time(self):
        return self._device_ack_time

    def binary_data(self):
        return self._binary_data

    @staticmethod
    def from_json(json):
        return DeviceConfig(version=json['version'], cloud_ack_time=json['cloudUpdateTime'],
                            device_ack_time=json['deviceAckTime'], binary_data=json['binaryData'])

class DeleteDeviceRequest(Request):
    def __init__(self, name: str = None) -> None:
        super().__init__(name)

class GetDeviceRequest(Request):
    def __init__(self, name: str = None) -> None:
        super().__init__(name)

class BindUnBindGatewayDeviceRequest(Request):
    def __init__(self, deviceId: str = None,
                       gatewayId: str = None) -> None:
        self._deviceid=deviceId
        self._gatewayid=gatewayId

    @property
    def deviceId(self):
        return self._deviceid

    @property
    def gatewayId(self):
        return self._gatewayid

class GetDeviceStatesList(Request):
    def __init__(self, name: str = None,
                numStates: int = None) -> None:
        super().__init__(name)
        self._numstates = numStates

    @property
    def numStates(self):
        return self._numstates

class GetDeviceConfigVersionsList(Request):
    def __init__(self, name: str = None,
                numVersions: int = None) -> None:
        super().__init__(name)
        self._numversions = numVersions

    @property
    def numVersions(self):
        return self._numversions

class ListDevicesRequest(Request):
    def __init__(self, parent:str = None ,
                 deviceNumIds: str = None,
                 deviceIds: str = None,
                 fieldMask: str = None,
                 gatewayListOptions: dict = None,
                 pageSize: int = None,
                 pageToken: str = None) -> None:
        self._parent = parent
        self._device_num_ids = deviceNumIds
        self._device_ids = deviceIds
        self._field_mask = fieldMask
        self._gateway_list_options = gatewayListOptions
        self._page_size = pageSize
        self._page_token = pageToken

    @property
    def parent(self):
        return self._parent

    @property
    def device_num_ids(self):
        return self._device_num_ids

    @property
    def device_ids(self):
        return self._device_ids

    @property
    def field_mask(self):
        return self._field_mask

    @property
    def gateway_list_options(self):
        return self._gateway_list_options

    @property
    def page_size(self):
        return self._page_size

    @property
    def page_token(self):
        return self._page_token

    def _prepare_params_for_list(self):
        params = {'parent':self.parent}
        if self.page_size is not None:
            params['pageSize'] = self.page_size
        if self.device_num_ids is not None:
            params['deviceNumIds'] = self.device_num_ids
        if self.device_ids is not None:
            params['deviceIds'] = self.device_ids
        if self.field_mask is not None:
            params['fieldMask'] = self.field_mask
        if self.gateway_list_options is not None:
            params['gatewayListOptions'] = self.gateway_list_options
        if self.page_token is not None:
            params['pageToken'] = self.page_token

class UpdateDeviceRequest(Request):
    def __init__(self, id: str = None, name: str = None, numId: str=None,
                 credentials: list=None, blocked: bool = None,
                 logLevel: str = None, metadata: dict = None, gatewayConfig : dict = None,
                 updateMask: str = None) -> None:
        self._id = id
        self._name = name
        self._num_id = numId
        self._credentials = credentials
        self._blocked = blocked
        self._log_level = logLevel
        self._meta_data = metadata
        self._gateway_config = gatewayConfig
        self._update_mask = updateMask

    def _prepare_params_body_for_update(self):
        params = {'name': self._name}
        if self._update_mask is not None:
            params['updateMask'] = self._update_mask

        body = {}
        if self._id is not None:
            body['id'] = self._id
        if self._name is not None:
            body['name'] = self._name
        if self._log_level is not None:
            body['logLevel'] = self._log_level
        if self._gateway_config is not None:
            body['gatewayConfig'] = self._gateway_config
        if self._meta_data is not None:
            body['metadata'] = self._meta_data
        if self._blocked is not None:
            body['blocked'] = self._blocked
        if self._credentials is not None:
            body['credentials'] = self._credentials

        return params, body

class ClearBladeDeviceManager():

    def __init__(self) -> None:
        #create the ClearBladeConfig object
        self._admin_cb_config = None
        self._regional_cb_config = None

    def _get_admin_clearblade_config(self):
        if self._admin_cb_config:
            return self._admin_cb_config

        service_account_file_path = os.environ.get("CLEARBLADE_CONFIGURATION")
        if not service_account_file_path:
            raise UnConfiguredEnvironment()
            #service_account_file_path = "C:\\Users\\GDas\\Downloads\\ingress_clearblade_service-credentials.json"

        service_account_data = None
        #parse the file and get all te required details.
        with open(service_account_file_path, mode='r') as service_account_file:
            service_account_data = json.load(service_account_file)

        if service_account_data is None:
            #TODO: raise exception
            return None

        system_key = service_account_data['systemKey']
        auth_token = service_account_data['token']
        api_url = service_account_data['url']
        project = service_account_data['project']

        self._admin_cb_config = ClearBladeConfig(system_key=system_key, auth_token=auth_token,
                                                 api_url=api_url, project=project)

        return self._admin_cb_config

    def _get_regional_config(self, region:str = None, registry:str = None):
        if self._regional_cb_config:
            return self._regional_cb_config

        self._admin_cb_config = self._get_admin_clearblade_config()
        region = "us-central1"
        registry = "gargi_python"

        sync_client = SyncClient(clearblade_config=self._admin_cb_config)
        request_body = {'region':region,'registry':registry, 'project':self._admin_cb_config.project}
        response = sync_client.post(api_name="getRegistryCredentials", is_webhook_folder=False, request_body=request_body)
        print(response)

        if response.status_code != 200:
            #TODO: raise some exceptions
            return None

        response_json = response.json()
        system_key = response_json['systemKey']
        auth_token = response_json['serviceAccountToken']
        api_url = response_json['url']

        self._regional_cb_config = ClearBladeConfig(system_key=system_key, auth_token=auth_token, api_url=api_url,
                                                    region=region, project=self._admin_cb_config.project)
        return self._regional_cb_config

    def _prepare_for_send_command(self,
                                  request: SendCommandToDeviceRequest,
                                  name: str = None,
                                  binary_data: bytes = None,
                                  subfolder: str = None):
        has_flattened_params = any([name, binary_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if request is None:
            request = SendCommandToDeviceRequest(name, binary_data, subfolder)
        params = {'name':request.name,'method':'sendCommandToDevice'}
        body = {'binaryData':request.binary_data.decode("utf-8")}

        return params,body

    def _create_device_body(self, device: Device) :
        return {'id':device.name, 'name':device.name,
                'credentials':device.credentials, 'lastErrorStatus':device.last_error_status,
                'config':device.config, 'state':device.state,
                'loglevel':device.log_level, 'metadata':device.meta_data,
                'gatewayConfig':device.config}

    def _create_device_from_response(self, json_response) -> Device :
        return Device.from_json(json=json_response)

    def _prepare_modify_cloud_config_device(self,
                                            request: ModifyCloudToDeviceConfigRequest,
                                            name, binary_data, version_to_update):

        has_flattened_params = any([name, binary_data])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if request is None:
            request = ModifyCloudToDeviceConfigRequest(name=name,version_to_update=version_to_update, binary_data=binary_data)

        params = {'name': request.name, 'method': 'modifyCloudToDeviceConfig'}
        body = {'binaryData': request.binary_data.decode("utf-8"), 'versionToUpdate':request.version_to_update}

        return params, body

    def _create_device_config(self, response):
        return DeviceConfig.from_json(response)

    def _create_device_list_from_response(self, json_response):
        devicesList = []
        print(json_response['devices'])
        for deviceJson in json_response['devices']:
            devicesList.append(Device.from_json(json=deviceJson))
        return devicesList

    def send_command(self,
                    request: SendCommandToDeviceRequest,
                    name: str = None,
                    binary_data: bytes = None,
                    subfolder: str = None):

        params, body = self._prepare_for_send_command(request, name, binary_data, subfolder)
        regional_config = self._get_regional_config()
        sync_client = SyncClient(clearblade_config=regional_config)
        return sync_client.post(api_name="cloudiot_devices", request_params=params, request_body=body)

    async def send_command_async(self,
                                 request: SendCommandToDeviceRequest = None,
                                 name: str = None,
                                 binary_data: str = None,
                                 subfolder: str = None ):

        params, body = self._prepare_for_send_command(request, name, binary_data, subfolder)
        async_client = AsyncClient(clearblade_config=self._get_regional_config())
        return await async_client.post(api_name="cloudiot_devices",
                                       request_params=params,
                                       request_body=body)

    def create(self, request: CreateDeviceRequest,
                     parent: str = None,
                     device: Device = None) -> Device:
        sync_client = SyncClient()
        body = self._create_device_body(request.device)
        response = sync_client.post(request_body=body)

        # return the device only if status code is 200
        # other wise return None
        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return None

    async def create_async(self, request: CreateDeviceRequest,
                           parent: str = None,
                           device: Device = None) -> Device:

        async_client = AsyncClient()
        body = self._create_device_body(request.device)
        response = await async_client.post(request_body=body)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return None

    def modify_cloud_device_config(self,
                                   request: ModifyCloudToDeviceConfigRequest,
                                   name:str = None,
                                   version_to_update : int = None,
                                   binary_data: bytes = None):
        sync_client = SyncClient()
        params, body = self._prepare_modify_cloud_config_device(request=request, name=name,
                                                                binary_data=binary_data, version_to_update=version_to_update)
        response = sync_client.post(request_params=params, request_body=body)

        if response.status_code == 200:
            return self._create_device_config(response.json)

        return None

    async def modify_cloud_device_config_async(self,
                                        request: ModifyCloudToDeviceConfigRequest,
                                        name:str = None,
                                        version_to_update : int = None,
                                        binary_data: bytes = None):
        params, body = self._prepare_modify_cloud_config_device(request=request, name=name,
                                                                binary_data=binary_data, version_to_update=version_to_update)
        async_client = AsyncClient()
        response = await async_client.post(request_params=params, request_body=body)
        if response.status_code == 200:
            return self._create_device_config(response.json)
        return None

    def list(self):
        pass

    def get(self,
            request: GetDeviceRequest) -> Device:
        sync_client = SyncClient()
        params = {'name':request.name}
        response = sync_client.get(request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return None

    async def get_async(self,
            request: GetDeviceRequest):
        async_client = AsyncClient()
        params = {'name':request.name}
        response = await async_client.get(request_params=params)

        if response.status_code == 200:
            return self._create_device_from_response(response.json())
        return None

    def delete(self,
               request: DeleteDeviceRequest):
        sync_client = SyncClient()
        params = {'name':request.name}
        response = sync_client.delete(api_name="cloudiot_devices",request_params=params)
        return response

    async def delete_async(self,
               request: DeleteDeviceRequest):
        async_client = AsyncClient()
        params = {'name':request.name}
        response = await async_client.delete(api_name="cloudiot_devices", request_params=params)
        return response

    def bindGatewayToDevice(self,
            request: BindUnBindGatewayDeviceRequest) :
        sync_client = SyncClient()
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'bindDeviceToGateway'}
        response = sync_client.post(api_name="cloudiot", request_params=params, request_body=body)

        return response

    async def bindGatewayToDevice_async(self,
            request: BindUnBindGatewayDeviceRequest) :
        async_client = AsyncClient()
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'bindDeviceToGateway'}
        response = await async_client.post(api_name="cloudiot", request_params=params, request_body=body)
        return response

    def unbindGatewayFromDevice(self,
            request: BindUnBindGatewayDeviceRequest) :
        sync_client = SyncClient()
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'unbindDeviceFromGateway'}
        response = sync_client.post(api_name="cloudiot", request_params=params, request_body=body)
        return response

    async def unbindGatewayFromDevice_async(self,
            request: BindUnBindGatewayDeviceRequest) :
        async_client = AsyncClient()
        body = {'deviceId':request.deviceId, 'gatewayId':request.gatewayId}
        params = {'method':'unbindDeviceFromGateway'}
        response = await async_client.post(api_name="cloudiot",request_params=params, request_body=body)
        return response

    def getDeviceSatesList(self,
            request: GetDeviceStatesList):
        sync_client = SyncClient()
        params = {'name':request.name, 'numStates':request.numStates}
        response = sync_client.get(api_name="cloudiot_devices_states",request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    async def getDeviceSatesList_async(self,
            request: GetDeviceRequest):
        async_client = AsyncClient()
        params = {'name':request.name, 'numStates':request.numStates}
        response = await async_client.get(request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    def getDeviceConfigVersionsList(self,
            request: GetDeviceConfigVersionsList):
        sync_client = SyncClient()
        params = {'name':request.name, 'numVersions':request.numVersions}
        response = sync_client.get(api_name="cloudiot_devices_configVersions",request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    async def getDeviceConfigVersionsList_async(self,
            request: GetDeviceConfigVersionsList):
        async_client = AsyncClient()
        params = {'name':request.name, 'numVersions':request.numVersions}
        response = await async_client.get(api_name="cloudiot_devices_configVersions", request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    def getDevicesList(self,
            request: ListDevicesRequest):
        sync_client = SyncClient()
        params = request._prepare_params_for_list()
        response = sync_client.get(api_name="cloudiot_devices",request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    async def getDevicesList_async(self,
            request: ListDevicesRequest):
        async_client = AsyncClient()
        params = request._prepare_params_for_list()
        response = await async_client.list(api_name="cloudiot_devices",request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    def updateDevice(self,
            request: UpdateDeviceRequest):
        sync_client = SyncClient()
        params, body = request._prepare_params_body_for_update()
        response = sync_client.patch(api_name= "",request_body=body, request_params=params)

        if response.status_code == 200:
            return response.json()
        return None

    async def updateDevice_async(self,
            request: UpdateDeviceRequest):
        async_client = AsyncClient()
        params, body = request._prepare_params_body_for_update()
        response = await async_client.patch(api_name="",request_body=body, request_params=params)

        if response.status_code == 200:
            return response.json()
        return None
