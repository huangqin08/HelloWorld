from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote
import pandas as pd
from datetime import datetime

# 参数修改区域
user=""
passwd=""
订单状态填写 = '待发货'
支付状态填写 = '已支付'
开始时间填写 =  datetime.now().strftime('%Y-%m-%d')
商品名称填写 = ''
#订单状态填写 = ''
#支付状态填写 = '未支付'
#开始时间填写 = '2021-07-13'
#商品名称填写 = ''

# 启动浏览器
options = Options()
# options.headless = True

driver = webdriver.Chrome('C:\\ruoyi\\chromedriver_win32\\chromedriver', options=options)

url = ""
driver.get(url)

# 登录
userElem = driver.find_element_by_xpath('//*[@id="txtUserName"]')
userElem.clear()
userElem.send_keys(user)

passwdElem = driver.find_element_by_xpath('//*[@id="txtPassword"]')
passwdElem.clear()
passwdElem.send_keys(passwd)

loginElem = driver.find_element_by_xpath('//*[@id="btnSave"]')
loginElem.click()

driver.implicitly_wait(2)

# 进入表单
订单管理 = driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[1]/div[1]/div[2]/ul/li[4]/span')
订单管理.click()
订单管理_订单管理 = driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[1]/div[1]/div[2]/ul/li[4]/a[1]')
订单管理_订单管理.click()

# 填写查询条件
订单状态 = Select(driver.find_element_by_xpath('//*[@id="ddlOrderStatus"]'))
订单状态.select_by_visible_text(订单状态填写)

支付状态 = Select(driver.find_element_by_xpath('//*[@id="ddlPayStatus"]'))
支付状态.select_by_visible_text(支付状态填写)

开始时间= driver.find_element_by_xpath('//*[@id="txtStartTime"]')
开始时间.clear()
开始时间.send_keys(开始时间填写)

商品名称 = driver.find_element_by_xpath('//*[@id="txtProductName"]')
商品名称.clear()
商品名称.send_keys(商品名称填写)

查询 = driver.find_element_by_xpath('//*[@id="ImageButton2"]')
查询.click()

try:
	导出Excel = driver.find_element_by_xpath('//*[@id="btnUpdate1"]')
	导出Excel.click()
except NoSuchElementException:
	print('没有查询到数据')
	driver.close()
	exit()

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
# 等待下载完成并返回路径
paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
xls_path = unquote(paths[0])[8:]
xls_path = xls_path.replace('/', '\\')
print('导出完成，文件在{}'.format(xls_path))

# 删除导出文件的第一行空白
xlsx_path = xls_path.split('.')[0] + '.xlsx'
df = pd.read_excel(xls_path, skiprows=1)
df.to_excel(xlsx_path, index=False)
print('转换完成，文件在{}'.format(xlsx_path))

driver.close()