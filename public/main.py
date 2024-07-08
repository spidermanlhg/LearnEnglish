from flask import Flask, request, jsonify,render_template
from werkzeug.utils import secure_filename
import os
import split_sound

import datetime

import pandas as pd


app = Flask(__name__)



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


 

if __name__ == '__main__':
    app.run( debug=True )