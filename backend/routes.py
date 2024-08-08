

from flask import (Blueprint, Flask, jsonify, request,send_file)
from werkzeug.utils import secure_filename
from config import cur_dir, db_config
from fn import *
from split_sound import split_sound
import os


# 创建蓝图
bp = Blueprint('my_routes', __name__)
@bp.route('/')
def index():
    return jsonify("This is index")


# 创建book文件夹
@bp.route('/api/add_book', methods=['POST'])
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


# 查询所有的books，返回书籍列表包括 书籍id，书籍名称，课程数量。
@bp.route('/api/books')
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
@bp.route('/api/books/<id>')
def get_lessons(id):

    query = f'''
                SELECT * FROM lessons
                INNER JOIN books ON lessons.book_id = books.id
                WHERE lessons.book_id = {id}
            '''

    lessons = query_all(query)

    return jsonify(lessons)


# 根据lesson_id 查询sentences 列表
@bp.route('/api/lessons/<id>')
def get_sentences(id):
    query = f"SELECT * FROM sentences where lesson_id = {id} "
    lesson = query_all(query)
    return jsonify(lesson)


# 批量上传课程音频文件
@bp.route('/api/upload', methods=['POST', 'GET'])
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
@bp.route('/api/split/<bookid>', methods=['GET'])
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
    query_all(query)

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
@bp.route('/api/split/lesson/<lessonid>', methods=['GET'])
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


# 服务端返回音频文件
@bp.route('/api/audio/<bid>/<lid>/<sid>', methods=['GET'])
def play_audio(bid, lid, sid):  # 注意这里添加了 bid 和 lid 作为参数

    # 指定音频文件的路径

    audio_path = os.path.join(cur_dir, "data", str(bid), str(lid), str(sid))

    # 使用 send_file 函数发送音频文件
    return send_file(audio_path, mimetype='audio/mpeg')


@bp.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


# 导出蓝图对象
def init_routes(app):
    app.register_blueprint(bp)
