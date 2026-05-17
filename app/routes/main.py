from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '欢迎使用 Flask 应用',
        'status': 'success'
    })


@main_bp.route('/health')
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy'
    })
