<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <!-- 头部中间区域 -->
      <div class="header-container">
        <!-- logo区域 -->
        <a href="/" class="logo"
          ><img src="../assets/image/kenny.png" class="logo-image" alt=""
        /></a>
        <!-- 导航栏区域 -->
        <el-menu
          :default-active="activeNavbarIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleNavbarSelect"
          text-color="#B2BAC2"
          active-text-color="#00a8ff"
          ref="navbarMenuRef"
          menu-trigger="click"
          :router="true"
        >
          <!-- 大屏幕时的导航 -->
          <el-menu-item index="/" class="hidden-xs-only">文章 </el-menu-item>
          <el-menu-item index="/gallery" class="hidden-xs-only"
            >照片</el-menu-item
          >
          <el-menu-item index="/aboutme" class="hidden-xs-only"
            >关于</el-menu-item
          >
          <!-- 小屏幕时变成子菜单导航 -->
          <el-submenu index="0" class="hidden-sm-and-up">
            <template slot="title">{{ menuIndexTitle }}</template>
            <el-menu-item index="/">文章</el-menu-item>
            <el-menu-item index="/gallery">照片</el-menu-item>
            <el-menu-item index="/aboutme">关于</el-menu-item>
          </el-submenu>
        </el-menu>
        <!-- 搜索框区域 -->
        <div class="search-box hidden-xxs-only">
          <el-input
            class="search-input "
            placeholder="搜索文章"
            suffix-icon="icon iconfont iconicon-test12"
            v-model="searchContent"
            @keyup.enter.native="toSearch"
          >
            <!-- <el-button
              slot="append"
              icon="icon iconfont iconicon-test12"
            ></el-button> -->
          </el-input>
          <!-- <input
            type="text"
            class="search-native-input "
            placeholder="搜索文章"
            v-model="searchContent"
            @keyup.enter.native="toSearch()"
          />
          <i class="icon iconfont iconicon-test12"></i> -->
        </div>
        <!--写文章区域 -->
        <div class="write-btn hidden-sm-and-down">
          <el-button type="primary" @click="toEditor">开始写作</el-button>
        </div>
        <!-- 登录/头像区域 -->
        <div class="login-avatar-box">
          <!-- 头像下拉区域 -->
          <el-dropdown
            v-if="this.$store.state.token"
            class="avatar-box"
            trigger="click"
            @command="handleAvatarCommand"
          >
            <!-- 头像区域 -->
            <el-avatar
              :size="35"
              :src="user.avatar"
              class="el-dropdown-link avatar-image"
            ></el-avatar>
            <!-- <img
              src="../assets/image/kenny1.png"
              alt="头像"
              class="el-dropdown-link avatar-image"
            /> -->
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="toEditor">开始写作</el-dropdown-item>
              <el-dropdown-item command="toUserCenter"
                >个人中心</el-dropdown-item
              >
              <el-dropdown-item command="toTags">标签云</el-dropdown-item>
              <el-dropdown-item command="toMyLikes">我的点赞</el-dropdown-item>
              <el-dropdown-item command="toMyFavorites"
                >我的收藏夹</el-dropdown-item
              >
              <el-dropdown-item command="toAdmin" v-if="user.role === 3"
                >博主后台</el-dropdown-item
              >
              <el-dropdown-item command="logout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-button
            type="primary"
            plain
            v-else
            class="login-btn"
            @click="toLogin"
            >登录</el-button
          >
        </div>
      </div>
    </el-header>
    <!-- 主题区域 -->
    <el-main class="back-top-main">
      <router-view></router-view>
      <el-backtop target=".back-top-main">
        <i class="el-icon-caret-top"></i>
      </el-backtop>
    </el-main>
    <!-- 尾部区域 -->
    <!-- <el-footer>footer</el-footer> -->
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activeNavbarIndex: '/',
      searchContent: '',
      // 当前登录用户
      user: {}
    }
  },
  computed: {
    menuIndexTitle: function() {
      const indexTitle = {
        '/': '文章',
        '/gallery': '照片',
        '/aboutme': '关于'
      }
      return indexTitle[this.activeNavbarIndex]
    }
  },
  methods: {
    // 注销功能
    logout() {
      this.$store.commit('clearToken')
      this.$router.push('/')
    },
    // 导航栏点击事件
    handleNavbarSelect(key, keyPath) {
      this.activeNavbarIndex = key
      // console.log(key, keyPath)
    },
    // 前往注册路由
    toLogin() {
      this.$router.push('/login')
    },
    toUserCenter() {
      this.$router.push(`/user/${this.$store.state.userid}`)
    },

    // 头像下拉菜单点击
    handleAvatarCommand(command) {
      if (command === 'logout') {
        this.logout()
      } else if (command === 'toUserCenter') {
        this.toUserCenter()
      } else if (command === 'toEditor') {
        this.toEditor()
      } else if (command === 'toTags') {
        this.toTags()
      } else if (command === 'toMyLikes') {
        this.toMyLikes(this.user.id)
      } else if (command === 'toMyFavorites') {
        this.toMyFavorites(this.user.id)
      } else if (command === 'toAdmin') {
        this.toAdmin()
      }
    },
    async getUserInfo() {
      const token = this.$store.state.token
      const backendUrl = `userinfo/?token=${token}`
      // const { data: res } = await this.$axios.get(backendUrl)
      try {
        const { data: res } = await this.$axios.get(backendUrl)
        if (res.code === 1000) {
          this.user = res.data
        } else {
          this.$message.error(res.error)
        }
      } catch (error) {
        this.$message.error('用户认证失败或过期，请重新登录！')
        this.$store.commit('clearToken')
        this.$router.push({ path: '/login' })
      }
    },
    // 前往编辑器写作路由
    toEditor() {
      this.$router.push({ path: '/editor' })
    },
    toSearch() {
      if (this.searchContent.trim() === '') {
        return this.$message.error('请输入搜索内容~')
      }
      this.$router.push({
        name: 'search',
        query: { query: this.searchContent }
      })
      this.searchContent = ''
    },
    toTags() {
      this.$router.push({ path: '/tags' })
    },
    // 前往我的点赞
    toMyLikes(userId) {
      this.$router.push({ path: `/user/${userId}/likes` })
    },
    // 前往我的收藏夹
    toMyFavorites(userId) {
      this.$router.push({ path: `/user/${userId}/favorites` })
    },
    toAdmin() {
      this.$router.push({ path: '/admin' })
    }
  },
  created() {
    // if (this.$store.state.token) {
    //   // console.log('create')
    //   this.getUserInfo()
    // }
  },
  watch: {
    // 监听路由变化，如果存在colomn，则使得直接进入url时激活栏目名称变化
    $route: {
      handler: function(val, oldVal) {
        if (this.$store.state.token) {
          console.log('watch')

          this.getUserInfo()
        }
        if (val.path.startsWith('/gallery')) {
          this.activeNavbarIndex = '/gallery'
        } else if (val.path.startsWith('/aboutme')) {
          this.activeNavbarIndex = '/aboutme'
        } else {
          this.activeNavbarIndex = '/'
        }
      },
      immediate: true
    }
  }
}
</script>
<style lang="less" scoped>
// 最外层盒子
.home-container {
  width: 100%;
  height: 100%;
  // 头部区域
  .el-header {
    border-bottom: 1px solid #f1f1f1;
    background: #ffffff;
    padding: 0;
    // 头部中间区域
    .header-container {
      display: flex;
      height: 100%;
      max-width: 960px;
      margin: auto;
      // 网站logo区域
      .logo {
        margin-right: 5px;
        width: 70px;
        // 网站logo照片
        .logo-image {
          height: 100%;
          width: auto;
        }
      }
      // 头部导航区域
      .el-menu {
        flex: 1;
        .el-menu-item {
          font-size: 16px;
        }
        .el-submenu {
          li.el-menu-item {
            font-size: 16px;
          }
        }
      }
      // 搜索框区域
      .search-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
        // margin: 10px;
        // padding: 0 15px;
        // background-color: #fff;
        // border-radius: 4px;
        // border: 1px solid #dcdfe6;
        // box-sizing: border-box;
        // color: #606266;

        transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
        // width: 100%;
        .search-native-input {
          height: 100%;
          outline: none;
          border: none;
        }
      }
      // 写文章按钮
      .write-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
      }
      //登录按钮或者头像区域
      .login-avatar-box {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0 10px;
        // 头像框
        .avatar-box {
          display: flex;
          justify-content: center;
          align-items: center;
        }
        .avatar-image {
          cursor: pointer;
        }
        // 自定义头像展示
        // .avatar-image {
        //   width: auto;
        //   height: 100%;
        //   border-radius: 50%;
        // }
      }
    }
  }
  // 主体区域
  .el-main {
    background: #f4f5f5;
    height: 100%;
    width: 100%;
    padding: 0;
    height: 100%;
    overflow: auto;
  }
  // 尾部区域
  .el-footer {
    background: ffffff;
    bottom: 0;
  }
}
</style>
