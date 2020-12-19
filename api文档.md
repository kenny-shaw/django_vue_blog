



# API文档

## api code 以及状态码设计

| 状态码 | code码 | 类型 | 说明                                    |
| ------ | ------ | ---- | --------------------------------------- |
| 200    | 1000   | 成功 | 成功请求（成功获取或者获取空数组）      |
| 200    | 1001   | 成功 | 没有数据                                |
| 200    | 1002   | 成功 | 分页无数据                              |
|        |        |      |                                         |
| 500    | 2000   | 失败 | 服务不可用，一般用于try catch异常后捕获 |
|        |        |      |                                         |
| 401    | 2001   | 失败 | 未登录或登录过期                        |
| 401    | 2002   | 失败 | 登录失败                                |
|        |        |      |                                         |
| 400    | 4001   | 失败 | 参数验证错误                            |
| 400    | 4002   | 失败 | 未传递相关参数                          |
|        |        |      |                                         |
| 404    | 4004   | 失败 | 给文章点赞，但是文章id不存在等情况      |
|        |        |      |                                         |
| 403    | 4003   | 失败 | 拒绝重复执行（点赞等）                  |
| 403    | 4006   | 失败 | 权限不足                                |
|        |        |      |                                         |
| 405    | 4005   | 失败 | （get等）方法不允许                     |



## 一、用户模块api

### 1.用户登录

**简要描述：**用于用户登录，返回token

**请求URL：**

` http://localhost:8000/api/v1/login`

**请求方式：**POST

**参数：**

| 参数名   | 必选 | 类型   | 参数说明 |
| -------- | ---- | ------ | -------- |
| username | 是   | string | 用户名   |
| password | 是   | string | 用户密码 |

**返回示例：**

```json
登录成功：
{
  "code": 1000,
  "token": "b4343a63-fa26-4563-8764-0199bbb8b158"
}
登录失败：
{
    "code": 4004,
    "error": "此用户名不存在"
}
或者
{
    "code": 2002,
    "error": "您的密码错误，请重新输入！"
}
```



### 2.用户注册

**简要描述：**用于用户注册

**请求URL：**

` http://localhost:8000/api/v1/register`

**请求方式：**POST

**参数：**

| 参数名    | 必选 | 类型    | 参数说明                |
| --------- | ---- | ------- | ----------------------- |
| username  | 是   | string  | 用户名                  |
| password  | 是   | string  | 用户密码                |
| password2 | 是   | string  | 确认密码                |
| email     | 否   | string  | 邮箱                    |
| gender    | 否   | integer | 性别（1保密，2男，3女） |
| avatar    | 否   | string  | 头像                    |
| brief     | 否   | string  | 简介                    |

**返回示例：**

```json
注册成功：
{
    "code": 1000,
    "data": {
        "username": "yeow",
        "password": "1234",
        "password2": "1234",
        "brief": "这个人很懒"
    }
}
验证数据失败：
{
    "code": 4001,
    "error": {
        "username": [
            "最短3个字符"
        ]
    }
}
这个只是示例，还有很多注册失败的情况，如两次密码不一致等
注册失败：
{
    "code": 2000,
    "error":"'用户注册失败"
}
```

### 3.用户信息展示及修改

- **用户信息展示**

**简要描述：**用于用户信息展示
**请求URL：**

` http://localhost:8000/api/v1/userinfo/?token=token`

**请求方式：**GET

**参数：**

| 参数名 | 必选 | 类型   | 参数说明  |
| ------ | ---- | ------ | --------- |
| token  | 是   | string | 用户token |

**返回示例：**

```json
返回成功：
{
    "code": 1000,
    "data": {
        "username": "kennyupdate",
        "email": null,
        "gender": "女",
        "avatar": "default",
        "brief": "你才懒呢"
    }
}
返回数据失败：

{
    "code": 2000,
    "error": "获取个人信息失败！"
}
{
    "code": "2001",
    "error": "用户认证失败"
}
```

- **用户信息修改**

**简要描述：**用于用户修改

**请求URL：**

` http://localhost:8000/api/v1/userinfo/?token=token`

**请求方式：**PUT

**参数：**

| 参数名   | 必选 | 类型    | 参数说明                |
| -------- | ---- | ------- | ----------------------- |
| token    | 是   | string  | 用户token               |
| username | 否   | string  | 用户名                  |
| email    | 否   | string  | 邮箱                    |
| gender   | 否   | integer | 性别（1保密，2男，3女） |
| avatar   | 否   | string  | 头像                    |
| brief    | 否   | string  | 简介                    |

**返回示例：**

```json
修改成功：
{
    "code": 1000,
    "data": {
        "username": "kennyupdate",
        "email": null,
        "gender": "女",
        "avatar": "default",
        "brief": "你才懒呢嘤嘤嘤"
    }
}
失败：
{
    "code": 2000,
    "error": "获取个人信息失败！"
}
{
    "code": "2001",
    "error": "用户认证失败"
}
```

- **用户粗略信息查看**

**简要描述：**用于用户个人中心粗略信息的查看，并且增加了用户获得的总点赞量、总阅读量,无需登录

**请求URL：**

` http://localhost:8000/api/v1/usergeneralinfo/pk`

**请求方式：**GET

**参数：**

| 参数名 | 必选 | 类型    | 参数说明 |
| ------ | ---- | ------- | -------- |
| pk     | 是   | integer | 用户id   |

**返回示例：**

```json
修改成功：
{
    "code": 1000,
    "data": {
        "username": "kennyupdate",
        "gender": "女",
        "avatar": "default",
        "brief": "你才懒呢嘤嘤嘤",
        "obtained_total_likes": 7,
        "obtained_total_views": 31,
        "date_joined": "2020-07-11T05:14:30.951502",
        "job": "student",
        "company": "wshdx"
    }
}
修改失败：
{
    "code": 4004,
    "error": "没有此用户！"
}
或者
{
    "code": 2000,
    "error": "获取个人信息失败！"
    }
}
```

### 

### 3.用户密码修改

**简要描述：**用于用户密码修改

**请求URL：**

` http://localhost:8000/api/v1/setpassword/?token=token`

**请求方式：**POST

**参数：**

| 参数名      | 必选 | 类型   | 参数说明 |
| ----------- | ---- | ------ | -------- |
| oldpassword | 是   | string | 旧密码   |
| newpassword | 是   | string | 新密码   |

**返回示例：**

```json
修改成功：
{
    "code": 1000,
    "data": {
        "id": 16,
        "username": "kennytest11",
        "email": "717556676ss@qq.com",
        "password": "pbkdf2_sha256$150000$pJmwUM2KjLpn$8gz2F2rRHcD2Ul6q273RF3wTytjseSlblnw8FAWbN4M=",
        "gender": 1,
        "avatar": "default",
        "role": 1,
        "brief": "密码加密测试",
        "date_joined": "2020-07-16T06:50:38.859483Z"
    }
}
修改失败：
{
    "code": 2001,
    "error": "您尚未登录"
}
{
    "code": 2002,
    "error": "原密码输入错误"
}
或者（还包括必须输入，以及最大长度的错误）
{
    "code": 4001,
    "error": {
        "non_field_errors": [
            "新旧密码不能一致，请重新输入！"
        ]
    }
}
或者
{
    "code": 2000,
    "error": "密码修改失败！"
}
```

### 4.用户密码重置

* 根据邮箱发送重置密码url（附带token）视图

**简要描述：**用于根据邮箱发送重置密码url

**请求URL：**

` http://localhost:8000/api/v1/resetpasswordemail`

**请求方式：**POST

**参数：**

| 参数名 | 必选 | 类型   | 参数说明 |
| ------ | ---- | ------ | -------- |
| email  | 是   | string | 注册邮箱 |

**返回示例：**

```json
发送成功：
{
    "code": 1000,
    "data": {
        "token": "fce266a6cc4003dd38fcfcb609aff716"
    }
}
发送后的邮件为一个带token的url，挂载时绑定到data中
失败：
{
    "code": 4004,
    "error": "此用户尚未注册，请前往注册"
}
或者（还包括必须输入，以及最大长度的错误）
{
    "code": 2000,
    "error": "发送邮件失败"
}
```

* 点击接收到的email来重置密码视图

**简要描述：**根据token获取用户，无需输入老密码即可修改

**请求URL：**

` http://localhost:8000/api/v1/resetpassword`

**请求方式：**POST

**参数：**

| 参数名       | 必选 | 类型   | 参数说明           |
| ------------ | ---- | ------ | ------------------ |
| newpassword  | 是   | string | 新密码，5-64位     |
| newpassword2 | 是   | string | 确认新密码，5-64位 |

**返回示例：**

```json
重置成功：
{
    "code": 1000,
    "data": {
        "id": 16,
        "username": "kennytest11",
        "email": "717556676ss@qq.com",
        "password": "pbkdf2_sha256$150000$z1nYyQnn7WZE$wWfLZm5z7BPHI6Zudp90FosqZ3ZX7NKBr45MxUv4E10=",
        "gender": 1,
        "avatar": "default",
        "role": 1,
        "brief": "密码加密测试",
        "date_joined": "2020-07-16T06:50:38.859483Z"
    }
}
失败：
{
    "code": 4001,
    "error": {
        "non_field_errors": [
            "两次输入密码不一致，请重新输入！"
        ]
    }
}
或者（还包括必须输入，以及最大长度的错误）
{
    "code": 2000,
    "error": "密码重置失败！"
}
```

### 5.设置token过期时间

**简要描述：**根据当前提交请求的时间与token数据库的创建更新时间相比，大于三天则失效，需要重新登录，如果请求的话，token数据库时间对对应更新

**示例URL：**

` http://localhost:8000/api/v1/userinfo/16?token=9f71a132156068e7c029478a28891af6`

**请求方式：**GET/POST

**参数：**

| 参数名   | 必选 | 类型 | 参数说明 |
| -------- | ---- | ---- | -------- |
| 相应参数 | 是   |      |          |

**返回示例：**

```json
发送成功示例：
 {
    "code": 1000,
    "data": {
        "username": "kennytest11",
        "email": "717556676ss@qq.com",
        "gender": "保密",
        "avatar": "default",
        "brief": "密码加密测试"
    }
}
认证失败（token错误）：
{
    "code": "2001",
    "error": "用户认证失败"
}
token过期
{
    "code": "2001",
    "error": "用户认证已过期，请重新登录"
}
或者
```

### 6.博主管理用户api

**功能描述：**博主查看所有用户信息，查看某个用户信息，修改某个用户信息，删除某个用户信息，需要登录以及权限等级为博主

* 查看所有用户信息

**功能描述：**博主查看所有用户信息

**示例URL：**

` http://localhost:8000/api/v1/accountadmin/?token=9f71a132156068e7c029478a28891af6&size=10,page=2`

**请求方式：**GET(list方法名)

**参数：**

| 参数名 | 必选 | 类型    | 参数说明                    |
| ------ | ---- | ------- | --------------------------- |
| token  | 是   | string  | token                       |
| size   | 否   | integer | 每页展示的数量<br />默认是5 |
| page   | 否   | integer | 当前页数<br />默认是1       |

**返回示例：**

```json
返回成功示例：
 {
    "code": 1000,
    "data": [
        {
            "id": 1,
            "username": "kennyupdate",
            "email": "717556676@qq333.com",
            "password": "123",
            "gender": 1,
            "avatar": "default",
            "role": 2,
            "brief": "你才懒呢嘤嘤嘤",
            "date_joined": "2020-07-11T05:14:30.951502"
        },
        {
            "id": 2,
            "username": "kennykmmmmkk",
            "email": "717556676@qqee.com",
            "password": "213213123",
            "gender": 1,
            "avatar": "1.png",
            "role": 1,
            "brief": "这个人很懒",
            "date_joined": "2020-07-13T12:00:35.465697"
        },
        ……]
}
没有用户：
{	
    "code": "1001",
    "error": "尚无用户注册!"
}
{	
    "code": "1002",
    "error": "暂无更多用户!"
}
异常
{
    "code": "2000",
    "error": "获取所有用户信息失败"
}
不是博主
{
    "detail": "您不是博主，不能访问哦~"
}
```

* 查看单个用户信息

**功能描述：**博主查看某个用户信息

**示例URL：**

` http://localhost:8000/api/v1/accountadmin/1?token=9f71a132156068e7c029478a28891af6`

**请求方式：**GET(retrieve方法名)

**参数：**无

**返回示例：**

```json
返回成功示例：
{
    "code": 1000,
    "data": {
        "id": 12,
        "username": "adddddaa",
        "email": "717556676@qqas.com",
        "password": "2132d13123",
        "gender": 1,
        "avatar": "1.png",
        "role": 1,
        "brief": "这个人很懒",
        "date_joined": "2020-07-13T14:23:38.678597"
    }
}
没有用户：
{	
    "code": 4004,
    "error": "此用户不存在"
}
异常
{
    "code": "2000",
    "error": "获取此用户信息失败"
}
不是博主
{
    "detail": "您不是博主，不能访问哦~"
}
```

* 查看单个用户信息

**功能描述：**博主修改某个用户信息

**示例URL：**

` http://localhost:8000/api/v1/accountadmin/12?token=9f71a132156068e7c029478a28891af6`

**请求方式：**PUT

**参数：**无

**返回示例：**

```json
返回成功示例：
{
    "code": 1000,
    "data": {
        "id": 12,
        "username": "adddddaa",
        "email": "12dd3@qq.com",
        "password": "pbkdf2_sha256$150000$jtvhZsoRnAas$up9ozAlzVIVboO+BywLfi719Z+tMTI3lVY5IuNl7U4E=",
        "gender": 2,
        "avatar": "123",
        "role": 3,
        "brief": "你才ssssdddd呢嘤ddddddff嘤嘤",
        "date_joined": "2020-07-13T14:23:38.678597"
    }
}
没有用户：
{	
    "code": 4004,
    "error": "此用户不存在"
}
异常
{
    "code": "2000",
    "error": "修改用户信息失败"
}
不是博主
{
    "detail": "您不是博主，不能访问哦~"
}
校验错误
```

* 删除某个用户

**功能描述：**博主删除某个用户

**示例URL：**

` http://localhost:8000/api/v1/accountadmin/1?token=9f71a132156068e7c029478a28891af6`

**请求方式：**DELETE

**参数：**无

**返回示例：**

```json
返回成功示例：
{
    "code": 1000,
    "data": {
        "id": 16,
        "username": "kennytest11",
        "email": "123@qq.com",
        "password": "pbkdf2_sha256$150000$z1nYyQnn7WZE$wWfLZm5z7BPHI6Zudp90FosqZ3ZX7NKBr45MxUv4E10=",
        "gender": 1,
        "avatar": "default",
        "role": 3,
        "brief": "你才懒呢嘤dddd嘤嘤",
        "date_joined": "2020-07-16T06:50:38.859483"
    }
}
没有用户：
{
    "code": 4004,
    "error": "此用户不存在！"
}
异常
{
    "code": 2000,
    "error": "删除用户失败"
}
不是博主
{
    "detail": "您不是博主，不能访问哦~"
}
```

* 增加用户

* **功能描述：**博主增加某个用户

  **示例URL：**

  ` http://localhost:8000/api/v1/accountadmin/?token=9f71a132156068e7c029478a28891af6`

  **请求方式：**POST

  **参数：**

  | 参数名   | 必选 | 类型    | 参数说明                 |
  | -------- | ---- | ------- | ------------------------ |
  | username | 是   | string  | 用户名，3-20位           |
  | password | 是   | string  | 新密码，5-20位           |
  | gender   | 否   | integer | 1保密 2男 3女            |
  | avatar   | 否   | string  | 头像max_length=256       |
  | role     | 否   | integer | 角色 1普通 2管理员 3博客 |
  | brief    | 否   | string  | max_length=256           |
  | email    | 是   | email   | max_length=64            |
  
**返回示例：**
  
```json
  返回成功示例：
  {
      "code": 1000,
      "data": {
          "username": "yyeow",
          "password": "1233211",
          "gender": 1,
          "role": 2,
          "brief": "dfa",
          "email": "yeow@qq.com"
      }
  }
  错误
  1.
  {
      "code": 4001,
      "error": {
          "username": [
              "account with this 用户名 already exists."
          ],
          "email": [
              "account with this 邮箱 already exists."
          ]
      }
  }
  2.
  {
      "code": 4001,
      "error": {
          "non_field_errors": [
              "两次输入密码不一致，请重新输入！"
          ]
      }
  }
  异常
  {
      "code": 2000,
      "error": "用户新增失败！"
  }
  不是博主
  {
      "detail": "您不是博主，不能访问哦~"
  }
  ```

### 7.绑定邮箱api

  **功能描述：**用于用户绑定邮箱，首先输入邮箱，后台会进行发送邮件，然后用户点开邮件中链接，进行绑定

  * 发送邮件

  **功能描述：**主要把用户token和email通过加密，并以query的形式拼接到邮箱中的链接中

  **示例URL：**

  ` http://localhost:8000/api/v1/emailbindsend/?token=token`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型   | 参数说明  |
| ------ | ---- | ------ | --------- |
| token  | 是   | string | 用户token |
| email  | 是   | string | 邮箱      |

  **返回示例：**

  ```json
  返回成功示例：
{
    "code": 1000,
    "data": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5ODE2NzQzNCwiZXhwIjoxNTk4MTcxMDM0fQ.eyJlbWFpbCI6IjcxNzU1NjY3NkBxcS5jb20iLCJ0b2tlbiI6ImQ1YzBiMWY1ZTYyZjhmMmY0Yjc2NjRmMmNlOGMxMTYzIn0.LwMwBIDEjecwd7vpsdXRoSxgWdBVJBqxGQVDuVcN2VUXiO9M60y_duTxXrUpr7CzncJgS3MY9jME09O-XaZnQQ"
}
  异常
  {
      "code": "2000",
      "error": "发送邮件失败"
  }

  ```

  * 确认绑定

    **功能描述：**通过邮箱中的链接，并通过一个特定的用户认证类，来解析出当前用户，以及email，并将email保存为当前用户的email

      **示例URL：**

      ` http://localhost:8000/api/v1/emailbind/?token=token`

      **请求方式：**POST

      **参数：**

    | 参数名 | 必选 | 类型   | 参数说明                        |
    | ------ | ---- | ------ | ------------------------------- |
    | token  | 是   | string | 用户token和email加密形成的token |

      **返回示例：**

    ```json
      返回成功示例：
    {
        "code": 1000,
        "data": {
            "id": 1,
            "role": 2,
            "username": "kenny",
            "email": "717556676@qq.com",
            "gender": "保密",
            "avatar": "http://qduxh573e.bkt.clouddn.com/Fpx_TGRR2GN9wrTM-IQKB8qhxxrr",
            "brief": "这个人很懒哦~",
            "job": "学生",
            "company": "武汉大学"
        }
    }
      异常
      {
          "code": "2000",
          "error": "邮箱绑定失败"
      }
    
    ```


## 二、文章模块

  ### 1.文章列表查看

  **简要描述：**查看所有文章,其中column不与tag搭配

  **示例URL：**

  ` http://localhost:8000/api/v1/articles/?sort=popular&size=10&page=2`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明                                    |
| ------ | ---- | ------- | ------------------------------------------- |
| sort   | 否   | string  | popular/newest 最热/最新                    |
| column | 否   | string  | columntitle获取对应文章列表                 |
| tag    | 否   | string  | tagtitle获取对应文章列表                    |
| size   | 否   | integer | 每页数量，default=5                         |
| page   | 否   | integer | 当前页，default=1                           |
| token  | 否   | string  | 可选token，用以获取是否被当前用户点赞、收藏 |

  **返回示例：**

  ```json
  返回成功示例：
  {
      "code": 1000,
      "data": [
          {
              "id": 36,
              "author": "kennyupdate",
              "column": "暂无栏目~",
              "tag": [],
              "article_likes": 0,
              "article_comments": 0,
              "title": "影评",
              "avatar": "1.png",
              "total_views": 0,
              "created": "2020-07-19T17:05:50.950833",
              "updated": "2020-07-19T17:05:50.950833",
              "likedbycuruser": 0,
              "favoritedbycuruser": 1
          },
          {
              "id": 37,
              "author": "kennyupdate",
              "column": "暂无栏目~",
              "tag": [],
              "article_likes": 0,
              "article_comments": 0,
              "title": "影评",
              "avatar": "1.png",
              "total_views": 0,
              "created": "2020-07-19T17:06:10.292372",
              "updated": "2020-07-19T17:06:10.292372",
              "likedbycuruser": 1,
              "favoritedbycuruser": 1
          },
     		......
      ]
  返回失败示例：
  没有文章：
  {
      "code": "1001",
      "error": "暂无文章~"
  }
  {
      "code": "1002",
      "error": "暂无更多文章~"
  }
  或者
{
      "code": "2000",
    "error": "获取文章列表失败！"
  }

  ```

  ### 2.文章详情查看

  **简要描述：**查看文章详情

  **示例URL：**

  ` http://localhost:8000/api/v1/articles/pk`

  **请求方式：**GET

  **参数：**无

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 文章id    |
| token  | 否   | string  | 用户token |

  **返回示例：**

  ```json
  返回成功示例：
{
    "code": 1000,
    "data": {
        "id": 1,
        "author": "kenny",
        "column": "编程",
        "tag": [
            "JavaScript"
        ],
        "article_likes": 0,
        "article_comments": 0,
        "title": "JavaScript中的原型与原型链",
        "content": "JavaScript中的原型与原型链JavaScript中的原型与原型链JavaScript中的原型与原型链",
        "content_text": "aaa",
        "avatar": null,
        "total_views": 5,
        "created": "2020-08-13T16:35:43.605194",
        "updated": "2020-08-17T13:35:15.393637",
        "likedbycuruser": 0,
        "favoritedbycuruser": 0
    }
}
  返回失败示例：
  没有文章：
  {
      "code": 4004,
      "error": "文章不存在~"
  }
  或者
{
      "code": "2000",
    "error": "获取文章详情失败！"
  }

  ```

  ### 3.文章创建

  **简要描述：**创建新文章

  **示例URL：**

  ` http://localhost:8000/api/v1/article/?token=token`

  **请求方式：**POST

  **参数：**

| 参数名      | 必选 | 类型    | 参数说明     |
| ----------- | ---- | ------- | ------------ |
| author      | 是   | Account | request.user |
| column      | 否   | string  | 文章栏目     |
| tag         | 是   | array   | 文章标签     |
| title       | 是   | string  | 文章标题     |
| content     | 否   | string  | 文章内容     |
| avatar      | 否   | string  | 文章标题图   |
| total_views | 否   | integer | 文章浏览量   |

  **示例数据**

  ```json
  { 
      "title":"1",
    "content":"21dfaqqq32",
          "avatar":"1.jpg",
    "column":"编程",
      "tag":["PYTHON","java","node","C++"]
  }
  ```

  

  **返回示例：**

  ```json
  创建成功示例：
  {
      "code": 1000,
      "data": {
          "id": 30,
          "author": "kennyupdate",
          "column": "编程",
          "tag": [
              "PYTHON",
              "java",
              "node",
              "C++"	
          ],
          "title": "1",
          "content": "21dfaqqq32",
          "avatar": "1.jpg",
          "total_views": 0,
          "created": "2020-07-19T15:42:06.646725",
          "updated": "2020-07-19T15:42:06.646725"
      }
  }
  返回失败示例：
  没有文章：
  {
      "code": "2000",
      "error": "添加标签失败"
  }
  或者
  {
      "code": "2000",
  "error": "新增文章失败！"
  }
  {
  "code": "4001",
  "error": "errors！"
  }
  ```

### 4.文章修改

**简要描述：**修改文章，作者和博主可以进行

  **示例URL：**

  ` http://localhost:8000/api/v1/article/pk?token=token`

  **请求方式：**PUT

  **参数：**

| 参数名      | 必选 | 类型    | 参数说明     |
| ----------- | ---- | ------- | ------------ |
| author      | 是   | Account | request.user |
| column      | 否   | string  | 文章栏目     |
| tag         | 是   | array   | 文章标签     |
| title       | 是   | string  | 文章标题     |
| content     | 否   | string  | 文章内容     |
| avatar      | 否   | string  | 文章标题图   |
| total_views | 否   | integer | 文章浏览量   |

  **示例数据**

```json
  { 
    "title":"1",
      "content":"21dfaqqq32",
    "avatar":"1.jpg",
      "column":"编程",
      "tag":["PYTHON","java","node","C++"]
  }  
```

**返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 12,
          "author": "kennyupdate",
          "column": "编程",
          "tag": [
              "PYTHON",
              "java",
              "node",
              "C++"
          ],
          "title": "1",
          "content": "21dfaqqq32",
          "avatar": "1.jpg",
          "total_views": 0,
          "created": "2020-07-19T12:43:31.740946",
          "updated": "2020-07-19T15:57:34.835568"
      }
  }
  返回失败示例：
  没有文章：
  {
      "code": 4004,
      "error": "该文章不存在"
  }
  或者
  {
      "code": "4006",
      "error": "您无权修改他人文章！"
  }
  或者
  {
      "code": "2000",
    "error": "添加标签失败！"
  }
{
      "code": "2000",
    "error": "添加文章失败！"
  }
{
      "code": "4001",
    "error": "validate errors"
  }
{
      "code": "4001",
    "error": "validate errors"
  }
  
  ```

  ### 5.文章删除

  **简要描述：**修改文章，作者和博主可以进行

  **示例URL：**

  ` http://localhost:8000/api/v1/article/pk?token=token`

  **请求方式：**DELETE

  **参数：无

| 参数名 | 必选 | 类型    | 参数说明 |
| ------ | ---- | ------- | -------- |
| pk     | 是   | integer | 文章id   |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 12,
          "author": "kennyupdate",
          "column": "编程",
          "tag": [
              "PYTHON",
              "java",
              "node",
              "C++"
          ],
          "title": "1",
          "content": "21dfaqqq32",
          "avatar": "1.jpg",
          "total_views": 0,
          "created": "2020-07-19T12:43:31.740946",
          "updated": "2020-07-19T15:57:34.835568"
      }
  }
  返回失败示例：
  没有文章：
  {
    "code": 4004,
      "error": "该文章不存在或已被删除"
}
  或者
{
      "code": "4006",
    "error": "您无权删除他人文章！"
  }
或者
  {
    "code": "2000",
      "error": "文章删除失败！"
}
  {
      "code": "4005",
      "error": "该api不存在"
}
  
  ```

  ### 6.文章栏目列表

  **简要描述：**获取栏目列表(无须登录及权限)

  **示例URL：**

  ` http://localhost:8000/api/v1/articlecolumns?size=2&page=2`

  **请求方式：**GET(list)

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明            |
| ------ | ---- | ------- | ------------------- |
| size   | 否   | integer | 每页数量，default=5 |
| page   | 否   | integer | 当前页，default=1   |

  **返回示例：**

  ```json
  成功示例：
    {
        "code": 1000,
        "data": [
            {
                "id": 1,
                "title": "编程",
                "brief": "此栏目主要用于记录编程blog哦~",
                "created": "2020-07-18T20:10:00.083735"
            },
            {
                "id": 2,
                "title": "随笔",
                "brief": "用于记录心情哦~",
                "created": "2020-07-18T20:10:23.570984"
            }
        ]
    }
  
  返回失败示例：
  没有文章：
  {
      "code": "1001",
      "error": "暂无文章栏目~"
  }
  {
      "code": "1002",
      "error": "暂无更多栏目~"
  }
  或者
  {
      "code": "2000",
      "error": "获取栏目列表失败！"
  }
  
  
  ```

  ### 7.文章栏目详情

  **简要描述：**获取栏目列表(无须登录及权限)

  **示例URL：**

  ` http://localhost:8000/api/v1/articlecolumns/1`

  **请求方式：**GET(retrieve)

    **参数：无

| 参数名 | 必选 | 类型 | 参数说明 |
| ------ | ---- | ---- | -------- |
|        |      |      |          |

    **返回示例：**
```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 1,
        "title": "编程",
        "brief": "此栏目主要用于记录编程blog哦~",
        "created": "2020-07-18T20:10:00.083735"
    }
}
  返回失败示例：
  没有文章：
  {
      "code": 4004,
      "error": "栏目不存在！"
  }
  或者
{
    "code": "2000",
 	 "error": "获取栏目详情失败！"
}

```

### 8.文章栏目增加

**简要描述：**增加某个栏目(需登录及博主权限)

**示例URL：**

` http://localhost:8000/api/v1/articlecolumn/`

**请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型   | 参数说明 |
| ------ | ---- | ------ | -------- |
| title  | 是   | string | 栏目名称 |
| brief  | 否   | string | 栏目简介 |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 6,
          "title": "课程1a",
          "brief": "主要记录sa课程~",
          "created": "2020-07-19T21:36:40.979417"
      }
  }
  返回失败示例：
  没有文章：
  {
      "code": "2000",
      "error": "新增栏目失败！"
  }
或
  {
      "detail": "您不是博主，不能访问哦~"
  }
  或者
  {
      "code": 4001,
      "error": {
          "title": [
              "This field may not be blank."
          ]
    }
  }
{
      "code": "4005",
      "error": "此api不存在！"
  }
  ```

### 9.文章栏目修改

**简要描述：**修改某个栏目(需登录及博主权限)

**示例URL：**

` http://localhost:8000/api/v1/articlecolumn/pk`

**请求方式：**PUT

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明         |
| ------ | ---- | ------- | ---------------- |
| pk     | 是   | integer | 所要修改的栏目id |
| title  | 是   | string  | 栏目名称         |
| brief  | 否   | string  | 栏目简介         |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 4,
          "title": "aaa",
          "brief": "主要记录sa课程~",
          "created": "2020-07-19T16:37:35.024894"
      }
  }	
  返回失败示例：
  没有文章：
  {
      "code": 4004,
      "error": "该栏目不存在或已被删除！"
  }
  或者
  {
      "code": "2000",
      "error": "栏目修改失败！"
  }
  {
      "detail": "您不是博主，不能访问哦~"
  }
  或者
  {
      "code": 4001,
      "error": {
          "title": [
              "This field may not be blank."
          ]
    }
  }
或
	{
      "code": "4005",
      "error": "此api不存在！"
  }
  ```

### 9.文章栏目删除

**简要描述：**删除某个栏目(需登录及博主权限)

**示例URL：**

` http://localhost:8000/api/v1/articlecolumn/pk`

**请求方式：**DELETE

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明         |
| ------ | ---- | ------- | ---------------- |
| pk     | 是   | integer | 所要修改的栏目id |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 4,
          "title": "aaa",
          "brief": "主要记录sa课程~",
          "created": "2020-07-19T16:37:35.024894"
      }
  }	
  返回失败示例：
  没有文章：
  {
      "code": 4004,
      "error": "该栏目不存在或已被删除！"
  }
  或者
  {
      "code": "2000",
      "error": "栏目删除失败！"
  }
  {
      "detail": "您不是博主，不能访问哦~"
	}
或
	{
      "code": "4005",
      "error": "此api不存在！"
  }
  
  ```

###  10.文章标签列表

**简要描述：**显示文章标签列表，并能获得最火标签

**示例URL：**

` http://localhost:8000/api/v1/articletags/?size=3&page=2&sort=popular`

**请求方式：**GET(LIST)

**参数：**

| 参数名 | 必选 | 类型    | 参数说明           |
| ------ | ---- | ------- | ------------------ |
| sort   | 否   | string  | 所要修改的栏目id   |
| size   | 否   | integer | 每页数量,default=5 |
| page   | 否   | 当前页  | 当前页，default=1  |

  **<u>注：sort和size配合使用得到最火标签列表，根据文章使用该标签数量计算热度</u>**

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": [
          {
              "id": 6,
              "articles_count": 5,
              "title": "C++",
              "created": "2020-07-19T14:14:46.540316"
          },
          {
              "id": 8,
              "articles_count": 2,
              "title": "FRAMEWORK",
              "created": "2020-07-19T22:29:53.228326"
          },
          {
              "id": 7,
              "articles_count": 1,
              "title": "DJANGO",
              "created": "2020-07-19T22:29:53.222343"
          }
      ]
  }
  返回失败示例：
  没有标签：
  {
      "code": "1001",
      "error": "暂无标签哦！"
  }
  或者
  {
      "code": "1002",
      "error": "暂无更多标签！"
  }
  {
      "code": "2000",
      "error": "获取标签列表失败！"
  }
  
  ```

  ###  11.文章标签详情

  **简要描述：**获取标签详情

  **示例URL：**

  ` http://localhost:8000/api/v1/articletags/1`

  **请求方式：**GET(RETRIEVE)

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明   |
| ------ | ---- | ------- | ---------- |
| pk     | 是   | integer | 文章标签id |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 1,
          "articles_count": 0,
          "title": "PYTHON_WEB",
          "created": "2020-07-18T20:09:08.371497"
      }
  }
  返回失败示例：
  此标签不存在：
  {
      "code": 4004,
      "error": "此标签不存在！"
  }
  或者
  {
      "code": "2000",
      "error": "获取标签失败！"
  }
  
  
  ```

  ###  12.文章标签增加

  **简要描述：**增加标签，没啥用。。。需要登录和博主权限

  **示例URL：**

  ` http://localhost:8000/api/v1/articletag/?token=博主token`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型   | 参数说明  |
| ------ | ---- | ------ | --------- |
| token  | 是   | string | 博主token |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 13,
          "articles_count": 0,
          "title": "API UPDATE",
          "created": "2020-07-20T22:05:01.955650"
      }
  }
  返回失败示例：
  不存在api，如果有pk，无法post：
  {
      "code": "4005",
      "error": "此api不存在！"
  }
  或者
  {
      "code": "2000",
      "error": "新增标签失败！"
  }
  或者{
      "code": "4001",
      "error": ser.errors
  }
  
  ```

  ###  13.文章标签修改

  **简要描述：**修改标签，需要登录和博主权限

  **示例URL：**

  ` http://localhost:8000/api/v1/articletag/1?token=博主token`

  **请求方式：**PUT

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明   |
| ------ | ---- | ------- | ---------- |
| pk     | 是   | integer | 文章标签id |
| token  | 是   | string  | 博主token  |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 13,
          "articles_count": 0,
          "title": "API",
          "created": "2020-07-20T22:05:01.955650"
      }
  }
  返回失败示例：
  不存在api，如果没有pk，无法put：
  {
      "code": "4005",
      "error": "此api不存在！"
  }
  或者
  {
      "code": 4004,
      "error": "该标签不存在或已被删除！"
  }
  {
      "code": "2000",
      "error": "标签修改失败！"
  }
  或者{
      "code": "4001",
      "error": ser.errors
  }
  
  ```

  ###  14.文章标签删除

  **简要描述：**删除标签，需要登录和博主权限

  **示例URL：**

  ` http://localhost:8000/api/v1/articletag/1?token=博主token`

  **请求方式：**PUT

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明   |
| ------ | ---- | ------- | ---------- |
| pk     | 是   | integer | 文章标签id |
| token  | 是   | string  | 博主token  |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 13,
          "articles_count": 0,
          "title": "API UPDATE",
          "created": "2020-07-20T22:05:01.955650"
      }
  }
  返回失败示例：
  不存在api，如果没有pk，无法delete：
  {
      "code": 4005,
      "error": "此api不存在！"
  }
  或者
  {
      "code": 4004,
      "error": "该标签不存在或已被删除！"
  }
  {
      "code": 2000,
      "error": "标签删除失败！"
  }
  
  ```

  ###  15.搜索文章

* 搜索文章

**简要描述：**采用drf-haystack与elasticsearch进行搜索，需要传递搜索参数text，来查询title和content中包含 text内容的文章以及可选的size、page和token

  **示例URL：**

  ` http://localhost:8000/api/v1/search/?text=1&size=2&token=ad89ad89-620d-4dbd-961a-f119a0dfb79e `

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明 |
| ------ | ---- | ------- | -------- |
| text   | 是   | string  | 查询内容 |
| size   | 否   | integer | 每页个数 |
| page   | 否   | integer | 第几页   |
| token  | 是   | string  | token    |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": [
        {
            "id": 1,
            "author": "kennyupdate",
            "column": "编程",
            "tag": [
                "PYTHON",
                "java",
                "node",
                "C++"
            ],
            "article_likes": 2,
            "article_comments": 4,
            "title": "<span class=\"highlighted\">1</span>",
            "summary": "2<span class=\"highlighted\">1</span>qqq32",
            "avatar": "1.jpg",
            "total_views": 27,
            "created": "2020-07-18T20:11:50.390335",
            "updated": "2020-07-26T11:45:59.373910",
            "likedbycuruser": 1,
            "favoritedbycuruser": 1
        },
        {
            "id": 3,
            "author": "qqq",
            "column": "编程",
            "tag": [],
            "article_likes": 0,
            "article_comments": 0,
            "title": "<span class=\"highlighted\">1</span>",
            "summary": "2<span class=\"highlighted\">1</span>32",
            "avatar": "1.jpg",
            "total_views": 0,
            "created": "2020-07-19T11:23:55.689244",
            "updated": "2020-07-19T11:23:55.689244",
            "likedbycuruser": 0,
            "favoritedbycuruser": 1
        }
    ]
}
返回失败示例：
  {
      "code": 1001,
      "error": "未搜索到相关文章！"
  }
  或者当前页不存在文章
  {
      "code": 1002,
      "error": "暂无更多文章"
  }
搜索失败
 {
      "code": 2000,
      "error": "搜索文章失败"
  }
  ```

  ###  16.获取用户文章

**简要描述：**传入用户id，获取其文章列表，并且能够最新最热，支持分页

  **示例URL：**

  ` http://localhost:8000/api/v1/userarticles/pk?&size=2&page=1&token=ad89ad89-620d-4dbd-961a-f119a0dfb79e `

  **请求方式：**GET

  **参数：**

| 参数名     | 必选 | 类型    | 参数说明 |
| ---------- | ---- | ------- | -------- |
| pk         | 是   | integer | 用户id   |
| size       | 否   | integer | 每页个数 |
| page       | 否   | integer | 第几页   |
| token      | 是   | string  | token    |
| sort_param | 否   | string  | 最新最热 |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": [
        {
            "id": 1,
            "author": "kennyupdate",
            "column": "编程",
            "tag": [
                "PYTHON",
                "java",
                "node",
                "C++"
            ],
            "article_likes": 3,
            "article_comments": 4,
            "title": "巩固你的HTML基础知识",
            "avatar": "http://qduxh573e.bkt.clouddn.com/050C0000525611A967583907F10CA01F",
            "total_views": 27,
            "created": "2020-07-18T20:11:50.390335",
            "updated": "2020-07-26T11:45:59.373910",
            "likedbycuruser": 0,
            "favoritedbycuruser": 0
        },
        {
            "id": 12,
            "author": "kennyupdate",
            "column": "编程",
            "tag": [
                "PYTHON",
                "java",
                "node",
                "C++"
            ],
            "article_likes": 0,
            "article_comments": 0,
            "title": "1",
            "avatar": "1.jpg",
            "total_views": 0,
            "created": "2020-07-19T12:43:31.740946",
            "updated": "2020-07-19T15:57:34.835568",
            "likedbycuruser": 0,
            "favoritedbycuruser": 0
        },
    ]
}
返回失败示例：
  {
      "code": 4004,
      "error": "该用户不存在！"
  }
  或者不存在文章
  {
      "code": 1001,
      "error": "该用户暂无文章"
  }
  或者当前页不存在文章
 {
      "code": 1002,
      "error": "暂无更多文章！"
  }
失败
 {
      "code": 2000,
      "error": "获取该用户文章列表失败"
  }
  ```



## 三、点赞模块

  ###  1.查看用户点赞文章列表

  **简要描述：**查看用户点赞文章列表，并且可以分页，不需要登录和博主权限

  **示例URL：**

  ` http://localhost:8000/api/v1/likearticles/pk?size=2&page=1`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明        |
| ------ | ---- | ------- | --------------- |
| pk     | 是   | integer | 文章id          |
| size   | 否   | integer | 每页多少，默认5 |
| page   | 否   | integer | 当前页。默认1   |
| sort   | 否   | string  | 排序方式        |

​	 **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": [
          {
              "id": 1,
              "author": "kennyupdate",
              "column": "编程",
              "tag": [
                  "PYTHON",
                  "java",
                  "node",
                  "C++"
              ],
              "article_likes": 2,
              "title": "1",
              "avatar": "1.jpg",
              "total_views": 16,
              "created": "2020-07-18T20:11:50.390335",
              "updated": "2020-07-20T20:19:06.207978"
          },
          {
              "id": 2,
              "author": "kennykmmmmkk",
              "column": "随笔",
              "tag": [
                  "PYTHON"
              ],
              "article_likes": 1,
              "title": "可惜没如果",
              "avatar": "1.png",
              "total_views": 0,
              "created": "2020-07-18T21:19:01.592119",
              "updated": "2020-07-18T21:19:01.592119"
          }
      ]
  }
  返回失败示例：
  不存在api，如果没有pk，无法get：
  {
      "code": "4002",
      "error": "未传递用户id！"
  }
  或者
  {
      "code": "4004",
      "error": "此用户不存在！"
  }
  {
      "code": "1001",
      "error": "此用户暂无喜欢的文章！"
  }
 	{
      "code": "1002",
      "error": "暂无更多喜欢的文章！"
  }
  {
      "code": "2000",	
      "error": "获取该用户喜欢的文章失败！"
  }
  
  ```

  ###  2.用户点赞文章

  **简要描述：**用户点赞文章，需要登录，无法重复点赞，或是重复取消点赞

  **示例URL：**

  ` http://localhost:8000/api/v1/likearticle/pk?token=用户token`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 文章id    |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 21,
          "user": "kennyupdate",
          "content_type": "article",
          "created": "2020-07-20T22:26:58.151904",
          "object_id": 10
      }
  }
  返回失败示例：
  不存在api，如果没有pk，无法post：
  {
      "code": 4002,
      "error": "未传递文章id！"
  }
  或者

  {
      "code": 4004,
      "error": "此文章不存在或已被删除！"
  }
  {
      "code": "4003",
      "error": "您已经点赞了哟！"
  }
  {
      "code": "2000",	
      "error": "点赞失败！"
  }
  {
      "code": "2000",	
      "error": ser.error
  }
  ```

  ###  3.用户取消点赞文章

  **简要描述：**用户取消点赞文章，需要登录，无法重复取消点赞

  **示例URL：**

  ` http://localhost:8000/api/v1/likearticle/pk?token=用户token`

  **请求方式：**DELETE

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 文章id    |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
  {
      "code": 1000,
      "data": {
          "id": 21,
          "user": "kennyupdate",
          "content_type": "article",
          "created": "2020-07-20T22:26:58.151904",
          "object_id": 10
      }
  }
  返回失败示例：
  不存在api，如果没有pk，无法delete：
  {
      "code": 4002,
      "error": "未传递相关参数！"
  }
  或者

  {
      "code": 4004,
      "error": "此文章不存在或已被删除！"
  }
  {
      "code": 4003,
      "error": "您尚未点赞哦！"
  }
  {
      "code": 2000,	
      "error": "取消点赞失败！"
  }

  ```

  ###  4.用户点赞评论

  **简要描述：**用户点赞评论，需要登录，无法重复点赞，或是重复取消点赞

  **示例URL：**

  ` http://localhost:8000/api/v1/likecomment/pk?token=用户token`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 评论id    |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 26,
        "user": "kennyupdate",
        "content_type": "comment",
        "created": "2020-07-25T10:08:40.697668",
        "object_id": 1
    }
}
  返回失败示例：
  不存在api，如果没有pk，无法post：
  {
      "code": 4002,
      "error": "未传递评论id值！"
  }
  或者

  {
      "code": 4004,
      "error": "评论不存在！"
  }
  {
      "code": 4003,
      "error": "您已经点赞了哟！"
  }
  {
      "code": 2000,	
      "error": "点赞失败！"
  }
  ```

  ###  5.用户取消点赞评论

 **简要描述：**用户取消点赞评论，需要登录，无法重复取消点赞

  **示例URL：**

  ` http://localhost:8000/api/v1/likearticle/pk?token=用户token`

  **请求方式：**DELETE

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 文章id    |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 26,
        "user": "kennyupdate",
        "content_type": "comment",
        "created": "2020-07-25T10:08:40.697668",
        "object_id": 1
    }
}
  返回失败示例：
  不存在api，如果没有pk，无法delete：
  {
      "code": 4002,
      "error": "未传递评论id值！"
  }
  或者

  {
      "code": 4004,
      "error": "此评论不存在或已被删除！"
  }
  {
      "code": 4003,
      "error": "您尚未点赞哦！"
  }
  {
      "code": 2000,	
      "error": "取消点赞失败！"
  }

  ```

## 四、图片模块

  ###  1.头像上传token获取

  **简要描述：**用于七牛云token获取，用于头像上传

  **示例URL：**

  ` http://localhost:8000/api/v1/userimagetoken/?token=用户token`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
  {
    "code": 1000,
    "data": "52-vV0d0uzjcmuQ3prX0Tmqb0mR_mt14y3WHB7Jl:AvjTc0RTFJuun9ieJDETthtuZxM=:eyJzY29wZSI6Imtlbm55cGljczprZW5ueXRlc3QxYXZhdGFyIiwiZGVhZGxpbmUiOjE1OTU0MjM2OTJ9"
}
  返回失败示例：
  或者
  {
      "code": "2000",
      "error": "获取用户头像上传token失败！"
  }
或者
{
    "code": "2001",
    "error": "用户认证失败"
}

  ```

  ###  2.博主照片上传token获取

  **简要描述：**用于七牛云token获取，用于相册照片上传，管理用户头像等。仅限博主权限

  **示例URL：**

  ` http://localhost:8000/api/v1/bloggerimageuploadtoken/?token=用户token`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| token  | 是   | integer | 用户token |

  **返回示例：**

  ```json
  成功示例：
  {
    "code": 1000,
    "data": "52-vV0d0uzjcmuQ3prX0Tmqb0mR_mt14y3WHB7Jl:AvjTc0RTFJuun9ieJDETthtuZxM=:eyJzY29wZSI6Imtlbm55cGljczprZW5ueXRlc3QxYXZhdGFyIiwiZGVhZGxpbmUiOjE1OTU0MjM2OTJ9"
}
  返回失败示例：
  不存在api，如果没有pk，无法DELETE：
  {
      "code": "1001",
      "error": "此文章不存在！"
  }
  或者
  {
      "code": "2000",
      "error": "获取相册照片上传token失败！"
  }

或者
{
    "code": "2001",
    "error": "用户认证失败"
}
{
    "detail": "您不是博主，不能访问哦~"
}

  ```

  ###  4.根据url上传图片

  **简要描述：**用于根据url上传网络图片，并返回存储到七牛云之后的url

  **示例URL：**

  ` http://localhost:8000/api/v1/uploadurltoqiniu/`

  **请求方式：**POST	

  **参数：**

| 参数名 | 必选 | 类型   | 参数说明            |
| ------ | ---- | ------ | ------------------- |
| url    | 是   | string | 要上传的网络图片url |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": "qduxh573e.bkt.clouddn.com/050C0000525611A967583907F10CA01F"
}
  返回失败示例：
  {
      "code": 4002,
      "error": "未传递图片url！"
  }
  或者
  {
      "code": "2000",
      "error": "上传图片失败！"
  }

  ```



## 五、评论模块

  ### 1.获取文章评论

**简要描述：**用于获取某篇文章的所有评论，无需登录

  **示例URL：**

  ` http://localhost:8000/api/v1/articlecomments/pk`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明                                              |
| ------ | ---- | ------- | ----------------------------------------------------- |
| pk     | 是   | integer | 文章id                                                |
| token  | 否   | string  | 用户token，上传此参数可确定各条评论是否被当前用户点赞 |

  **返回示例：**

  ```json
  成功示例：
  {
    "code": 1000,
    "data": [
        {
            "id": 7,
            "user": "kennyupdate",
            "content": "根评论",
            "created": "2020-07-24T16:03:49.755390",
            "children": [],
            "comment_likes": 0
        },
        {
            "id": 1,
            "user": "kennyupdate",
            "content": "adfasdfdasf",
            "created": "2020-07-24T10:22:43.312314",
            "children": [
                {
                    "id": 2,
                    "user": "kenykmmmmkk",
                    "content": "asdf",
                    "created": "2020-07-24T10:32:23.648469",
                    "reply_to": "kennyupdate",
                    "comment_likes": 0
                },
                {
                    "id": 9,
                    "user": "kennyupdate",
                    "content": "我是2号评论的子评论",
                    "created": "2020-07-24T16:20:08.317893",
                    "reply_to": "kenykmmmmkk",
                    "comment_likes": 1
                }
            ],
            "comment_likes": 0
        }
    ]
}
  返回失败示例：
 如果没有pk，无法查找评论：
  {
      "code": 4002,
      "error": "未传递文章id值！"
  }
  或者
  {
      "code": 4004,
      "error": "此文章不存在！"
  }

或者
{
    "code": 1001,
    "error": "此文章暂无评论"
}
{
    "code": 2000,
    "error": "获取评论失败"
}


  ```

### 2.发表文章评论

**简要描述：**用于发表文章评论，需要登录，需要两个参数，article_pk，comment_pk，分别代表文章id与父评论				id。前者必须传递，根据后者是否传递来确认发表的评论是否是父评论

  **示例URL：**

  ` http://localhost:8000/api/v1/articlecomment/article_pk/comment_pk/?token=token`

  **请求方式：**POST

  **参数：**

| 参数名     | 必选 | 类型    | 参数说明  |
| ---------- | ---- | ------- | --------- |
| article_pk | 是   | integer | 文章id    |
| comment_pk | 是   | integer | 父评论id  |
| token      | 是   | string  | 用户token |

  **返回示例：**

  ```json
  成功示例：
  {
    "code": 1000,
    "data": {
        "id": 10,
        "user": "kennyupdate",
        "content": "我是1号文章1号评论的子评论",
        "reply_to": "kennyupdate",
        "created": "2020-07-25T09:46:49.797758",
        "comment_likes": 0
    }
}
返回失败示例：
 如果没有pk，无法查找评论：
  {
      "code": 4002,
      "error": "未传递文章id值！"
  }
  或者
  {
      "code": 4004,
      "error": "此文章不存在！"
  }

或者
{
    "code": 4004,
    "error": "此父评论不存在"
}
{
    "code": 2000,
    "error": "评论失败"
}


  ```

### 3.删除文章评论

**简要描述：**用于删除文章评论，需要登录，需要pk参数，代表评论id。其中博主、所评论文章的作者，以及评论人本人有权删除评论

  **示例URL：**

  ` http://localhost:8000/api/v1/articlecomment/pk?token=token`

  **请求方式：**DELETE

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明  |
| ------ | ---- | ------- | --------- |
| pk     | 是   | integer | 评论id    |
| token  | 是   | string  | 用户token |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 10,
        "user": "kennyupdate",
        "content": "我是1号文章1号评论的子评论",
        "reply_to": "kennyupdate",
        "created": "2020-07-25T09:46:49.797758",
        "comment_likes": 0
    }
}
返回失败示例：
 如果没有pk，无法查找评论：
  {
      "code": 4002,
      "error": "未传递评论id值！"
  }
  或者
  {
      "code": 4004,
      "error": "评论不存在！"
  }

{
    "code": 2000,
    "error": "评论删除失败"
}

{
    "code": 4006,
    "error": "您的权限不足，无法删除评论"
}

  ```

## 六、收藏夹模块

### 1.查看用户收藏夹列表

**简要描述：**用于查看用户收藏夹列表，无需登录

  **示例URL：**

  ` http://localhost:8000/api/v1/userfavorites/user_pk/(article_pk)?size=2&page=1`

  **请求方式：**GET

  **参数：**

| 参数名     | 必选 | 类型     | 参数说明        |
| ---------- | ---- | -------- | --------------- |
| user_pk    | 是   | integer  | 用户id          |
| article_pk | 否   | integer  | 文章id          |
| size       | 否   | integer  | 每页个数，默认5 |
| page       | 否   | interger | 默认1           |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": [
        {
            "user": "kennyupdate",
            "title": "GIdafasd1S",
            "brief": "afdfsfa",
            "article_counts": "0",
            "avatar": "1.png",
            "createdorupdated": "2020-07-26T09:35:39.087307",
            "favoritedbycurfavorite": 0
        },
        {
            "user": "kennyupdate",
            "title": "GI1S",
            "brief": "地理信息科学",
            "article_counts": "4",
            "avatar": "1.png",
            "createdorupdated": "2020-07-25T19:00:07.873277",
            "favoritedbycurfavorite": 0
        },
        {
            "user": "kennyupdate",
            "title": "python",
            "brief": "暂无收藏夹简介~",
            "article_counts": "32",
            "avatar": "1.png",
            "createdorupdated": "2020-07-25T15:49:39.662468",
            "favoritedbycurfavorite": 1
        }
    ]
}
返回失败示例：
 如果没有pk：
  {
      "code": 4002,
      "error": "未传递用户id！"
  }
  或者
  {
      "code": 4004,
      "error": "用户不存在！"
  }
或者
  {
      "code": 1001,
      "error": "此用户暂无收藏夹！"
  }
{
    "code": 2000,
    "error": "获取收藏夹列表失败"
}
  ```

### 2.查看某个收藏夹详情

**简要描述：**用于查看某个收藏夹详情，无需登录，需要传递收藏夹id，由于收藏夹列表获取也是只需要一个参数，因此分为两个视图

  **示例URL：**

  ` http://localhost:8000/api/v1/favoritedetail/pk`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明 |
| ------ | ---- | ------- | -------- |
| pk     | 是   | integer | 收藏夹id |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "user": "kennyupdate",
        "title": "GI1S",
        "brief": "地理信息科学",
        "article_counts": "4",
        "avatar": "1.png",
        "createdorupdated": "2020-07-25T19:00:07.873277"
    }
}
返回失败示例：
 如果没有pk，：
  {
      "code": 4002,
      "error": "未传递收藏夹id！"
  }
  或者
  {
      "code": 4004,
      "error": "此收藏夹不存在！"
  }
或者
  {
      "code": 2000,
      "error": "获取收藏夹详情失败！"
  }
  ```

### 3.查看某个收藏夹所有文章列表

**简要描述：**用于查看某个收藏夹文章列表，可以分页，支持最新最热排序无需登录，需要传递收藏夹id，由于收藏夹文章列表获取也是只需要一个参数，因此还是新增一个视图

  **示例URL：**

  ` http://localhost:8000/api/v1/favoritearticles/pk?sort=newest&size=size&page=page`

  **请求方式：**GET

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明                              |
| ------ | ---- | ------- | ------------------------------------- |
| pk     | 是   | integer | 收藏夹id                              |
| sort   | 否   | string  | newest最新、popular最热、默认创建时间 |
| size   | 否   | integer | 每页展示数量，默认5                   |
| page   | 否   | integer | 当前页数，默认1                       |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": [
        {
            "id": 2,
            "author": "kennykmmmmkk",
            "column": "随笔",
            "tag": [
                "PYTHON"
            ],
            "article_likes": 1,
            "article_comments": 0,
            "title": "可惜没如果",
            "avatar": "1.png",
            "total_views": 7,
            "created": "2020-07-18T21:19:01.592119",
            "updated": "2020-07-25T18:35:04.494109",
            "likedbycuruser": 0
        },
        {
            "id": 3,
            "author": "qqq",
            "column": "编程",
            "tag": [],
            "article_likes": 0,
            "article_comments": 0,
            "title": "1",
            "avatar": "1.jpg",
            "total_views": 0,
            "created": "2020-07-19T11:23:55.689244",
            "updated": "2020-07-19T11:23:55.689244",
            "likedbycuruser": 0
        }
    ]
}
返回失败示例：
 如果没有pk，：
  {
      "code": 4002,
      "error": "未传递收藏夹id！"
  }
  或者
  {
      "code": 4004,
      "error": "此收藏夹不存在！"
  }
  {
      "code": 1001,
      "error": "此收藏夹暂无文章！"
  }
  {
      "code": 1002,
      "error": "暂无更多文章！"
  }
或者
  {
      "code": 2000,
      "error": "获取收藏夹文章列表失败！"
  }
  ```

### 4.增加、删除、修改收藏夹

* **增加收藏夹**

**简要描述：**用于用户增加收藏夹，需要登录

  **示例URL：**

  ` http://localhost:8000/api/v1/favorite/`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型         | 参数说明   |
| ------ | ---- | ------------ | ---------- |
| title  | 是   | string       | 收藏夹标题 |
| brief  | 否   | string       | 收藏夹简介 |
| user   | 是   | request.user | 当前用户   |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "user": "kennyupdate",
        "title": "test",
        "brief": "afdfsfa",
        "article_counts": "0",
        "avatar": "1.png",
        "createdorupdated": "2020-07-26T10:04:58.181957"
    }
}
返回失败示例：
 如果有pk，不能post：
  {
      "code": 4005,
      "error": "此api不存在！"
  }
  或者
  {
      "code": 4001,
      "error": ser.errors(主要title的unique)
  }
或者
  {
      "code": 2000,
      "error": "新建收藏夹失败！"
  }
  ```

* **修改收藏夹**

**简要描述：**用于用户修改收藏夹，需要登录，需要传递收藏夹pk

  **示例URL：**

  ` http://localhost:8000/api/v1/favorite/pk`

  **请求方式：**POST

  **参数：**

| 参数名 | 必选 | 类型         | 参数说明   |
| ------ | ---- | ------------ | ---------- |
| title  | 否   | string       | 收藏夹标题 |
| brief  | 否   | string       | 收藏夹简介 |
| user   | 否   | request.user | 当前用户   |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "user": "kennyupdate",
        "title": "tes1t",
        "brief": "aaa",
        "article_counts": "0",
        "avatar": "1.png",
        "createdorupdated": "2020-07-26T10:11:11.456487"
    }
}
返回失败示例：
 如果没有pk，不能put：
  {
      "code": 4002,
      "error": "未传递收藏夹id！"
  }
  或者
  {
      "code": 4004,
      "error":"收藏夹不存在"
  }
  {
      "code": 4006,
      "error": "您无法修改他人的收藏夹"
  }
  {
      "code": 4001,
      "error": ser.errors(主要title的unique)
  }
或者
  {
      "code": 2000,
      "error": "修改收藏夹信息失败！"
  }
  ```

* **删除收藏夹**

**简要描述：**用于用户删除收藏夹，需要登录，需要传递收藏夹pk

  **示例URL：**

  ` http://localhost:8000/api/v1/favorite/pk`

  **请求方式：**DELETE

  **参数：**

| 参数名 | 必选 | 类型    | 参数说明 |
| ------ | ---- | ------- | -------- |
| pk     | 是   | integer | 收藏夹id |
| token  |      |         |          |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "user": "kennyupdate",
        "title": "tes1t",
        "brief": "aaa",
        "article_counts": "0",
        "avatar": "1.png",
        "createdorupdated": "2020-07-26T10:11:11.456487"
    }
}
返回失败示例：
 如果没有pk，不能delete：
  {
      "code": 4002,
      "error": "未传递收藏夹id！"
  }
  或者
  {
      "code": 4004,
      "error":"收藏夹不存在"
  }
  {
      "code": 4006,
      "error": "您无法删除他人的收藏夹"
  }
  {
      "code": 4001,
      "error": ser.errors(主要title的unique)
  }
或者
  {
      "code": 2000,
      "error": "删除收藏夹信息失败！"
  }
  ```

### 5.收藏文章、取消收藏

* **收藏某文章到某文件夹**

**简要描述：**用于用户收藏某文章到某收藏夹，需要登录，需要收藏夹pk与文章pk

  **示例URL：**

  ` http://localhost:8000/api/v1/favoritearticle/favorite_pk/article_pk?token=token `

  **请求方式：**POST

  **参数：**

| 参数名      | 必选 | 类型    | 参数说明 |
| ----------- | ---- | ------- | -------- |
| favorite_pk | 是   | integer | 收藏夹id |
| article_pk  | 是   | integer | 文章id   |
| token       | 是   | string  | token    |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 5,
        "author": "qqq",
        "column": "编程",
        "tag": [],
        "article_likes": 0,
        "article_comments": 0,
        "title": "1",
        "content": "2132",
        "avatar": "1.jpg",
        "total_views": 0,
        "created": "2020-07-19T11:26:11.056397",
        "updated": "2020-07-19T11:26:11.056397",
        "likedbycuruser": 0
    }
}
返回失败示例：
 如果有pk，不能post：
  {
      "code": 4002,
      "error": "未传递收藏夹id或者文章id！"
  }
  或者
  {
      "code": 4004,
      "error": "收藏夹或文章不存在"
  }
收藏夹不是当前用户的
 {
      "code": 4006,
      "error": "您没有权限进行此操作"
  }
无法重复添加
 {
      "code": 4003,
      "error": "您已经将此文章添加至该收藏夹"
  }
或者
  {
      "code": 2000,
      "error": "将文章添加至收藏夹失败！"
  }
  ```

* **取消收藏某文章到某文件夹**

**简要描述：**用于用户收藏某文章到某收藏夹，需要登录，需要收藏夹pk与文章pk

  **示例URL：**

  ` http://localhost:8000/api/v1/favoritearticle/favorite_pk/article_pk?token=token `

  **请求方式：**POST

  **参数：**

| 参数名      | 必选 | 类型    | 参数说明 |
| ----------- | ---- | ------- | -------- |
| favorite_pk | 是   | integer | 收藏夹id |
| article_pk  | 是   | integer | 文章id   |
| token       | 是   | string  | token    |

  **返回示例：**

  ```json
  成功示例：
{
    "code": 1000,
    "data": {
        "id": 5,
        "author": "qqq",
        "column": "编程",
        "tag": [],
        "article_likes": 0,
        "article_comments": 0,
        "title": "1",
        "content": "2132",
        "avatar": "1.jpg",
        "total_views": 0,
        "created": "2020-07-19T11:26:11.056397",
        "updated": "2020-07-19T11:26:11.056397",
        "likedbycuruser": 0
    }
}
返回失败示例：
 如果有pk，不能post：
  {
      "code": 4002,
      "error": "未传递收藏夹id或者文章id！"
  }
  或者
  {
      "code": 4004,
      "error": "收藏夹或文章不存在"
  }
收藏夹不是当前用户的
 {
      "code": 4006,
      "error": "您没有权限进行此操作"
  }
无法重复添加
 {
      "code": 4003,
      "error": "此文章不在该收藏夹中"
  }
或者
  {
      "code": 2000,
      "error": "收藏夹移除该文章失败！"
  }
  ```







  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

