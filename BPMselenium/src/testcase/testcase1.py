# coding=utf-8
'''
Created on 2016-7-22
@author: Jennifer
Project:登录百度测试用例
'''
import os
from HTMLTestRunner import HTMLTestRunner
from selenium import webdriver
import unittest, time

from config.settings import chrome_driver_path


class BaiduTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.base_url = "https://www.baidu.com"

    def test_baidu(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("unittest")
        driver.find_element_by_id("su").click()
        time.sleep(3)
        title = driver.title
        self.assertEqual(title, u"unittest_百度搜索")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
