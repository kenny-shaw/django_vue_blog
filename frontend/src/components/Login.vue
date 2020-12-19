<template>
  <div class="login_container">
    <div class="login_box">
      <h1 class="login_title">账密登录</h1>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-width="0px"
        @keyup.enter.native="login"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名~"
            prefix-icon="icon iconfont iconicon-test35"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            placeholder="请输入密码~"
            show-password
            prefix-icon="icon iconfont iconicon-test26"
          ></el-input>
        </el-form-item>
        <el-button type="primary" @click="login" class="login_button"
          >登录</el-button
        >
      </el-form>
      <div class="login_prompt_box">
        <a href="" @click.prevent="toRegister">注册账号</a>
        <a href="" @click.prevent="toResetEmail">忘记密码</a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 登录方法
    login() {
      this.$refs.loginFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$axios.post('login/', this.loginForm)
        if (res.code !== 1000) {
          return this.$message.error(res.error)
        } else {
          this.$store.commit('saveToken', {
            token: res.data.token,
            username: this.loginForm.username,
            userid: res.data.userid
          })
        }
        // 登录后跳转
        var url = this.$route.query.nextUrl
        if (url) {
          this.$router.push({ path: url })
        } else {
          this.$router.push({ path: '/' })
        }
      })
    },
    // 前往注册路由
    toRegister() {
      var url = this.$route.query.nextUrl
      if (url) {
        this.$router.push({ path: '/register', query: { nextUrl: url } })
      } else {
        this.$router.push({ path: '/register' })
      }
    },
    // 前往重置密码路由
    toResetEmail() {
      var url = this.$route.query.nextUrl
      if (url) {
        this.$router.push({ path: '/reset/email', query: { nextUrl: url } })
      } else {
        this.$router.push({ path: '/reset/email' })
      }
    }
  }
}
</script>
<style lang="less" scoped>
.login_container {
  width: 100%;
  height: 100%;
  background: #487eb0;
  display: flex;
  justify-content: center;
  align-items: center;

  .login_box {
    max-width: 300px;
    height: 300px;
    width: 300px;
    background: #f4f5f5;
    box-sizing: border-box;
    padding: 10px;
    border-radius: 1%;
    box-shadow: 1px 1px 1px #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    .login_title {
      font-size: 18px !important;
    }
    .login_button {
      width: 100%;
    }
    .login_prompt_box {
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
      a {
        text-decoration: none;
        font-size: 14px;
        color: #006cff;
      }
    }
  }
}
</style>
