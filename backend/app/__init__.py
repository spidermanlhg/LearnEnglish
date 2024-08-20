from flask import Flask, session,redirect,request
from app.api.publick_routes import bp
from app.api.admin_routes import admin
from app.api.account import ac
from datetime import timedelta

#获取用户登录信息
def auth():

    if request.path.startswith('static'):
        return 

    if request.path == "/login":
        return 

    if request.path == "/api/login":
        return 

    user_info = session.get("user_info")

    if user_info:
        print(user_info)
        return 
    
    return { "status":"fail", "error":"登录失败"  }, 401



def create_app():
    app = Flask(__name__ )

    app.register_blueprint(bp)
    app.register_blueprint(admin)
    app.register_blueprint(ac)


    app.secret_key ="nicaibudaomima"   #session加密key
    app.permanent_session_lifetime = timedelta(days=30)
    app.before_request( auth ) #用户登录的拦截器

    return app
