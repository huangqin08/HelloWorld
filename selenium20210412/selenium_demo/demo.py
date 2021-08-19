from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()
# driver.get('https://oatest.guojingold.com/default/coframe/auth/login/loginFront.jsp')
# driver.find_element_by_id('userId$text').send_keys('009410')
# driver.find_element_by_id('password$text').send_keys('000000')
# # driver.find_element_by_class_name('button-login').click()
# driver.find_element_by_css_selector('#form1 > div.login-btn.center > div').click()


driver.get('https://mail.126.com/')

iframe = driver.find_elements_by_tag_name("iframe")[0]
driver.switch_to.frame(iframe)
driver.find_element_by_xpath('//input[@data-placeholder="邮箱帐号或手机号码"]').send_keys('huangqin_08')
driver.find_element_by_xpath('//input[@data-placeholder="输入密码"]').send_keys('0huangqin520')
driver.find_element_by_xpath('//*[@id="dologin"]').click()
# driver.find_element_by_id('userId$text').send_keys('009410')
# driver.find_element_by_id('password$text').send_keys('000000')
# driver.find_element_by_css_selector('#form1 > div.login-btn.center > div').click()
