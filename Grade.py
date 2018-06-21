import requests
import json
# from queue import *
from queue import Queue
import operator as op
from concurrent.futures import ThreadPoolExecutor
import time
# from .Task import Task
from ShowapiRequest import ShowapiRequest
import base64

from GradeHandler import *

'''
   start()方法是开始发送查询的入口，其实现逻辑是首先是从任务队列中取出任务，如果任务队列为空则休息
   10s，再次尝试。当却出一个任务后，会判断当前这个任务是否已经准备好了，准备好的条件有两个满足其一即可:
       1.第一次进入任务队列。
       2.离上一次请求时间间隔大于2分钟
   再请求后，获取请求结果判断是否已经查询到成绩，如果查询到了则保存，如果没有查询到，判断是否是验证码错误，
   若不是则将本次task重新入队，
   若是则将该任务信息有误，加入到Erro队列，由外部的业务来进行处理，对其信息更正后，加入到VcodeQueue验证码队列
   
   而对于需要验证的任务，即在VcodeQueue中的任务是做一下处理：
    首先根据开放的接口查询此任务的信息受否被锁定，锁定即需要验证。如果没有被锁定，那么就将其直接加入查询任务队列，
    如果锁定了，就会申请其验证码，并通过第三方的验证码识别平台识别出结果，放到请求中，进行查询。
    对于查询结果，如果是查询成功则直接输出，如果是验证码错误则重入验证队列，其它情况(暂无此考生成绩)则放入查询队列。
   '''


# 使用元类方式实现单例
class Singleton(type):
    _inst = {}

    def __call__(self, *args, **kw):
        if self not in self._inst:
            self._inst[self] = super(Singleton, self).__call__(*args, **kw)
        return self._inst[self]


# 查询成绩的主要实现类，单例
class Grade(metaclass=Singleton):
    def __init__(self, max_thread):
        # 线程池，其中的线程用于发送同一名同学的信息查询成绩
        self.__threadpool = ThreadPoolExecutor(max_workers=max_thread)
        self.VcodeThreadPool = ThreadPoolExecutor(3)
        # 任务队列，用于存放每一个没有查出成绩的学生信息
        self.taskQueue = Queue()
        # 错误队列,用于存储信息错误的任务
        self.errorQueue = Queue()
        # 验证码队列，用于存储需要验证码的任务
        self.VcodeQueue = Queue()

    # 向任务队列中获取任务
    def getQueryTask(self):
        return self.taskQueue.get()

    # 向任务队列中新增任务
    def putQueryTask(self, val):
        self.taskQueue.put(val)

    def queryTaskEmpty(self):
        if self.taskQueue.empty():
            return True
        else:
            return False

        # 向任务队列中获取任务

    def getErroTask(self):
        return self.errorQueue.get()
        # 向任务队列中新增任务

    def putErroTask(self, val):
        self.errorQueue.put(val)

    def ErroQueueEmpty(self):
        if self.errorQueue.empty():
            return True
        else:
            return False

    def pubVcodeTask(self, val):
        self.VcodeQueue.put(val)

    def getVcodeTask(self):
        return self.VcodeQueue.get()

    def VcodeQueueEmpty(self):
        if self.VcodeQueue.empty():
            return True
        else:
            return False

    '''
    查询入口
    '''

    def start(self):
        while (True):
            # 队列是否为空
            if (self.queryTaskEmpty()):
                time.sleep(10)
            else:
                task = self.getQueryTask()
                # 该任务是否已经准备好了
                if (task.isOK()):
                    queryResult = self.tryGeyGrade(task.list)
                    # 是否查询到了成绩
                    if (op.eq(queryResult.code, "00")):
                        # 查询到成绩了，对结果进行保存
                        print(queryResult.result)

                        #################################################################
                        #################################################################
                        #################################################################
                        #


                    else:
                        # 更新任务查询时间
                        task.lastTime = time.time()
                        # 验证码错误，将任务加入到信息错误队列
                        if (op.eq(queryResult.code, "11")):
                            # task.isFirst = True
                            self.putErroTask(task)
                        # 没有查询到成绩，再次入队
                        else:
                            self.putQueryTask(task)
                else:
                    # 任务没有准备好，也重新入队
                    self.putQueryTask(task)
            # 去除需要验证的任务。
            self.removeVCode()

    '''
        实现了具体一次请求。
    '''

    def getGrade(self, list, cookie, vcode):
        url = "http://api.sceea.cn/Handler/GetSpcjkHandler.ashx"

        payload = {'jsoncallPP': "jQuery1604053855526216852_1528987015756",
                   '_': "1528987016391", 'yzm': vcode, 'zkzh': list[0], 'sfzh': list[1],
                   'ksh': list[2]
                   }
        headers = {'Accept': "*/*",
                   'Referer': "http://cx.sceea.cn/html/GKCJResult.htm",
                   'Connection': "keep-alive",
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                   'Accept-Encoding': "gzip, deflate, sdch",
                   'Accept-Language': "zh-CN,zh;q=0.8",
                   'Host': "api.sceea.cn",
                   'Cookie': cookie}
        r = requests.get(url, headers=headers, params=payload)
        result = r.content.decode()
        start = result.index('(') + 1
        result = result[start:-1]
        # print (result)
        return result

    '''
        使用多线程发送请求，并判断请求结果返回。
    '''

    def tryGeyGrade(self, list):
        future1 = self.__threadpool.submit(self.getGrade, list, "", "请点击").result()
        future2 = self.__threadpool.submit(self.getGrade, list, "", "请点击").result()
        future3 = self.__threadpool.submit(self.getGrade, list, "", "请点击").result()

        queryResult1 = self.getQueryResult(future1)
        queryResult2 = self.getQueryResult(future2)
        queryResult3 = self.getQueryResult(future3)

        if (op.eq(queryResult1.code, "00")):
            return queryResult1
        elif (op.eq(queryResult2.code, "00")):
            return queryResult2
        elif (op.eq(queryResult3.code, "00")):
            return queryResult3
        else:
            return queryResult1

    '''
        查询是否成功
    '''

    def getQueryResult(self, rusultjson):
        result = json.loads(rusultjson)
        resultcode = result["ResultCode"]
        queryResult = QueryResult(result, resultcode)
        return queryResult

    '''
    获取验证码
    '''

    def getVCode(self):
        url = "http://api.sceea.cn/Handler/ValidateImageHandler.ashx"
        param = {'t': "0.4928954305102806"}
        headers = {'Accept': "*/*",
                   'Referer': "http://cx.sceea.cn/html/GKCJResult.htm",
                   'Connection': "keep-alive",
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                   'Accept-Encoding': "gzip, deflate, sdch",
                   'Accept-Language': "zh-CN,zh;q=0.8",
                   'Host': "api.sceea.cn", }
        r = requests.get(url, headers=headers, params=param)
        # result = r.content.decode()
        result = []
        data = r.content
        if r.headers.__contains__("Set-Cookie"):
            print(r.headers["Set-Cookie"])
            result.append(r.headers["Set-Cookie"])

        r = ShowapiRequest("http://route.showapi.com/184-2", "67803", "8a3c2b317d6141b8995b01e537cd0d61")
        r.addBodyPara("img_base64", base64.b64encode(data))
        r.addBodyPara("typeId", "34")
        r.addBodyPara("convert_to_jpg", "0")
        # r.addFilePara("img", r"C:\Users\showa\Desktop\使用过的\4.png") #文件上传时设置
        res = r.post()
        vcodeResult = json.loads(res.text)
        print(vcodeResult)  # 返回信息
        # 取出验证码
        vcode = vcodeResult['showapi_res_body']['Result']
        print(vcode)
        result.append(vcode)
        return result

    # 检验是否需要验证码
    def checkQueryKey(self, key):
        url = "http://api.sceea.cn/Handler/CheckQueryKey.ashx?"
        payload = {'QueryKey': key,
                   'jsoncallback': "jQuery1607929645241359475_1529509783762",
                   '_': "1529509790937"
                   }
        headers = {'Accept': "*/*",
                   'Referer': "http://cx.sceea.cn/html/GKCJResult.htm",
                   'Connection': "keep-alive",
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                   'Accept-Encoding': "gzip, deflate, sdch",
                   'Accept-Language': "zh-CN,zh;q=0.8",
                   'Host': "api.sceea.cn"}
        r = requests.get(url, headers=headers, params=payload)
        result = r.content.decode()
        Sindex = result.find('{') + 1
        Eindex = result.find('}')
        ExistsKey = result[Sindex:Eindex]
        if ExistsKey.__contains__('1'):
            return False
        else:
            return True

    # 将需要验证的队列转换到不需验证的队列中，或者查询成功
    def removeVCode(self):
        if (self.VcodeQueueEmpty()):
            time.sleep(1)
        else:
            self.VcodeThreadPool.submit(self.removeVcodeTask)

    def removeVcodeTask(self):
        task = self.getVcodeTask();
        ksh = task.list[2]

        if self.checkQueryKey(ksh):
            self.putQueryTask(task)
        else:

            cookie_code = self.getVCode()
            result = self.getGrade(task.list, cookie_code[0], cookie_code[1])
            queryResult = self.getQueryResult(result)
            print(result)
            if (op.eq(queryResult.code, "11")):
                self.pubVcodeTask(task)
            elif (op.eq(queryResult.code, "00")):
                print(result)
            else:
                self.putQueryTask(task)


class QueryResult:
    def __init__(self, result, code):
        self.result = result
        self.code = code


t = Grade(3)


create_task("oIviQ07f2YPlk-uHLYAG1BUB8iRI", tel="13551055575", kaoshenghao="17510101120649", zhunkaozheng="010102113", shenfenzheng="510104199905254884")

t.start()
