from devices import *

class DeviceManagerClient():

    def send_command_to_device(self,request:SendCommandToDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.send_command(request)

    def create_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.create(request=request)

    def modify_cloud_to_device_config(self, request: ModifyCloudToDeviceConfigRequest,
                                      name: str = None,
                                      version_to_update = -1,
                                      binary_data:bytes = None):

        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.modify_cloud_device_config(request=request,
                                                            name=name,
                                                            version_to_update=version_to_update,
                                                            binary_data=binary_data)

    def delete_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.delete(request=request)

    def get_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.get(request=request)

    def bind_device_to_gateway(self, request : BindUnBindGatewayDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.bindGatewayToDevice(request=request)

    def unbind_device_from_gateway(self, request : BindUnBindGatewayDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.unbindGatewayFromDevice(request=request)

    def set_device_state(self, request : SetDeviceStateRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return cb_device_manager.setDeviceState(request=request)

class DeviceManagerAsyncClient():

    async def send_command_to_device(self, request:SendCommandToDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.send_command_async(request)

    async def create_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.create_async(request)

    async def modify_cloud_to_device_config(self, request: ModifyCloudToDeviceConfigRequest,
                                            name: str = None,
                                            version_to_update = -1,
                                            binary_data:bytes = None):

        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.modify_cloud_device_config_async(request=request,
                                                            name=name,
                                                            version_to_update=version_to_update,
                                                            binary_data=binary_data)

    async def delete_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.delete_async(request=request)

    async def get_device(self, request):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.get_async(request=request)

    async def bind_device_to_gateway(self, request : BindUnBindGatewayDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.bindGatewayToDevice_async(request=request)

    async def unbind_device_from_gateway(self, request : BindUnBindGatewayDeviceRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.unbindGatewayFromDevice_async(request=request)

    async def set_device_state(self, request : SetDeviceStateRequest):
        cb_device_manager = ClearBladeDeviceManager()
        return await cb_device_manager.setDeviceState_async(request=request)
