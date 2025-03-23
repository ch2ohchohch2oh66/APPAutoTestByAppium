#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Andy Freeman
# Date: 2025/3/16
# Description: Keep Hungry Keep Foolish
import logging
import time

from appium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

logger.info('**** 测试开始 ****')
# 连接Appium Server，初始化自动化环境
logger.info('连接Appium Server')
driver = webdriver.Remote('http://localhost:4723/wd/hub',
  options=UiAutomator2Options().load_capabilities(desired_caps))
logger.info('连接Appium Server成功')

# 设置缺省等待时间
driver.implicitly_wait(5)
time.sleep(5)

# 如果有`青少年保护`界面，点击`我知道了`
iknow = driver.find_elements(By.ID, "text3")
if iknow:
  logger.info('处理青少年保护弹窗')
  iknow.click()
else:
  logger.info('青少年保护弹窗不存在')

# 等待搜索框可交互
wait = WebDriverWait(driver, 10)
logger.info('等待搜索框可交互')
sbox = wait.until(EC.element_to_be_clickable((By.ID, 'expand_search')))
logger.info('搜索框可交互')
sbox.click()

# 再次查找元素并发送文本
logger.info('等待搜索框可交互')
sbox = wait.until(EC.element_to_be_clickable((By.ID, 'search_src_text')))
logger.info('搜索框可交互')
sbox.click()
logger.info('清空搜索框')
sbox.clear()
logger.info('输入搜索文本')
sbox.send_keys('哪吒')

# 输入回车键，确认搜索
logger.info('输入回车键')
driver.press_keycode(AndroidKey.ENTER)

# 等待视频列表加载完毕
try:
    logger.info('开始等待视频列表加载')
    eles = wait.until(EC.presence_of_all_elements_located((By.ID, 'title')))
    logger.info(f'视频列表加载完毕，共找到 {len(eles)} 个视频')
except TimeoutException as e:
    logger.error(f'视频列表加载超时：{e}')
    eles = []  # 如果加载失败，设置为空列表以避免后续代码报错

# 打印视频标题
if not eles:
    logger.info('视频列表为空，无标题可打印')
else:
    logger.info('开始遍历视频列表，打印视频标题')
    for ele in eles:
        logger.info(ele.text)
    logger.info('视频标题打印结束')


logger.info('**** 测试结束 ****')
time.sleep(3)
driver.quit()

