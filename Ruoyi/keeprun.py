import os
import time
from datetime import datetime

interval = 1

while True:
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    	os.system("taskkill /f /im chromedriver.exe")
	os.system("taskkill /f /im chrome.exe")
	os.system('python ruoyi.py')
	time.sleep(interval)