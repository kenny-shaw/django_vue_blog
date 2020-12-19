<template>
  <div class="register_container">
    <div class="register_box">
      <h1 class="register_title">用户注册</h1>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-width="0px"
        @keyup.enter.native="register"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名~"
            prefix-icon="icon iconfont iconicon-test35"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            placeholder="请输入密码~"
            show-password
            prefix-icon="icon iconfont iconicon-test26"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password2">
          <el-input
            v-model="registerForm.password2"
            placeholder="请再次输入密码~"
            show-password
            prefix-icon="icon iconfont iconicon-test26"
          ></el-input>
        </el-form-item>
        <el-button type="primary" @click="register" class="register_button"
          >注册</el-button
        >
      </el-form>
      <div class="register_prompt_box">
        <a href="" @click.prevent="toLogin">已有账号</a>
        <a href="" @click.prevent="toResetEmail">忘记密码</a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        password2: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        password2: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 注册方法
    register() {
      this.$refs.registerFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$axios.post(
          'register/',
          this.registerForm
        )
        if (res.code !== 1000) {
          console.log(res.error)
          if (res.error.username) {
            return this.$message.error(res.error.username[0])
          } else if (res.error.non_field_errors) {
            return this.$message.error(res.error.non_field_errors[0])
          }
          return this.$message.error(res.error)
        } else {
          this.$message.success('注册成功')
        }
        // 注册后跳转到登录界面，并且仍然带着还未访问的nextUrl
        var url = this.$route.query.nextUrl
        if (url) {
          this.$router.push({ path: url })
        } else {
          this.$router.push({ path: '/login' })
        }
      })
    },
    // 前往登录路由
    toLogin() {
      var url = this.$route.query.nextUrl
      if (url) {
        this.$router.push({ path: '/login', query: { nextUrl: url } })
      } else {
        this.$router.push({ path: '/login' })
      }
    },
    // 前往忘记密码的发送邮件路由页面
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
.register_container {
  width: 100%;
  height: 100%;
  background: #487eb0;
  display: flex;
  justify-content: center;
  align-items: center;

  .register_box {
    max-width: 300px;
    min-height: 300px;
    width: 300px;
    background: #f4f5f5;
    box-sizing: border-box;
    padding: 10px;
    border-radius: 1%;
    box-shadow: 1px 1px 1px #fff;
    .register_title {
      font-size: 18px !important;
    }
    .register_button {
      width: 100%;
    }
    .register_prompt_box {
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
