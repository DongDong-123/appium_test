# coding:utf-8
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time, os
from readConfig import ReadConfig


def login():
    username, password = ReadConfig().get_user(), ReadConfig().get_password()
    desired_caps = {'platformName': 'Android',
                    'deviceName': '127.0.0.1:62001',
                    'platformVersion': '5.1.1',
                    'noReset': True,
                    'browserName': 'Chrome'
                    }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    print('浏览器启动成功')

    driver.get(ReadConfig().get_root_url())
    print(driver.contexts)
    driver.switch_to.context('NATIVE_APP')
    print('切换到原始APP成功')

    driver.switch_to.context('CHROMIUM')
    print('切换到CHROMIUM成功')
    driver.find_element_by_id("appLogin").click()
    driver.find_element_by_xpath("//div[@class='login-item']/a[2]").click()
    # 输入账号密码
    driver.find_element_by_id("tb_user").send_keys(username)
    driver.find_element_by_id("tb_password").send_keys(password)

    driver.find_element_by_xpath("//div[@class='submit']").click()
    return driver


if __name__ == '__main__':
    login()
