# django-vue前后端分离的博客项目

### 1.描述

此项目为一个**前后台分离**的**个人博客项目**

### 2.模块

* 用户模块
  * 登录、注册、忘记密码
  * 个人中心（发布的文章、点赞的文章、收藏夹等）
  * 编辑个人资料（头像、性别、职位、公司、个人介绍等）
  * 账号设置（邮箱绑定、密码重置、账号注销）
* 文章模块
  * 文章栏目分类显示
  * 文章标签云
  * 文章点赞、评论、收藏
  * 文章编写（mavoneditor，标题图上传、新建标签、栏目选择等）
  * 文章搜索功能
  * 最热文章
* 评论模块
  * 支持表情
  * 支持点赞
  * 最多两级评论
* 情侣纪念模块
  * 头像设置
  * 在一起天数
* 博主后台模块
  * 用户管理
  * 标签管理
  * 栏目管理
  * 情侣管理

### 3.界面（仿掘金）

### 4.技术栈

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
  * docker

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

