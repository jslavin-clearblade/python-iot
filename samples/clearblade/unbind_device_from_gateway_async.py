import asyncio
import os

from clearblade.cloud import iot_v1


async def sample_unbind_device_from_gateway_async():
    async_client = iot_v1.DeviceManagerAsyncClient()

    parent = async_client.registry_path(
        "api-project-320446546234", 
        "us-central1", 
        "rajas-test")

    request = iot_v1.UnbindDeviceFromGatewayRequest(
        parent=parent,
        deviceId='test-dev-1',
        gatewayId='smason_test_gateway'
    )
    
    response = await async_client.unbind_device_from_gateway(request)
    print(response)

os.environ["CLEARBLADE_CONFIGURATION"] = "/Users/rajas/Downloads/test-credentials.json"
asyncio.run(sample_unbind_device_from_gateway_async())