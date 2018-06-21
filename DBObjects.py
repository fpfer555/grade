from datetime import datetime
from pony.orm import *
from GlobalSettings import GlobalSettings


# init db
db = Database()
sql_debug(True)


class UserMain(db.Entity):
    username = PrimaryKey(str)
    username_str = Optional(str)
    password = Optional(str, volatile="")
    auth_token = Optional(str, volatile=True)
    login_expires = Optional(int, volatile=True)
    init_score = Optional(int)
    id_card_1 = Optional(str)
    CLASS = Optional(bool, default=True)
    sex = Optional(int, default=1)
    lang = Optional(str, default='English')
    score_list = Optional(LongStr)
    account_expires = Optional(int)
    need_fill = Required(bool, default=True)
    location = Optional(str)
    filled = Required(bool)
    refill_count = Required(int, default=0)
    user_type = Required(int)
    user_payed_state = Required(int, default=0)
    user_auth = Required(str, default="AB")
    user_sp_code = Optional(str)
    wx_openid = Optional(str)
    wx_name = Optional(str)
    tel = Optional(str)


class UserAdmin(db.Entity):
    username = PrimaryKey(str)
    username_str = Optional(str)
    password = Optional(str, volatile="")
    auth_token = Optional(str, volatile=True)
    login_expires = Optional(int, volatile=True)
    account_expires = Optional(int)
    user_type = Required(int)
    info = Optional(Json)


class CardMain(db.Entity):
    user = Optional(str, nullable=True)
    card_id = PrimaryKey(str)
    password = Required(str)
    card_type = Required(int)
    card_code = Optional(str)


class NewCard(db.Entity):
    card_id = PrimaryKey(str)
    user = Optional(str, nullable=True)
    password = Required(str)
    card_type = Required(str)
    card_code = Optional(str)
    active_times = Required(int, default=1)
    ex_date = Optional(datetime)
    ex_days = Optional(int, default=-1)
    data1 = Optional(str)
    data2 = Optional(str)
    data3 = Optional(Json)
    data4 = Optional(datetime)
    data5 = Optional(datetime)


class BigData_Fill(db.Entity):
    user = Required(str)
    content = Required(LongStr)
    total_score = Required(int)
    sex = Required(str)
    majortype = Required(str)
    main_score = Required(int)
    lang = Required(str)
    province = Required(str)
    pro_type = Required(str)
    sp_req = Optional(str)
    timestamp = Required(int)


class SysLog(db.Entity):
    index = PrimaryKey(int, auto=True)
    user_name = Optional(str)
    action = Optional(str)
    data = Optional(str)


class Appointment(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    USER_NAME = Required(str)
    USER_NAME_STR = Optional(str)
    DATE_TIME = Optional(datetime, default=lambda: datetime.now())
    PHONE = Required(str)
    CODE = Required(str)
    DATING_DATE_TIME = Optional(datetime, default=lambda: datetime.now())
    EX_DATE_TIME = Optional(datetime, default=lambda: datetime.now())
    AP_NAME = Optional(str)
    AP_CLASS = Optional(str)
    AP_AREA = Optional(str)


class Alpha_ACEE(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    USER_NAME = Optional(str)
    USER_NAME_STR = Optional(str)
    DATE_TIME_CREATE = Optional(datetime, default=lambda: datetime.now())
    PARAMETERS = Optional(Json)
    ACEE = Optional(Json)
    LOG = Optional(Json)
    EX1 = Optional(datetime, nullable=True)
    EX2 = Optional(Json, nullable=True)


class USER_SCHOOL(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    USER_NAME = Optional(str)
    USER_SCH = Optional(str, nullable=True)
    USER_STU_NUM = Optional(str, nullable=True)
    USER_INFO = Optional(Json, nullable=True)


class MAIN_TASK(db.Entity):
    ID = PrimaryKey(int, auto=True)
    USER_NAME = Optional(str, unique=True)
    USER_TEL = Optional(str)
    USER_KAOHAO = Optional(str)
    USER_ZHUNKAOZHENG = Optional(str)
    USER_SHENFENZHENG = Optional(str)
    TASK_STATE = Optional(int, default=0)  # 0:正常待查。 # 1：发生错误。 # 2：成功； # 3：发生错误，并得到了更新
    TASK_RESULT = Optional(Json)
    DATA01 = Optional(Json)
    AC_TIME = Optional(float)


# =========================================    文科    ========================================
class A_Sch_Query(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    KEY_SCHOOL_BID = Required(str)
    SCHOOL_TOP_LEVEL = Optional(str)
    SCHOOL_NAME = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    LOGO_ADDR = Optional(str)
    SEX_REQUEST = Optional(str)
    LATEST_DIFF = Required(int)
    MIN_SCORE = Optional(Json)
    WANTED_NUM = Optional(Json)
    SP_NUM = Optional(Json)
    HIS_NUM = Required(Json)


class A_Sch_Info(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    SCHOOL_BID = Required(str)
    SCHOOL_NAME = Optional(str)
    SCHOOL_DES = Optional(LongStr)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_LEVEL = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_ADDR = Optional(str)
    SCHOOL_TEL = Optional(str)
    SCI_SCHOOL_HIS = Required(Json)
    SCI_SCHOOL_PROS = Required(Json)


class A_Major_Query(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_POP = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    SCORE_MIN = Optional(str)
    DIFF_B1 = Required(int)
    SEX_REQUEST = Optional(str)
    RE_SCHOOLS = Optional(Json)


class A_Major_Info(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    PRO_JOB = Optional(str)
    PRO_SCALE = Optional(str)
    PRO_CAREERS = Optional(LongStr)
    PRO_LEVEL = Optional(str)
    PRO_REMARK = Optional(LongStr)
    PRO_SCHOOLS = Optional(Json)


class A_CC_Major_Query(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    UN_ID = Required(Json)
    SCHOOL_NAME = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    SEX_REQUEST = Optional(str)
    PRO_LIST = Optional(Json)


class A_Line_Diff_1st_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_2nd_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_1st_UnderG(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_2nd_UnderG(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_Spe_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_Spe_High(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_Line_Diff_Spe_Low(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class A_RANK_B1(db.Entity):
    RANK = PrimaryKey(int)
    YEAR = Required(int)
    UN_ID = Required(Json)


class A_RANK_B1_ADV(db.Entity):
    RANK = PrimaryKey(int)
    YEAR = Required(int)
    UN_ID = Required(Json)


# =========================================    理科    ========================================
class S_Sch_Query(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    KEY_SCHOOL_BID = Required(str)
    SCHOOL_TOP_LEVEL = Optional(str)
    SCHOOL_NAME = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    LOGO_ADDR = Optional(str)
    SEX_REQUEST = Optional(str)
    LATEST_DIFF = Required(int)
    MIN_SCORE = Optional(Json)
    WANTED_NUM = Optional(Json)
    SP_NUM = Optional(Json)
    HIS_NUM = Required(Json)


class S_Sch_Info(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    SCHOOL_BID = Required(str)
    SCHOOL_NAME = Optional(str)
    SCHOOL_DES = Optional(LongStr)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_LEVEL = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_ADDR = Optional(str)
    SCHOOL_TEL = Optional(str)
    SCI_SCHOOL_HIS = Required(Json)
    SCI_SCHOOL_PROS = Required(Json)


class S_Major_Query(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_POP = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    SCORE_MIN = Optional(str)
    DIFF_B1 = Required(int)
    SEX_REQUEST = Optional(str)
    RE_SCHOOLS = Optional(Json)


class S_Major_Info(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    PRO_JOB = Optional(str)
    PRO_SCALE = Optional(str)
    PRO_CAREERS = Optional(LongStr)
    PRO_LEVEL = Optional(str)
    PRO_REMARK = Optional(LongStr)
    PRO_SCHOOLS = Optional(Json)


class S_CC_Major_Query(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    UN_ID = Required(Json)
    SCHOOL_NAME = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    SEX_REQUEST = Optional(str)
    PRO_LIST = Optional(Json)


class S_Line_Diff_1st_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_2nd_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_1st_UnderG(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_2nd_UnderG(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_Spe_Adv(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_Spe_High(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_Line_Diff_Spe_Low(db.Entity):
    DIFF = PrimaryKey(int)
    YEAR = Optional(int)
    UN_ID = Required(Json)


class S_RANK_B1(db.Entity):
    RANK = PrimaryKey(int)
    YEAR = Required(int)
    UN_ID = Required(Json)


class S_RANK_B1_ADV(db.Entity):
    RANK = PrimaryKey(int)
    YEAR = Required(int)
    UN_ID = Required(Json)


# ====================================  补充
class A_Major_Query_NEW(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_POP = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    SCORE_MIN = Optional(str)
    DIFF_B1 = Required(int)
    SEX_REQUEST = Optional(str)
    RE_SCHOOLS = Optional(Json)


class S_Major_Query_NEW(db.Entity):
    PRO_INDEX = PrimaryKey(int, auto=True)
    KEY_PRO_BID = Required(str)
    PRO_NAME = Optional(str)
    PRO_CLASS_ONE = Optional(str)
    PRO_CLASS_TWO = Optional(str)
    PRO_POP = Optional(str)
    PRO_DEGREE = Optional(str)
    PRO_YEAR = Optional(str)
    SCORE_MIN = Optional(str)
    DIFF_B1 = Required(int)
    SEX_REQUEST = Optional(str)
    RE_SCHOOLS = Optional(Json)


class S_Sch_Query_New(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    KEY_SCHOOL_BID = Required(str)
    SCHOOL_TOP_LEVEL = Optional(str)
    SCHOOL_RELATED_LINE = Optional(int)
    SCHOOL_NAME = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    LOGO_ADDR = Optional(str)
    SEX_REQUEST = Optional(str)
    LATEST_DIFF = Required(int)
    MIN_SCORE = Optional(Json)
    WANTED_NUM = Optional(Json)
    SP_NUM = Optional(Json)
    HIS_NUM = Required(Json)


class A_Sch_Query_New(db.Entity):
    INDEX = PrimaryKey(int, auto=True)
    KEY_SCHOOL_BID = Required(str)
    SCHOOL_TOP_LEVEL = Optional(str)
    SCHOOL_RELATED_LINE = Optional(int)
    SCHOOL_NAME = Optional(str)
    SCHOOL_PROVINCE = Optional(str)
    SCHOOL_OWNER = Optional(str)
    SCHOOL_TYPE = Optional(str)
    SCHOOL_PROPERTY = Optional(str)
    IS_985 = Optional(bool)
    IS_211 = Optional(bool)
    LOGO_ADDR = Optional(str)
    SEX_REQUEST = Optional(str)
    LATEST_DIFF = Required(int)
    MIN_SCORE = Optional(Json)
    WANTED_NUM = Optional(Json)
    SP_NUM = Optional(Json)
    HIS_NUM = Required(Json)


# =============================================    启动
# reload DB
def reload_db():
    global db
    db = Database()
    is_db_reload_failed = True
    for db_info in GlobalSettings.dbs:
        try:
            db.bind('mysql', host=db_info['host'], port=db_info['port'],
                    user=db_info['user'], passwd=db_info['password'], db=db_info['db'])
            is_db_reload_failed = False
            break
        except Exception as e:
            print(e)
    if is_db_reload_failed:
        raise Exception('DB Reload Err')
    db.generate_mapping(create_tables=True)


# load DB
is_db_load_failed = True
for db_i in GlobalSettings.dbs:
    try:
        db.bind('mysql', host=db_i['host'], port=db_i['port'], user=db_i['user'],
                passwd=db_i['password'], db=db_i['db'])
        is_db_load_failed = False
        break
    except Exception as err:
        print(err)
if is_db_load_failed:
    raise Exception('DB Load Err')
db.generate_mapping(create_tables=True)
