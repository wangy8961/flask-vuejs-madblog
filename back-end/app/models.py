import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import jwt
from time import time
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


# 粉丝关注他人
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

# 评论点赞
comments_likes = db.Table(
    'comments_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


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
    # followeds 是该用户关注了哪些用户列表
    # followers 是该用户的粉丝列表
    followeds = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # 用户发表的评论列表
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')
    # 用户最后一次查看 收到的评论 页面的时间，用来判断哪些收到的评论是新的
    last_recived_comments_read_time = db.Column(db.DateTime)
    # 用户最后一次查看 用户的粉丝 页面的时间，用来判断哪些粉丝是新的
    last_follows_read_time = db.Column(db.DateTime)
    # 用户最后一次查看 收到的点赞 页面的时间，用来判断哪些点赞是新的
    last_likes_read_time = db.Column(db.DateTime)
    # 用户最后一次查看 关注的人的博客 页面的时间，用来判断哪些文章是新的
    last_followeds_posts_read_time = db.Column(db.DateTime)
    # 用户的通知
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic', cascade='all, delete-orphan')
    # 用户发送的私信
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='sender', lazy='dynamic',
                                    cascade='all, delete-orphan')
    # 用户接收的私信
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic',
                                        cascade='all, delete-orphan')
    # 用户最后一次查看私信的时间
    last_messages_read_time = db.Column(db.DateTime)

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
            'followeds_count': self.followeds.count(),
            'followers_count': self.followers.count(),
            'posts_count': self.posts.count(),
            'followeds_posts_count': self.followeds_posts().count(),
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128),
                'followeds': url_for('api.get_followeds', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'posts': url_for('api.get_user_posts', id=self.id),
                'followeds_posts': url_for('api.get_user_followeds_posts', id=self.id),
                'comments': url_for('api.get_user_comments', id=self.id)
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
            'user_name': self.name if self.name else self.username,
            'user_avatar': base64.b64encode(self.avatar(24).
                                            encode('utf-8')).decode('utf-8'),
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
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))

    def is_following(self, user):
        '''判断当前用户是否已经关注了 user 这个用户对象，如果关注了，下面表达式左边是1，否则是0'''
        return self.followeds.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        '''当前用户开始关注 user 这个用户对象'''
        if not self.is_following(user):
            self.followeds.append(user)

    def unfollow(self, user):
        '''当前用户取消关注 user 这个用户对象'''
        if self.is_following(user):
            self.followeds.remove(user)

    def followeds_posts(self):
        '''获取当前用户的关注者的所有博客列表'''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.author_id)).filter(
                followers.c.follower_id == self.id)
        # 包含当前用户自己的博客列表
        # own = Post.query.filter_by(user_id=self.id)
        # return followed.union(own).order_by(Post.timestamp.desc())
        return followed.order_by(Post.timestamp.desc())

    def add_notification(self, name, data):
        '''给用户实例对象增加通知'''
        # 如果具有相同名称的通知已存在，则先删除该通知
        self.notifications.filter_by(name=name).delete()
        # 为用户添加通知，写入数据库
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def new_recived_comments(self):
        '''用户收到的新评论计数
        包括:
        1. 用户的所有文章下面新增的评论
        2. 用户发表的评论(或下面的子孙)被人回复了
        '''
        last_read_time = self.last_recived_comments_read_time or datetime(1900, 1, 1)
        # 用户发布的所有文章
        user_posts_ids = [post.id for post in self.posts.all()]
        # 用户文章下面的新评论, 即评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是自己(文章的作者)
        q1 = set(Comment.query.filter(Comment.post_id.in_(user_posts_ids), Comment.author != self).all())

        # 用户发表的评论被人回复了，找到每个用户评论的所有子孙
        q2 = set()
        for c in self.comments:
            q2 = q2 | c.get_descendants()
        q2 = q2 - set(self.comments.all())  # 除去子孙中，用户自己发的(因为是多级评论，用户可能还会在子孙中盖楼)，自己回复的不用通知
        # 用户收到的总评论集合为 q1 与 q2 的并集
        recived_comments = q1 | q2
        # 最后，再过滤掉 last_read_time 之前的评论
        return len([c for c in recived_comments if c.timestamp > last_read_time])

    def new_follows(self):
        '''用户的新粉丝计数'''
        last_read_time = self.last_follows_read_time or datetime(1900, 1, 1)
        return self.followers.filter(followers.c.timestamp > last_read_time).count()

    def new_likes(self):
        '''用户收到的新点赞计数'''
        last_read_time = self.last_likes_read_time or datetime(1900, 1, 1)
        # 当前用户发表的所有评论当中，哪些被点赞了
        comments = self.comments.join(comments_likes).all()
        # 新的点赞记录计数
        new_likes_count = 0
        for c in comments:
            # 获取点赞时间
            for u in c.likers:
                if u != self:  # 用户自己点赞自己的评论不需要被通知
                    res = db.engine.execute("select * from comments_likes where user_id={} and comment_id={}".format(u.id, c.id))
                    timestamp = datetime.strptime(list(res)[0][2], '%Y-%m-%d %H:%M:%S.%f')
                    # 判断本条点赞记录是否为新的
                    if timestamp > last_read_time:
                        new_likes_count += 1
        return new_likes_count

    def new_followeds_posts(self):
        '''用户关注的人的新发布的文章计数'''
        last_read_time = self.last_followeds_posts_read_time or datetime(1900, 1, 1)
        return self.followeds_posts().filter(Post.timestamp > last_read_time).count()

    def new_recived_messages(self):
        '''用户未读的私信计数'''
        last_read_time = self.last_messages_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


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
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                               cascade='all, delete-orphan')

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
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_post', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'comments': url_for('api.get_post_comments', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'summary', 'body', 'timestamp', 'views']:
            if field in data:
                setattr(self, field, data[field])


db.event.listen(Post.body, 'set', Post.on_changed_body)  # body 字段有变化时，执行 on_changed_body() 方法


class Comment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    mark_read = db.Column(db.Boolean, default=False)  # 文章作者会收到评论提醒，可以标为已读
    disabled = db.Column(db.Boolean, default=False)  # 屏蔽显示
    # 评论与对它点赞的人是多对多关系
    likers = db.relationship('User', secondary=comments_likes, backref=db.backref('liked_comments', lazy='dynamic'))
    # 外键，评论作者的 id
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 外键，评论所属文章的 id
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # 自引用的多级评论实现
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    # 级联删除的 cascade 必须定义在 "多" 的那一侧，所以不能这样定义: parent = db.relationship('Comment', backref='children', remote_side=[id], cascade='all, delete-orphan')
    parent = db.relationship('Comment', backref=db.backref('children', cascade='all, delete-orphan'), remote_side=[id])

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    def get_descendants(self):
        '''获取评论的所有子孙'''
        data = set()

        def descendants(comment):
            if comment.children:
                data.update(comment.children)
                for child in comment.children:
                    descendants(child)
        descendants(self)
        return data

    def get_ancestors(self):
        '''获取评论的所有祖先'''
        data = []

        def ancestors(comment):
            if comment.parent:
                data.append(comment.parent)
                ancestors(comment.parent)
        ancestors(self)
        return data

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'mark_read': self.mark_read,
            'disabled': self.disabled,
            'likers_id': [user.id for user in self.likers],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'post': {
                'id': self.post.id,
                'title': self.post.title,
                'author_id': self.post.author.id
            },
            'parent_id': self.parent.id if self.parent else None,
            # 'children': [child.to_dict() for child in self.children] if self.children else None,
            '_links': {
                'self': url_for('api.get_comment', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'post_url': url_for('api.get_post', id=self.post_id),
                'parent_url': url_for('api.get_comment', id=self.parent.id) if self.parent else None,
                'children_url': [url_for('api.get_comment', id=child.id) for child in self.children] if self.children else None
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp', 'mark_read', 'disabled', 'author_id', 'post_id', 'parent_id']:
            if field in data:
                setattr(self, field, data[field])

    def is_liked_by(self, user):
        '''判断用户 user 是否已经对该评论点过赞'''
        return user in self.likers

    def liked_by(self, user):
        '''点赞'''
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        '''取消点赞'''
        if self.is_liked_by(user):
            self.likers.remove(user)


class Notification(db.Model):  # 不需要分页
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def __repr__(self):
        return '<Notification {}>'.format(self.id)

    def get_data(self):
        return json.loads(str(self.payload_json))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'name': self.user.name,
                'avatar': self.user.avatar(128)
            },
            'timestamp': self.timestamp,
            'payload': self.get_data(),
            '_links': {
                'self': url_for('api.get_notification', id=self.id),
                'user_url': url_for('api.get_user', id=self.user_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])


class Message(PaginatedAPIMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'sender': self.sender.to_dict(),
            'recipient': self.recipient.to_dict(),
            '_links': {
                'self': url_for('api.get_message', id=self.id),
                'sender_url': url_for('api.get_user', id=self.sender_id),
                'recipient_url': url_for('api.get_user', id=self.recipient_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])
