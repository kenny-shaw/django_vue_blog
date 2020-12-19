import Vue from 'vue'
import VueRouter from 'vue-router'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

// 主页组件
// import Home from '../components/Home.vue'
// 登录组件
// import Login from '../components/Login.vue'
// 注册组件
// import Register from '../components/Register.vue'
// 找回密码发送邮件组件
// import ResetEmail from '../components/ResetEmail.vue'
// 找回密码重置密码组件
// import ResetPassword from '../components/ResetPassword.vue'
// 文章列表组件（所有文章列表、某栏目文章列表、某标签文章列表等）
// import ArticleList from '../components/ArticleList.vue'
// 所有文章列表组件
// import ColumnArticle from '../components/ColumnArticle.vue'
// 用户中心组件
// import UserCenter from '../components/UserCenter.vue'
// 用户中心文章组件
// import UserCenterArticle from '../components/UserCenterArticle.vue'
// 用户中心喜欢组件
// import UserCenterLike from '../components/UserCenterLike.vue'
// 用户中心收藏夹组件
// import UserCenterFavorite from '../components/UserCenterFavorite.vue'
// 收藏夹文章列表组件
// import FavoriteArticle from '../components/FavoriteArticle.vue'
// 标签文章列表组件
// import TagArticle from '../components/TagArticle.vue'
// 标签列表组件
// import Tag from '../components/Tag.vue'
// 创作编辑器组件
// import Editor from '../components/Editor.vue'
// 文章查看组件
// import Post from '../components/Post.vue'
// 用户个人信息以及账号设置组件
// import UserSetting from '../components/UserSetting.vue'
// 用户个人信息更改组件
// import UserProfile from '../components/UserProfile.vue'
// 用户账号相关信息编辑组件
// import UserAccount from '../components/UserAccount.vue'
// 绑定邮箱组件
// import EmailBind from '../components/EmailBind.vue'
// 文章搜索组件
// import Search from '../components/Search.vue'
// 后台管理组件
// import Admin from '../components/Admin.vue'
// 后台管理用户组件
// import AdminUser from '../components/AdminUser.vue'
// 后台管理栏目组件
// import AdminColumn from '../components/AdminColumn.vue'
// 后台管理标签组件
// import AdminTag from '../components/AdminTag.vue'
// 后台管理情侣组件
// import AdminLover from '../components/AdminLover.vue'

// 主页组件
// import Home from '../components/Home.vue'
const Home = () =>
  import(
    /* webpackChunkName: "Home_ArticleList_ColumnArticle" */ '../components/Home.vue'
  )
// 文章列表组件（所有文章列表、某栏目文章列表、某标签文章列表等）
// import ArticleList from '../components/ArticleList.vue'
const ArticleList = () =>
  import(
    /* webpackChunkName: "Home_ArticleList_ColumnArticle" */ '../components/ArticleList.vue'
  )
// 所有文章列表组件
// import ColumnArticle from '../components/ColumnArticle.vue'
const ColumnArticle = () =>
  import(
    /* webpackChunkName: "Home_ArticleList_ColumnArticle" */ '../components/ColumnArticle.vue'
  )

// 登录组件
// import Login from '../components/Login.vue'
const Login = () =>
  import(
    /* webpackChunkName: "Login_Register_ResetEmail_ResetPassword" */ '../components/Login.vue'
  )
// 注册组件
// import Register from '../components/Register.vue'
const Register = () =>
  import(
    /* webpackChunkName: "Login_Register_ResetEmail_ResetPassword" */ '../components/Register.vue'
  )
// 找回密码发送邮件组件
// import ResetEmail from '../components/ResetEmail.vue'
const ResetEmail = () =>
  import(
    /* webpackChunkName: "Login_Register_ResetEmail_ResetPassword" */ '../components/ResetEmail.vue'
  )
// 找回密码重置密码组件
// import ResetPassword from '../components/ResetPassword.vue'
const ResetPassword = () =>
  import(
    /* webpackChunkName: "Login_Register_ResetEmail_ResetPassword" */ '../components/ResetPassword.vue'
  )

// 用户中心组件
// import UserCenter from '../components/UserCenter.vue'
const UserCenter = () =>
  import(
    /* webpackChunkName: "UserCenter_Article_Like_Favorite" */ '../components/UserCenter.vue'
  )
// 用户中心文章组件
// import UserCenterArticle from '../components/UserCenterArticle.vue'
const UserCenterArticle = () =>
  import(
    /* webpackChunkName: "UserCenter_Article_Like_Favorite" */ '../components/UserCenterArticle.vue'
  )
// 用户中心喜欢组件
// import UserCenterLike from '../components/UserCenterLike.vue'
const UserCenterLike = () =>
  import(
    /* webpackChunkName: "UserCenter_Article_Like_Favorite" */ '../components/UserCenterLike.vue'
  )
// 用户中心收藏夹组件
// import UserCenterFavorite from '../components/UserCenterFavorite.vue'
const UserCenterFavorite = () =>
  import(
    /* webpackChunkName: "UserCenter_Article_Like_Favorite" */ '../components/UserCenterFavorite.vue'
  )

// 收藏夹文章列表组件
// import FavoriteArticle from '../components/FavoriteArticle.vue'
const FavoriteArticle = () =>
  import(
    /* webpackChunkName: "FavoriteArticle_TagArticle_Tag_Search" */ '../components/FavoriteArticle.vue'
  )
// 标签文章列表组件
// import TagArticle from '../components/TagArticle.vue'
const TagArticle = () =>
  import(
    /* webpackChunkName: "FavoriteArticle_TagArticle_Tag_Search" */ '../components/TagArticle.vue'
  )
// 标签列表组件
// import Tag from '../components/Tag.vue'
const Tag = () =>
  import(
    /* webpackChunkName: "FavoriteArticle_TagArticle_Tag_Search" */ '../components/Tag.vue'
  )
// 文章搜索组件
// import Search from '../components/Search.vue'
const Search = () =>
  import(
    /* webpackChunkName: "FavoriteArticle_TagArticle_Tag_Search" */ '../components/Search.vue'
  )

// 创作编辑器组件
// import Editor from '../components/Editor.vue'
const Editor = () =>
  import(/* webpackChunkName: "Editor_Post" */ '../components/Editor.vue')
// 文章查看组件
// import Post from '../components/Post.vue'
const Post = () =>
  import(/* webpackChunkName: "Editor_Post" */ '../components/Post.vue')

// 用户个人信息以及账号设置组件
// import UserSetting from '../components/UserSetting.vue'
const UserSetting = () =>
  import(
    /* webpackChunkName: "UserSetting_UserProfile_UserAccount_EmailBind" */ '../components/UserSetting.vue'
  )
// 用户个人信息更改组件
// import UserProfile from '../components/UserProfile.vue'
const UserProfile = () =>
  import(
    /* webpackChunkName: "UserSetting_UserProfile_UserAccount_EmailBind" */ '../components/UserProfile.vue'
  )
// 用户账号相关信息编辑组件
// import UserAccount from '../components/UserAccount.vue'
const UserAccount = () =>
  import(
    /* webpackChunkName: "UserSetting_UserProfile_UserAccount_EmailBind" */ '../components/UserAccount.vue'
  )
// 绑定邮箱组件
// import EmailBind from '../components/EmailBind.vue'
const EmailBind = () =>
  import(
    /* webpackChunkName: "UserSetting_UserProfile_UserAccount_EmailBind" */ '../components/EmailBind.vue'
  )

// 后台管理组件
// import Admin from '../components/Admin.vue'
const Admin = () =>
  import(
    /* webpackChunkName: "Admin_User_Column_Tag_Lover" */ '../components/Admin.vue'
  )
// 后台管理用户组件
// import AdminUser from '../components/AdminUser.vue'
const AdminUser = () =>
  import(
    /* webpackChunkName: "Admin_User_Column_Tag_Lover" */ '../components/AdminUser.vue'
  )
// 后台管理栏目组件
// import AdminColumn from '../components/AdminColumn.vue'
const AdminColumn = () =>
  import(
    /* webpackChunkName: "Admin_User_Column_Tag_Lover" */ '../components/AdminColumn.vue'
  )
// 后台管理标签组件
// import AdminTag from '../components/AdminTag.vue'
const AdminTag = () =>
  import(
    /* webpackChunkName: "Admin_User_Column_Tag_Lover" */ '../components/AdminTag.vue'
  )
// 后台管理情侣组件
// import AdminLover from '../components/AdminLover.vue'
const AdminLover = () =>
  import(
    /* webpackChunkName: "Admin_User_Column_Tag_Lover" */ '../components/AdminLover.vue'
  )
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '',
        component: ArticleList,
        children: [
          // 跟路由，全部文章
          { path: '', component: ColumnArticle },
          // 栏目路由，获得栏目的所有文章
          {
            path: 'column/:column',
            component: ColumnArticle,
            name: 'column',
            props: true
            // meta: { requireAuth: true }
          }
        ]
      },
      // 登录路由
      { path: '/login', name: 'login', component: Login },
      // 注册路由
      { path: '/register', name: 'register', component: Register },
      // 重置密码发送邮件路由
      {
        path: '/reset/email',
        name: 'resetSendEmail',
        component: ResetEmail
      },
      // 重置密码路由
      {
        path: '/reset/password',
        name: 'resetPassword',
        component: ResetPassword
      },
      // 用户信息、账号设置
      {
        path: '/user/settings',
        component: UserSetting,
        children: [
          { path: '', component: UserProfile },
          { path: 'profile', component: UserProfile },
          { path: 'account', component: UserAccount }
        ]
      },
      {
        path: '/emailbind',
        component: EmailBind
      },
      // 用戶中心路由
      {
        path: '/user/:id',
        component: UserCenter,
        props: true,
        children: [
          { path: '', name: 'userCenterHome', component: UserCenterArticle },
          {
            path: 'articles',
            name: 'userCenterArticle',
            component: UserCenterArticle
          },
          {
            path: 'likes',
            name: 'userCenterLike',
            component: UserCenterLike
          },
          {
            path: 'favorites',
            name: 'userCenterFavorite',
            component: UserCenterFavorite
          }
        ]
      },
      // 获取收藏夹文章列表路由
      {
        path: '/favorite/:id',
        name: 'favorite',
        props: true,
        component: FavoriteArticle
      },
      // 获取标签文章列表路由
      {
        path: '/tag/:tagTitle',
        name: 'tag',
        props: true,
        component: TagArticle
      },
      {
        path: '/tags',
        name: 'tags',
        component: Tag
      },
      // 查看文章
      {
        path: '/post/:id',
        component: Post,
        props: true
      },
      // 搜索文章
      {
        path: 'search',
        name: 'search',
        component: Search
      },
      {
        path: 'admin',
        component: Admin,
        children: [
          { path: '', component: AdminUser },
          { path: 'user', component: AdminUser },
          { path: 'column', component: AdminColumn },
          { path: 'tag', component: AdminTag },
          { path: 'lover', component: AdminLover }
        ]
      }
    ]
  },
  // 新建文章
  {
    path: '/editor/',
    component: Editor,
    meta: { requireAuth: true }
  },
  // 修改文章
  {
    path: '/editor/:id',
    component: Editor,
    meta: { requireAuth: true },
    props: true
  }
]

const router = new VueRouter({
  routes
})

export default router
