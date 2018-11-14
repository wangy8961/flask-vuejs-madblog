from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from tests import TestConfig


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john')
        u.set_password('pass1234')
        self.assertTrue(u.check_password('pass1234'))
        self.assertFalse(u.check_password('123456'))

    def test_avatar(self):
        u = User(username='john', email='john@163.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         '5ad2197b80f2010461c700d80fd35e9d'
                                         '?d=identicon&s=128'))

    def test_follow_and_unfollow(self):
        # 测试关注、取消关注其它用户
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followeds.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followeds.count(), 1)
        self.assertEqual(u1.followeds.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followeds.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(title='post from john', body='post from john', author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(title='post from susan', body='post from susan', author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(title='post from mary', body='post from mary', author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(title='post from david', body='post from david', author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts.all()
        f2 = u2.followed_posts.all()
        f3 = u3.followed_posts.all()
        f4 = u4.followed_posts.all()
        self.assertEqual(f1, [p2, p4])
        self.assertEqual(f2, [p3])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [])
