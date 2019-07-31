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

    def get_element_list(self) -> list:
        r"""解析uidump.xml文件并将其中包含的空间元素以列表的形式返回.
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

