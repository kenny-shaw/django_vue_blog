from django.conf.urls import url, include
from api.views import accountview, articleview, imageview, commentview, likeview,favoriteview,searchview,loverview
from rest_framework import routers
# 搜索路由
# router=routers.DefaultRouter()
# router.register(r'search',searchview.ArticleSearchView,base_name='article_search')
urlpatterns = [
    # 关于用户路由
    # 登录路由
    url(r'^login/$', accountview.AuthView.as_view()),
    # 注册路由
    url(r'^register/$', accountview.RegisterView.as_view()),
    # 注销账号路由
    url(r'^cancelaccount/$', accountview.CancelAccountView.as_view()),
    # 用户信息查看及修改路由
    url(r'^userinfo/$', accountview.UserInfoView.as_view()),
    # 用户个人中心概略信息向他人展示以及增加总点赞量、总阅读量等信息
    url(r'^usergeneralinfo/(?P<pk>\d+)$', accountview.UserGeneralInfoView.as_view()),
    # 用户密码修改路由
    url(r'^setpassword/$', accountview.SetPasswordView.as_view()),
    # 根据邮箱发送密码重置邮件路由
    url(r'^resetpasswordemail/$', accountview.ResetPasswordEmailView.as_view()),
    # 重置密码路由
    url(r'^resetpassword/$', accountview.ResetPasswordView.as_view()),
    # 管理员查看所有用户信息路由
    url(r'^accountadmin/$', accountview.AccountAdminView.as_view({'get': 'list'})),
    # 管理员查看单个用户信息路由
    url(r'^accountadmin/(?P<pk>\d+)$', accountview.AccountAdminView.as_view({'get': 'retrieve'})),
    # 邮箱绑定第一步路由，发送邮件
    url(r'^emailbindsend/$', accountview.EmailBindSendView.as_view()),
    # 邮箱绑定第二步路由，完成绑定
    url(r'^emailbind/$', accountview.EmailBindView.as_view()),



    # 关于文章路由
    # 查看文章列表
    url(r'^articles/$', articleview.ArticleReadView.as_view({'get': 'list'})),
    # 查看文章详情
    url(r'^articles/(?P<pk>\d+)$', articleview.ArticleReadView.as_view({'get': 'retrieve'})),
    # 查看某作者文章列表，需要传入用户id
    url(r'^userarticles/(?P<pk>\d+)$', articleview.UserArticleReadView.as_view()),
    # 文章的增删改
    url(r'^article/(?P<pk>\d*)$', articleview.ArticleManipulateView.as_view()),

    # 文章栏目查看
    url(r'^articlecolumns/$', articleview.ArticleColumnReadView.as_view({'get': 'list'})),
    url(r'^articlecolumns/(?P<pk>\d+)$', articleview.ArticleColumnReadView.as_view({'get': 'retrieve'})),
    # 文章栏目增删改
    url(r'^articlecolumn/(?P<pk>\d*)$', articleview.ArticleColumnManipulateView.as_view()),

    # 文章标签查看
    url(r'^articletags/$', articleview.ArticleTagReadView.as_view({'get': 'list'})),
    url(r'^articletags/(?P<title>[\s\S]+)$', articleview.ArticleTagReadView.as_view({'get': 'retrieve'})),
    # 文章标签增删改
    url(r'^articletag/(?P<pk>\d*)$', articleview.ArticleTagManipulateView.as_view()),

    # 点赞相关url
    # 查看某人喜欢的文章
    url(r'^likearticles/(?P<pk>\d+)$', likeview.ArticleLikeReadView.as_view()),
    # 对id为pk的文章进行点赞,取消点赞
    url(r'^likearticle/(?P<pk>\d+)$', likeview.ArticleLikeManipulateView.as_view()),
    # 对评论进行点赞/取消点赞
    url(r'^likecomment/(?P<pk>\d+)$', likeview.CommentLikeManipulateView.as_view()),

    # 图片上传token获取url
    # 个人头像上传
    url(r'^userimagetoken/$', imageview.ImageUploadTokenView.as_view({'get': 'userimagetoken'})),
    url(r'^bloggerimageuploadtoken/$', imageview.BloggerImageUploadTokenView.as_view()),
    # 根据url上传图片到七牛云
    url(r'^uploadurltoqiniu/$', imageview.UploadUrlToQiniuView.as_view()),
    # 在七牛云删除文件
    url(r'^deleteimagefromqiniu/(?P<key>[\s\S]+)$', imageview.DeleteImageFromQiniuView.as_view()),

    # 评论相关url
    # 获取文章所有评论
    url(r'^articlecomments/(?P<pk>\d+)$', commentview.ArticleCommentReadView.as_view()),
    # 对文章发表评论
    url(r'^articlecomment/(?P<article_pk>\d+)/(?P<comment_pk>\d*)$', commentview.ArticleCommentAddView.as_view()),
    # 删除评论
    url(r'^articlecomment/(?P<pk>\d+)$', commentview.ArticleCommentDeleteView.as_view()),
    # 获取某条评论
    url(r'^comments/(?P<pk>\d+)$', commentview.CommentDetailReadView.as_view()),


    # 收藏夹相关url
    # 获取某用户的收藏夹列表，传递用户id,传递文章id是为了加一个该文章是否已被当前收藏夹收藏的信息
    url(r'^userfavorites/(?P<user_pk>\d+)/(?P<article_pk>\d*)$', favoriteview.FavoriteReadListView.as_view()),
    # 获取某个收藏夹详情，传递收藏夹id
    url(r'^favoritedetail/(?P<pk>\d+)$', favoriteview.FavoriteReadDetailView.as_view()),
    # 获取某个收藏夹所有文章列表，传递收藏夹id
    url(r'^favoritearticles/(?P<pk>\d+)$', favoriteview.FavoriteArticleListView.as_view()),
    # 增加修改删除收藏夹信息，不包括文章，只包括title和brief
    url(r'^favorite/(?P<pk>\d*)$', favoriteview.FavoriteManipulateView.as_view()),
    # 向收藏夹添加文章以及某收藏夹移除文章，需要传递收藏夹id、文章id，需要登录
    url(r'^favoritearticle/(?P<favorite_pk>\d+)/(?P<article_pk>\d+)$', favoriteview.FavoriteArticleManipulateView.as_view()),
    url(r'^search/$',searchview.ArticleSearchView.as_view()),

    # 情侣路由
    # 情侣信息查看
    url(r'^loverdetail/$', loverview.LoverReadView.as_view()),
    # 情侣信息更改（头像等）
    url(r'^loverupdate/$', loverview.LoverManipulateView.as_view()),

    # 测试路由
    # url(r"",include(router.urls))
]
