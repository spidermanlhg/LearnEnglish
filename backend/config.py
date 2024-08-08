import os,sys
from dotenv import load_dotenv
import pymysql

# 加载.env文件
# 本地测试环境 和 线上正式环境 各放一个.env文件，里面写每个环境自己的配置。
load_dotenv()

# 从 .env 文件中获取环境变量
environment = os.getenv('ENVIRONMENT')
database_host = os.getenv('DATABASE_HOST')
database_user = os.getenv('DATABASE_USER')
database_pwd = os.getenv('DATABASE_PWD')


# 获取当前脚本的完整路径， 读写文件的时候，需要这个路径
script_path = os.path.abspath(sys.argv[0])
cur_dir = os.path.dirname(script_path)  # 去掉脚本名称，只保留目录路径

# 数据库配置项
db_config = {
    'host': database_host,
    'user': database_user,
    'password': database_pwd,
    'database': 'learn_english',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}