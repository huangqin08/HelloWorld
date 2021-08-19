from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 参数修改区域
user=""
passwd=""
# 手动填写excel文件路径
# xlsx_path = ""
# 使用自动导出的文件路径
from yunshangcheng import xlsx_path, xls_path

# 启动浏览器
driver = webdriver.Chrome('C:\\ruoyi\\chromedriver_win32\\chromedriver')
url = ""
driver.get(url)

# 登录
userElem = driver.find_element_by_xpath('//*[@id="signupForm"]/input[1]')
userElem.clear()
userElem.send_keys(user)

passwdElem = driver.find_element_by_xpath('//*[@id="signupForm"]/input[2]')
passwdElem.clear()
passwdElem.send_keys(passwd)

loginElem = driver.find_element_by_xpath('//*[@id="btnSubmit"]')
loginElem.click()

driver.implicitly_wait(2)

# 找到导入页面
功能管理边栏按钮 = driver.find_element_by_xpath('//*[@id="side-menu"]/li[6]/a')
功能管理边栏按钮.click()

渠道订单导入及匹配按钮 = driver.find_element_by_xpath('//*[@id="side-menu"]/li[6]/ul/li[5]/a')
渠道订单导入及匹配按钮.click()

def frame_switch(xpath):
    driver.switch_to.frame(driver.find_element_by_xpath(xpath))

frame_switch('//*[@id="content-main"]/iframe[2]')

导入按钮 = driver.find_element_by_xpath('//*[@id="toolbar"]/a[1]')
导入按钮.click()

上传按钮 = driver.find_element_by_xpath('//*[@id="file"]')
上传按钮.send_keys(xlsx_path)

time.sleep(2) # 等待上传
try:
	确认导入按钮 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
		(By.CSS_SELECTOR, '#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0')))
	确认导入按钮.click()
except TimeoutException:
	print("确认导入失败")
	driver.close()
	exit()

time.sleep(2) # 等待导入
导入表格第一行 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
	(By.XPATH, '//*[@id="table"]/tbody/tr[1]')))
try:
	导入表格第一行 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
		(By.XPATH, '//*[@id="table"]/tbody/tr[1]')))
except TimeoutException:
	print("导入失败，导入后没发现表格数据")
	driver.close()
	exit()

# 点击提交
try:
	提交按钮 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
			(By.XPATH, '//*[@id="saveBtn"]')))
	提交按钮.click()
except TimeoutException:
	print("找不到提交按钮")
	driver.close()
	exit()
except:
	print("提交失败")
	driver.close()
	exit()

try:
	保存订单确认 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
			(By.XPATH, '//*[@id="layui-layer3"]/div[3]/a[1]')))
	保存订单确认.click()
except TimeoutException:
	print("找不到保存确认")
	driver.close()
	exit()

time.sleep(2) # 等待保存
try:
	保存成功确认 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
			(By.XPATH, '//*[@id="layui-layer4"]/div[3]/a')))
	保存成功确认.click()
except TimeoutException:
	print("找不到保存成功确认")
	driver.close()
	exit()

print('保存成功')
driver.close()

# 打印导入状态
# try:
# 	导入状态 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
# 		(By.XPATH, '//*[@id="layui-layer3"]/div[2]')))
# 	print(导入状态.text)
# 	确认按钮 = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
# 		(By.XPATH, '//*[@id="layui-layer3"]/div[3]/a')))
# 	确认按钮.click()
# except TimeoutException:
# 	print("找不到导入状态")
# 	driver.close()
# 	exit()