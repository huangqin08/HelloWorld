# conding :utf-8
import os
import time
import unittest  # 构建测试集，包含src/testsuite目录下的所有以test开头的.py文件

from HTMLTestRunner import HTMLTestRunner

case_path = os.path.join(os.getcwd(), 'src/testcase')
suite = unittest.defaultTestLoader.discover(start_dir=case_path, pattern='test*.py')

if __name__ == '__main__':
    # runner=HTMLTestRunner.HTMLTestRunner(stream=fb,title=u'邮件报告的描述',description=u'测试Team')
    # runner.run(suite)
    # filePath = '\\report\\Report.html'  # 确定生成报告的路径
    filePath = os.path.join(os.getcwd(), 'report\\Report.html')
    fp = open(filePath, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'自动化测试报告',
        # description='详细测试用例结果',    #不传默认为空
        # tester=u"Findyou"  # 测试人员名字，不传默认为QA
    )
    runner.run(suite)
    # 运行测试用例
    fp.close()
