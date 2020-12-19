# django-vue前后端分离的博客项目

## 项目详情（第一期）

使用django vue来实现一个前后端分离的博客项目

### 模块

* 用户模块
  * 登录
  * 注册
  * 个人中心
* 文章模块
  * 文章列表
  * 文章详情
  * 点赞
  * 收藏
  * 评论
* 消息通知模块
* 评论模块
* 相册模块(七牛云)
  * 相册列表
  * 相册详情（照片列表）
  * 照片详情
* 视频模块（cc视频）
* ...

### 界面（掘金）

## 技术栈

* 准备工作
  * api设计（接口文档）
    1. 支付宝错误code号
    2. restful规范
  * 数据库设计（er图） 注重content-type
* 后端 backends
  * django
  * django rest framework
  * django cors headers
  * (前期sqlite)mysql
* 前端 frontends
  * vue
  * vue-element
  * fontawesome
  * bootstrap
  * axios
* 部署
  * linux服务器
  * nginx web服务器
  * 改用mysql数据库
  * （docker）

## 步骤

1. 后端
   1. 安装django
   2. 创建django项目my_blog
   3. 添加博客的Model，添加原始数据
   4. 使用restframework来添加serializer、viewset、urls
   5. 设置跨域cors headers
2. 前端
   1. 安装node vue
   2. vue-cli脚手架创建项目
   3. 修改index.html主页 添加bootstrap以及fontawesome依赖
   4. 修改App.vue和核心组件
   5. 添加axios
   6. 添加请求后端代码
