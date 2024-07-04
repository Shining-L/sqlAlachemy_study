# 提交数据
# 1.向模型提交数据 保存模型实例
# 2.保存
# session 是一个会话对象,管理数据库操作,作用是程序和数据库之间的中介
"""
session.add() ,创建一个新的模型对象，并且把它添加到会话中
session.commit() , 持久化， 把会话中的所有更改(新增、删除、更新)永久的保存到数据库中
session.rollback()， 如果事务过程发生了异常，可以使用session.rollback()来回滚更改
"""
# db.session.add(user)
from flask import Blueprint, jsonify, request

img_bp = Blueprint('images', __name__, url_prefix="/img")
from models import images, db
from sqlalchemy.orm import load_only
from sqlalchemy import func


@img_bp.route('/update', methods=['POST', "PUT"])
def img_update():
    # 从前端发送过来的数据，进行筛选，校验，保存
    # img_id = images.query.get(1)
    # img_id.img_name = "Python"
    # db.session.add(img_id)
    # db.session.commit()
    #
    # data = {
    #     "img_id": img_id.img_id,
    #     "img_name": img_id.img_name
    # }
    # return jsonify({"msg": "更新成功!", "data": data}), 200

    # 第二种方式
    img_name = request.json.get('img_name')

    if img_name is None:
        return {"msg": '无效的数据'}
    # 根据ID,name，修改一条数据
    images.query.filter_by(img_id=1).update({"img_name": img_name})
    db.session.commit()

    return jsonify({"msg": "更新成功!"}), 200
    # img = images()
    # db.session.add(img)
    # db.session.commit()


@img_bp.route('/list')
def img_list():
    # 从前端发送过来的数据，进行筛选，校验，保存
    # .query是属于session中对享，是一个属性，用于启动一个查询操作,
    # session是sqlalchemy ORM的核心，代表了一个数据库会话，
    #  images.query 实际上创建一个查询对象，这个对象是查询构造器(Query对象)
    # img = images.query.order_by(images.img_id.desc()).all() 降序方法
    # img = images.query.order_by(images.img_id.asc()).all()
    # img = db.session.query(images).all()
    # img = images.query.offset(2).all()
    # img = images.query.limit(5).all()
    # img = images.query.filter(images.category_id == 2).order_by(images.img_id.desc()).offset(0).limit(5).all()
    # img = images.query.options(load_only(images.img_name, images.category_id)).all()
    # 返回查询对象，所以需要通过迭代器遍
    # 聚合查询 聚合函数 -- 使用query对象构建了一个查询，依次使用了filter\group_by\方法
    # sql语句：select images.img_id , COUNT(images.img_id) from images where images.category_id=1 group by images.img_id;
    img = db.session.query(images.img_id, func.count(images.img_id)).filter(images.category_id == 1).group_by(
        images.img_id).all()
    data_list = []
    for img in img:
        data = {
            "id": img.img_id,
            "name": img.img_name,
            'category_id': img.category_id
        }
        data_list.append(data)
    return jsonify(data_list)


# 查询单个数据
@img_bp.route('/one')
def one():
    img = images.query.first()
    data = {
        "id": img.img_id,
        "name": img.img_name
    }

    return jsonify(data)


@img_bp.route('/one/<int:img_id>', methods=['GET'])
def get_img(img_id):
    # 请求 json
    # 表格 formdata
    img_id = images.query.get(img_id)
    # img_id = images.query.filter_by(img_id=img_id).order_by(images.img_id.desc()).all()

    if img_id:
        data = {
            "id": img_id.img_id,
            "name": img_id.img_name
        }
        return jsonify({'message': 'success', 'data': data}), 200
    else:
        return jsonify({"status": 1, "message": "数据格式为空"}), 404


@img_bp.route('/del/<int:img_id>', methods=['DELETE'])
def del_img(img_id):
    img_id = images.query.get(img_id)

    if img_id is None:
        return {"status": 1, "msg": "资源不存在", 'data': {}}, 404

    try:
        db.session.delete(img_id)
        db.session.flush()  # 发送所有挂起的保存到数据库的SQL命令，但是不会提交事务
        db.session.commit()  # 提交事务

    except Exception as e:
        db.session.rollback()  # 回滚事务
        return {"status": 1, "msg": str(e), "data": {}}, 500

    return {
        "status": 0,
        "msg": "删除成功",
        "data": {}
    }
    # db.session.delete(img_id)
    # db.session.commit()

    # images.query.filter_by(img_id=img_id).delete()
    # db.session.commit()
