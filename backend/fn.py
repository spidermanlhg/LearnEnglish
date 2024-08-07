from flask import Flask, request, jsonify,render_template,send_file
from werkzeug.utils import secure_filename
import os,sys,shutil
from split_sound import split_sound
import pymysql
import datetime
from dotenv import load_dotenv


from config import db_config


# 查询多条记录
def query_all(query):
    """
    执行SQL查询并返回所有结果。

    参数:
    - query (str): SQL查询语句。

    返回:
    - list of tuples: 包含查询结果的所有行，如果没有结果则返回空列表。
    """
    connection = pymysql.connect(**db_config)
    results = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
    except Exception as e:
        # 记录异常，可以是日志或者其他形式的错误记录
        print(f"An error occurred while executing the query: {e}")
        # 根据需求决定是否抛出异常，或者返回错误信息
        # raise  # 抛出异常
        return {"error": str(e), "results": []}
    finally:
        # 确保数据库连接在任何情况下都被关闭
        if connection:
            connection.close()

    return results

#查询单条记录
def query_one(query):
    """
    执行一个SQL查询并返回第一条结果。
    
    参数:
    - query (str): 要执行的SQL查询语句。
    
    返回:
    - tuple: 查询结果的第一条记录，如果没有结果则返回None。
    """
    connection = pymysql.connect(**db_config)
    result = None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
    except Exception as e:
        # 可以在这里记录错误，例如写入日志
        print(f"An error occurred during the query operation: {e}")
        # 可以选择抛出异常，或者根据需要返回错误信息
        raise  # 抛出异常，让调用者处理
        # 或者返回错误信息
        # return {"error": str(e), "result": None}
    finally:
        # 确保连接在任何情况下都会关闭
        if connection:
            connection.close()
    
    return result


#新增记录 ，函数返回新增的行数id
def query_insert(query):
    """
    执行SQL插入操作并返回插入的行数和行ID。

    参数:
    - query (str): SQL插入语句。

    返回:
    - dict: 包含'rowcount'和'lastrowid'的字典，分别表示受影响的行数和新插入行的ID。
    """
    connection = pymysql.connect(**db_config)
    result = {'rowcount': 0, 'lastrowid': None}

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            result['rowcount'] = cursor.rowcount
            result['lastrowid'] = cursor.lastrowid
    except Exception as e:
        # 记录异常，可以是日志或者其他形式的错误记录
        print(f"An error occurred while executing the insert query: {e}")
        # 根据需求决定是否抛出异常，或者返回错误信息
        # raise  # 抛出异常
        return {"error": str(e), "rowcount": 0, "lastrowid": None}
    finally:
        # 确保数据库连接在任何情况下都被关闭
        if connection:
            connection.close()

    return result


#删除记录 
def query_delete(query):
    connection = pymysql.connect(**db_config)
    result = {'success': False, 'rows_affected': 0}
    
    try:
        with connection.cursor() as cursor:
            rows_affected = cursor.execute(query)
            connection.commit()
            result['success'] = True
            result['rows_affected'] = rows_affected
    except Exception as e:
        print(f"An error occurred during delete operation: {e}")
    finally:
        connection.close()
    
    return result
