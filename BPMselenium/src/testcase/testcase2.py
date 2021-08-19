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
import selenium.webdriver.support.ui as ui
from config.settings import chrome_driver_path


class BPMTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_driver_path)
        self.base_url = "https://mail.126.com/"

    def test_BPM(self):
        driver = self.driver
        driver.get(self.base_url)
        print('代码运行到这了')
        time.sleep(5)
        iframe = driver.find_elements_by_tag_name("iframe")[1]
        driver.switch_to.frame(iframe)
        a=driver.find_element_by_xpath(".").get_attribute("id")
        print(a)
        # driver.switch_to.frame("x-URS-iframe")

        # driver.find_element_by_name("email").send_keys("123")
        # driver.find_element_by_name("password").send_keys("456")
        # driver.find_element_by_xpath('//form[@id="login-form"]').clear()
        # driver.find_element_by_name("email").send_keys("huangqin_08")
        # driver.find_element_by_name("password").send_keys("0huangqin520")
        # # wait = ui.WebDriverWait(driver, 5)
        # # wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="userId$text"]'))
        # # driver.find_element_by_xpath('//*[@id="userId$text"]').send_keys("009410")
        # #
        # # driver.find_element_by_class_name("mini-textbox-input")
        # driver.find_element_by_class_id("dologin-login").click()
        # time.sleep(3)
        # title = driver.title
        # self.assertEqual(title, u"unittest_BPM登录")
    #
    # def tearDown(self):
    #     self.driver.quit()


if __name__ == "__main__":
    unittest.main()
