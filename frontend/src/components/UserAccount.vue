<template>
  <div class="user-account-detail">
    <!-- 询问是否删除收藏夹dialog区域 -->
    <el-dialog
      title="提示"
      :visible.sync="cancelAccountDialogVisible"
      width="30%"
      center
    >
      <span>是否注销？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelAccountDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="cancelAccount()">确 定</el-button>
      </span>
    </el-dialog>
    <h1 class="user-account-title">账号设置</h1>
    <ul class="account-setting-list">
      <!-- 头像区域 -->
      <li class="account-setting-item ">
        <span class="title">邮箱</span>
        <span class="item-detail">{{ user.email }}</span>
        <a
          class="action-btn"
          @click.prevent="openEmailBindBox"
          v-if="user.email !== ''"
          >换绑</a
        >
        <a class="action-btn" @click.prevent="openEmailBindBox" v-else>绑定</a>
      </li>
      <li class="account-setting-item setting-username">
        <span class="title">密码</span>
        <span class="item-detail"></span>
        <a class="action-btn" @click.prevent="openSetPasswordBox">修改</a>
      </li>
      <li class="account-setting-item">
        <span class="title">账号注销</span>
        <span class="item-detail"></span>
        <a class="action-btn" @click.prevent="openCancelAccountDialog">注销</a>
      </li>
    </ul>
    <div
      class="account-modal-box"
      v-if="setPasswordBoxVisible || emailBindBoxVisible"
    >
      <!-- 重置密码容器 -->
      <div class="set-password-box" v-if="setPasswordBoxVisible">
        <div class="set-password-title-close">
          <h1 class="set-password-title">修改密码</h1>
          <a
            class="el-icon-close close-btn"
            @click.prevent="closeSetPasswordBox"
          ></a>
        </div>

        <el-form
          ref="setPasswordFormRef"
          :model="setPasswordForm"
          :rules="rules"
          label-width="0px"
        >
          <el-form-item prop="oldpassword">
            <el-input
              v-model="setPasswordForm.oldpassword"
              placeholder="请输入原密码~"
              show-password
              prefix-icon="icon iconfont iconicon-test26"
            ></el-input>
          </el-form-item>
          <el-form-item prop="newpassword">
            <el-input
              v-model="setPasswordForm.newpassword"
              placeholder="请输入新密码~"
              show-password
              prefix-icon="icon iconfont iconicon-test26"
            ></el-input>
          </el-form-item>
          <el-form-item prop="newpassword2">
            <el-input
              v-model="setPasswordForm.newpassword2"
              placeholder="请再次输入新密码~"
              show-password
              prefix-icon="icon iconfont iconicon-test26"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="setPassword"
            class="set-password-button"
            >修改</el-button
          >
        </el-form>
      </div>
      <!-- 绑定邮箱容器 -->
      <div class="email-bind-box" v-if="emailBindBoxVisible">
        <div class="email-bind-title-close">
          <h1 class="email-bind-title">绑定邮箱</h1>
          <a
            class="el-icon-close close-btn"
            @click.prevent="closeEmailBindBox"
          ></a>
        </div>

        <el-form
          ref="emailBindFormRef"
          :model="emailBindForm"
          :rules="emailBindRules"
          label-width="0px"
          @keyup.enter.native="sendEmailBindEmail"
        >
          <el-form-item prop="email">
            <el-input
              v-model="emailBindForm.email"
              placeholder="请输入邮箱~"
              prefix-icon="icon iconfont iconicon-test33"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="sendEmailBindEmail"
            class="email-bind-button"
            >绑定</el-button
          >
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: {},
      // 控制确认注销账号dialog显示或隐藏
      cancelAccountDialogVisible: false,
      // 控制修改密码容器显示与隐藏
      setPasswordBoxVisible: false,
      // 控制修改密码容器显示与隐藏
      emailBindBoxVisible: false,
      setPasswordForm: {
        oldpassword: '',
        newpassword: '',
        newpassword2: ''
      },
      emailBindForm: {
        email: ''
      },
      rules: {
        oldpassword: [
          { required: true, message: '请输入原密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        newpassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        newpassword2: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      },
      emailBindRules: {
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
    },
    // 打开注销账号提示对话框
    openCancelAccountDialog() {
      this.cancelAccountDialogVisible = true
    },
    // 注销账号
    async cancelAccount() {
      const token = this.$store.state.token
      const backendUrl = `cancelaccount/?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.$message.success('账号注销成功')
        this.$store.commit('clearToken')
        this.$router.push({ path: '/' })
      } else {
        this.$message.error(res.error)
      }
    },
    async setPassword() {
      this.$refs.setPasswordFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `setpassword/?token=${token}`
        const { data: res } = await this.$axios.post(
          backendUrl,
          this.setPasswordForm
        )
        if (res.code === 1000) {
          this.$message.success('密码重置成功')
          this.$store.commit('clearToken')
          this.$router.push({ path: '/login' })
        } else {
          this.$message.error(res.error)
        }
      })
    },
    // 开启修改密码容器
    openSetPasswordBox() {
      this.setPasswordBoxVisible = true
    },
    // 关闭更改密码容器
    closeSetPasswordBox() {
      this.setPasswordBoxVisible = false
    },
    // 开启修改密码容器
    openEmailBindBox() {
      this.emailBindBoxVisible = true
    },
    // 关闭更改密码容器
    closeEmailBindBox() {
      this.emailBindBoxVisible = false
    },
    async sendEmailBindEmail() {
      this.$refs.emailBindFormRef.validate(async valid => {
        if (!valid) return
        if (
          this.emailBindForm.email.toLowerCase() ===
          this.user.email.toLowerCase()
        ) {
          return this.$message.error('您已绑定此邮箱')
        }
        const token = this.$store.state.token
        const backendUrl = `emailbindsend/?token=${token}`
        const { data: res } = await this.$axios.post(
          backendUrl,
          this.emailBindForm
        )
        if (res.code === 1000) {
          this.$message.success('邮件发送成功，请前往邮箱进行查看绑定~')
          this.closeEmailBindBox()
        } else {
          this.$message.error(res.error)
        }
      })
    }
  },
  created() {
    this.getUserInfo()
  }
}
</script>
<style lang="less" scoped>
.user-account-detail {
  height: 100%;
  width: 100%;
  // overflow: auto;
  .user-account-title {
    font-size: 24px;
    font-weight: 700;
    margin: 16px 0;
  }
  .account-setting-list {
    list-style: none;
    .account-setting-item {
      padding: 24px 0;
      border-top: 1px solid #f1f1f1;
      display: flex;
      align-items: center;
      .title {
        font-size: 15px;
        color: #333;
        width: 120px;
      }
      .item-detail {
        flex: 1;
        color: #909090;
        font-size: 16px;
      }
      .action-btn {
        font-size: 14px;
        color: #007fff;
      }
    }
  }
  .account-modal-box {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 400;
    .set-password-box {
      max-width: 300px;
      min-height: 300px;
      width: 300px;
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;

      .set-password-title-close {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        .set-password-title {
          flex: 1;
          font-size: 18px !important;
        }
        .close-btn {
          &:hover {
            color: #007fff;
          }
          // color: red;
        }
      }

      .set-password-button {
        width: 100%;
      }
    }
    .email-bind-box {
      max-width: 300px;
      // min-height: 300px;
      width: 300px;
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      .email-bind-title-close {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        .email-bind-title {
          flex: 1;
          font-size: 18px !important;
        }
        .close-btn {
          &:hover {
            color: #007fff;
          }
          // color: red;
        }
      }

      .email-bind-button {
        width: 100%;
      }
    }
  }
}
</style>
