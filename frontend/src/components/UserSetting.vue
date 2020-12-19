<template>
  <el-container>
    <el-header height="46px">
      <!-- 居中区域 -->
      <div class="user-settings-header">
        <div class="return-user-center">
          <a class="icon iconfont iconicon-test66"></a>
          <a class="title" @click.prevent="toUserCenter">返回个人中心</a>
        </div>
        <a
          :class="['user-profile-btn', { 'is-profile': isProfile }]"
          @click="toUserSettingsProfile"
          >个人资料</a
        >
        <a
          :class="['user-account-btn', { 'is-profile': !isProfile }]"
          @click="toUserSettingsAccout"
          >账号设置</a
        >
      </div>
    </el-header>
    <el-main>
      <!-- 中间区域 -->
      <el-container class="user-settings-container">
        <!-- 内部主体区域 -->
        <div class="user-settings-inner-container padding-12-600 ">
          <router-view :user="user"></router-view>
        </div>
      </el-container>
    </el-main>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      isProfile: '',
      user: {}
    }
  },
  methods: {
    toUserSettingsAccout() {
      this.$router.push({ path: '/user/settings/account' })
    },
    toUserSettingsProfile() {
      this.$router.push({ path: '/user/settings/profile' })
    },
    async toUserCenter() {
      this.$router.push({ path: `/user/${this.user.id}` })
    },
    // 获取当前用户信息
    async getUserInfo() {
      const token = this.$store.state.token
      const backendUrl = `userinfo/?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.user = res.data
      } else {
        this.$message.error(res.error)
      }
    }
  },
  created() {
    this.getUserInfo()
  },
  watch: {
    // 监听路由变化，如果存在colomn，则使得直接进入url时激活栏目名称变化
    $route: {
      handler: function(val, oldVal) {
        if (val.path === '/user/settings/account') {
          this.isProfile = false
        } else {
          this.isProfile = true
        }
      },
      immediate: true
    }
  }
}
</script>
<style lang="less" scoped>
.is-profile {
  color: #007fff;
}
.el-header,
.el-main {
  margin: 0;
  padding: 0;
}
.el-container {
  width: 100%;
  height: 100%;
  .el-header {
    background: #fff;
    .user-settings-header {
      max-width: 960px;
      margin: auto;
      height: 100%;
      display: flex;
      align-items: center;

      .return-user-center {
        a {
          font-size: 14px;
        }
        .title {
          &:hover {
            color: #007fff;
          }
        }
      }
      .user-profile-btn {
        margin: 0 20px;
        font-size: 14px;
      }
      .user-account-btn {
        font-size: 14px;
      }
    }
  }
  .el-main {
    .user-settings-container {
      max-width: 960px;
      margin: auto;
      height: 100%;
      .user-settings-inner-container {
        border-radius: 2px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        box-sizing: border-box;
        background: #fff;
        width: 100%;
        height: 100%;
        max-width: 750px;
        max-height: 750px;
        margin-top: 15px;
        padding: 32px 48px 84px;
      }
    }
  }
}
/* 当屏幕小于600时，padding变为12 */
@media screen and (max-width: 600px) {
  .padding-12-600 {
    padding: 12px !important;
  }
}
</style>
