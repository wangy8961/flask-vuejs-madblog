from flask import jsonify, g
from app.api import bp
from app.api.auth import basic_auth
from app.extensions import db


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    # 每次用户登录（即成功获取 JWT 后），更新 last_seen 时间
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token': token})
