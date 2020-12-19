<template>
  <el-container>
    <div class="email-bind-confirm-box">
      <h1 class="title">邮箱绑定</h1>
      <div class="success-box" v-if="isSuccess">
        <i class="icon iconfont iconicon-test45 success-icon"></i>
        <h1 class="success-title">您已成功完成邮箱绑定~</h1>
      </div>
      <a
        href="#"
        class="confirm-link"
        v-if="!isSuccess"
        @click.prevent="confirmBindEmail"
        >请点击此处完成邮箱绑定~</a
      >
    </div>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      isSuccess: false
    }
  },
  methods: {
    async confirmBindEmail() {
      const token = this.$route.query.token
      const backendUrl = `emailbind/?token=${token}`
      const { data: res } = await this.$axios.post(backendUrl)
      if (res.code === 1000) {
        this.$message.success('您已成功绑定邮箱~')
        this.isSuccess = true
      } else {
        this.$message.error(res.error)
      }
    }
  }
}
</script>
<style lang="less" scoped>
.el-container {
  // background: #fff;
  width: 100%;
  max-width: 960px;
  height: 100%;
  margin: auto;
  .email-bind-confirm-box {
    border-radius: 2px;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    box-sizing: border-box;
    background: #fff;
    width: 100%;
    height: 100%;
    max-width: 700px;
    max-height: 700px;
    margin-top: 15px;
    padding: 32px 48px 84px;
    .title {
      font-size: 24px;
      font-weight: 700;
      padding: 16px 0;
      border-bottom: 1px solid #f1f1f1;
      margin-bottom: 14px;
    }
    .success-box {
      display: flex;
      align-items: center;
      .success-icon {
        font-size: 20px;
        color: #83c73a;
      }
      .success-title {
        margin-left: 12px;
        font-size: 18px;
        font-weight: 600;
        padding: 16px 0;
      }
    }
    .confirm-link {
      font-size: 14px;
      margin-top: 20px;
      &:hover {
        color: #007fff;
      }
    }
  }
}
</style>
