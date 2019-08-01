import os
import random
import re
import time
from PIL import ImageDraw, Image
from appium import webdriver
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common import exceptions as Ex
from selenium.webdriver.support.wait import WebDriverWait
from lib.public.logger import logger


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_the_instance'):
            cls._the_instance = object.__new__(cls)
        return cls._the_instance


class KeyWords(Singleton):

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver

    def set_again(self, driver: webdriver.Remote):
        """
        Single case mode, when Dr Changes, reset.

        :Args:
         - driver: Create a new driver that will issue commands using the wire protocol.
        """
        self.driver = driver
        return self

    def wait(self, seconds):
        """
        Sets an implicit wait for an element to be found

        :Args:
         - seconds: Amount of time to wait (in seconds)
        """
        start_time = time.time()
        self.driver.implicitly_wait(seconds)
        logger.info("Recessive waiting {0} seconds, Spend {1} seconds".format(seconds, time.time()-start_time))

    def key_code(self, num):
        """
        Sends a key_code to the device.

        :Args:
         - num: the key_code to be sent to the device, INT TYPE
        """
        start_time = time.time()
        try:
            self.driver.press_keycode(num)
            logger.info("The physical keyboard number for the operation is {0}, \
            Spend {1} seconds".format(num, time.time()-start_time))
        except Exception:
            logger.warning('The physical keyboard performs an error, Spend {0} seconds'.format(time.time()-start_time))
            raise

    def long_key_code(self, num):
        """
        Long press the physical keyboard

        :Args:
         - num: the key_code to be sent to the device, INT TYPE
        """
        start_time = time.time()
        try:
            self.driver.long_press_keycode(num)
            logger.info("Long press the physical keyboard number is{0}, Spend \
            {1} seconds".format(num, time.time()-start_time))
        except Exception:
            logger.warning("Long press the physical keyboard number is{0}, Spend \
            {1} seconds".format(num, time.time()-start_time))
            raise

    def key_event(self, arg):
        """
        Mobile keyboard operation event.

        :Args:
         - arg: Select parameters, default HOME,BACK,CAMERA, DICT TYPE
        """
        event_list = {'HOME': 3, 'BACK': 4, 'CAMERA': 27}
        if arg in event_list:
            self.key_code(int(event_list[arg]))

    def find_element(self, *loc):
        """
        Repackage the single element location method

        :Args:
         - loc: Element localizer, TUPLE TYPE
        """
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception:
            logger.warning('Please enter the correct targeting elements!')
            raise

    def save_screenshot_as_picture(self, filename):
        """
        Saves a screenshot of the current window to a PNG image file

        :Args:
         - filename: filename: The full path you wish to save your screenshot to. This
           should end with a `.png` extension.
        """
        start_time = time.time()
        try:
            _tmp_path = os.path.dirname(os.path.abspath(__file__))
            _tmp_path = os.path.join(_tmp_path, "../result/imgs/{}.png".format(filename))
            image = self.driver.get_screenshot_as_file(_tmp_path)
            logger.info("The screenshot is successful, the name of the picture is {0}, \
             Spend {1} seconds ".format(filename, time.time()-start_time))
            return image
        except Exception:
            logger.warning("Screenshots failed, Spend {0} seconds".format(time.time()-start_time))
            raise

    def get_latest_picture(self):
        """
        Get the latest screen shot picture.
        """
        start_time = time.time()
        try:
            _tmp_path = os.path.dirname(os.path.abspath(__file__))
            _tmp_path = os.path.join(_tmp_path, "../result/imgs/")
            dirs = os.listdir(_tmp_path)
            if dirs is not None:
                dirs.sort()
                new_image = dirs[-1]
                logger.info("Get the latest screenshot is {0}, spend {1} \
                seconds".format(new_image, time.time()-start_time))
                return new_image
            else:
                logger.warning("The directory {0} is empty".format(dirs))
        except FileNotFoundError:
            raise

    def find_elements(self, *loc, index=None, find_way='random'):
        """
        Repackage a set of element location methods.

        :Args:
         - loc: Element localizer, TUPLE TYPE
         - index: Element index, INT TYPE DEFAULT NONE
         - find_way: Element Location Method, STR TYPE DEFAULT RANDOM
        """
        try:
            if find_way == 'random':
                if len(self.driver.find_elements(*loc)) > 0:
                    num = random.randint(1, len(self.driver.find_elements(*loc)))
                    return self.driver.find_elements(*loc)[num]
            else:
                return self.driver.find_elements(*loc)[index]
        except Exception:
            logger.warning('No related elements are found in the interface.')
            raise

    def elements_click(self, *loc, index):
        """
        Click on one of the set of elements.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - index: Locate a set of element index values, INT TYPE
        """
        start_time = time.time()
        try:
            logger.info("Click the element <{0} -> {1}>,  Spend {2} \
            seconds".format(loc[0], loc[1], time.time() - start_time))
            return self.find_elements('normal', *loc)[index].click()
        except Exception:
            logger.warning("Click the element <{0} -> {1}>,  Spend {2} \
            seconds".format(loc[0], loc[1], time.time() - start_time))
            raise

    def random_click(self, *loc):
        """
        Random click on one of the elements.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            logger.info("Random click the element <{0} -> {1}>, Spend {2}\
            seconds ".format(loc[0], loc[1], time.time() - start_time))
            return self.find_elements(*loc).click()
        except Exception:
            logger.warning("No element found, click failure, Spend {0} seconds".format(time.time()-start_time))
            raise

    @staticmethod
    def change_element_name(*loc):
        """
        Element location removes illegal characters for automatic naming of screen shots picture.

        :Args:
        - loc：Element localizer, TUPLE TYPE.
        """
        if loc[0] in ['link text', 'name']:
            return loc[1]
        else:
            return re.sub('[\/:*?"<>|]', '-', loc[1])

    def red_element(self, *loc):
        """
        [image processing] marking the elements of the current operation with the matrix (red).

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        element = self.find_element(*loc)
        self.save_screenshot_as_picture(self.change_element_name(*loc))
        box = (element.location["x"], element.location["y"],
               element.location["x"] + element.size["width"],
               element.location["y"] + element.size["height"])
        _tmp_path = os.path.dirname(os.path.abspath(__file__))
        _tmp_path = os.path.join(_tmp_path, "../result/imgs/")
        new_image = os.path.join(_tmp_path, self.get_latest_picture())
        img = Image.open(new_image)
        draw = ImageDraw.Draw(img)
        draw.rectangle((box[0], box[1], box[2], box[3]), outline='#8B0000')
        return img.save(new_image)

    def get_element_image(self, *loc):
        """
        Just truncate an image of an element and save it to the corresponding file directory.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        element = self.find_element(*loc)
        self.save_screenshot_as_picture(self.change_element_name(*loc))
        box = (element.location["x"], element.location["y"],
               element.location["x"] + element.size["width"],
               element.location["y"] + element.size["height"])
        _tmp_path = os.path.dirname(os.path.abspath(__file__))
        _tmp_path = os.path.join(_tmp_path, "../result/imgs/")
        new_image = os.path.join(_tmp_path, self.get_latest_picture())
        img = Image.open(new_image)
        im = img.crop(box)
        _tmp2_path = os.path.dirname(os.path.abspath(__file__))
        _tmp2_path = os.path.join(_tmp_path, "../result/cimgs/")
        return im.save(_tmp2_path, self.change_element_name(*loc))

    def get_text(self, *loc):
        """
        Gets the element text value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            self.red_element(*loc)
            logger.info("Get the text <{0} -> {1}>, Spend {2} seconds".format(loc[0], loc[1], time.time() - start_time))
            return self.find_element(*loc).text
        except Exception:
            logger.warning("Gets the element text failed, Spend {0} seconds".format(time.time()-start_time))
            raise

    def click(self, *loc):
        """
        Click on the element

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            self.red_element(*loc)
            logger.info("Click the element <{0} -> {1}>, Spend {2} \
            seconds".format(loc[0], loc[1], time.time() - start_time))
            return self.find_element(*loc).click()
        except Exception:
            logger.warning("Element click failure, Spend {0} seconds".format(time.time()-start_time))
            raise

    def send_keys(self, value, *loc, clear_first=True):
        """
        Text input

        :Args:
         - clear_first: Clean up the contents in the input box, default Boolean value True.
         - loc: Element localizer, TUPLE TYPE.
         - value: The input Element location text value
        """
        start_time = time.time()
        try:
            if clear_first:
                self.find_element(*loc).clear()
            self.red_element(*loc)
            logger.info("Clear and input text to the element <{0} -> {1}> content: {2}, \
            Spend {3} time ".format(loc[0], loc[1], value, time.time() - start_time))
            return self.find_element(*loc).send_keys(value)
        except Exception:
            logger.warning("Element not found, text input failed, Spend {0} seconds".format(time.time()-start_time))
            raise

    def get_attribute(self, *loc, attribute):
        """
        Gets the element attribute value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - attribute: Element attributes, STR TYPE.
        """
        start_time = time.time()
        try:
            attr = self.find_element(*loc).get_attribute(attribute)
            logger.info("Gets the attribute {2} of the element <{0} -> {1} >, Spend {3} \
            seconds".format(loc[0], loc[1], attribute, time.time() - start_time))
            return attr
        except Exception:
            logger.warning("Gets the attribute {2} of the element <{0} -> {1} >, Spend \
             {3} seconds".format(loc[0], loc[1], attribute, time.time()-start_time))
            raise

    def text_in_element(self, loc, text, time_out=10):
        """
        Determines whether the expected text value is equal to the actual element text value.

        :Args:
         - loc: Element localizer, TUPLE TYPE.
         - text: Element location text value, STR TYPE.
         - time_out: Wait time, default 10 seconds, INT OR FLOAT TYPE.
        """
        start_time = time.time()
        try:
            WebDriverWait(self.driver, time_out, 0.5).until(Ec.text_to_be_present_in_element(loc, text))
            logger.info('the text: {0} in element <{1} -> {2} >, Spend {3}\
             seconds'.format(text, loc[0], loc[1], time.time()-start_time))
            return True
        except TimeoutError:
            logger.warning('the text: {0} not in element <{1} -> {2} >, Spend {3}\
             seconds'.format(text, loc[0], loc[1], time.time()-start_time))
            return False

    def sleep(self, seconds):
        """
        Sets an Mandatory wait for an element to be found

        :Args:
         - seconds: Amount of time to wait (in seconds)
        """
        time.sleep(seconds)
        logger.info("Mandatory waiting {0}".format(seconds))

    def quit(self):
        """
        Close the browser window.
        """
        start_time = time.time()
        self.driver.quit()
        logger.info('Close all browser Windows, Spend {0} seconds'.format(time.time()-start_time))

    def switch_to_h5(self, *loc):
        """
        Switch to the  H5 interface

        :Args:
         - loc: Element localizer, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            current_windows = self.driver.current_context
            self.click(*loc)
            self.wait(3)
            all_windows = self.driver.contexts
            if len(all_windows) > 1:
                for handle in all_windows:
                    if handle != current_windows:
                        self.driver.switch_to.context(handle)
                logger.info('Switch to the H5 interface, Spend {0} seconds'.format(time.time() - start_time))
        except Exception:
            logger.warning('Switch to the H5 interface, Spend {0} seconds'.format(time.time() - start_time))
            raise

    def switch_to_native(self):
        """
        Switch to the  native page
        """
        start_time = time.time()
        try:
            current_windows = self.driver.current_context
            all_windows = self.driver.contexts
            if len(all_windows) > 1:
                for handle in all_windows:
                    if handle != current_windows:
                        self.driver.switch_to.context(handle)
                logger.info('Switch to the native page, Spend {0} seconds'.format(time.time() - start_time))
        except Exception:
            logger.warning('Switch to the native page, Spend {0} seconds'.format(time.time() - start_time))
            raise

    def js(self, script):
        """
        Execute the js script

        :Args:
         - script: JavaScript, STR TYPE.
        """
        start_time = time.time()
        try:
            self.driver.execute_script(script)
            logger.info(" Execute the JS script is {0}, Spend {1} seconds".format(script, time.time()-start_time))
        except Exception:
            logger.warning('JS script execution fails.')
            raise

    @property
    def get_width(self):
        """
        Get the phone screen width.
        """
        return self.driver.get_window_size()['width']

    @property
    def get_height(self):
        """
        Get the phone screen height.
        """
        return self.driver.get_window_size()['height']

    def swipe_down(self, count=1, timeout=500):
        """
        The phone screen slides down.

        :Args:
         - count: Slide number, INT TYPE.
         - timeout: Slide duration, default 500.
        """
        width, height = self.get_width, self.get_height
        start_time = time.time()
        try:
            while count:
                self.driver.swipe(width*0.5, height*0.25, height*0.75, timeout)
                count -= 1
            logger.info("The phone screen slides down {0} count, Spend {1}".format(count, time.time()-start_time))
        except Exception:
            logger.warning("The phone screen slides down {0} count, Spend {1}".format(count, time.time()-start_time))
            raise

    def swipe_left(self, count=1, timeout=500):
        """
        The phone screen slides to the left.

        :Args:
         - count: Slide number, INT TYPE.
         - timeout: Side duration, default 500.
        """
        width, height = self.get_width, self.get_height
        start_time = time.time()
        try:
            while count:
                self.driver.swipe(width*0.75, height*0.5, width*0.05, timeout)
                count -= 1
            logger.info("The phone screen slides left {0} count, Spend {1}".format(count, time.time()-start_time))
        except Exception:
            logger.warning("The phone screen slides left {0} count, Spend {1}".format(count, time.time()-start_time))
            raise

    def reset(self):
        """
        Reset the application
        """
        self.driver.reset()

    def is_select(self, *loc):
        """
        Check whether the control is selected.

        :Args:
         - loc: Element locator, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            self.find_element(*loc).is_selected()
            logger.info('The element <{0} -> {1} > has been selected,\
            Spend {2} seconds'.format(loc[0], loc[1], time.time()-start_time))
            return True
        except (Ex.NoSuchElementException, Ex.ElementNotSelectableException, Ex.TimeoutException):
            logger.warning('The element <{0} -> {1} > has not been selected,\
            Spend {2} seconds'.format(loc[0], loc[1], time.time()-start_time))
            return False

    def element_scroll(self, el_loc, tar_loc):
        """
        ELEMENT SCROLL

        :Args:
         - el_loc: drag locator, TUPLE TYPE.
         - tar_loc: target locator, TUPLE TYPE.

        :Usage:
            driver.element_scroll(*drap_locator, *target_locator)
        """
        start_time = time.time()
        try:
            element = self.find_element(*el_loc)
            target = self.find_element(*tar_loc)
            self.driver.scroll(element, target)
            logger.info('element <{0} -> {1} > scroll to element <{2} -> {3} >,\
             Spend {4} seconds'.format(el_loc[0], el_loc[1], tar_loc[0], tar_loc[1], time.time()-start_time))
        except Exception:
            logger.warning('element scroll fail,Spend {0} seconds'.format(time.time()-start_time))
            raise

    def drag_and_drop(self, el_loc, tar_loc):
        """
        Mouse drag and drop event

        :Args:
         - el_loc: drag locator, TUPLE TYPE.
         - tar_loc: target locator, TUPLE TYPE.
        """
        start_time = time.time()
        try:
            element = self.find_element(*el_loc)
            target = self.find_element(*tar_loc)
            self.driver.drag_and_drop(element, target)
            logger.info('element <{0} -> {1} > move to element <{2} -> {3} >, \
            Spend {4} seconds'.format(el_loc[0], el_loc[1], tar_loc[0], tar_loc[1], time.time()-start_time))
        except Exception:
            logger.warning('drag and drop fail,Spend {0} seconds'.format(time.time()-start_time))
            raise

    def tap(self, *coordinates, timeout=10):
        """
        Simulate finger click

        :Args:
         - coordinates: coordinates, TUPLE OR LIST TYPE.
         - timeout: Duration,DEFAULT 10.
        """
        start_time = time.time()
        try:
            self.driver.tap(*coordinates, timeout)
            logger.info('Simulate finger click, Spend {0}'.format(time.time()-start_time))
        except Exception:
            logger.warning('Simulate finger click failure, Spend {0}'.format(time.time()-start_time))
            raise

    def background_app(self, timeout=5):
        """
        App background operation

        :Args:
         - timeout: Duration, DEFAULT 5, STR TYPE.
        """
        start_time = time.time()
        try:
            self.driver.background_app(timeout)
            logger.info("App background operation {0} seconds, Spend {1}\
             seconds".format(timeout, time.time()-start_time))
        except Exception:
            logger.warning("App background running failure.")
            raise

    def check_install_app(self, package):
        """
        Check to see if the app is installed.

        :Args:
         - package: app install package, STR TYPE.
        """
        start_time = time.time()
        self.driver.is_app_installed(package)
        logger.info("Installed app {0}, Spend {1} seconds".format(package, time.time()-start_time))

    def close_app(self):
        """
        Stop app running application
        """
        start_time = time.time()
        self.driver.close_app()
        logger.info("Close the app, Spend {0} seconds".format(time.time()-start_time))

    def shake_device(self):
        """
        Shake the device
        """
        start_time = time.time()
        self.driver.shake()
        logger.info("Shake the driver, Spend {0} seconds".format(time.time()-start_time))

    def start_toggle_location_services(self):
        """
        Toggle the location services on the device
        """
        start_time = time.time()
        self.driver.toggle_location_services()
        logger.info("Toggle the location services on the device".format(time.time()-start_time))

    def get_page_source(self):
        """
        Gets the source of the current page
        """
        start_time = time.time()
        logger.info("Gets the source of the current page".format(time.time()-start_time))
        return self.driver.page_source
