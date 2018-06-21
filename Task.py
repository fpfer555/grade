import time

'''
任务类，主要存放学生信息和任务上一次查询的时间
'''


class Task:
    def __init__(self, zkzh, sfzh, ksh, mission_id, the_time):
        self.lastTime = the_time
        self.list = [zkzh, sfzh, ksh]
        self.isFirst = True;
        self.uid = mission_id
        self.result = None

    '''
    判断任务 是否准备好。
    '''

    def isOK(self):
        if self.isFirst:
            return True
        currentTime = time.time()
        timeGap = currentTime - self.lastTime
        if timeGap > 120:
            return True
        else:
            return False
