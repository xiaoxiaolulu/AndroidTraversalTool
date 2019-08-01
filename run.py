from lib.utils import get_devices
from appium import webdriver
from lib.public.parser import DumpParser
from lib.public.logger import logger
import selenium

'''测试代码'''
D = DumpParser('uidump.xml')
for value in D.get_element_path():
    print(value)
# driver = webdriver.Remote('http://localhost:4723/wd/hub', get_devices.capabilities()[0])
# driver.implicitly_wait(15)
# D = DumpParser('uidump.xml')
# for value in D.get_element_path():
#     try:
#         driver.find_element_by_xpath(value).click()
#         logger.debug('Click element xpath is {}'.format(value))
#     except selenium.common.exceptions.NoSuchElementException:
#         logger.warning(value)
#         continue
