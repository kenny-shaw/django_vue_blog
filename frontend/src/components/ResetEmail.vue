<template>
  <div class="reset_email_container">
    <div class="reset_email_box">
      <h1 class="reset_email_title">找回密码</h1>
      <el-form
        ref="resetEmailFormRef"
        :model="resetEmailForm"
        :rules="rules"
        label-width="0px"
        @keyup.enter.native="resetSendEmail"
      >
        <el-form-item prop="email">
          <el-input
            v-model="resetEmailForm.email"
            placeholder="请输入邮箱~"
            prefix-icon="icon iconfont iconicon-test33"
          ></el-input>
        </el-form-item>

        <el-button
          type="primary"
          @click="resetSendEmail"
          class="reset_email_button"
          >找回</el-button
        >
      </el-form>
      <div class="reset_email_prompt_box">
        <a href="" @click.prevent="toLogin">已有账号</a>
        <a href="" @click.prevent="toRegister">注册账号</a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      resetEmailForm: {
        email: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },

          {
            pattern: /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
            message: '请输入正确的邮箱',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    // 重置发送email方法
    resetSendEmail() {
      const nextUrl = this.$route.query.nextUrl
      let backendUrl = ''
      if (nextUrl) {
        backendUrl = `resetpasswordemail/?nextUrl=${nextUrl}`
      } else {
        backendUrl = 'resetpasswordemail/'
      }
      this.$refs.resetEmailFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$axios.post(
          backendUrl,
          this.resetEmailForm
        )
        if (res.code !== 1000) {
          return this.$message.error(res.error)
        } else {
          this.$message.success('请前往邮箱查看邮件')
        }
        // 发送邮件后跳转到登录界面
        // 或者nextUrl，但是有路由预拦截，所以仍会跳到登录
        var url = this.$route.query.nextUrl
        if (url) {
          this.$router.push({ path: url })
        } else {
          this.$router.push({ path: '/login' })
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
    // 前往登录路由
    toLogin() {
      var url = this.$route.query.nextUrl
      if (url) {
        this.$router.push({ path: '/login', query: { nextUrl: url } })
      } else {
        this.$router.push({ path: '/login' })
      }
    }
  }
}
</script>
<style lang="less" scoped>
.reset_email_container {
  width: 100%;
  height: 100%;
  background: #487eb0;
  display: flex;
  justify-content: center;
  align-items: center;

  .reset_email_box {
    max-width: 300px;
    min-height: 300px;
    width: 300px;
    background: #f4f5f5;
    box-sizing: border-box;
    padding: 10px;
    border-radius: 1%;
    box-shadow: 1px 1px 1px #fff;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    .reset_email_title {
      font-size: 18px !important;
    }
    .reset_email_button {
      width: 100%;
    }
    .reset_email_prompt_box {
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
