from flask import Blueprint
from models import Categories, images, db
from datetime import datetime
from sqlalchemy import or_, and_, not_
from sqlalchemy.orm import load_only, contains_eager

cate_bp = Blueprint('categories', __name__, url_prefix="/cate")


# 查询所有的内容
@cate_bp.route('/')
def index():
    """
    filter_by
    filter
    是两种完全不同的查询构建方法,用于在数据中查询过程中添加过滤条件.
    filter_by 用于等值过滤 即查询条件是一个等式 =  返回的是一个查询对象，可以继续添加其他的条件
    filter 用于更复杂的过滤条件
    
    SELECT img_categories.cate_id AS img_categories_cate_id, img_categories.cate_name AS img_categories_cate_name, img_categories.email AS img_categories_email, img_categories.showed AS img_categories_showed, img_categories.created_time AS img_categories_created_time 
FROM img_categories 
WHERE img_categories.cate_id = ?
    """

    cate_id = Categories.query.filter_by(cate_id=1).all()
    data = []
    if cate_id:
        data = {
            'cate_id': cate_id[0].cate_id,
            'cate_name': cate_id[0].cate_name,
            'email': cate_id[0].email,
            'showed': cate_id[0].showed,
            'created_time': cate_id[0].created_time,
            'image': []
        }
        for i in cate_id[0].image:
            secod = {
                'img_id': i.img_id,
                'img_name': i.img_name,
                'category_id': i.category_id
            }
            data['image'].append(secod)
    return data


@cate_bp.route('/one')
def one():
    # cata_name = Categories.query.filter(Categories.cate_name == '风景图片').first()
    # cata_name = Categories.query.filter(or_(Categories.cate_name.startswith('风景'), Categories.showed != "1")).first()

    # TypeError: The view function for 'categories.one' did not return a valid response.
    # The function either returned None or ended without a return statement. 没有返回一个有效的响应，或者是为None

    # cata_name = Categories.query.filter(and_(Categories.cate_name.startswith('风景'), Categories.showed != "1")).first()
    # 非 就是条件判断为真则结果为假，若条件结果为假，则为真
    cata_name = Categories.query.filter(not_(Categories.cate_name.startswith('豪车'))).first()
    # img_id = Categories.query.join(Categories.image).options(load_only(Categories.cate_id, Categories.cate_name),
    #                                                          contains_eager(Categories.image).load_only(
    #                                                              images.img_name)).all()
    # print(img_id)
    if cata_name:
        data = {
            'cate_id': cata_name.cate_id,
            'cate_name': cata_name.cate_name,
            'email': cata_name.email,
            'showed': cata_name.showed,
            'created_time': cata_name.created_time,
            'image': []
        }
        for i in cata_name.image:
            secod = {
                'img_id': i.img_id,
                'img_name': i.img_name,
                'category_id': i.category_id
            }
            data['image'].append(secod)
        return data
