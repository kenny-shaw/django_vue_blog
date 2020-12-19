<template>
  <div class="reset_password_container">
    <div class="reset_password_box">
      <h1 class="reset_password_title">找回密码</h1>
      <el-form
        ref="resetPasswordFormRef"
        :model="resetPasswordForm"
        :rules="rules"
        label-width="0px"
        @keyup.enter.native="resetPassword"
      >
        <el-form-item prop="newpassword">
          <el-input
            v-model="resetPasswordForm.newpassword"
            placeholder="请输入新密码~"
            prefix-icon="icon iconfont iconicon-test26"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item prop="newpassword2">
          <el-input
            v-model="resetPasswordForm.newpassword2"
            placeholder="请再次输入新密码~"
            prefix-icon="icon iconfont iconicon-test26"
            show-password
          ></el-input>
        </el-form-item>

        <el-button
          type="primary"
          @click="resetPassword"
          class="reset_password_button"
          >重置</el-button
        >
      </el-form>
      <!-- <div class="reset_password_prompt_box">
        <a href="" @click.prevent="toLogin">已有账号</a>
        <a href="">忘记密码</a>
      </div> -->
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      resetPasswordForm: {
        newpassword: '',
        newpassword2: ''
      },
      rules: {
        newpassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        newpassword2: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 重置密码方法
    resetPassword() {
      const token = this.$route.query.token
      this.$refs.resetPasswordFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$axios.post(
          `resetpassword/?token=${token}`,
          this.resetPasswordForm
        )
        if (res.code !== 1000) {
          if (res.error.non_field_errors) {
            return this.$message.error(res.error.non_field_errors[0])
          }
          return this.$message.error(res.error)
        } else {
          this.$message.success('密码重置成功')
        }
        // 发送邮件后跳转到登录界面
        // 或者nextUrl，但是有路由预拦截，所以仍会跳到登录
        var url = this.$route.query.nextUrl
        console.log(url)
        if (url) {
          this.$router.push({ path: url })
        } else {
          this.$router.push({ path: '/login' })
        }
      })
    }
  }
}
</script>
<style lang="less" scoped>
.reset_password_container {
  width: 100%;
  height: 100%;
  background: #487eb0;
  display: flex;
  justify-content: center;
  align-items: center;

  .reset_password_box {
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
    .reset_password_title {
      font-size: 18px !important;
    }
    .reset_password_button {
      width: 100%;
    }
    // .reset_email_prompt_box {
    //   margin-top: 12px;
    //   display: flex;
    //   justify-content: space-between;
    //   a {
    //     text-decoration: none;
    //     font-size: 14px;
    //     color: #006cff;
    //   }
    // }
  }
}
</style>
