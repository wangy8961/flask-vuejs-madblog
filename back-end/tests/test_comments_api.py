from base64 import b64encode
from datetime import datetime, timedelta
import json
import unittest
from app import create_app, db
from app.models import User, Post, Comment
from tests import TestConfig


class CommentsAPITestCase(unittest.TestCase):
    def setUp(self):
        '''每个测试之前执行'''
        self.app = create_app(TestConfig)  # 创建Flask应用
        self.app_context = self.app.app_context()  # 激活(或推送)Flask应用上下文
        self.app_context.push()
        db.create_all()  # 通过SQLAlchemy来使用SQLite内存数据库，db.create_all()快速创建所有的数据库表
        self.client = self.app.test_client()  # Flask内建的测试客户端，模拟浏览器行为

    def tearDown(self):
        '''每个测试之后执行'''
        db.session.remove()
        db.drop_all()  # 删除所有数据库表
        self.app_context.pop()  # 退出Flask应用上下文

    def get_basic_auth_headers(self, username, password):
        '''创建Basic Auth认证的headers'''
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_token_auth_headers(self, username, password):
        '''创建JSON Web Token认证的headers'''
        headers = self.get_basic_auth_headers(username, password)
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']
        return {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_create_comment(self):
        # 测试在某篇博客文章下面发表评论
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        p = Post(title='first post from david', body='post from david', author=u2,
                 timestamp=datetime.utcnow() + timedelta(seconds=1))
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(p)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        # 1. 用户不传入任何必须的参数时
        data = json.dumps({})
        response = self.client.post('/api/comments/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You must post JSON data.')
        # 2. 缺少 body 时
        data = json.dumps({'post_id': 1})
        response = self.client.post('/api/comments/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'Body is required.')
        # 3. 缺少 post_id 时
        data = json.dumps({'body': 'comment from john'})
        response = self.client.post('/api/comments/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'Post id is required.')
        # 4. post_id 不正确，即找不到对应的博客文章时
        data = json.dumps({'post_id': 2, 'body': 'comment from john'})
        response = self.client.post('/api/comments/', headers=headers, data=data)
        self.assertEqual(response.status_code, 404)
        # 5. 正确提供参数时
        data = json.dumps({'post_id': 1, 'body': 'comment from john'})
        response = self.client.post('/api/comments/', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

    def test_get_comments(self):
        # 测试返回评论集合
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        p = Post(title='first post from david', body='post from david', author=u2,
                 timestamp=datetime.utcnow() + timedelta(seconds=1))

        c1 = Comment(body='first comment from john')
        c1.author = u1
        c1.post = p
        c2 = Comment(body='second comment from john')
        c2.author = u1
        c2.post = p

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(p)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/comments/', headers=headers)
        self.assertEqual(response.status_code, 200)
        # 判断返回的评论集合
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 2)
        self.assertIsNotNone(json_response.get('items'))
        self.assertEqual(json_response['items'][0]['body'], 'second comment from john')  # 倒序排列
        self.assertEqual(json_response['items'][1]['body'], 'first comment from john')

    def test_get_comment(self):
        # 测试返回单个评论
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        p = Post(title='first post from david', body='post from david', author=u2,
                 timestamp=datetime.utcnow() + timedelta(seconds=1))

        c1 = Comment(body='first comment from john')
        c1.author = u1
        c1.post = p
        c2 = Comment(body='second comment from john')
        c2.author = u1
        c2.post = p

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(p)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        headers = self.get_token_auth_headers('david', '123')
        response = self.client.get('/api/comments/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        # 判断返回的评论集合
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['body'], 'first comment from john')
        self.assertEqual(json_response['author']['username'], 'john')

    def test_update_comment(self):
        # 测试修改单个评论
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        p = Post(title='first post from david', body='post from david', author=u2,
                 timestamp=datetime.utcnow() + timedelta(seconds=1))

        c1 = Comment(body='first comment from john')
        c1.author = u1
        c1.post = p
        c2 = Comment(body='first comment from susan')
        c2.author = u3
        c2.post = p

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(p)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        # 1. 不允许修改别人的评论
        data = json.dumps({'body': 'Hello, I am john'})
        response = self.client.put('/api/comments/2', headers=headers, data=data)
        self.assertEqual(response.status_code, 403)
        # 2. 没提供任何参数时
        data = json.dumps({})
        response = self.client.put('/api/comments/1', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You must post JSON data.')
        # 3. 缺少 body 时
        # data = json.dumps({'disabled': True})
        # response = self.client.put('/api/comments/1', headers=headers, data=data)
        # self.assertEqual(response.status_code, 400)
        # json_response = json.loads(response.get_data(as_text=True))
        # self.assertEqual(json_response['message'], 'Body is required.')
        # 4. 正常提供参数，成功修改
        data = json.dumps({'body': 'Hello, I am john'})
        response = self.client.put('/api/comments/1', headers=headers, data=data)
        self.assertEqual(response.status_code, 200)
        # 判断返回的信息中时候已更改了body字段
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['body'], 'Hello, I am john')

    def test_delete_comment(self):
        # 测试删除单个评论
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        p = Post(title='first post from david', body='post from david', author=u2,
                 timestamp=datetime.utcnow() + timedelta(seconds=1))

        c1 = Comment(body='first comment from john')
        c1.author = u1
        c1.post = p
        c2 = Comment(body='first comment from susan')
        c2.author = u3
        c2.post = p

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(p)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        # 1. 不允许删除别人的评论
        response = self.client.delete('/api/comments/2', headers=headers)
        self.assertEqual(response.status_code, 403)
        # 2. 删除自己的评论是成功的
        response = self.client.delete('/api/comments/1', headers=headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(as_text=True), '')
