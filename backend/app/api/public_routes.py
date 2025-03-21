

from flask import (Blueprint, Flask, jsonify, request,send_file)
from werkzeug.utils import secure_filename
from config import cur_dir, db_config
from app.utils.db import *
from app.utils.split_sound import split_sound
import os,shutil


# 创建蓝图
pr = Blueprint('public', __name__ , url_prefix="/api" )
@pr.route('/')
def index():
    return jsonify("This is index")



# 查询所有的books，返回书籍列表包括 书籍id，书籍名称，课程数量。
@pr.route('/books')
def get_books():

    # 查询书籍列表
    query = "SELECT * FROM books"
    books = query_all(query)

    # 查询每本书籍已上传了多少节课程
    group_query = "SELECT book_id as id, COUNT(*) AS total FROM LESSONS GROUP BY `book_id` "
    total = query_all(group_query)

    # 把每本书的课程数量合并到书籍列表中
    for i in books:
        for j in total:
            if i['id'] == j['id']:
                i.update(j)

    return jsonify(books)


# 根据book_id 查询 lessons 列表，返回lesson的id，名称，分隔状态
@pr.route('/books/<id>')
def get_lessons(id):

    query = f'''
                SELECT lessons.id as id, lessons.book_id as book_id, books.name as book_name, lessons.name as name, lessons.status as status
                FROM lessons
                INNER JOIN books ON lessons.book_id = books.id
                WHERE lessons.book_id = {id}
            '''

    lessons = query_all(query)

    print(lessons)

    return jsonify(lessons)


# 根据lesson_id 查询sentences 列表
@pr.route('/lessons/<id>')
def get_sentences(id):
    query = f"SELECT * FROM sentences where lesson_id = {id} "
    lesson = query_all(query)
    return jsonify(lesson)



@pr.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

