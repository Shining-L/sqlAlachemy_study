from models import db
from sqlalchemy import func
from sqlalchemy.orm import relationship

"""
一对多： 一个父对象与多个字对象关联
多对多
一对一
多对一

relationship 用于两个模型之间建立关联
通常在我们父模型中使用，用于定义与子模型的关系
"""


# 创建数据库类 分类表 自定义模型类就可以使用sqlalchemy提供的各种orm的特性
class Categories(db.Model):
    __tablename__ = "img_categories"
    # __tablename__ 指定模型对应的数据库表名
    # status = 1`

    # 对应数据表中的列
    # id name对应的就是数据表中的字段名
    cate_id = db.Column(db.Integer, primary_key=True, index=True)
    # 用户名重复，昵称已经被占用了 unique 不能重复
    cate_name = db.Column(db.String(10), unique=True, index=True)
    # 账号
    email = db.Column(db.String(50), unique=True)
    #  True / false 设置为可选 server_default默认值传字符串
    showed = db.Column(db.Boolean, server_default="1", nullable=False)
    created_time = db.Column(db.Date, server_default=func.current_date(), nullable=False)
    # 一对多关系  backref 
    # relationships(name, secondary, primaryjoin, backref)
    # select
    """
        image = relationships("images", backref="category", lazy=True)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        TypeError: 'module' object is not callable
    """
    # primaryjoin 是一个定义关系的关键字参数，用于指定两个表之间的连接条件，这些条件将用于创建关系的主键连接
    """
    sqlalchemy.exc.ArgumentError: Could not locate any relevant foreign key columns for primary join condition 'img_categories.cate_id = images.img_id' on relationship Categories.image.  Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or are annotated in the join condition with the foreign() annotation.
    uselist = False 不在是一对多，而是一对一 
    """
    image = relationship("images", primaryjoin="Categories.cate_id==images.category_id", backref="category", lazy=True)


class images(db.Model):
    __tablename__ = "images"
    img_id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(50), nullable=False)
    # 外键 添加外键约束的时候，需要给这个约束指定名称
    category_id = db.Column(db.Integer, db.ForeignKey('img_categories.cate_id'),
                            nullable=False)
    