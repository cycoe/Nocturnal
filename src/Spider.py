#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from requests import Session, Request, exceptions
from bs4 import BeautifulSoup
from src.UrlBean import UrlBean


class Spider(object):

    def __init__(self):
        self.urlBean = UrlBean()
        self.session = Session()  # 实例化 session 对象

        # 实例化验证码识别器对象
        # from src.classifier import Classifier
        # self.classifier = Classifier()
        # self.classifier.loadTrainingMat()

        self.classFilter = [3, 4, 5, 6, 11, 12]
        self.speechFilter = [0, 1, 3, 4, 5, 6, 7]

    def formatHeaders(self, referer=None, contentLength=None, originHost=None):
        """
        生成请求的 headers，referer 参数的默认值为 None
        若 referer 为 None，则 headers 不包括 referer 参数
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'graduate.buct.edu.cn:8080',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        }
        if referer:
            headers['Referer'] = referer
        if originHost:
            headers['Origin'] = originHost

        return headers

    def getVIEWSTATE(self):
        """
        正则获取登录页面的 "__VIEWSTATE"
        """
        VIEWSTATE = re.findall('<.*name="__VIEWSTATE".*value="(.*)?".*/>', self.response.text)
        if len(VIEWSTATE) > 0:
            return VIEWSTATE
        else:
            return None

    def getEVENTVALIDATION(self):
        """
        正则获取登录页面的 "__EVENTVALIDATION"
        """
        EVENTVALIDATION = re.findall('<.*name="__EVENTVALIDATION".*value="(.*)?".*/>', self.response.text)
        if len(EVENTVALIDATION) > 0:
            return EVENTVALIDATION
        else:
            return None

    def prepareJwglFirst(self):
        headers = self.formatHeaders()
        req = Request('GET', self.urlBean.jwglLoginUrl, headers=headers)
        return self.session.prepare_request(req)

    def prepareFetchVerCode(self):
        headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl)
        req = Request('GET', self.urlBean.verifyCodeUrl, headers=headers)
        return self.session.prepare_request(req)

    def prepareJwglLogin(self):
        """
        实例化登录 jwgl 需要的 request
        __VIEWSTATE 和 __EVENTVALIDATION 可从网页源代码中获取
        """
        postData = {
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '_ctl0:txtusername': self.urlBean.studentID,
            '_ctl0:txtpassword': self.urlBean.jwglPassword,
            '_ctl0:txtyzm': self.verCode,
            '_ctl0:ImageButton1.x': '43',
            '_ctl0:ImageButton1.y': '21',
        }
        headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl, originHost=self.urlBean.jwglOriginUrl)
        req = Request('POST', self.urlBean.jwglLoginUrl, headers=headers, data=postData)
        return self.session.prepare_request(req)

    def prepareJwglLoginDone(self):
        headers = self.formatHeaders(referer=self.urlBean.jwglLoginUrl)
        req = Request('GET', self.urlBean.jwglLoginDoneUrl, headers=headers)
        return self.session.prepare_request(req)

    def prepareFetchClassList(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.studentID}
        req = Request('GET', self.urlBean.fetchClassListUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def preparePostClass(self, classId):
        """
        实例化登录 jwgl 需要的 request
        __VIEWSTATE 和 __EVENTVALIDATION 可从网页源代码中获取
        """
        postData = {
            '__EVENTTARGET': 'dgData__ctl' + classId + '_Linkbutton1',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
        }
        headers = self.formatHeaders(referer=self.urlBean.fetchClassListUrl + '?xh=' + self.urlBean.studentID, originHost=self.urlBean.jwglOriginUrl)
        payload = {'xh': self.urlBean.studentID}
        req = Request('POST', self.urlBean.fetchClassListUrl, headers=headers, data=postData, params=payload)
        return self.session.prepare_request(req)

    def prepareFetchSchedule(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.studentID}
        req = Request('GET', self.urlBean.fetchScheduleUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    def prepareGetEnglishTest(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.studentID}
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
        headers = self.formatHeaders(referer=self.urlBean.englishTestUrl + '?xh=' + self.urlBean.studentID, originHost=self.urlBean.jwglOriginUrl)
        payload = {'xh': self.urlBean.studentID}
        req = Request('POST', self.urlBean.englishTestUrl, headers=headers, data=postData, params=payload)
        return self.session.prepare_request(req)

    def prepareFetchSpeechList(self):
        headers = self.formatHeaders(referer=self.urlBean.leftMenuReferer)
        payload = {'xh': self.urlBean.studentID}
        req = Request('GET', self.urlBean.fetchSpeechListUrl, headers=headers, params=payload)
        return self.session.prepare_request(req)

    # def prepareGetGrade(self):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121605',
    #     }
    #     req = Request('GET', self.getGradeUrl, headers=headers, params=params)
    #     return self.session.prepare_request(req)
    #
    # def preparePastGrade(self):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121605',
    #     }
    #     postData = {
    #         '__EVENTTARGET': '',
    #         '__EVENTARGUMENT': '',
    #         '__VIEWSTATE': self.getVIEWSTATE(),  # 此参数非常重要，通过函数从当前网页源代码获取
    #         'hidLanguage': '',
    #         'ddlXN': '',
    #         'ddlXQ': '',
    #         'ddl_kcxz': '',
    #         'btn_zcj': '历年成绩',
    #     }
    #     req = Request('POST', self.getGradeUrl, headers=headers, params=params, data=postData)
    #     return self.session.prepare_request(req)
    #
    # def prepareSchedule(self):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121603',
    #     }
    #     req = Request('GET', self.getScheduleUrl, headers=headers, params=params)
    #     return self.session.prepare_request(req)
    #
    # def preparePastSchedule(self, xn_, xq_):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121603',
    #     }
    #     postData = {
    #         '__EVENTTARGET': 'xnd',
    #         '__EVENTARGUMENT': '',
    #         '__VIEWSTATE': self.getVIEWSTATE(),  # 此参数非常重要，通过函数从当前网页源代码获取
    #         'xnd': xn_,
    #         'xqd': xq_,
    #     }
    #     req = Request('POST', self.getScheduleUrl, headers=headers, params=params, data=postData)
    #     return self.session.prepare_request(req)
    #
    # def prepareClass(self):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121101',
    #     }
    #     req = Request('GET', self.postClassUrl, headers=headers, params=params)
    #     return self.session.prepare_request(req)
    #
    # def prepareGetClass(self):
    #     headers = self.formatHeaders(self.response.url)
    #     params = {
    #         'xh': self.studentID,
    #         'xm': self.username,
    #         'gnmkdm': 'N121101',
    #     }
    #     postData = {
    #         '__EVENTTARGET': '',
    #         '__EVENTARGUMENT': '',
    #         '__VIEWSTATE': self.getVIEWSTATE(),  # 此参数非常重要，通过函数从当前网页源代码获取
    #         'DrDl_Nj': self.studentID[:4],
    #         'zymc': self.major + '主修专业||' + self.studentID[:4],
    #         'xx': '',
    #         'Button5': '本专业选课'
    #     }
    #     req = Request('POST', self.postClassUrl, headers=headers, params=params, data=postData)
    #     return self.session.prepare_request(req)

    def jwglLogin(self):
        """
        教务网登录函数
        tryNum --> 尝试登录的最大次数，防止因递归深度过大导致溢出
        """

        while True:
            self.response = self.session.send(self.prepareJwglFirst())  # GET 方法获取登录网站的 '__VIEWSTATE'
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.getEVENTVALIDATION() is not None:
                break
            print("retrying fetching viewState...")

        while True:

            while True:
                codeImg = self.session.send(self.prepareFetchVerCode())  # 获取验证码图片
                if codeImg.status_code == 200:
                    break
                else:
                    print("retrying fetching vertifyCode...")

            with open('check.gif', 'wb') as fr:  # 保存验证码图片
                for chunk in codeImg:
                    fr.write(chunk)

            self.verCode = input("input verify code:")
            # self.verCode = self.classifier.recognizer("check.gif")  # 识别验证码

            while True:
                self.response = self.session.send(self.prepareJwglLogin())
                if self.response.status_code == 200:
                    break

            while True:
                self.response = self.session.send(self.prepareJwglLoginDone())
                if self.response.status_code == 200:
                    break

            if re.search('Default', self.response.url):  # 若 response.url 中匹配到 Default，则认为登录成功
                print("\n")
                print("#######################")
                print("# login successfully! #")
                print("#######################")
                print("\n")
                break
            else:
                print("\n")
                print("#######################")
                print("# wrong vertify code! #")
                print("# retrying...         #")
                print("#######################")
                print("\n")

        return self

    def fetchClassList(self):

        while True:
            self.response = self.session.send(self.prepareFetchClassList())
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print("retrying fetching class list...")

        print(self.response.url)
        print('fetched class list\n')

        return self.formatClassList()

    def postClass(self, classId):

        while True:
            self.response = self.session.send(self.preparePostClass(classId))
            if self.response.status_code == 200:
                print('post class successfully')
                break
            else:
                print('retrying...')

        return self.formatClassList()

    def fetchSchedule(self):

        while True:
            self.response = self.session.send(self.prepareFetchSchedule())
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

        while True:
            self.response = self.session.send(self.prepareFetchSpeechList())
            self.VIEWSTATE = self.getVIEWSTATE()
            self.EVENTVALIDATION = self.getEVENTVALIDATION()
            if self.VIEWSTATE is not None and self.EVENTVALIDATION is not None:
                break
            else:
                print("retrying fetching speech list...")

        print(self.response.url)
        print('fetched speech list\n')

        return self.formatSpeechList()

    def formatSpeechList(self):

        htmlBody = BeautifulSoup(self.response.text, 'html.parser')
        tempList = htmlBody.find_all('table', class_='GridBackColor')[1].find_all('tr', nowrap='nowrap')
        speechList = []
        for tempRow in tempList:
            # if tempRow.find('img', border='0', alt='我要报名') is not None:
            #     checkStatus = 0
            # elif tempRow.find('img', border='0', alt='退选当前课程') is not None:
            #     checkStatus = 1
            # else:
            #     checkStatus = -1
            #
            # if re.search('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow)):
            #     buttonId = re.findall('<a.*id="(.*)?".*><img.*>.*</a>', str(tempRow))[0]
            # else:
            #     buttonId = None
            #
            # speechRow = [checkStatus, buttonId]

            tempRow = tempRow.find_all('td')
            speechRow = []
            for i in self.speechFilter:
                item = re.findall('<td.*>(.*)?</td>', str(tempRow[i]))
                if len(item) == 0:
                    speechRow.append('')
                else:
                    speechRow.append(item[0])
            speechList.append(speechRow)

        return speechList

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

    # def getPastGrade(self):
    #     """
    #     获取历年成绩
    #     """
    #     self.response = self.session.send(self.prepareGetGrade(), timeout=5)
    #     self.response = self.session.send(self.preparePastGrade(), timeout=5)
    #     gradeMat = self.formatTable(self.response.text)
    #     gradeMat = [[row[i] for i in range(len(row)) if i in self.remainList] for row in gradeMat]
    #     self.outputTable(gradeMat, outputPath='grade.md')
    #
    # def getPastSchedule(self, xn_, xq_):
    #     self.response = self.session.send(self.prepareSchedule(), timeout=5)
    #     self.response = self.session.send(self.preparePastSchedule(xn_, xq_), timeout=5)
    #     scheduleMat = self.formatTable(self.response.text)
    #     with open('schedule.md', 'w') as fr:
    #         fr.write(str(scheduleMat))
    #         # self.outputTable(scheduleMat, outputPath='schedule.md')
    #
    # def getClassList(self):
    #     self.response = self.session.send(self.prepareClass(), timeout=5)
    #     self.response = self.session.send(self.prepareGetClass(), timeout=5)
    #
    # def outputTable(self, tableMat, outputPath):
    #     """
    #     将成绩输出成 md 格式
    #     """
    #     tableMat.insert(1, [':------' for i in range(len(tableMat[0]))])
    #     with open(outputPath, 'w') as fr:
    #         for row in tableMat:
    #             fr.write('|')
    #             for each in row:
    #                 fr.write(each)
    #                 fr.write('|')
    #             fr.write('\n')
    #
    # def formatTable(self, tableBody):
    #     """
    #     将抓取到的成绩解析成列表
    #     """
    #     from bs4 import BeautifulSoup
    #     import re
    #     soup = BeautifulSoup(tableBody, 'html.parser')
    #     return soup.br.table
    #     tableRow = soup.br.table.find_all('tr')
    #     tableMat = [i.find_all('td') for i in tableRow]
    #     return [[each.get_text().strip() for each in row] for row in tableMat]

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
