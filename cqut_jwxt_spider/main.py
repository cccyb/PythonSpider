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

        # print '模拟登录教务系统,然后嘿嘿!(比如获取四六级成绩)  →_→ '
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
        soup2 = content[1]

        main_url = page2.geturl()  # 登录成功后教务系统主页url

        xscjcx_url = re.sub(r'xs_main', 'xscjcx', main_url) + '&xm=陈钰博&gnmkdm=N121604'  # 查询四六级成绩url

        headers2 = {
            'Host': self.Host,
            'Referer': main_url,
            'User-Agent': self.User_Agent,
        }

        content = self.getPage(xscjcx_url, headers=headers2)
        soup3 = content[1]

        __EVENTTARGET = soup3.find('input', attrs={'name': '__EVENTTARGET'}).attrs['value']
        __EVENTARGUMENT = soup3.find('input', attrs={'name': '__EVENTARGUMENT'}).attrs['value']
        __VIEWSTATE = soup3.find('input', attrs={'name': '__VIEWSTATE'}).attrs['value']
        hidLanguage = ''
        # ddlXN = soup3.find('select', id='ddlXN').find_all('')
        ddlXN = ''
        # ddlXQ = soup3.find('select', id='ddlXQ').find('option', attrs={'selected': 'selected'}).get_text()
        ddlXQ = ''
        # ddl_kcxz = soup3.find('select', id='ddl_kcxz').find('option', attrs={'selected': 'selected'}).attrs['value']
        ddl_kcxz = ''
        btn_zcj = soup3.find('input', attrs={'name': 'btn_zcj'}).attrs['value']

        # print __EVENTTARGET
        # print __EVENTARGUMENT
        # print __VIEWSTATE
        # print hidLanguage
        # print ddlXN
        # print ddlXQ
        # print ddl_kcxz
        # print btn_zcj

        postdata2 = urllib.urlencode({
            '__EVENTTARGET': __EVENTTARGET,
            '__EVENTARGUMENT': __EVENTARGUMENT,
            '__VIEWSTATE': __VIEWSTATE,
            'hidLanguage': hidLanguage,
            'ddlXN': ddlXN,
            'ddlXQ': ddlXQ,
            'ddl_kcxz': ddl_kcxz,
            'btn_zcj': btn_zcj.encode('gb2312', 'replace'),
        })

        content = self.getPage(xscjcx_url, postdata2, headers2)
        soup4 = content[1]
        row = soup4.find(class_='datelist').find_all('tr')[2]
        for item in row.find_all('td'):
            print item

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


# 程序主入口
cqut = CQUT(root_url)
cqut.start()

