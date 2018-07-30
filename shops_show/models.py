from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/reptile?charset=utf8"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# 绑定app至SQLAlchemy
db = SQLAlchemy(app)


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    title = db.Column(db.String(100))
    comment = db.Column(db.Integer)
    seller = db.Column(db.String(50))
    tags = db.Column(db.String(100))
    shop_class = db.Column(db.String(20))
    url = db.Column(db.String(255))
    img_path = db.Column(db.String(255))
    source = db.Column(db.String(20))
    crawl_time = db.Column(db.String(50))

    def __repr__(self):
        return self.name

if __name__=="__main__":
    pass