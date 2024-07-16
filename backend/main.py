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



# 上传音频文件接口
@app.route('/api/upload/<path>', methods=['POST'])
def upload( path ):

    new_path = 'uploads/' + path 

    if not os.path.exists( new_path):
        os.mkdir( new_path )
    else:
        return jsonify(False)    

    file = request.files['file']

    file.save( new_path+ "//" + file.filename)

    return jsonify(True)   



@app.route('/api/sentence/<int:sid>/<int:tid>', methods=['GET'])
def sentence(sid,tid):
    
    
    fiels =  os.listdir( 'uploads/' + str(sid)  )

    return jsonify( fiels[ int(tid)-1] )



# @app.route('/api/split', methods=['POST']  )
# def split(sid,tid):
    
#     split_sound( )

#     return jsonify( fiels[ int(tid)-1] )


# 服务端返回音频文件
@app.route('/audio/<bid>/<lid>/<sid>', methods=['GET'])
def play_audio(bid, lid, sid):  # 注意这里添加了 bid 和 lid 作为参数

    # 指定音频文件的路径
    audio_path = f'data/{bid}/{lid}/{sid}.mp3'
    
    # 使用 send_file 函数发送音频文件
    return send_file(audio_path, mimetype='audio/mpeg')


 

if __name__ == '__main__':
    app.run( debug=True )