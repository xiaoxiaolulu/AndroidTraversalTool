import os
import platform

system = platform.system()
find_command = 'findstr' if system == 'Windows' else 'grep'

if 'ANDROID_HOME' in os.environ:
    if system == 'Windows':
        command = os.path.join(
            os.environ['ANDROID_HOME'],
            'platform-tools',
            'adb.exe'
        )
    else:
        command = os.path.join(
            os.environ['ANDROID_HOME'],
            'platform-tools',
            'adb'
        )


class Adb(object):

    def __init__(self, device=None):
        if device is not None:
            self.device = '-s {0}'.format(device)
        else:
            self.device = ''

    def adb_arguments(self, args):
        return os.popen('adb {0} {1}'.format(self.device, args)).readlines()

    def shell_arguments(self, args):
        return os.popen('adb {0} shell {1}'.format(self.device, args)).readlines()

    def device_name(self):
        r"""获取设备名
        """
        return self.shell_arguments('getprop ro.serialno')[0]

    def device_version(self):
        r"""获取安卓版本
        """
        return self.shell_arguments('getprop ro.build.version.release')[0].strip()
