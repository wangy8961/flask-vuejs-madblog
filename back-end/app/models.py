from datetime import datetime, timedelta
from hashlib import md5
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app
from app.extensions import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    # 设置数据库表名，Post模型中的外键 user_id 会引用 users.id
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # 反向引用，直接查询出当前用户的所有博客文章; 同时，Post实例中会有 author 属性
    # cascade 用于级联删除，当删除user时，该user下面的所有posts都会被级联删除
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''头像'''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def get_jwt(self, expires_in=3600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'name': self.name if self.name else self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))


class Post(PaginatedAPIMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    # 外键, 直接操纵数据库当user下面有posts时不允许删除user，下面仅仅是 ORM-level “delete” cascade
    # db.ForeignKey('users.id', ondelete='CASCADE') 会同时在数据库中指定 FOREIGN KEY level “ON DELETE” cascade
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''
        target: 有监听事件发生的 Post 实例对象
        value: 监听哪个字段的变化
        '''
        if not target.summary:  # 如果前端不填写摘要，是空str，而不是None
            target.summary = value[:200] + '  ... ...'  # 截取 body 字段的前200个字符给 summary

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'body': self.body,
            'timestamp': self.timestamp,
            'views': self.views,
            'author': self.author.to_dict(),
            '_links': {
                'self': url_for('api.get_post', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'summary', 'body']:
            if field in data:
                setattr(self, field, data[field])


db.event.listen(Post.body, 'set', Post.on_changed_body)  # body 字段有变化时，执行 on_changed_body() 方法
