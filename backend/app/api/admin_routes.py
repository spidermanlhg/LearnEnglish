from flask import (Blueprint, Flask, jsonify, request,send_file)
from werkzeug.utils import secure_filename
from config import cur_dir, db_config
from app.utils.db import *
from app.utils.split_sound import split_sound
import os,shutil


# 创建蓝图
admin = Blueprint('admin', __name__)


# 创建book文件夹
@admin.route('/api/add_book', methods=['POST'])
def add_book():
    # 获取POST请求中的数据
    book_name = request.json.get('book_name')

    if not book_name:
        return jsonify({'error': 'Missing book_name'}), 400

    # 插入书籍信息到数据库

    # 插入书籍信息，book_id自增，不需要传入
    query = f"INSERT INTO books (name) VALUES ('{book_name}') "
    # 执行插入操作，并获取刚插入的书籍的自增id
    result = query_insert(query)

    book_id = result['lastrowid']

    # 创建以书籍id为名的文件夹
    folder_path = os.path.join(cur_dir, 'uploads', str(book_id))
    os.makedirs(folder_path)

    return jsonify(
        {'message': f'Book added successfully', 'book_id': book_id}), 200


# 批量上传课程音频文件
@admin.route('/api/upload', methods=['POST', 'GET'])
def upload_files():

    bookid = request.args.get("bookid")

    if request.method == 'POST':
        f = request.files['file']
        bookname = secure_filename(f.filename)
        f.save(os.path.join(cur_dir, 'uploads', bookid, bookname))

    # 插入书籍信息，book_id自增，不需要传入
    query = f"INSERT INTO lessons (book_id, name) VALUES( '{bookid}', '{bookname}' )"
    query_insert(query)

    return jsonify({'message': 'successfully', }), 200


# 根据bookid批量拆分 本书下所有的mp3音频文件，并把拆分后的mp3音频文件存入到sentence表中。
@admin.route('/api/split/<bookid>', methods=['GET'])
def split_book(bookid):

    path = os.path.join(cur_dir, "data", str(bookid))

    # 判断目录是否存在
    if os.path.exists(path):

        # 在生成前，先删除掉已存在分隔的音频文件，以免分隔后的文件重复。
        shutil.rmtree(path, ignore_errors=True)
        # 同时删除数据库中，这个bookid下所有的sentences。
        query = f"DELETE FROM sentences where book_id = {bookid} "
        query_delete(query)

    # 根据bookid查询所有的lessons
    query = f"SELECT * FROM lessons where book_id = {bookid} "
    lessons = query_all(query)

    # 对所有的lessons遍历
    for i in lessons:
        sound_list = split_sound(
            audiopath=os.path.join(
                cur_dir, "uploads", str(bookid), i['name']),
            audiotype="mp3",
            output=os.path.join(cur_dir, "data", str(bookid), str(i['id']))
        )

        for s in sound_list:

            query = f"INSERT INTO sentences (sn, book_id, lesson_id, name) VALUES ( {s['sn'] }, { bookid } ,{i['id']}, '{s['name']}' )"
            query_insert(query)

    return jsonify({'message': 'Files split successfully'})


# 根据lessonid分隔音频
@admin.route('/api/split/lesson/<lessonid>', methods=['GET'])
def split_lesson(lessonid):

    # 根据lesson id 查询课程信息
    query = f'SELECT * FROM `lessons` WHERE `id` = {lessonid}'
    query_one( query )

    audiopath = os.path.join(
        cur_dir, "uploads", str(
            lesson['book_id']), lesson['name'])
    audiotype = "mp3"
    output = os.path.join(
        cur_dir, "data", str(
            lesson['book_id']), str(
            lesson['id']))

    sound_list = split_sound(
        audiopath=audiopath,
        audiotype=audiotype,
        output=output)

    print(sound_list)

    return jsonify({'message': 'Files split successfully'})


