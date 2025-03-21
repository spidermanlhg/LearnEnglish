from flask import Flask, session,redirect,request,url_for
from app.api.public_routes import pr
from app.api.admin_routes import ar
from app.api.account_routes import ac
from app.api.file_routes import fr
from datetime import timedelta

#获取用户登录信息
def auth():
    if request.path.startswith('/admin') and 'user_id' not in session:
        return '', 401

def create_app():
    app = Flask(__name__ )

    app.register_blueprint(pr)
    app.register_blueprint(ar)
    app.register_blueprint(ac)
    app.register_blueprint(fr)


    app.secret_key ="nicaibudaomima"   #session加密key
    app.permanent_session_lifetime = timedelta(days=30)
    # app.before_request( auth ) #用户登录的拦截器

    return app
