from flask import Blueprint, request,jsonify, render_template,session,redirect,url_for
import hashlib,os

from app.utils.db import *

ac = Blueprint("account" , __name__)


@ac.route( '/api/login' , methods = ['POST']  )
def login():
    
    try:
        role = request.json.get('role')
        username = request.json.get("username")
        password = request.json.get("password")

        if not all([role, username, password]):
            return {"status": "fail", "error": "请填写完整的登录信息"}
        
        # 使用参数化查询防止SQL注入
        sql = "select * from users where role=%s and username=%s and password=%s"
        params = (int(role), username, password)
        # print(params,sql)
        user_info = query_one(sql, params)

        if user_info:
            session["user_info"] = user_info
            session.permanent = True
            return {"status": "ok", "user_info": user_info}
        else:
            return {"status": "fail", "error": "用户名或密码错误"}
            
    except Exception as e:
        return {"status": "fail", "error": str(e)}


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
 
        

        



