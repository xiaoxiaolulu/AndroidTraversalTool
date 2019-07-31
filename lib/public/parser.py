from lib.public.logger import logger

try:
    import xml.etree.CElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class DumpParser(object):

    AndroidNodeClassTypeList = [
        'android.widget.TextView',
        'android.widget.ImageView',
        'android.widget.EditText',
        'android.widget.Button',
        'android.widget.CheckBox',
        'android.widget.RadioGroup',
        'android.widget.Toast',
        'android.widget.Spinner',
        'android.widget.ListView',
        'android.widget.TabHost',
        'android.widget.AutoCompleteTextView',
        'android.widget.RatingBar'
        'android.widget.TableLayout',
        'android.widget.RelativeLayout',
        'android.widget.FrameLayout',
        'android.widget.AbsoluteLayout'
        'android.widget.LinearLayout',
        'android.widget.RadioButton',
        'android.widget.ToggleButton',
        'android.widget.AnalogClock',
        'android.widget.DigitalClock',
        'android.widget.DatePicker',
        'android.widget.TimePicker'
    ]

    def __init__(self, filepath: str):
        self.path = filepath

    @property
    def get_element_list(self) -> list:
        r"""解析uidump.xml文件并将其中包含的控件元素以列表的形式返回.
        """
        try:
            tree = ET.parse(self.path)
            nodes = tree.getiterator("node")
            if len(nodes) == 0:
                for tag in self.AndroidNodeClassTypeList:
                    nodes.extend(tree.getiterator(tag))
            element = []
            for node in nodes:
                element.append(node.attrib)
            return element
        except (FileNotFoundError, FileExistsError):
            logger.warning("File {} not found, please check the corresponding path".format(self.path))

    def get_element_path(self) -> list:
        r"""获取元素xpath定位信息，并以list类型数据返回
        """

        node = self.get_element_list

        if isinstance(node, list):
            element = []
            for tags in node:
                text = tags['text'] if tags['text'] != '' else None
                resource_id = tags['resource-id'] if tags['resource-id'] != '' else None

                if text and resource_id is None:
                    element.append("//*[@text='{}']".format(text))
                if resource_id  and text is None:
                    element.append("//*[@resource-id='{}']".format(resource_id ))
                if text and resource_id:
                    element.append("//*[@resource-id='{}'][@text='{}']".format(resource_id , text))
        return element
