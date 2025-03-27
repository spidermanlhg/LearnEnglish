
from flask import (Blueprint, Flask, jsonify, request,send_file)
from werkzeug.utils import secure_filename
from config import cur_dir
import os,shutil

# 创建蓝图
fr = Blueprint('files', __name__ , url_prefix='/api/audio' )
@fr.route('/')


# 服务端返回音频文件
@fr.route('/<bid>/<lid>/<sid>', methods=['GET'])
def play_audio(bid, lid, sid):
    # 指定音频文件的路径
    audio_path = os.path.join(cur_dir, "data", str(bid), str(lid), str(sid))
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        return jsonify({'error': 'Audio file not found'}), 404
        
    try:
        # 使用send_file函数发送音频文件，显式设置mimetype和添加headers
        response = send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name=os.path.basename(audio_path)
        )
        response.headers['Content-Type'] = 'audio/mpeg'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


