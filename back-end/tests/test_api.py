from base64 import b64encode
from datetime import datetime, timedelta
import json
import re
import unittest
from app import create_app, db
from app.models import User, Post
from tests import TestConfig


class APITestCase(unittest.TestCase):
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

    ###
    # 404等错误处理
    ###
    def test_404(self):
        # 测试请求不存在的API时
        response = self.client.get('/api/wrong/url')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'Not Found')

    ###
    # 用户认证相关测试
    ###
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

    def test_get_token(self):
        # 测试用户登录，即获取JWT，需要输入正确的用户名和密码，通过Basic Auth之后发放JWT令牌
        # 首先创建一个测试用户
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()

        # 输入错误的用户密码
        headers = self.get_basic_auth_headers('john', '456')
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 401)

        # 输入正确的用户密码
        headers = self.get_basic_auth_headers('john', '123')
        response = self.client.post('/api/tokens', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        self.assertTrue(re.match(r'(.+)\.(.+)\.(.+)', json_response.get('token')))

    def test_not_attach_jwt(self):
        # 测试请求头Authorization中没有附带JWT时，会返回401错误
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)

    def test_attach_jwt(self):
        # 测试请求头Authorization中有附带JWT时，允许访问那些需要认证的API
        # 首先创建一个测试用户
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        # 附带JWT到请求头中
        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        # 有些API不需要认证，比如 /api/posts/
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    ###
    # 用户API
    ###
    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_create_user(self):
        # 测试用户注册
        headers = self.get_api_headers()
        # 1. 用户不传入任何必须的参数时
        data = json.dumps({})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 2. 缺少 username 时
        data = json.dumps({'email': 'john@163.com', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 3. 缺少 email 时
        data = json.dumps({'username': 'john', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 4. 缺少 password 时
        data = json.dumps({'username': 'john', 'email': 'john@163.com'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 5. username 或者 email 已存在时
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        data = json.dumps({'username': 'john', 'email': 'john@163.com', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message']['username'], 'Please use a different username.')
        self.assertEqual(json_response['message']['email'], 'Please use a different email address.')
        # 6. 正确提供参数时
        data = json.dumps({'username': 'david', 'email': 'david@163.com', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

    def test_get_users(self):
        # 测试获取用户列表
        # 首先创建几个测试用户
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        # 附带JWT到请求头中
        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/', headers=headers)
        self.assertEqual(response.status_code, 200)
        # 判断返回的用户集合中包含刚创建的这个用户
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 3)
        self.assertIsNotNone(json_response.get('items'))
        self.assertEqual(json_response['items'][0]['username'], 'john')
        self.assertEqual(json_response['items'][1]['username'], 'david')
        self.assertEqual(json_response['items'][2]['username'], 'susan')

    def test_get_user(self):
        # 测试获取一个用户
        # 首先创建一个测试用户
        headers = self.get_api_headers()
        data = json.dumps({'username': 'john', 'email': 'john@163.com', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # 附带JWT到请求头中
        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        # 判断返回的用户是否就是刚创建的这个用户
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost' + json_response['_links']['self'], url)
        self.assertEqual(json_response['username'], 'john')
        # 请求的自己这个用户，所以响应中会包含 email 字段，不包含 is_following 字段
        self.assertIsNotNone(json_response['email'])
        self.assertIsNone(json_response.get('is_following'))

    def test_update_user(self):
        # 测试修改用户
        # 首先创建一个测试用户
        headers = self.get_api_headers()
        data = json.dumps({'username': 'john', 'email': 'john@163.com', 'password': '123'})
        response = self.client.post('/api/users/', headers=headers, data=data)
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # 附带JWT到请求头中
        headers = self.get_token_auth_headers('john', '123')
        # 1. 用户不传入任何必须的参数时（可以传入空字符串，但不能是空的 JSON）
        data = json.dumps({})
        response = self.client.put(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        # 2. 如果传入了 username 或者 email，但是不是合法的数据时
        data = json.dumps({'username': '', 'email': '1@1'})
        response = self.client.put(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message']['username'], 'Please provide a valid username.')
        self.assertEqual(json_response['message']['email'], 'Please provide a valid email address.')
        # 3. 如果传入了 username 或者 email，但已存在时
        u = User(username='david', email='david@163.com')
        u.set_password('123')
        db.session.add(u)
        db.session.commit()
        data = json.dumps({'username': 'david', 'email': 'david@163.com'})
        response = self.client.put(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message']['username'], 'Please use a different username.')
        self.assertEqual(json_response['message']['email'], 'Please use a different email address.')
        # 4. 正确传入要修改的字段值时
        data = json.dumps({'about_me': 'I love DevOps'})
        response = self.client.put(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 200)
        # 判断返回的信息中时候已更改了about_me字段
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost' + json_response['_links']['self'], url)
        self.assertEqual(json_response['about_me'], 'I love DevOps')

    def test_delete_user(self):
        # 测试删除用户
        # 首先创建三个测试用户
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        # 删除自己的账户是成功的
        headers = self.get_token_auth_headers('susan', '123')
        response = self.client.delete('/api/users/3', headers=headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(as_text=True), '')
        # 删除别人的账户是不允许的
        headers = self.get_token_auth_headers('john', '123')
        response = self.client.delete('/api/users/2', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_follow(self):
        # 测试关注其它用户
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        # 1. 不允许关注自己
        response = self.client.get('/api/follow/1', headers=headers)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You cannot follow yourself.')
        # 2. 成功关注还没有关注过的人
        response = self.client.get('/api/follow/2', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You are now following 2.')
        # 3. 已经关注过的人，你不能重复关注
        response = self.client.get('/api/follow/2', headers=headers)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You have already followed that user.')

    def test_unfollow(self):
        # 测试取消关注其它用户
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        # 1. 不允许取消关注自己
        response = self.client.get('/api/unfollow/1', headers=headers)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You cannot unfollow yourself.')
        # 2. 不允许取消关注还没有关注过的人
        response = self.client.get('/api/unfollow/2', headers=headers)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You are not following this user.')
        # 3. 成功取消关注
        # 先关注
        response = self.client.get('/api/follow/2', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You are now following 2.')
        # 开始取消关注
        response = self.client.get('/api/unfollow/2', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'You are not following 2 anymore.')

    def test_get_followeds(self):
        # 测试获取你已关注的人的列表
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)

        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/1/followeds/', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['items'][0]['username'], 'david')
        self.assertEqual(json_response['items'][1]['username'], 'susan')

    def test_get_followers(self):
        # 测试获取你的粉丝列表
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        u2.follow(u1)
        u3.follow(u1)

        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/1/followers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['items'][0]['username'], 'david')
        self.assertEqual(json_response['items'][1]['username'], 'susan')

    def test_get_user_posts(self):
        # 测试返回用户自己的博客列表
        # 创建用户
        u = User(username='john', email='john@163.com')
        u.set_password('123')
        db.session.add(u)
        # 创建几篇博客
        now = datetime.utcnow()
        p1 = Post(title='first post from john', body='post from john', author=u,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(title='second post from john', body='post from john', author=u,
                  timestamp=now + timedelta(seconds=4))
        db.session.add_all([p1, p2])
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/1/posts/', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 2)
        self.assertIsNotNone(json_response.get('items'))
        self.assertEqual(json_response['items'][0]['title'], 'second post from john')  # 倒序排列
        self.assertEqual(json_response['items'][1]['title'], 'first post from john')

    def test_get_user_followed_posts(self):
        # 测试返回你关注的人的博客列表
        u1 = User(username='john', email='john@163.com')
        u1.set_password('123')
        u2 = User(username='david', email='david@163.com')
        u2.set_password('123')
        u3 = User(username='susan', email='susan@163.com')
        u3.set_password('123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)

        now = datetime.utcnow()
        p1 = Post(title='first post from david', body='post from david', author=u2,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(title='second post from david', body='post from david', author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(title='first post from susan', body='post from susan', author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(title='second post from susan', body='post from susan', author=u3,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        headers = self.get_token_auth_headers('john', '123')
        response = self.client.get('/api/users/1/followeds-posts/', headers=headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 4)
        self.assertIsNotNone(json_response.get('items'))
        self.assertEqual(json_response['items'][0]['title'], 'second post from david')  # 倒序排列
        self.assertEqual(json_response['items'][1]['title'], 'first post from susan')
        self.assertEqual(json_response['items'][2]['title'], 'second post from susan')
        self.assertEqual(json_response['items'][3]['title'], 'first post from david')
