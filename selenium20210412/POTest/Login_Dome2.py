from POTest.POtest_Dome1 import Action
from selenium.webdriver.common.keys import Keys

class Login(Action):

    input_name_loc = ('xpath', '//input[@placeholder=‘邮箱帐号或手机号码’]')
    input_password_loc = ('xpath', '//input[@placeholder=‘输入密码’]')
    enter_login_loc = Keys.ENTER
    frame_loc = (0)

    def __init__(self, driver, page_url=None, page_title=None):
        # Action.__init__(self, driver, page_url, page_title)
        super().__init__(driver, page_url, page_title)

    def open(self):
        """打开页面"""
        self._open(self.page_url, self.page_title)


    def change_frame(self):
        """切换frame"""
        self.switch_frame(self.frame_loc)


    def input_name(self, login_name):
        """输入登录名"""
        self.send_keys(self.input_name_loc, login_name)


    def input_password(self, login_password):
        """输入密码"""
        self.send_keys(self.input_password_loc, login_password)


    def enter_login(self):
        """模拟登陆点击回车"""
        self.send_keys(self.input_password_loc, self.enter_login_loc, False)


    def get_login_message(self):
        """获取登录后的信息以断言"""
        return self.driver.title
