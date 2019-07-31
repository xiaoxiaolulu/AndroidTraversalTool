#  2019-07-31
1. 新建项目
```text
使用 uiautomator dump 获取app上的页面元素
1. adb shell /system/bin/uiautomator dump --compressed /data/local/tmp/uidump.xml
2. adb pull /data/local/tmp/uidump.xml C:/Users/cxy-07-03/Desktop 
```