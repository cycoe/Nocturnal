#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from requests import Session, Request, exceptions
from bs4 import BeautifulSoup
from modules.UrlBean import UrlBean
from modules.Logger import Logger
from modules.OutputFormater import OutputFormater


class Spider(object):
    """
    爬虫体
    """

    def __init__(self):
        self.urlBean = UrlBean()    # 实例化 url 管理对象
        self.session = Session()    # 实例化 session 对象，用于 handle 整个会话

        # 实例化验证码识别器对象
        # from modules.classifier import Classifier
        # self.classifier = Classifier()
        # self.classifier.loadTrainingMat()

        self.classFilter = [3, 4, 5, 6, 11, 12]
        self.speechFilter = [0, 1, 3, 4, 5, 6, 7]

        self.buttonPattern = re.compile('<a.*href=".*?\'(.*?)?\'.*".*><img.*>.*</a>')
        self.removeTd = re.compile('<td.*>(.*)?</td>')

    @staticmethod
    def formatHeaders(referer=None, contentLength=None, originHost=None):
        """
        生成请求的 headers

        :param referer: 跳转标记，告诉 web 服务器自己是从哪个页面跳转过来的
        :param contentLength: 未知
        :param originHost: 原始主机地址
        :returns: headers 字典
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'graduate.buct.edu.cn:8080',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'Referer': referer,
            'Content-Length': contentLength,
            'Origin': originHost,
        }

        return headers

    def getVIEWSTATE(self):
        """
        正则获取页面的 __VIEWSTATE

        :returns: 页面的 __VIEWSTATE
        """
        VIEWSTATE = re.findall('<.*name="__VIEWSTATE".*value="(.*)?".*/>', self.response.text)
        if len(VIEWSTATE) > 0:
            return VIEWSTATE
        else:
            return None

    def getEVENTVALIDATION(self):
        """
        正则获取页面的 __EVENTVALIDATION

        :returns: 页面的 __EVENTVALIDATION
        """
        EVENTVALIDATION = re.findall('<.*name="__EVENTVALIDATION".*value="(.*)?".*/>', self.response.text)
        if len(EVENTVALIDATION) > 0:
            return EVENTVALIDATION
        else:
            return None

    def prepare(self,
                referer=None,
                originHost=None,
                method='GET',
                url=None,
                data=None,
                params=None):
        """
        生成用于请求的 prepare

        :param referer: 跳转标记，告诉 web 服务器自己是从哪个页面跳转过来的
        :param originHost: 原始主机地址
        :param method: 请求方法 in ['GET', 'POST']
        :param url: 请求的 url 地址
        :param data: 封装的 post 数据
        :param params: post 参数
        :return: prepare 对象
        """
        headers = self.formatHeaders(referer=referer, originHost=originHost)
        req = Request(method, url, headers=headers, data=data, params=params)
        return self.session.prepare_request(req)

    # def prepareJwglFirst(self):
    #     headers = self.formatHeaders()
    #     req = Request('GET', self.urlBean.jwglLoginUrl, headers=headers)
    #     return self.session.prepare_request(req)
    #
    # def prepareFetchVerCode(self):
    #     headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl)
    #     req = Request('GET', self.urlBean.verifyCodeUrl, headers=headers)
    #     return self.session.prepare_request(req)
    #
    # def prepareJwglLogin(self):
    #     """
    #     实例化登录 jwgl 需要的 request
    #     __VIEWSTATE 和 __EVENTVALIDATION 可从网页源代码中获取
    #     """
    #     postData = {
    #         '__VIEWSTATE': self.VIEWSTATE,
    #         '__EVENTVALIDATION': self.EVENTVALIDATION,
    #         '_ctl0:txtusername': self.urlBean.userName,
    #         '_ctl0:txtpassword': self.urlBean.jwglPassword,
    #         '_ctl0:txtyzm': self.verCode,
    #         '_ctl0:ImageButton1.x': '43',
    #         '_ctl0:ImageButton1.y': '21',
    #     }
    #     headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl, originHost=self.urlBean.jwglOriginUrl)
    #     req = Request('POST', self.urlBean.jwglLoginUrl, headers=headers, data=postData)
    #     return self.session.prepare_request(req)
    #
    # def prepareJwglLoginDone(self):
    #     headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl)
    #     req = Request('GET', self.urlBean.jwglLoginDoneUrl, headers=headers)
    #     return self.session.prepare_request(req)
    #
    # def prepareFetchClassList(self):
    #     headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
    #     payload = {'xh': self.urlBean.userName}
    #     req = Request('GET', self.urlBean.fetchClassListUrl, headers=headers, params=payload)
    #     return self.session.prepare_request(req)
    #
    # def preparePostClass(self, classId):
    #     """
    #     实例化登录 jwgl 需要的 request
    #     __VIEWSTATE 和 __EVENTVALIDATION 可从网页源代码中获取
    #     """
    #     postData = {
    #         '__EVENTTARGET': 'dgData__ctl' + classId + '_Linkbutton1',
    #         '__EVENTARGUMENT': '',
    #         '__VIEWSTATE': self.VIEWSTATE,
    #         '__EVENTVALIDATION': self.EVENTVALIDATION,
    #     }
    #     headers = self.formatHeaders(referer=self.urlBean.fetchClassListUrl + '?xh=' + self.urlBean.userName, originHost=self.urlBean.jwglOriginUrl)
    #     payload = {'xh': self.urlBean.userName}
    #     req = Request('POST', self.urlBean.fetchClassListUrl, headers=headers, data=postData, params=payload)
    #     return self.session.prepare_request(req)

    def prepareFetchSchedule(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.userName}
        req = Request('GET', self.urlBean.fetchScheduleUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def prepareGetEnglishTest(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.userName}
        req = Request('GET', self.urlBean.englishTestUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def preparePostEnglishTest(self):
        """
        实例化登录 jwgl 需要的 request
        __VIEWSTATE 和 __EVENTVALIDATION 可从网页源代码中获取
        """
        postData = {
            '__EVENTTARGET': self.buttonId,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'WUCpyjhdy:HFpath': 'E:\gmis4.0\pyxx\pyxx\WordCells\djks.docx',
            'WUCpyjhdy:HFfilename': '等级考试确认单',
            'WUCpyjhdy:HFdatatype': '26',
        }
        headers = self.formatHeaders(referer=self.urlBean.englishTestUrl + '?xh=' + self.urlBean.userName, originHost=self.urlBean.jwglOriginUrl)
        payload = {'xh': self.urlBean.userName}
        req = Request('POST', self.urlBean.englishTestUrl, headers=headers, data=postData, params=payload)
        return self.session.prepare_request(req)

    def prepareFetchSpeechList(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.userName}
        req = Request('GET', self.urlBean.fetchSpeechListUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def login(self):
        """
        登录教务网
        """
        
        if self.urlBean.checkUserFile():
            self.urlBean.readUserInfo()
        else:
            self.urlBean.userName = input("> UserName: ")
            self.urlBean.password = input("> Password: ")

        prepareBody = self.prepare(referer=None,
                                   originHost=None,
                                   method='GET',
                                   url=self.urlBean.jwglLoginUrl,
                                   data=None,
                                   params=None)

        while True:
            self.response = self.session.send(prepareBody)  # GET 方法获取登录网站的 '__VIEWSTATE'
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            Logger.log("retrying fetching login page viewState...", Logger.info)

        while True:

            prepareBody = self.prepare(referer=self.urlBean.jwglLoginUrl,
                                       originHost=None,
                                       method='GET',
                                       url=self.urlBean.verifyCodeUrl,
                                       data=None,
                                       params=None)

            while True:
                codeImg = self.session.send(prepareBody)  # 获取验证码图片
                if codeImg.status_code == 200:
                    break
                else:
                    Logger.log("retrying fetching vertify code...", Logger.info)

            with open('check.gif', 'wb') as fr:  # 保存验证码图片
                for chunk in codeImg:
                    fr.write(chunk)

            print_vertify_code()
            verCode = input("input verify code:")
            # verCode = self.classifier.recognizer("check.gif")  # 识别验证码

            postData = {
                '__VIEWSTATE': self.VIEWSTATE,
                '__EVENTVALIDATION': self.EVENTVALIDATION,
                '_ctl0:txtusername': self.urlBean.userName,
                '_ctl0:txtpassword': self.urlBean.password,
                '_ctl0:txtyzm': verCode,
                '_ctl0:ImageButton1.x': '43',
                '_ctl0:ImageButton1.y': '21',
            }
            prepareBody = self.prepare(referer=self.urlBean.jwglLoginUrl,
                                       originHost=self.urlBean.jwglOriginUrl,
                                       method='POST',
                                       url=self.urlBean.jwglLoginUrl,
                                       data=postData,
                                       params=None)

            while True:
                self.response = self.session.send(prepareBody)
                if self.response.status_code == 200:
                    break

            if re.search('密码错误', self.response.text):
                Logger.log('wrong password!', ['cleaning password file', 'exiting...'], level=Logger.error)
                print(OutputFormater.table([['wrong password!'], ['cleaning password file'], ['exiting...']], padding=2))
                self.urlBean.cleanUserInfo()
                exit(0)

            elif re.search('请输入验证码', self.response.text):
                Logger.log('please input vertify code!', ['retrying...'], level=Logger.warning)
                print(OutputFormater.table([['please input vertify code!'], ['retrying...']], padding=2))

            elif re.search('验证码错误', self.response.text):
                Logger.log('wrong vertify code!', ['retrying...'], level=Logger.warning)
                print(OutputFormater.table([['wrong vertify code!'], ['retrying...']], padding=2))

            else:
                Logger.log('login successfully!', ['userName: ' + self.urlBean.userName, 'password: ' + self.urlBean.password], level=Logger.warning)
                print(OutputFormater.table([['login successfully!']], padding=2))
                self.urlBean.dumpUserInfo()
                break

        return self

    def fetchClassList(self):

        params = {'xh': self.urlBean.userName}
        prepareBody = self.prepare(referer=self.urlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=self.urlBean.fetchClassListUrl,
                                   data=None,
                                   params=params)

        while True:
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('retrying fetching class list...'))

        return self.formatClassList()

    def postClass(self, classId):

        postData = {
            '__EVENTTARGET': 'dgData__ctl' + classId + '_Linkbutton1',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
        }
        payload = {'xh': self.urlBean.userName}
        prepareBody = self.prepare(referer=self.urlBean.fetchClassListUrl + '?xh=' + self.urlBean.userName,
                                   originHost=self.urlBean.jwglOriginUrl,
                                   method='POST',
                                   url=self.urlBean.fetchClassListUrl,
                                   data=postData,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                print('post class successfully')
                break
            else:
                print('retrying...')

        return self.formatClassList()

    def fetchSchedule(self):

        payload = {'xh': self.urlBean.userName}
        prepareBody = self.prepare(referer=self.urlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=self.urlBean.fetchScheduleUrl,
                                   data=None,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                break
            else:
                print("retrying fetching schedule...")

        soup = BeautifulSoup(self.response.text, 'html.parser')
        with open('schedule.md', 'w') as fr:
            fr.write(str(soup.find_all('table', class_='GridViewStyle')[0]))

        return self

    def getEnglishTest(self):

        while True:
            self.response = self.session.send(self.prepareGetEnglishTest())
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print("retrying fetching English test view status...")

    def postEnglishTest(self):

        while True:
            self.response = self.session.send(self.preparePostEnglishTest())
            if self.response.status_code == 200:
                print("request english test successfully!")
                break
            else:
                print("retrying...")

    def getEnglishTestStatus(self):

        htmlbody = BeautifulSoup(self.response.text, 'html.parser')
        htmlbody = htmlbody.find_all('table', class_='GridBackColor')[0]
        tempList = htmlbody.find_all('tr')
        self.buttonId = re.findall('<a href=".*" id="(.*)?">.*</a>', str(tempList[1].find('a')))
        if tempList[1].find('img', border='0', alt='申请当前考试') is not None:
            return False
        elif tempList[1].find('img', border='0', alt='取消考试申请') is not None:
            return True
        else:
            return True

    def fetchSpeechList(self):

        payload = {'xh': self.urlBean.userName}
        prepareBody = self.prepare(referer=self.urlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=self.urlBean.fetchSpeechListUrl,
                                   data=None,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('retrying fetching speech list...'))

        return self.formatSpeechList()

    def postSpeech(self, buttonId):

        postData = {
            '__EVENTTARGET': buttonId,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'txtyzm': '',
        }
        payload = {'xh': self.urlBean.userName}
        prepareBody = self.prepare(referer=self.urlBean.fetchSpeechListUrl + '?xh=' + self.urlBean.userName,
                                   originHost=self.urlBean.jwglOriginUrl,
                                   method='POST',
                                   url=self.urlBean.fetchSpeechListUrl,
                                   data=postData,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('retrying posting speech detail...'))

        postData = {
            '__EVENTTARGET': 'lbsq',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'myscrollheight': '0',
        }
        prepareBody = self.prepare(referer=self.urlBean.speechDetailUrl,
                                   originHost=self.urlBean.jwglOriginUrl,
                                   method='POST',
                                   url=self.urlBean.speechDetailUrl,
                                   data=postData,
                                   params=None)

        while True:
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                break
            else:
                print(Logger.log('retrying posting speech request...'))

        return self

    def formatSpeechList(self):

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        tempSelected_ = htmlBody.find_all('table', class_='GridBackColor')[0].find_all('tr', nowrap='nowrap')
        tempSelectable_ = htmlBody.find_all('table', class_='GridBackColor')[1].find_all('tr', nowrap='nowrap')
        selected_ = []
        selectable_ = []

        for tempRow in tempSelected_[1:]:
            tempRow = tempRow.find_all('td')
            buttonId = re.findall(self.buttonPattern, str(tempRow[-2]))[0]
            speechRow = [buttonId]
            for i in self.speechFilter:
                item = re.findall(self.removeTd, str(tempRow[i]))
                if len(item) == 0:
                    speechRow.append('')
                else:
                    speechRow.append(item[0])
            selected_.append(speechRow)

        for tempRow in tempSelectable_[1:]:
            tempRow = tempRow.find_all('td')
            buttonId = re.findall(self.buttonPattern, str(tempRow[-2]))[0]
            speechRow = [buttonId]
            for i in self.speechFilter:
                item = re.findall(self.removeTd, str(tempRow[i]))
                if len(item) == 0:
                    speechRow.append('')
                else:
                    speechRow.append(item[0])
            selectable_.append(speechRow)

        return selected_, selectable_

    def formatClassList(self):

        with open('class.html', 'w') as fr:
            fr.write(self.response.text)

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        tempList = htmlBody.find_all('tr', nowrap='nowrap')[:-1]
        classList = []
        for tempRow in tempList:
            if tempRow.find('img', border='0', alt='选择当前课程') is not None:
                checkStatus = 0
            elif tempRow.find('img', border='0', alt='退选当前课程') is not None:
                checkStatus = 1
            else:
                checkStatus = -1

            if re.search('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow)):
                buttonId = re.findall('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow))[0]
            else:
                buttonId = None

            tempRow = tempRow.find_all('td')
            classRow = [checkStatus, buttonId]
            for i in self.remainList:
                item = re.findall('<td.*>(.*)?</td>', str(tempRow[i]))
                if len(item) == 0:
                    classRow.append('')
                else:
                    classRow.append(item[0])
            classList.append(classRow)

        return classList

    def clean(self):
        """
        爬取结束关闭会话
        """
        self.session.close()
        print('exiting...')


class VerifyError(Exception):
    """
    验证码错误类
    """

    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return self.errorInfo


class PasswordError(Exception):
    """
    密码错误类
    """

    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return self.errorInfo


def print_vertify_code():
    from PIL import Image
    fullVector = []
    img = Image.open('check.gif')
    img = img.convert('RGBA')
    imgWidth = img.size[0]
    imgHeight = img.size[1]
    pixdata = img.load()
    for j in range(imgHeight):
        row = ''
        for i in range(imgWidth):
            if pixdata[i, j][0] + pixdata[i, j][1] + pixdata[i, j][2] < 3 * 180:
                row += '#'
            else:
                row += ' '
        fullVector.append(row)
    print('\n'.join(fullVector))