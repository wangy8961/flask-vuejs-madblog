# [Flask Vue.js全栈开发的 `最新完整代码` 及使用方式](http://www.madmalls.com/blog/post/latest-code/)

[![Python](https://img.shields.io/badge/python-v3.4%2B-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-v2.5.2-orange.svg)](https://cn.vuejs.org/index.html)
[![vue-router](https://img.shields.io/badge/vue--router-v3.0.1-lightgrey.svg)](https://router.vuejs.org/zh/)
[![axios](https://img.shields.io/badge/axios-v0.18.0-yellow.svg)](https://github.com/axios/axios)
[![Bootstrap4](https://img.shields.io/badge/Bootstrap-v4.1.3-blue.svg)](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[![webpack](https://img.shields.io/badge/webpack-v3.6.0-brightgreen.svg)](https://webpack.js.org/)


## 测试地址: [www.madblog.ga](http://www.madblog.ga)

> 本系列的最新代码及使用方式将持续更新到： http://www.madmalls.com/blog/post/latest-code/


![pic 01](http://www.madmalls.com/api/medias/uploaded/madblogxuan-chuan-tu-01-60c24e78.png)
![pic 02](http://www.madmalls.com/api/medias/uploaded/github-madblog-xuan-chuan-tu-02-c023d0d7.png)
![pic 03](http://www.madmalls.com/api/medias/uploaded/madblogxuan-chuan-tu-02-cf3edae1.png)


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
- [Flask Vue.js全栈开发｜第10章：用户通知](http://www.madmalls.com/blog/post/user-notifications/)
- [Flask Vue.js全栈开发｜第11章：私信](http://www.madmalls.com/blog/post/send-private-messages/)
- [Flask Vue.js全栈开发｜第12章：黑名单](http://www.madmalls.com/blog/post/blacklist/)
- [Flask Vue.js全栈开发｜第13章：喜欢文章](http://www.madmalls.com/blog/post/like-posts/)
- [Flask Vue.js全栈开发｜第14章：邮件支持](http://www.madmalls.com/blog/post/email-support/)
- [Flask Vue.js全栈开发｜第15章：权限管理](http://www.madmalls.com/blog/post/rbac/)
- [Flask Vue.js全栈开发｜第16章：管理后台](http://www.madmalls.com/blog/post/admin/)
- [Flask Vue.js全栈开发｜第17章：RQ实现后台任务](http://www.madmalls.com/blog/post/redis-queue/)
- [Flask Vue.js全栈开发｜第18章：Elasticsearch全文搜索](http://www.madmalls.com/blog/post/elasticsearch-for-madblog/)
- [Flask Vue.js全栈开发｜第19章：国际化](http://www.madmalls.com/blog/post/i18n/)
- [Flask Vue.js全栈开发｜第20章：Linux云主机部署](http://www.madmalls.com/blog/post/deployment-on-linux/)
- [Flask Vue.js全栈开发｜第21章：Docker容器部署](http://www.madmalls.com/blog/post/deployment-on-docker-containers/)


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
