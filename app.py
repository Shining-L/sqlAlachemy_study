from flask import Flask
from flask_migrate import Migrate
from models import db
from img_app import img_bp
from img_app import cate_bp

app = Flask(__name__)


# 导入配置文件

class Baseconfig(object):
    # mysql sqlite 协议名：表示使用mysql数据库/sqlite数据库
    # :// 协议分隔符
    # /test.db 表示数据库文件的路径
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = True


app.config.from_object(Baseconfig)

#  使用init_app方法将app关联起来
db.init_app(app)
# 实例化迁移类
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here

    return 'Hello World!'


app.register_blueprint(img_bp)
app.register_blueprint(cate_bp)
print(app.url_map)
if __name__ == '__main__':
    app.run()
