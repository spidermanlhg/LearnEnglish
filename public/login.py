
from split_sound import split_sound
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import shutil
from flask import Flask, render_template,request,session,redirect,url_for,make_response,Response
from datetime import datetime , timedelta


# app = Flask( __name__ )

# app.secret_key = '459deb4beb0c7bdc487972b4e3a31ab575b895a97d6926623459f302d7ed5a68'


# @app.route( "/login" ,methods=["GET", "POST"]  )
# def login():
    
#     print( session.get("name") )

#     if request.method == "GET":

#         username = request.cookies.get('username')

#         if username :
#             return redirect("/user")
#         else:
#             return  render_template('login.html')


#     if request.method == 'POST':

#         # print( request.form["name"] )

#         username = request.form["username"]
#         password = request.form["password"]
        
#         if  (username == "lhg")  &  (password=="123456") :

#             # expires = datetime.now() + timedelta(seconds=10 ) 

#             # resp = make_response(   render_template( "user.html" , username=username   )   )
#             # resp.set_cookie('username', 'lhg' ,  max_age=expires  )

#             # response对象
#             resp = Response("username")
#             # 设置cookie值
#             resp.set_cookie("username","lhg")
            
#             return  redirect( "/user" )

#         else:

#             return "账号错误"
            

# @app.route( "/user" ,methods=["GET", "POST"]  )
# def user():

#     if request.method == 'GET':

#         username = request.cookies.get('username')

#         if username:
#             return render_template("user.html" , username=username )
#         else:
#             return redirect("/login")
    

#     if request.method == "POST":

#         resp = make_response(  render_template( "login.html"   )   )  # 设置响应体

#         resp.delete_cookie("username")




# app = Flask( __name__ )
# # Set the secret key to some random bytes. Keep this really secret!
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))


# if __name__ == "__main__":
#     app.run( host= "0.0.0.0", port=5000,  debug=True )


# import redis
# import json
# # 连接redis服务器
# r = redis.Redis(  host='10.100.3.38',  port=6379,  db=8   )
# # key为database
# # r.set('webname','www.biancheng.net')
# # print( r.get('webname') )

# # print(  r.get(   "age" )   )

# r.set( )

# r.mset({'username':'jacak','password':'123'})


# print( r.mget( "username" ) )

# d =  {"a":1} 

# a = [1,2,3]


# r.set(  "arr",  json.dumps(a)  )

# r.set( "dict",  json.dumps(d)    )



# #mset参数为字典
# r.mset({'username':'jacak','password':'123'})
# print(r.mget('username','password'))
# # 查看value长度
# print(r.strlen('username'))
# # 数值操作
# r.set('age','15')
# r.incrby('age',5)
# r.decrby('age',5)
# r.incr('age')
# r.decr('age')
# r.incrbyfloat('age',5.2)
# r.incrbyfloat('age',-10.5)
# print(r.get('age'))
# # 删除key
# r.delete('username')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pymongo import MongoClient
import os, sys


#连接mongo数据库，连接crm库


#连接mongo数据库，连接crm表
def get_mongodb(x):
    
    '''
    x传入mongo的数据库名称
    return 一个数据库对象
    '''
    #directConnection 增加了参数directConnection = True , 不使用集群，而是使用直连的方式连接 mongo
    conn = MongoClient( host='127.0.0.1', port=27017, username = 'spidermanlhg', password = '19830125' )
    db = conn[x]
    return db


db = get_mongodb('test')

