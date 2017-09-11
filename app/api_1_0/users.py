from flask import jsonify, request, g, abort, url_for, current_app, session
from .. import db
from ..models import Permission, User
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/render')
def render():
    if session.get('json_list'):
        response = jsonify(count=session.get('json_list')[0],
                           step0=session.get('json_list')[1],
                           step1=session.get('json_list')[2],
                           step2=session.get('json_list')[3],
                           step3=session.get('json_list')[4],
                           step4=session.get('json_list')[5],
                           step5=session.get('json_list')[6],
                           step6=session.get('json_list')[7],
                           step7=session.get('json_list')[8] if len(session.get('json_list')) > 8 else '',
                           step8=session.get('json_list')[9] if len(session.get('json_list')) > 9 else '',
                           step9=session.get('json_list')[10] if len(session.get('json_list')) > 10 else '',
                           step10=session.get('json_list')[11] if len(session.get('json_list')) > 11 else '',
                           step11=session.get('json_list')[12] if len(session.get('json_list')) > 12 else '',
                           step12=session.get('json_list')[13] if len(session.get('json_list')) > 13 else '',
                           step13=session.get('json_list')[14] if len(session.get('json_list')) > 14 else '')
    else:
        response = jsonify(step0='Failed')
    return response


@api.route('/users')
def get_users():
    users = User.query.all()
    # return jsonify({'users': [user.to_json() for user in users]})
    return jsonify(username="username",
                   email="email",
                   id="id")


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


# 后台解析JSON文件
# @api.route('/users/', methods=['POST'])
# @permission_required(Permission.WRITE_ARTICLES)
# def new_post():
#     # 从传来的JSON获得username等
#     # username = request.json.get('username')
#     # 再用这个username去更新该条数据库中其他字段信息
#     post = Post.from_json(request.json)
#     post.author = g.current_user
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_json()), 201, \
#         {'Location': url_for('api.get_post', id=post.id, _external=True)}
#
#
# @api.route('/users/<int:id>', methods=['PUT'])
# @permission_required(Permission.WRITE_ARTICLES)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     if g.current_user != post.author and \
#             not g.current_user.can(Permission.ADMINISTER):
#         return forbidden('Insufficient permissions')
#     post.body = request.json.get('body', post.body)
#     db.session.add(post)
#     return jsonify(post.to_json())