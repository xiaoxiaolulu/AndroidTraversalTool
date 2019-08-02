import yaml
import selenium
from os import path
from lib.utils.server import StartAppiumServer
from lib.utils import get_devices
from appium import webdriver
from lib.public.parser import DumpParser
from lib.public.logger import logger
from lib.public.keywords import KeyWords
from selenium.webdriver.common.by import By


def run():

    def operate_yaml(filepath: str) -> dict:
        extension = ['.yml', '.yaml']
        if path.splitext(filepath)[-1] in extension:
            with open(filepath, encoding='utf-8') as stream:
                content = yaml.safe_load(stream)
                return content

    # 启动登录配置项
    confing = operate_yaml('.\conf\conf.yaml')
    if isinstance(confing, dict):
        login_setting = confing.get('LoginSetting')
        device = get_devices.get_android_devices()[0]
        server = StartAppiumServer(device)
        remote = webdriver.Remote('http://localhost:{}/wd/hub'.format(server.main()), get_devices.capabilities()[0])
        driver = KeyWords(remote)
        driver.sleep(30)
        driver.swipe_left(login_setting.get('SwipeLeft'))
        for element in login_setting.get('OperateElement'):
            for key, tags in element.items():
                if tags.get('Action') == "click":
                    driver.click(*(By.XPATH, tags.get('Xpath')))
                else:
                    driver.send_keys(tags.get('value', *(By.XPATH, tags.get('Xpath'))))


if __name__ == '__main__':
    run()


# '''测试代码'''
# driver = webdriver.Remote('http://localhost:4723/wd/hub', get_devices.capabilities()[0])
# import os
# while True:

#     import xml
#     try:
#         D = DumpParser('uidump.xml')
#         for value in D.get_element_path():
#             try:
#                 d = KeyWords(driver)
#                 d.wait(25)
#                 d.swipe_left(4)
#                 d.click(*(By.XPATH, value))
#                 import random
#                 d.send_keys(random.randint(4700, 4900),  *(By.XPATH, value))
#             except Exception as error:
#                 logger.warning(value)
#                 logger.warning(error)
#                 break
#     except (xml.etree.ElementTree.ParseError, PermissionError, UnboundLocalError):
#         # try:
#         #     os.remove('uidump.xml')
#         # except FileNotFoundError:
#         #     continue
#         continue
