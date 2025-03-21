
from flask import (Blueprint, Flask, jsonify, request,send_file)
from werkzeug.utils import secure_filename
from config import cur_dir
import os,shutil

# 创建蓝图
fr = Blueprint('files', __name__ , )
@fr.route('/')


# 服务端返回音频文件
@fr.route('/audio/<bid>/<lid>/<sid>', methods=['GET'])
def play_audio(bid, lid, sid):  # 注意这里添加了 bid 和 lid 作为参数

    # 指定音频文件的路径

    print( cur_dir )

    audio_path = os.path.join(cur_dir, "data", str(bid), str(lid), str(sid))

    # 使用 send_file 函数发送音频文件
    return send_file(audio_path, mimetype='audio/mpeg')


