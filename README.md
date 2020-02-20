# [Flask Vue.js全栈开发](https://madmalls.com/blog/category/flask/)

[![Python](https://img.shields.io/badge/python-v3.4%2B-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-v2.5.2-orange.svg)](https://cn.vuejs.org/index.html)
[![vue-router](https://img.shields.io/badge/vue--router-v3.0.1-lightgrey.svg)](https://router.vuejs.org/zh/)
[![axios](https://img.shields.io/badge/axios-v0.18.0-yellow.svg)](https://github.com/axios/axios)
[![Bootstrap4](https://img.shields.io/badge/Bootstrap-v4.1.3-blue.svg)](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[![webpack](https://img.shields.io/badge/webpack-v3.6.0-brightgreen.svg)](https://webpack.js.org/)


# <span style="color: red">测试地址: http://120.77.33.143 </span>

**RESTful API：** http://120.77.33.143:5000/api/posts （用 `Firefox` 查看返回的 `JSON` 数据更佳），或者将仓库内的 `flask-vuejs-madblog.postman_collection.json` 导入你的 `Postman` 工具

> 本系列的最新代码及使用方式将持续更新到： https://madmalls.com/blog/post/latest-code/


![pic 01](https://madmalls.com/api/medias/uploaded/madblogxuan-chuan-tu-01-60c24e78.png)
![pic 02](https://madmalls.com/api/medias/uploaded/github-madblog-xuan-chuan-tu-02-c023d0d7.png)
![pic 03](https://madmalls.com/api/medias/uploaded/madblogxuan-chuan-tu-02-cf3edae1.png)


# 1. Flask Vue.js全栈开发教程系列

- [Flask Vue.js全栈开发｜第1章：创建第一个Flask RESTful API](https://madmalls.com/blog/post/first-flask-test-restful-api/)
- [Flask Vue.js全栈开发｜第2章：Vue.js通过axios访问Flask RESTful API](https://madmalls.com/blog/post/axios-use-flask-api/)
- [Flask Vue.js全栈开发｜第3章：Flask设计User用户相关API](https://madmalls.com/blog/post/provide-users-api/)
- [Flask Vue.js全栈开发｜第4章：Vue.js调用API实现用户注册/登录/退出](https://madmalls.com/blog/post/user-register-and-login/)
- [Flask Vue.js全栈开发｜第5章：个人主页与用户头像](https://madmalls.com/blog/post/profile-page-and-avatars/)
- [Flask Vue.js全栈开发｜第6章：博客文章CURD与Markdown](https://madmalls.com/blog/post/post-curd-and-markdown/)
- [Flask Vue.js全栈开发｜第7章：粉丝关注大神](https://madmalls.com/blog/post/followers-and-followeds/)
- [Flask Vue.js全栈开发｜第8章：单元测试](https://madmalls.com/blog/post/flask-unit-test/)
- [Flask Vue.js全栈开发｜第9章：用户评论](https://madmalls.com/blog/post/user-comments/)
- [Flask Vue.js全栈开发｜第10章：用户通知](https://madmalls.com/blog/post/user-notifications/)
- [Flask Vue.js全栈开发｜第11章：私信](https://madmalls.com/blog/post/send-private-messages/)
- [Flask Vue.js全栈开发｜第12章：黑名单](https://madmalls.com/blog/post/blacklist/)
- [Flask Vue.js全栈开发｜第13章：喜欢文章](https://madmalls.com/blog/post/like-posts/)
- [Flask Vue.js全栈开发｜第14章：邮件支持](https://madmalls.com/blog/post/email-support/)
- [Flask Vue.js全栈开发｜第15章：权限管理](https://madmalls.com/blog/post/rbac/)
- [Flask Vue.js全栈开发｜第16章：管理后台](https://madmalls.com/blog/post/admin/)
- [Flask Vue.js全栈开发｜第17章：RQ实现后台任务](https://madmalls.com/blog/post/redis-queue/)
- [Flask Vue.js全栈开发｜第18章：Elasticsearch全文搜索](https://madmalls.com/blog/post/elasticsearch-for-madblog/)
- [Flask Vue.js全栈开发｜第19章：国际化](https://madmalls.com/blog/post/i18n/)
- [Flask Vue.js全栈开发｜第20章：Linux云主机部署](https://madmalls.com/blog/post/deployment-on-linux/)
- [Flask Vue.js全栈开发｜第21章：Docker容器部署](https://madmalls.com/blog/post/deployment-on-docker-containers/)
- [Flask Vue.js全栈开发｜第22章：(番外篇) 用 Flask-RESTful 插件实现 API](https://madmalls.com/blog/post/designing-a-restful-api-using-flask-restful/)



# 2. 如何使用

# <span style="color: red">Github 仓库中只包含前半部分代码，获取最新完整代码请前往: [Flask Vue.js全栈开发](https://madmalls.com/blog/category/vuejs/) </span>

## 2.1 git clone

<span style="color: red">Github 仓库中只包含前半部分代码，想获取最新完整代码请前往: https://madmalls.com/blog/post/latest-code/ </span>

```bash
$ git clone https://github.com/wangy8961/flask-vuejs-madblog.git
```

## 2.2 Backend


### （1）提供 `.env` 文件

复制 `backend/.env.example`，并重命名为 `backend/.env`，然后修改里面的邮箱配置，具体参考: https://madmalls.com/blog/post/email-support/#12-qq

### （2）修改 `config.py` 文件

修改 `back-end/config.py` 中的配置，比如 `SECRET_KEY` 和 `SQLALCHEMY_DATABASE_URI`

> `ADMINS` 这个配置一定要修改！

```
ADMINS = ['xxx@qq.com']  # 管理员的邮箱地址
```

因为在这个列表中的邮箱地址，在注册时，会自动赋予管理员的角色

### （3）启动后端 Flask 应用

Open a new terminal:

```bash
$ cd back-end
$ python -m venv venv
$ source venv/bin/activate  # 如果是Windows环境，则执行 venv\Scripts\activate
(venv)$ pip install -r requirements.txt

# Flask-Migrate create database
(venv)$ flask db upgrade

# Pre deploy, eg. insert roles
(venv)$ flask deploy

# create back-end/.env file, like this
FLASK_APP=madblog.py
FLASK_DEBUG=1

(venv)$ flask run
```

浏览器访问: `http://localhost:5000/api/ping`，比如返回 `"Pong!"` 则说明正常


## 2.3 Frontend

### （1）安装 Node.js

请前往 [官方网站](https://nodejs.org/zh-cn/) 下载并安装 `LTS` 版本

安装好后，由于 `npm` 命令使用的国外镜像，在国内下载依赖包时很慢，这里换成 [淘宝 NPM 镜像](https://npm.taobao.org/)

打开 `cmd`：

```bash
$ npm install -g cnpm --registry=https://registry.npm.taobao.org
```

之后，用 `cnpm` 来代替 `npm` 命令

### （2）运行前端应用

Open a new terminal:

```bash
$ cd front-end
$ cnpm install
$ npm run dev
```

浏览器访问: `http://localhost:8080`


## 2.4 注册管理员账号

浏览器访问: `http://localhost:8080/#/register` 注册你的管理员账号 (注册时填写的 Email 在配置文件 `config.py` 的 `ADMINS` 中即可！)

然后登录你的这个邮箱，去激活账号。Have fun
