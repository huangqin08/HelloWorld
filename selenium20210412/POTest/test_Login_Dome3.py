# -*- coding: UTF-8 -*-
import unittest
from time import sleep
from POTest.Login_Dome2 import Login
from selenium import webdriver
from ddt import ddt,data

class Demo(unittest.TestCase):

    def setUp(self):
        self.url = "https://mail.163.com/"
        self.title = "网易"
        self.user_name = "009410"  # 登录账户
        self.user_password = ""  # 登录密码
        self.driver = webdriver.Chrome()

    def test_wangyi_login(self):
        """登录网易邮箱"""
        login_page = Login(self.driver, self.url, self.title)
        login_page.open()
        login_page.change_frame()
        sleep(3)
        login_page.input_name(self.user_name)
        login_page.input_password(self.user_password)
        sleep(2)
        login_page.enter_login()
        sleep(5)
        print(login_page.get_login_message())
        assert "网易邮箱6.0版" in login_page.get_login_message()

    def tearDown(self):
        self.driver.close()

if __name__ == " __main__ ":
    unittest.main()
