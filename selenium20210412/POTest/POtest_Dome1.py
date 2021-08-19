from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Action(object):
    """
    Action封装所有页面都公用的方法
    """

    # 初始化driver、url、title等
    def __init__(self, driver, page_url=None, page_title=None):
        self.page_url = page_url
        self.page_title = page_title
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

    def open(self):
        """
        定义open方法，调用_open()进行打开链接
        """
        self._open(self.page_url, self.page_title)

    def on_page(self, page_title):
        """
        使用current_url获取当前窗口Url地址，进行与配置地址作比较，返回比较结果（True False）
        """
        return page_title in self.driver.title

    def _open(self, page_url, page_title):
        """
        打开页面，校验页面链接是否加载正确
        """
        # 使用get打开访问链接地址
        if page_url and page_title is not None:
            self.driver.get(page_url)
            print("打开网址：%s" % page_url)
            print("网址预期标题: %s" % page_title)
            # 使用assert进行校验，打开的链接地址是否与配置的地址一致。调用on_page()方法
            assert self.on_page(page_title), u"打开页面%s失败" % page_url

    def find_element(self, *locator):
        try:
            print("定位元素:%s" % (locator,))
            return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(locator))
        except Exception as msg:
            print(u"%s 页面中未能找到 %s 元素" % (self, locator))
            print("错误信息%s" % msg)

    def send_keys(self, locator, value, clear_first=True):
        """
        重写定义send_keys方法
        """
        element = self.find_element(*locator)
        if clear_first:
            element.clear()
            element.send_keys(value)
        else:
            element.send_keys(value)
        print("输入值：%s" % value)

    def switch_frame(self, frame_loc):
        """
        切换frame，
        :param frame_loc:id、name、element、index
        :return:
        """
        self.driver.switch_to.frame(frame_loc)
