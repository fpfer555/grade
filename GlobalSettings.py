from os.path import dirname
from os.path import abspath
from os.path import join
import json
from datetime import datetime


class GlobalSettings:
    root_dir = dirname(abspath(__file__))

    # load conf.json
    conf = json.loads(open(join(root_dir, "conf", "conf.json")).read())

    # 数据库连接
    dbs = conf['dbs']
