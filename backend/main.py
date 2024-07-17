from flask import Flask, request, jsonify,render_template,send_file
from werkzeug.utils import secure_filename
import os
# import split_sound
import pymysql
import datetime

import pandas as pd

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


db_config = {
    'host': '120.46.184.38',
    'user': 'spidermanlhg',
    'password': '19830125',
    'database': 'learn_english',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def query_db(query):

    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()


# 创建book文件夹
@app.route( '/api/add_book' , methods=['POST'] )
def add_book():
    # 获取POST请求中的数据
    book_name = request.json.get('book_name')

    if not book_name:
        return jsonify({'error': 'Missing book_name'}), 400

    # 插入书籍信息到数据库
    try:
        connection = pymysql.connect(**db_config)

        cursor = connection.cursor()
        # 插入书籍信息，book_id自增，不需要传入
        insert_query = "INSERT INTO books (name) VALUES (%s)"
        cursor.execute(insert_query, (book_name))
        connection.commit()

        # 获取刚插入的书籍的自增id
        book_id = cursor.lastrowid

        # 创建以书籍id为名的文件夹
        folder_path = os.path.join(os.getcwd(), 'uploads', str(book_id))
        os.makedirs(folder_path)

        return jsonify({'message': 'Book added successfully', 'book_id': book_id}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()




# 显示所有的books
@app.route('/api/books')
def get_books():
    query = "SELECT * FROM books"
    books = query_db(query)
    book_list = [{"id": book["id"], "name": book['name']} for book in books]
    return jsonify(book_list)


# 根据book_id 查询 lessons 列表
@app.route('/api/books/<id>')
def get_lessons(id):
    query = f"SELECT * FROM lessons where book_id = {id} "
    lesson = query_db(query)
    return jsonify(lesson)


# 根据lesson_id 查询sentences 列表
@app.route('/api/lessons/<id>')
def get_sentences(id):
    query = f"SELECT * FROM sentences where lesson_id = {id} "
    lesson = query_db(query)
    return jsonify(lesson)



#批量上传课程音频文件
@app.route('/api/upload', methods=['POST', 'GET'])
def upload_files():
    # 获取book_id
    # book_id = request.form.get('book_id')


    # # 检查book_id是否存在
    # if not book_id:
    #     return jsonify({'error': 'Missing book_id parameter'}), 400
    
    # # 检查是否有上传的文件
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file part in the request'}), 400
    
    # files = request.files.getlist('file')

    # if 'file' not in request.files:
    #     return 'No file part'
    # file = request.files['file']
    # # 处理文件，比如保存到服务器某个路径
    # file.save('/uploaded/')
    # return 'File uploaded successfully'

    bookid = request.args.get("bookid")
 

    if request.method == 'POST':
        f = request.files['file']
        # print(request.files)
        bookname = secure_filename(f.filename)
        f.save(os.path.join( 'uploads' , bookname))


    try:
        connection = pymysql.connect(**db_config)

        cursor = connection.cursor()
        # 插入书籍信息，book_id自增，不需要传入
        insert_query = "INSERT INTO lessons (book_id, name) VALUES( %s, %s )"
        cursor.execute(insert_query, (bookid, bookname)  )
        connection.commit()


        return jsonify({'message': 'successfully',}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        connection.close()
    

    return 'file uploaded successfully'

   
    # # 检查是否有文件上传
    # if len(files) == 0:
    #     return jsonify({'error': 'No files uploaded'}), 400
    
    # # 创建存储文件的路径
    # book_upload_folder = os.path.join(app.config['upload'], str(book_id))
    # os.makedirs(book_upload_folder, exist_ok=True)

    # # 处理每个上传的文件
    # for file in files:
    #     # 检查文件名
    #     if file.filename == '':
    #         return jsonify({'error': 'One of the uploaded files has no filename'}), 400
        
    #     # 安全获取文件名
    #     filename = secure_filename(file.filename)

    #     # 保存文件到指定路径
    #     file.save(os.path.join(book_upload_folder, filename))

    #     # 将文件信息存入数据库
    #     new_lesson = Lesson(book_id=book_id, name=filename)
    #     db.session.add(new_lesson)
    #     db.session.commit()

    # return jsonify({'message': 'Files uploaded successfully'}), 200




# @app.route('/api/split', methods=['POST']  )
# def split(sid,tid):
    
#     split_sound( )

#     return jsonify( fiels[ int(tid)-1] )


# 服务端返回音频文件
@app.route('/audio/<bid>/<lid>/<sid>', methods=['GET'])
def play_audio(bid, lid, sid):  # 注意这里添加了 bid 和 lid 作为参数

    # 指定音频文件的路径
    audio_path = f'data/{bid}/{lid}/{sid}'
    
    # 使用 send_file 函数发送音频文件
    return send_file(audio_path, mimetype='audio/mpeg')





    
 

if __name__ == '__main__':
    app.run( debug=True )