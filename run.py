from lib.utils import get_devices
from appium import webdriver
from lib.public.parser import DumpParser
from lib.public.logger import logger
import selenium
from lib.utils.server import StartAppiumServer
from lib.public.keywords import KeyWords
from selenium.webdriver.common.by import By
'''测试代码'''
driver = webdriver.Remote('http://localhost:4723/wd/hub', get_devices.capabilities()[0])
import os
while True:
    # os.popen("adb shell /system/bin/uiautomator dump --compressed /data/local/tmp/uidump.xml")
    # os.popen("adb pull /data/local/tmp/uidump.xml")
    import xml
    try:
        D = DumpParser('uidump.xml')
        for value in D.get_element_path():
            try:
                d = KeyWords(driver)
                d.wait(25)
                # d.swipe_left(4)
                d.click(*(By.XPATH, value))
                import random
                d.send_keys(random.randint(4700, 4900),  *(By.XPATH, value))
            except Exception as error:
                logger.warning(value)
                logger.warning(error)
                break
    except (xml.etree.ElementTree.ParseError, PermissionError, UnboundLocalError):
        # try:
        #     os.remove('uidump.xml')
        # except FileNotFoundError:
        #     continue
        continue
