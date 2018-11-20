# [Flask Vue.js全栈开发](http://www.madmalls.com/blog/category/vuejs/)

[![Python](https://img.shields.io/badge/python-v3.4%2B-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-v2.5.2-orange.svg)](https://cn.vuejs.org/index.html)
[![vue-router](https://img.shields.io/badge/vue--router-v3.0.1-lightgrey.svg)](https://router.vuejs.org/zh/)
[![axios](https://img.shields.io/badge/axios-v0.18.0-yellow.svg)](https://github.com/axios/axios)
[![Bootstrap4](https://img.shields.io/badge/Bootstrap-v4.1.3-blue.svg)](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[![webpack](https://img.shields.io/badge/webpack-v3.6.0-brightgreen.svg)](https://webpack.js.org/)


![pic 01](http://www.madmalls.com/admin/medias/uploaded/github-madblog-show-pic-01-2f8ce5a7.png)
![pic 02](http://www.madmalls.com/admin/medias/uploaded/github-madblog-show-pic-02-41de56aa.png)
![pic 03](http://www.madmalls.com/admin/medias/uploaded/1-you-ke-cha-kan-ping-lun-lie-biao-7bd80108.png)

# 1. Flask Vue.js全栈开发教程系列

- [Flask Vue.js全栈开发｜第1章：创建第一个Flask RESTful API](http://www.madmalls.com/blog/post/first-flask-test-restful-api/)
- [Flask Vue.js全栈开发｜第2章：Vue.js通过axios访问Flask RESTful API](http://www.madmalls.com/blog/post/axios-use-flask-api/)
- [Flask Vue.js全栈开发｜第3章：Flask设计User用户相关API](http://www.madmalls.com/blog/post/provide-users-api/)
- [Flask Vue.js全栈开发｜第4章：Vue.js调用API实现用户注册/登录/退出](http://www.madmalls.com/blog/post/user-register-and-login/)
- [Flask Vue.js全栈开发｜第5章：个人主页与用户头像](http://www.madmalls.com/blog/post/profile-page-and-avatars/)
- [Flask Vue.js全栈开发｜第6章：博客文章CURD与Markdown](http://www.madmalls.com/blog/post/post-curd-and-markdown/)
- [Flask Vue.js全栈开发｜第7章：粉丝关注大神](http://www.madmalls.com/blog/post/followers-and-followeds/)
- [Flask Vue.js全栈开发｜第8章：单元测试](http://www.madmalls.com/blog/post/flask-unit-test/)
- [Flask Vue.js全栈开发｜第9章：用户评论](http://www.madmalls.com/blog/post/user-comments/)
- 站内消息 (敬请期待)
- 权限管理 (敬请期待)
- 邮件的用处 (敬请期待)
- 修改用户设置 (敬请期待)
- 管理员视角 (敬请期待)
- Celery任务队列与定时任务 (敬请期待)
- Elasticsearch全站搜索 (敬请期待)
- 国际化 (敬请期待)
- 性能优化 (敬请期待)
- Linux云主机部署 (敬请期待)
- Docker容器部署 (敬请期待)

# 2. 如何使用

## 2.1 git clone

```bash
$ git clone https://github.com/wangy8961/flask-vuejs-madblog.git
```

## 2.2 Backend

Open a new terminal:

```bash
$ cd back-end
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt

# Flask-Migrate create database
(venv)$ flask db upgrade

# create back-end/.env file, like this
FLASK_APP=madblog.py
FLASK_DEBUG=1

(venv)$ flask run
```

浏览器访问: `http://localhost:5000/api/ping`

## 2.3 Frontend

Open a new terminal:

```bash
$ cd front-end
$ npm install
$ npm run dev
```

浏览器访问: `http://localhost:8080`
