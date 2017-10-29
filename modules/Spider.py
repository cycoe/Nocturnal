#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from requests import Session, Request, exceptions
from bs4 import BeautifulSoup
from modules.UrlBean import UrlBean
from modules.Logger import Logger
from Config import Config


class Spider(object):
    """
    爬虫体
    """

    def __init__(self):
        self.session = Session()    # 实例化 session 对象，用于 handle 整个会话

        # 实例化验证码识别器对象
        # from modules.classifier import Classifier
        # self.classifier = Classifier()
        # self.classifier.loadTrainingMat()

        self.classFilter = [3, 4, 5, 6, 11, 12]
        self.speechFilter = [0, 1, 3, 4, 5, 6, 7]
        self.VIEWSTATE = ''
        self.EVENTVALIDATION = ''

        self.buttonPattern = re.compile('<a.*href=".*?\'(.*?)?\'.*".*><img.*>.*</a>')
        self.removeTd = re.compile('<td.*>(.*)?</td>')
        self.viewStatePattern = re.compile('<.*name="__VIEWSTATE".*value="(.*)?".*/>')
        self.eventValidationPattern = re.compile('<.*name="__EVENTVALIDATION".*value="(.*)?".*/>')

    @staticmethod
    def formatHeaders(referer=None, contentLength=None, originHost=None):
        """
        封装请求的 headers

        :param referer: 跳转标记，告诉 web 服务器自己是从哪个页面跳转过来的
        :param contentLength: 作用未知
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
        VIEWSTATE = re.findall(self.viewStatePattern, self.response.text)
        if len(VIEWSTATE) > 0:
            return VIEWSTATE
        else:
            return None

    def getEVENTVALIDATION(self):
        """
        正则获取页面的 __EVENTVALIDATION

        :returns: 页面的 __EVENTVALIDATION
        """
        EVENTVALIDATION = re.findall(self.eventValidationPattern, self.response.text)
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

    def prepareFetchSchedule(self):
        headers = self.formatHeaders(referer=UrlBean.leftMenuReferer)
        payload = {'xh': Config.confDict['userName']}
        req = Request('GET', UrlBean.fetchScheduleUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def prepareGetEnglishTest(self):
        headers = self.formatHeaders(referer=UrlBean.leftMenuReferer)
        payload = {'xh': Config.confDict['userName']}
        req = Request('GET', UrlBean.englishTestUrl, headers=headers, params=payload)
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
        headers = self.formatHeaders(referer=UrlBean.englishTestUrl + '?xh=' + Config.confDict['userName'], originHost=UrlBean.jwglOriginUrl)
        payload = {'xh': Config.confDict['userName']}
        req = Request('POST', UrlBean.englishTestUrl, headers=headers, data=postData, params=payload)
        return self.session.prepare_request(req)

    def prepareFetchSpeechList(self):
        headers = self.formatHeaders(referer=UrlBean.leftMenuReferer)
        payload = {'xh': Config.confDict['userName']}
        req = Request('GET', UrlBean.fetchSpeechListUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def login(self):
        """
        登录教务网
        """

        # 在登录前请求一次登录页面，获取网页的隐藏表单数据
        prepareBody = self.prepare(referer=None,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.jwglLoginUrl,
                                   data=None,
                                   params=None)

        Config.initAttempt()
        while Config.descAttempt():
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            Logger.log("Retrying fetching login page viewState...", level=Logger.warning)
        if not Config.descAttempt():
            Logger.log('Up to max attempts!', ['Maybe remote server unreachable'], level=Logger.error)
            return False

        if Config.checkConfFile():
            Config.loadConfFile()
        else:
            Config.confDict['userName'] = input("> UserName: ")
            Config.confDict['password'] = input("> Password: ")
        # 登录主循环
        reInput = False  # 是否需要重新输入用户名和密码
        while True:
            if reInput:
                Config.confDict['userName'] = input("> UserName: ")
                Config.confDict['password'] = input("> Password: ")
                reInput = False

            # 获取验证码
            prepareBody = self.prepare(referer=UrlBean.jwglLoginUrl,
                                       originHost=None,
                                       method='GET',
                                       url=UrlBean.verifyCodeUrl,
                                       data=None,
                                       params=None)

            Config.initAttempt()
            while Config.descAttempt():
                codeImg = self.session.send(prepareBody)  # 获取验证码图片
                if codeImg.status_code == 200:
                    break
                else:
                    Logger.log("retrying fetching vertify code...", level=Logger.warning)
            if not Config.descAttempt():
                Logger.log('Up to max attempts!', ['Maybe remote server unreachable'], level=Logger.error)
                return False

            with open('check.gif', 'wb') as fr:  # 保存验证码图片
                for chunk in codeImg:
                    fr.write(chunk)

            print_vertify_code()
            verCode = input("> input verify code: ")
            # verCode = self.classifier.recognizer("check.gif")  # 识别验证码

            # 发送登陆请求
            postData = {
                '__VIEWSTATE': self.VIEWSTATE,
                '__EVENTVALIDATION': self.EVENTVALIDATION,
                '_ctl0:txtusername': Config.confDict['userName'],
                '_ctl0:txtpassword': Config.confDict['password'],
                '_ctl0:txtyzm': verCode,
                '_ctl0:ImageButton1.x': '43',
                '_ctl0:ImageButton1.y': '21',
            }
            prepareBody = self.prepare(referer=UrlBean.jwglLoginUrl,
                                       originHost=UrlBean.jwglOriginUrl,
                                       method='POST',
                                       url=UrlBean.jwglLoginUrl,
                                       data=postData,
                                       params=None)

            Config.initAttempt()
            while Config.descAttempt():
                self.response = self.session.send(prepareBody)
                if self.response.status_code == 200:
                    break
            if not Config.descAttempt():
                Logger.log('Up to max attempts!', ['Maybe remote server unreachable'], level=Logger.error)
                return False

            if re.search('用户名不存在', self.response.text):
                print(Logger.log('No such a user!', ['Cleaning password file'], level=Logger.error))
                Config.cleanConfFile()
                reInput = True

            elif re.search('密码错误', self.response.text):
                print(Logger.log('Wrong password!', ['Cleaning password file'], level=Logger.error))
                Config.cleanConfFile()
                reInput = True

            elif re.search('请输入验证码', self.response.text):
                print(Logger.log('Please input vertify code!', ['Retrying...'], level=Logger.error))

            elif re.search('验证码错误', self.response.text):
                print(Logger.log('Wrong vertify code!', ['Retrying...'], level=Logger.error))

            else:
                print(Logger.log('Login successfully!', ['UserName: ' + Config.confDict['userName']], level=Logger.error))
                Config.dumpConfFile()
                break

        return True

    def fetchClassList(self):

        params = {'xh': Config.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchClassListUrl,
                                   data=None,
                                   params=params)

        Config.initAttempt()
        while Config.descAttempt():
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('retrying fetching class list...'))
        if not Config.descAttempt():
            Logger.log('Up to max attempts!', ['Maybe you need to re-login'], level=Logger.error)
            return False

        return self.formatClassList()

    def postClass(self, classId):

        postData = {
            '__EVENTTARGET': 'dgData__ctl' + classId + '_Linkbutton1',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
        }
        payload = {'xh': Config.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.fetchClassListUrl + '?xh=' + Config.confDict['userName'],
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='POST',
                                   url=UrlBean.fetchClassListUrl,
                                   data=postData,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                print('Post class successfully')
                break
            else:
                print('Retrying...')

        return self.formatClassList()

    def fetchSchedule(self):

        payload = {'xh': Config.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchScheduleUrl,
                                   data=None,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                break
            else:
                print("Retrying fetching schedule...")

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
                print("Retrying fetching English test view status...")

    def postEnglishTest(self):

        while True:
            self.response = self.session.send(self.preparePostEnglishTest())
            if self.response.status_code == 200:
                print("Request english test successfully!")
                break
            else:
                print("Retrying...")

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

        payload = {'xh': Config.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchSpeechListUrl,
                                   data=None,
                                   params=payload)

        Config.initAttempt()
        while Config.descAttempt():
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('Retrying fetching speech list...', level=Logger.warning))
        if not Config.descAttempt():
            Logger.log('Up to max attempts!', ['Maybe you need to re-login'], level=Logger.error)
            return False

        return self.formatSpeechList()

    def postSpeech(self, buttonId):

        postData = {
            '__EVENTTARGET': buttonId,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'txtyzm': '',
        }
        payload = {'xh': Config.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.fetchSpeechListUrl + '?xh=' + Config.confDict['userName'],
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='POST',
                                   url=UrlBean.fetchSpeechListUrl,
                                   data=postData,
                                   params=payload)

        Config.initAttempt()
        while Config.descAttempt():
            self.response = self.session.send(prepareBody)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print(Logger.log('Retrying posting speech detail...', level=Logger.warning))
        if not Config.descAttempt():
            Logger.log('Up to max attempts!', ['Maybe you need to re-login'], level=Logger.error)
            return False

        postData = {
            '__EVENTTARGET': 'lbsq',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'myscrollheight': '0',
        }
        prepareBody = self.prepare(referer=UrlBean.speechDetailUrl,
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='POST',
                                   url=UrlBean.speechDetailUrl,
                                   data=postData,
                                   params=None)

        Config.initAttempt()
        while Config.descAttempt():
            self.response = self.session.send(prepareBody)
            if self.response.status_code == 200:
                break
            else:
                print(Logger.log('Retrying posting speech request...', level=Logger.warning))
        if not Config.descAttempt():
            Logger.log('Up to max attempts!', ['Maybe you need to re-login'], level=Logger.error)
            return False

        return True

    def formatSpeechList(self):
        """
        format speech list to matrix

        :return tempSelected_: return the HTML form of selected speech list
        :return selected_: return the matrix form of selected speech list
        :return selectable_: return the matrix form of selectable speech list
        """

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

        return tempSelected_, selected_, selectable_

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
    pixData = img.load()
    for j in range(imgHeight):
        row = ''
        for i in range(imgWidth):
            if pixData[i, j][0] + pixData[i, j][1] + pixData[i, j][2] < 3 * 180:
                row += '#'
            else:
                row += ' '
        fullVector.append(row)
    print('\n'.join(fullVector))