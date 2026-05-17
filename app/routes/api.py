from flask import Blueprint, jsonify, request
from app import db
from app.models import User

api_bp = Blueprint('api', __name__)


@api_bp.route('/users', methods=['GET'])
def get_users():
    """获取所有用户"""
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'count': len(users)
    })


@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建新用户"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': '用户名和邮箱是必填项'}), 400
    
    user = User(
        username=data['username'],
        email=data['email']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': '用户创建成功',
        'user': user.to_dict()
    }), 201


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取指定用户"""
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()})
