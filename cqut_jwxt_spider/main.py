# coding:utf-8
import cookielib
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup

root_url = 'http://jwxt.i.cqut.edu.cn/'  # 教务系统网站入口地址

# 重庆理工大学教务系统模拟登录类
class CQUT():
    def __init__(self, root_url):
        self.root_url = root_url
        self.checkCodeUrl = 'CheckCode.aspx'  # 验证码url名字
        self.file_name = 'checkCode.jpg'  # 验证码图片名
        self.Host = 'jwxt.i.cqut.edu.cn'  # host
        self.User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.RadioButtonList1 = u"学生".encode('gb2312', 'replace')  # 登录人员类型

    def start(self):
        content = self.getPage(self.root_url)
        soup = content[1]
        redirect_url = content[2]

        __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'}).attrs['value']
        checkCode_url = re.sub(r'default2.aspx', self.checkCodeUrl, redirect_url)  # 验证码图片地址

        print '模拟登录教务系统,然后嘿嘿!(比如获取四六级成绩)  →_→ '
        userName = raw_input("请输入学号:")
        password = raw_input("请输入密码:")

        checkCode = self.getCheckCode(checkCode_url)  # 得到验证码数字

        # 登录
        # headers
        headers = {
            'Host': self.Host,
            'Referer': redirect_url,
            'User-Agent': self.User_Agent
        }

        # post数据
        postdata = urllib.urlencode({
            '__VIEWSTATE': __VIEWSTATE,
            'txtUserName': userName,
            'TextBox2': password,
            'txtSecretCode': checkCode,
            'RadioButtonList1': self.RadioButtonList1,
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': ''
        })

        content = self.getPage(redirect_url, postdata, headers)
        page2 = content[0]

        main_url = page2.geturl()  # 登录成功后教务系统主页url

        djkscx_url = re.sub(r'xs_main', 'xsdjkscx', main_url) + '&xm=陈钰博&gnmkdm=N121605'  # 查询四六级成绩url

        headers2 = {
            'Referer': main_url,
            'User-Agent': self.User_Agent
        }

        # 获取指定板块内容
        content = self.getPage(djkscx_url, headers=headers2)
        soup3 = content[1]

        self.printData(soup3)

    # 爬取指定url的解析完成的网页内容
    def getPage(self, url, postdata=None, headers=None):
        try:
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            if postdata is None:
                if headers is None:
                    request = urllib2.Request(url)
                else:
                    request = urllib2.Request(url, headers=headers)
            else:
                if headers is not None:
                    request = urllib2.Request(url, postdata, headers)
            page = opener.open(request)
            redirect_url = opener.open(request).geturl()  # 得到重定向url
            soup = BeautifulSoup(page, 'html.parser')
            return page, soup, redirect_url
        # 无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"爬取失败,错误原因", e.reason
                return None

    # 返回验证码
    def getCheckCode(self, checkCode_url):
        # 下载验证码
        conn = urllib2.urlopen(checkCode_url)
        f = open(self.file_name, 'wb')
        f.write(conn.read())
        print '验证码已下载至:', os.path.abspath(self.file_name), ' 请查看后输入'
        f.close()

        # 手动输入验证码
        checkCode = raw_input("验证码是:")
        return checkCode

    # 打印数据
    def printData(self, soup):

        table = soup.find(class_='datelist')

        tr = table.find_all('tr')

        for row in tr:
            count = 0
            for item in row.find_all('td'):
                if count == 6:  # 只打印前7项数据
                    break
                print item.get_text().center(10),
                count += 1
            print '\n'

# 程序主入口
cqut = CQUT(root_url)
cqut.start()

