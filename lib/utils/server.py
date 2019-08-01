import time
import random
import platform
import subprocess
from lib.public.logger import logger


class StartAppiumServer(object):

    def __init__(self, device):
        self.device = device

    def __start_driver(self, aport, bpport):

        command = "appium -p %s -bp %s -U %s" % (aport, bpport, self.device)
        if platform.system() == 'Windows':
            subprocess.Popen(command, shell=True)

        else:
            appium = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, close_fds=True)
            while True:
                appium_line = appium.stdout.readline().strip()
                logger.debug(appium_line)
                time.sleep(1)
                if 'listener started' in appium_line or 'Error: listen' in appium_line:
                    break

    def start_appium(self):
        aport = random.randint(4700, 4900)
        bpport = random.randint(4700, 4900)
        self.__start_driver(aport, bpport)

        logger.debug(
            'start appium :p %s bp %s device:%s' %
            (aport, bpport, self.device))
        time.sleep(10)
        return aport

    def main(self):
        """

        :return: 启动appium
        """
        return self.start_appium()


if __name__ == '__main__':
    s = StartAppiumServer('baec20fa')
    s.main()