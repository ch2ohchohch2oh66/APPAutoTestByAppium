#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/3/16
# Description: Keep Hungry Keep Foolish

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

desired_caps = {
  'platformName': 'Android', # 被测终端系统类型
  'platformVersion': '12', # 系统版本
  'deviceName': 'MyHwPhone', # 设备名，安卓手机可以随意填写
  'appPackage': 'tv.danmaku.bili', # 启动APP Package名称
  'appActivity': 'tv.danmaku.bili.MainActivityV2', # 启动Activity名称
  'unicodeKeyboard': True, # 自动化需要输入中文时填True
  'resetKeyboard': True, # 执行完程序恢复原来输入法
  'noReset': True,       # 不要重置App
  'newCommandTimeout': 6000,
  'automationName' : 'UiAutomator2'
}

# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub',
  options=UiAutomator2Options().load_capabilities(desired_caps))

# 设置缺省等待时间
driver.implicitly_wait(5)

# 如果有`青少年保护`界面，点击`我知道了`
iknow = driver.find_elements(By.ID, "text3")
if iknow:
    iknow.click()

# 等待搜索框可交互
wait = WebDriverWait(driver, 10)
sbox = wait.until(EC.element_to_be_clickable((By.ID, 'search_text')))

# 点击输入框
sbox.click()

# 再次查找元素并发送文本
sbox = wait.until(EC.element_to_be_clickable((By.ID, 'search_src_text')))
sbox.click()
sbox.send_keys('哪吒')

# 输入回车键，确认搜索
driver.press_keycode(AndroidKey.ENTER)

# 等待视频列表加载完毕
eles = wait.until(EC.presence_of_all_elements_located((By.ID, 'title')))

# 打印视频标题
for ele in eles:
    print(ele.text)

input('**** Press to quit..')
driver.quit()
