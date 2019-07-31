import yaml
import subprocess
from lib.utils import shell
from lib.public.logger import logger


def get_android_devices():
    r"""获取设备名
    """
    android_devices_list = []
    devices = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for device in devices.stdout.readlines():
        if isinstance(device, (bytes, bytearray)):
            device = device.decode('utf-8')
        if 'device' in device and 'devices' not in device:
            android_devices_list.append(device.split('\t')[0])

    return android_devices_list


def save_devices_yaml():
    r"""将安卓设备信息存入yaml文件
    """

    device_list = []
    for device in get_android_devices():
        cmd = shell.Adb(device)
        device_list.append(
            {'deviceName': device, 'platformName':
                'Android', 'platformVersion': cmd.device_version()})
        logger.info(
            'Get the android device is {0}, android version is {1}'.format(
                device, cmd.device_version()))

    with open('./conf/device.yaml', 'w') as f:
        yaml.dump(device_list, f)


def capabilities():
    r"""获取测试设备参数信息
    """

    desired_caps = []

    with open('./conf/conf.yaml') as stream:
        content = yaml.safe_load(stream)['Capabilities']

    with open('./conf/device.yaml') as stream:
        for device in yaml.safe_load(stream):
            desired_caps.append(dict(content, **device))

    return desired_caps


