from DBObjects import *
from Task import Task
from json import dumps
import time

state_ready = 0
state_err = 1
state_succeed = 2
state_err_reload = 3


# 新建一个任务,自动判断是否正常（从系统外触发）
@db_session
def create_task(user_name: str, tel: str, kaoshenghao: str, zhunkaozheng: str, shenfenzheng: str):
    try:
        # 检查数据库中是否已经有该任务
        try:
            the_task = MAIN_TASK.get(USER_NAME=user_name)
        except:
            print("grade query - multi misson err")
            return True

        # 有：判断任务状态：异常、异常重置：置为err_reloed；    其它：置为：正常等待。
        the_state = state_ready
        if the_task is not None:
            if the_task.TASK_STATE == state_err:
                the_state = state_err_reload
            if the_task.TASK_STATE == state_err_reload:
                the_state = state_err_reload
            # 删除老任务（为了队列）
            the_task.delete()
            commit()

        # 新建任务
        MAIN_TASK(
            USER_NAME=user_name,
            USER_TEL=tel,
            USER_KAOHAO=kaoshenghao,
            USER_ZHUNKAOZHENG=zhunkaozheng,
            USER_SHENFENZHENG=shenfenzheng,
            TASK_STATE=the_state,
            AC_TIME=time.time()
        )
        commit()

        return False
    except Exception as e:
        print(e)
        print('grade query - err')
        return True


# 读取一个正常任务 / 或者判断是否有正常任务可用
# 返回 Task 实例
@db_session
def read_normal_task():
    try:# 尝试从数据库获取一个正常任务
        task_rcd = select(t for t in MAIN_TASK if t.TASK_STATE == state_ready).first()
        if task_rcd is None:
            return None
        a_task = Task(task_rcd.USER_ZHUNKAOZHENG, task_rcd.USER_SHENFENZHENG, task_rcd.USER_KAOHAO, task_rcd.ID, task_rcd.AC_TIME)
        return a_task
    except Exception as e:
        print("read_normal_task - err")
        print(e)
        return None


# 读取一个异常任务 / 或者判断是否有异常任务可用
@db_session
def read_err_reload_task():
    try:
        task_rcd = select(t for t in MAIN_TASK if t.TASK_STATE == state_err_reload).first()
        if task_rcd is None:
            return None
        a_task = Task(task_rcd.USER_ZHUNKAOZHENG, task_rcd.USER_SHENFENZHENG, task_rcd.USER_KAOHAO, task_rcd.ID, task_rcd.AC_TIME)
        return a_task
    except Exception as e:
        print("read_sp_task")
        print(e)
        return None


# 查询成绩成功的执行函数
@db_session
def put_succeed_result(task: Task):
    try:
        # 基于task，找到数据库中这条记录
        uid = task.uid
        the_task = MAIN_TASK.get(ID=uid)

        if the_task is None:
            print("put_succeed_result - task id err")
            return True

        # 更新这条记录
        the_task.TASK_STATE = 2
        the_task.TASK_RESULT = dumps(task.result)
        commit()

        # 通知用户
        print(task.result)
        return False
    except Exception as e:
        print(e)
        return True


# 查询成绩异常（学生信息有误）的执行函数
@db_session
def put_err_result(task: Task):
    try:
        # 基于task，找到这条记录
        uid = task.uid
        the_task = MAIN_TASK.get(ID=uid)

        if the_task is None:
            print("put_err_result - task id err")
            return True

        # 更新这条记录状态
        the_task.TASK_STATE = state_err
        commit()
        return False
    except Exception as e:
        print("put_err_result - err")
        print(e)
        return False


# 验证码识别错误的执行函数 - 排到末尾？
@db_session
def put_retry_task(task: Task):
    try:
        # 基于task，找到这条记录
        uid = task.uid
        the_task = MAIN_TASK.get(ID=uid)

        if the_task is None:
            print("put_retry_task - task id err")
            return True

        # 把任务信息提出来
        user_name = the_task.USER_NAME
        tel = the_task.USER_TEL
        kaoshenghao = the_task.USER_KAOHAO
        zhunkaozheng = the_task.USER_SHENFENZHENG
        shenfenzheng = the_task.USER_SHENFENZHENG

        # 删了这条记录
        the_task.delete()
        commit()

        # 新建一条记录
        # 新建任务
        MAIN_TASK(
            USER_NAME=user_name,
            USER_TEL=tel,
            USER_KAOHAO=kaoshenghao,
            USER_ZHUNKAOZHENG=zhunkaozheng,
            USER_SHENFENZHENG=shenfenzheng,
            TASK_STATE=state_err_reload,
            AC_TIME=time.time()
        )
        commit()
        return False
    except Exception as e:
        print("put_retry_task - err")
        print(e)
        return False


# 正常的孩纸 - 排到末尾？
@db_session
def put_normal_task(task: Task):
    try:
        # 基于task，找到这条记录
        uid = task.uid
        the_task = MAIN_TASK.get(ID=uid)

        if the_task is None:
            print("put_normal_task - task id err")
            return True

        # 把任务信息提出来
        user_name = the_task.USER_NAME
        tel = the_task.USER_TEL
        kaoshenghao = the_task.USER_KAOHAO
        zhunkaozheng = the_task.USER_SHENFENZHENG
        shenfenzheng = the_task.USER_SHENFENZHENG

        # 删了这条记录
        the_task.delete()
        commit()

        # 新建一条记录
        # 新建任务
        MAIN_TASK(
            USER_NAME=user_name,
            USER_TEL=tel,
            USER_KAOHAO=kaoshenghao,
            USER_ZHUNKAOZHENG=zhunkaozheng,
            USER_SHENFENZHENG=shenfenzheng,
            TASK_STATE=state_ready,
            AC_TIME=time.time()
        )
        commit()
        return False
    except Exception as e:
        print("put_normal_task - err")
        print(e)
        return False

