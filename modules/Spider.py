#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from requests import Session, Request, exceptions
from bs4 import BeautifulSoup
from modules.UrlBean import UrlBean
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.Network import Network
from modules.img2Vector import img2Vector
from modules.String import String


def load_tag():
    tag_set = []
    for index in range(48, 58):
        tag = [int(item) for item in str(bin(index))[2:]]
        if len(tag) < 7:
            tag.insert(0, 0)
        tag_set.append(tag)

    for index in range(65, 91):
        tag = [int(item) for item in str(bin(index))[2:]]
        if len(tag) < 7:
            tag.insert(0, 0)
        tag_set.append(tag)

    return tag_set


class Spider(object):
    """
    爬虫体
    """

    MAX_ATTEMPT = 0
    NO_SUCH_A_USER = 1
    WRONG_PASSWORD = 2
    EMPTY_VERTIFY_CODE = 3
    WRONG_VERTIFY_CODE = 4
    LOGIN_SUCCESSFULLY = 5

    def __init__(self, output):
        self.session = Session()    # 实例化 session 对象，用于 handle 整个会话
        self.output = output
        self.network = Network()
        self.network.load_tag(load_tag()).set_structure([300, 200, 100, 7]).load_weight()

        # 实例化验证码识别器对象
        # from modules.classifier import Classifier
        # self.classifier = Classifier()
        # self.classifier.loadTrainingMat()

        self.classFilter = [3, 4, 5, 6, 11, 12, 13]
        self.reportFilter = [0, 1, 3, 4, 5, 6, 7]
        self.VIEWSTATE = ''
        self.EVENTVALIDATION = ''
        self.response = None

        # self.buttonPattern = re.compile('<a.*href=".*?\'(.*?)?\'.*".*><img.*>.*</a>')
        self.buttonPattern = re.compile('<a.*id="(.*?)?".*><img.*>.*</a>')
        self.removeTd = re.compile('<td.*>(.*)?</td>')
        self.viewStatePattern = re.compile('<.*name="__VIEWSTATE".*value="(.*)?".*/>')
        self.eventValidationPattern = re.compile('<.*name="__EVENTVALIDATION".*value="(.*)?".*/>')

    def open_session(self):
        self.session = Session()  # 实例化 session 对象，用于 handle 整个会话

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
        return VIEWSTATE if len(VIEWSTATE) > 0 else None

    def getEVENTVALIDATION(self):
        """
        正则获取页面的 __EVENTVALIDATION

        :returns: 页面的 __EVENTVALIDATION
        """
        EVENTVALIDATION = re.findall(self.eventValidationPattern, self.response.text)
        return EVENTVALIDATION if len(EVENTVALIDATION) > 0 else None

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
        payload = {'xh': MisUtils.confDict['userName']}
        req = Request('GET', UrlBean.fetchScheduleUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def prepareGetEnglishTest(self):
        headers = self.formatHeaders(referer=UrlBean.leftMenuReferer)
        payload = {'xh': MisUtils.confDict['userName']}
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
        headers = self.formatHeaders(referer=UrlBean.englishTestUrl + '?xh=' + MisUtils.confDict['userName'], originHost=UrlBean.jwglOriginUrl)
        payload = {'xh': MisUtils.confDict['userName']}
        req = Request('POST', UrlBean.englishTestUrl, headers=headers, data=postData, params=payload)
        return self.session.prepare_request(req)

    def prepare_login(self):
        # 在登录前请求一次登录页面，获取网页的隐藏表单数据
        prepareBody = self.prepare(referer=None,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.jwglLoginUrl,
                                   data=None,
                                   params=None)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            self.output(Logger.log(String['failed_fetch_login'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['server_unreachable']], level=Logger.error))
            return Spider.MAX_ATTEMPT

    def login(self, username, password):
        """
        登录教务网
        """

        # 获取验证码
        prepareBody = self.prepare(referer=UrlBean.jwglLoginUrl,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.verifyCodeUrl,
                                   data=None,
                                   params=None)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            codeImg = self.session.send(prepareBody, timeout=MisUtils.timeout)  # 获取验证码图片
            if codeImg.status_code == 200:
                break
            else:
                self.output(Logger.log(String['failed_fetch_vertify_code'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['server_unreachable']], level=Logger.error))
            return Spider.MAX_ATTEMPT

        with open('check.gif', 'wb') as fr:  # 保存验证码图片
            for chunk in codeImg:
                fr.write(chunk)

        # self.output_vertify_code()
        verCode = ''
        vectors_ = img2Vector('check.gif')
        if vectors_:
            for vector in vectors_:
                verCode += chr(int(''.join([str(item) for item in self.network.classify(vector)]), base=2))
        # self.output(verCode)
        # verCode = self.classifier.recognizer("check.gif")  # 识别验证码

        # 发送登陆请求
        postData = {
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '_ctl0:txtusername': username,
            '_ctl0:txtpassword': password,
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

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            if self.response.status_code == 200:
                break

        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['server_unreachable']], level=Logger.error))
            return Spider.MAX_ATTEMPT

        if re.search('用户名不存在', self.response.text):
            self.output(Logger.log(String['no_such_a_user'], [String['clean_password']], level=Logger.error))
            return Spider.NO_SUCH_A_USER

        elif re.search('密码错误', self.response.text):
            self.output(Logger.log(String['wrong_password'], [String['clean_password']], level=Logger.error))
            return Spider.WRONG_PASSWORD

        elif re.search('请输入验证码', self.response.text):
            self.output(Logger.log(String['empty_vertify_code'], [String['retrying']], level=Logger.error))
            return Spider.EMPTY_VERTIFY_CODE

        elif re.search('验证码错误', self.response.text):
            self.output(Logger.log(String['wrong_vertify_code'], [String['retrying']], level=Logger.error))
            return Spider.WRONG_VERTIFY_CODE

        else:
            self.output(Logger.log(String['login_successfully'], [String['username'] + MisUtils.confDict['userName']], level=Logger.error))
            return Spider.LOGIN_SUCCESSFULLY

    def fetchClassList(self):

        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchClassListUrl,
                                   data=None,
                                   params=payload)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                self.output(Logger.log('retrying fetching class list...', level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['re-login']], level=Logger.error))
            return False

        return self.formatClassList()

    def postClass(self, button_id):

        postData = {
            '__EVENTTARGET': button_id,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
        }
        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.fetchClassListUrl + '?xh=' + MisUtils.confDict['userName'],
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='POST',
                                   url=UrlBean.fetchClassListUrl,
                                   data=postData,
                                   params=payload)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            if self.response.status_code == 200:
                print('Post class successfully')
                break
            else:
                print('Retrying...')
        if not MisUtils.get_attempt():
            print(Logger.log(String['max_attempts'], [String['re-login']], level=Logger.error))
            return False

        return True

    def fetchReportList(self):
        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchReportListUrl,
                                   data=None,
                                   params=payload)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                self.output(Logger.log(String['failed_fetch_report'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['re-login']], level=Logger.error))
            return False

        return self.formatReportList()

    def postReport(self, buttonId):
        # 获取验证码
        prepareBody = self.prepare(referer=UrlBean.jwglLoginUrl,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.verifyCodeUrl,
                                   data=None,
                                   params=None)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            codeImg = self.session.send(prepareBody, timeout=MisUtils.timeout)  # 获取验证码图片
            if codeImg.status_code == 200:
                break
            else:
                self.output(Logger.log(String['failed_fetch_vertify_code'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['server_unreachable']], level=Logger.error))
            return False

        with open('check.gif', 'wb') as fr:  # 保存验证码图片
            for chunk in codeImg:
                fr.write(chunk)

        verCode = ''
        vectors_ = img2Vector('check.gif')
        if vectors_:
            for vector in vectors_:
                verCode += chr(int(''.join([str(item) for item in self.network.classify(vector)]), base=2))

        postData = {
            '__EVENTTARGET': buttonId,
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            'txtyzm': verCode,
        }
        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.fetchReportListUrl + '?xh=' + MisUtils.confDict['userName'],
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='POST',
                                   url=UrlBean.fetchReportListUrl,
                                   data=postData,
                                   params=payload)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                self.output(Logger.log(String['failed_post_report'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['re-login']], level=Logger.error))
            return False

        # postData = {
        #     '__EVENTTARGET': 'lbsq',
        #     '__EVENTARGUMENT': '',
        #     '__VIEWSTATE': self.VIEWSTATE,
        #     '__EVENTVALIDATION': self.EVENTVALIDATION,
        #     'myscrollheight': '0',
        # }
        # prepareBody = self.prepare(referer=UrlBean.reportDetailUrl,
        #                            originHost=UrlBean.jwglOriginUrl,
        #                            method='POST',
        #                            url=UrlBean.reportDetailUrl,
        #                            data=postData,
        #                            params=None)
        #
        # MisUtils.initAttempt()
        # while MisUtils.descAttempt():
        #     self.response = self.session.send(prepareBody)
        #     if self.response.status_code == 200:
        #         break
        #     else:
        #         self.output(Logger.log('Retrying posting report request...', level=Logger.warning))

        return True

    def fetchSchedule(self):

        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=None,
                                   method='GET',
                                   url=UrlBean.fetchScheduleUrl,
                                   data=None,
                                   params=payload)

        while True:
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            if self.response.status_code == 200:
                break
            else:
                self.output("Retrying fetching schedule...")

        soup = BeautifulSoup(self.response.text, 'html.parser')
        with open('schedule.md', 'w') as fr:
            fr.write(str(soup.find_all('table', class_='GridViewStyle')[0]))

        return self

    def getEnglishTest(self):

        while True:
            self.response = self.session.send(self.prepareGetEnglishTest(), timeout=MisUtils.timeout)
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                self.output("Retrying fetching English test view status...")

    def postEnglishTest(self):

        while True:
            self.response = self.session.send(self.preparePostEnglishTest(), timeout=MisUtils.timeout)
            if self.response.status_code == 200:
                self.output("Request english test successfully!")
                break
            else:
                self.output("Retrying...")

    def getEnglishTestStatus(self):

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        htmlBody = htmlBody.find_all('table', class_='GridBackColor')[0]
        tempList = htmlBody.find_all('tr')
        self.buttonId = re.findall('<a href=".*" id="(.*)?">.*</a>', str(tempList[1].find('a')))
        if tempList[1].find('img', border='0', alt='申请当前考试') is not None:
            return False
        elif tempList[1].find('img', border='0', alt='取消考试申请') is not None:
            return True
        else:
            return True

    def fetchGrade(self):
        payload = {'xh': MisUtils.confDict['userName']}
        prepareBody = self.prepare(referer=UrlBean.leftMenuReferer,
                                   originHost=UrlBean.jwglOriginUrl,
                                   method='GET',
                                   url=UrlBean.fetchGradeUrl,
                                   data=None,
                                   params=payload)

        MisUtils.initAttempt()
        while MisUtils.descAttempt():
            self.response = self.session.send(prepareBody, timeout=MisUtils.timeout)
            if self.response.status_code == 200:
                break
            else:
                self.output(Logger.log(String['failed_fetch_grade'], [String['retrying']], level=Logger.warning))
        if not MisUtils.get_attempt():
            self.output(Logger.log(String['max_attempts'], [String['re-login']], level=Logger.error))
            return False

        return self.formatGradeList()

    def formatGradeList(self):
        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        comp_grade = htmlBody.find_all('table', class_='GridViewStyle')[0]      # compulsory course grades
        elect_grade = htmlBody.find_all('table', class_='GridViewStyle')[1]     # elective course grades

        grade = comp_grade.find_all('tr', class_='GridViewRowStyle')
        grade.extend(elect_grade.find_all('tr', class_='GridViewRowStyle'))
        grade = [[re.findall(self.removeTd, str(item))[0] for item in grade_line.find_all('td')] for grade_line in grade]

        return grade

    def formatReportList(self):
        """
        format report list to matrix

        :return tempSelected_: return the HTML form of selected report list
        :return selected_: return the matrix form of selected report list
        :return selectable_: return the matrix form of selectable report list
        """

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        tempSelected_ = htmlBody.find_all('table', class_='GridBackColor')[0].find_all('tr', nowrap='nowrap')
        tempSelectable_ = htmlBody.find_all('table', class_='GridBackColor')[1].find_all('tr', nowrap='nowrap')
        selected_ = []
        selectable_ = []

        for tempRow in tempSelected_[1:]:
            tempRow = tempRow.find_all('td')
            # buttonId = re.findall(self.buttonPattern, str(tempRow[-1]))[0]
            reportRow = ['Selected']
            for i in self.reportFilter:
                item = re.findall(self.removeTd, str(tempRow[i]))
                reportRow.append(item[0] if item else '')
            selected_.append(reportRow)

        for tempRow in tempSelectable_[1:]:
            tempRow = tempRow.find_all('td')
            buttonId = re.findall(self.buttonPattern, str(tempRow[-1]))[0]
            reportRow = [buttonId]
            for i in self.reportFilter:
                item = re.findall(self.removeTd, str(tempRow[i]))
                reportRow.append(item[0] if item else '')
            selectable_.append(reportRow)

        return selected_, selectable_

    def formatClassList(self):

        with open('class.html', 'w') as fr:
            fr.write(self.response.text)

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        tempTable_ = htmlBody.find_all('table', class_='GridBackColor')[0].find_all('tr', nowrap='nowrap')
        selectable_ = []
        selected_ = []

        for tempRow in tempTable_:
            tempRow = tempRow.find_all('td')
            buttonId = re.findall(self.buttonPattern, str(tempRow[-1]))[0] if re.search(self.buttonPattern, str(tempRow[-1])) else ''
            buttonId_ = buttonId[0:6] + '$' + buttonId[7:12] + '$' + buttonId[13:]
            classRow = [buttonId_]
            for i in self.classFilter:
                item = re.findall(self.removeTd, str(tempRow[i]))
                classRow.append(item[0] if item else '')

            if re.search('选择当前课程', str(tempRow[-1])):
                selectable_.append(classRow)
            elif re.search('退选当前课程', str(tempRow[-1])):
                selected_.append(classRow)
            else:
                selected_.append(classRow)

        print(selected_)
        return selectable_, selected_

        # tempList = htmlBody.find_all('tr', nowrap='nowrap')[:-1]
        # classList = []
        # for tempRow in tempList:
        #     if tempRow.find('img', border='0', alt='选择当前课程') is not None:
        #         checkStatus = 0
        #     elif tempRow.find('img', border='0', alt='退选当前课程') is not None:
        #         checkStatus = 1
        #     else:
        #         checkStatus = -1
        #
        #     if re.search('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow)):
        #         buttonId = re.findall('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow))[0]
        #     else:
        #         buttonId = None
        #
        #     tempRow = tempRow.find_all('td')
        #     classRow = [checkStatus, buttonId]
        #     for i in self.remainList:
        #         item = re.findall('<td.*>(.*)?</td>', str(tempRow[i]))
        #         if len(item) == 0:
        #             classRow.append('')
        #         else:
        #             classRow.append(item[0])
        #     classList.append(classRow)
        #
        # return classList

    def clean(self):
        """
        爬取结束关闭会话
        """
        self.output(Logger.log(String['close_session']))
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


# def print_vertify_code():
#     from PIL import Image
#     fullVector = []
#     img = Image.open('check.gif')
#     img = img.convert('RGBA')
#     imgWidth = img.size[0]
#     imgHeight = img.size[1]
#     pixData = img.load()
#     for j in range(imgHeight):
#         row = ''
#         for i in range(imgWidth):
#             if pixData[i, j][0] + pixData[i, j][1] + pixData[i, j][2] < 3 * 180:
#                 row += '#'
#             else:
#                 row += ' '
#         fullVector.append(row)
#     print('\n'.join(fullVector))
