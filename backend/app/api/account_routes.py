from flask import Blueprint, request,jsonify, render_template,session,redirect,url_for
import hashlib,os

from app.utils.db import *

ac = Blueprint("account" , __name__)


@ac.route( '/api/login' , methods = ['POST']  )
def login():
    
    role = request.json.get('role')
    username = request.json.get("username")
    password = request.json.get("password")

    # print( username )

    sql = f"select * from users where role={int(role)} and username='{username}' and password='{password}'"
    user_info = query_one( sql  )

    if user_info:
        
        session["user_info"] = user_info
        session.permanent = True

        return { "status":"ok", "user_info":user_info }
    
    else :
        return { "status":"fail", "error":"用户名或密码错误"  }


# 获取登录用户信息
@ac.route( '/api/cur_user' , methods = ['get']  )
def cur_user():
    
    user_info = session.get("user_info")

    if not user_info:
        return {"status": "fail", "error": "用户未登录"}

    username = user_info.get('username')

    return {"status": "ok", "username": username }


# 获取登录用户信息
@ac.route( '/api/logout' , methods = ['get']  )
def logout():
    
    session.pop('user_info', None)

    return { "status":"ok",  "msg":"退出登录" }
 
        

        



