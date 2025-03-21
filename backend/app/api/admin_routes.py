from flask import (Blueprint, Flask, jsonify, request, send_file, session)
from werkzeug.utils import secure_filename
from config import db_config
from app.utils.db import query_all, query_one, query_insert, query_delete, query_update
from app.utils.split_sound import split_sound
import os,shutil

# 获取当前文件所在目录的上级目录作为项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 创建蓝图
ar = Blueprint('admin', __name__ , url_prefix='/api/admin'  )


# 创建book文件夹，并把新创建的文件夹名称写入数据库中。
@ar.route('/add_book', methods=['POST'])
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
@ar.route('/upload', methods=['POST', 'GET'])
def upload_files():

    bookid = request.args.get("bookid")

    if request.method == 'POST':
        f = request.files['file']
        bookname = secure_filename(f.filename)
        f.save(os.path.join(BASE_DIR, 'uploads', bookid, bookname))

    # 插入书籍信息，book_id自增，不需要传入
    query = f"INSERT INTO lessons (book_id, name) VALUES( '{bookid}', '{bookname}' )"
    query_insert(query)

    return jsonify({'message': 'successfully', }), 200


# 根据bookid批量拆分 本书下所有的mp3音频文件，并把拆分后的mp3音频文件存入到sentence表中。
@ar.route('/split/<bookid>', methods=['GET'])
def split_book(bookid):

    path = os.path.join(BASE_DIR, "data", str(bookid))

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
                BASE_DIR, "uploads", str(bookid), i['name']),
            audiotype="mp3",
            output=os.path.join(BASE_DIR, "data", str(bookid), str(i['id'])),
            by_sentence=True,
            min_segment_length=1.5,  # 最小分段长度（秒）
            max_segment_length=8.0   # 最大分段长度（秒）
        )

        print( sound_list )

        for s in sound_list:

            # 检查是否有文本内容，如果有则存储到数据库
            if 'text' in s:
                query = "INSERT INTO sentences (sn, book_id, lesson_id, name, text) VALUES (%s, %s, %s, %s, %s)"
                params = (s['sn'], bookid, i['id'], s['name'], s['text'])
            else:
                query = "INSERT INTO sentences (sn, book_id, lesson_id, name) VALUES (%s, %s, %s, %s)"
                params = (s['sn'], bookid, i['id'], s['name'])
            query_insert(query, params)

    return jsonify({'message': 'Files split successfully'})


# 根据lessonid，单独分隔音频
@ar.route('/split/lesson/<lessonid>', methods=['GET'])
def split_lesson(lessonid):
    try:
        print(f'开始处理课程 {lessonid}')
        # 根据lesson id 查询课程信息
        query = f'SELECT * FROM `lessons` WHERE `id` = {lessonid}'
        print(f'执行查询: {query}')
        lesson = query_one(query)
        
        if not lesson:
            print(f'未找到课程 {lessonid}')
            return jsonify({'error': 'Lesson not found'}), 404

        print(f'找到课程: {lesson}')
        audiopath = os.path.join(
            BASE_DIR, "uploads", str(
                lesson['book_id']), lesson['name'])
        
        print(f'音频文件路径: {audiopath}')
        # 检查音频文件是否存在
        if not os.path.exists(audiopath):
            print(f'音频文件不存在: {audiopath}')
            return jsonify({'error': f'Audio file not found: {lesson["name"]}'}), 404

        audiotype = "mp3"
        output = os.path.join(
            BASE_DIR, "data", str(
                lesson['book_id']), str(
                lesson['id']))

        print(f'处理课程 {lessonid}, 音频文件: {audiopath}, 输出目录: {output}')

        # 在生成前，先删除掉已存在分隔的音频文件，以免分隔后的文件重复
        if os.path.exists(output):
            print(f'删除已存在的输出目录: {output}')
            shutil.rmtree(output, ignore_errors=True)
            # 同时删除数据库中，这个lessonid下所有的sentences
            query = f"DELETE FROM sentences where lesson_id = {lessonid}"
            print(f'删除已存在的句子记录: {query}')
            query_delete(query)

        # 确保输出目录存在
        print(f'创建输出目录: {os.path.dirname(output)}')
        os.makedirs(os.path.dirname(output), exist_ok=True)

        print(f'调用split_sound函数拆分音频')
        sound_list = split_sound(
            audiopath=audiopath,
            audiotype=audiotype,
            output=output,
            by_sentence=True,
            min_segment_length=1.5,  # 最小分段长度（秒）
            max_segment_length=8.0   # 最大分段长度（秒）
        )

        if not sound_list:
            print(f'未生成任何音频片段')
            return jsonify({'error': 'No segments were generated from the audio file'}), 500

        print(f'生成了 {len(sound_list)} 个音频片段')
        
        # 将拆分后的句子信息写入数据库
        for s in sound_list:
            # 检查是否有文本内容，如果有则存储到数据库
            if 'text' in s:
                query = "INSERT INTO sentences (sn, book_id, lesson_id, name, text) VALUES (%s, %s, %s, %s, %s)"
                params = (s['sn'], lesson['book_id'], lessonid, s['name'], s['text'])
                print(f'插入带文本的句子: {s["name"]}, 文本: {s["text"][:30]}...')
            else:
                query = "INSERT INTO sentences (sn, book_id, lesson_id, name) VALUES (%s, %s, %s, %s)"
                params = (s['sn'], lesson['book_id'], lessonid, s['name'])
                print(f'插入不带文本的句子: {s["name"]}')
            query_insert(query, params)

        # 更新lesson的status为1，表示已完成拆分
        update_query = f"UPDATE lessons SET status = 1 WHERE id = {lessonid}"
        query_update(update_query)

        return jsonify({'message': 'Files split successfully', 'segments': len(sound_list)})

    except Exception as e:
        print(f'处理课程 {lessonid} 时出错: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# 删除单个lesson
@ar.route('/delete_lessons/<lessonid>', methods=['POST', 'DELETE'])
def delete_lesson(lessonid):
    try:
        # 查询课程信息
        query = f'SELECT * FROM lessons WHERE id = {lessonid}'
        lesson = query_one(query)
        
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404

        # 删除关联的sentences记录
        query_delete(f'DELETE FROM sentences WHERE lesson_id = {lessonid}')

        # 删除课程记录
        query_delete(f'DELETE FROM lessons WHERE id = {lessonid}')

        # 删除音频文件
        audio_path = os.path.join(BASE_DIR, 'uploads', str(lesson['book_id']), lesson['name'])
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # 删除拆分后的目录
        split_dir = os.path.join(BASE_DIR, 'data', str(lesson['book_id']), str(lessonid))
        if os.path.exists(split_dir):
            shutil.rmtree(split_dir)

        return jsonify({'message': 'Lesson deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 删除单个book
@ar.route('/delete_book/<bookid>', methods=['DELETE'])
def delete_book(bookid):
    try:
        # 查询书籍信息
        query = f'SELECT * FROM books WHERE id = {bookid}'
        book = query_one(query)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # 检查是否存在lessons
        query = f'SELECT COUNT(*) as count FROM lessons WHERE book_id = {bookid}'
        result = query_one(query)
        
        if result['count'] > 0:
            return jsonify({
                'error': 'Cannot delete book',
                'message': f'Book has {result["count"]} lessons. Please delete all lessons first.'
            }), 400

        # 删除书籍记录
        query_delete(f'DELETE FROM books WHERE id = {bookid}')

        # 删除书籍相关文件夹
        upload_dir = os.path.join(BASE_DIR, 'uploads', str(bookid))
        data_dir = os.path.join(BASE_DIR, 'data', str(bookid))
        
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

        return jsonify({'message': 'Book deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 批量删除lessons
@ar.route('/delete_lessons', methods=['POST', 'DELETE'])
def delete_lessons():
    # 检查用户是否已登录
    # user_info = session.get('user_info')
    # if not user_info:
    #     return jsonify({'error': 'Unauthorized access'}), 401
        
    try:
        # 获取要删除的lesson id列表
        lesson_ids = request.json.get('lesson_ids', [])
        
        if not lesson_ids or not isinstance(lesson_ids, list):
            return jsonify({'error': 'Missing or invalid lesson_ids parameter'}), 400
            
        success_count = 0
        failed_ids = []
        
        for lessonid in lesson_ids:
            try:
                # 查询课程信息
                query = f'SELECT * FROM lessons WHERE id = {lessonid}'
                lesson = query_one(query)
                
                if not lesson:
                    failed_ids.append({'id': lessonid, 'reason': 'Lesson not found'})
                    continue

                # 删除关联的sentences记录
                query_delete(f'DELETE FROM sentences WHERE lesson_id = {lessonid}')

                # 删除课程记录
                query_delete(f'DELETE FROM lessons WHERE id = {lessonid}')

                # 删除音频文件
                audio_path = os.path.join(BASE_DIR, 'uploads', str(lesson['book_id']), lesson['name'])
                if os.path.exists(audio_path):
                    os.remove(audio_path)

                # 删除拆分后的目录
                split_dir = os.path.join(BASE_DIR, 'data', str(lesson['book_id']), str(lessonid))
                if os.path.exists(split_dir):
                    shutil.rmtree(split_dir)
                    
                success_count += 1
                
            except Exception as e:
                failed_ids.append({'id': lessonid, 'reason': str(e)})
        
        result = {
            'message': f'{success_count} lessons deleted successfully',
            'success_count': success_count,
            'total_count': len(lesson_ids)
        }
        
        if failed_ids:
            result['failed_ids'] = failed_ids
            
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


