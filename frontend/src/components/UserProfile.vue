<template>
  <div class="user-profile-detail">
    <h1 class="user-profile-title">个人资料</h1>
    <ul class="profile-setting-list">
      <!-- 头像区域 -->
      <li class="profile-setting-item setting-avatar">
        <span class="title">头像</span>
        <div class="avatar-uploader">
          <el-avatar
            shape="square"
            :size="72"
            :src="user.avatar"
            :key="user.avatar"
            fit="cover"
          ></el-avatar>
          <el-upload
            class="el-uploader"
            action="http://up.qiniup.com"
            :limit="1"
            :on-exceed="handleAvatarExceed"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :data="qiniuData"
            ref="uploadAvatarRef"
          >
            <el-button size="mini" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">
              只能上传jpg/png/jepg文件，且不超过5M
            </div>
          </el-upload>
        </div>
      </li>
      <li class="profile-setting-item setting-username">
        <span class="title">用户名</span>
        <input type="text" class="item-input" v-model="user.username" />
      </li>
      <li class="profile-setting-item">
        <span class="title">性别</span>
        <select v-model="user.gender" class="item-select">
          <option value="1">保密</option>
          <option value="2">男</option>
          <option value="3">女</option>
        </select>
      </li>
      <li class="profile-setting-item">
        <span class="title">职位</span>
        <input type="text" class="item-input" v-model="user.job" />
      </li>
      <li class="profile-setting-item">
        <span class="title">公司</span>
        <input type="text" class="item-input" v-model="user.company" />
      </li>
      <li class="profile-setting-item">
        <span class="title">个人介绍</span>
        <input type="text" class="item-input" v-model="user.brief" />
      </li>
      <li class="profile-setting-item">
        <el-button type="primary" size="small" @click="postUserInfo"
          >提交</el-button
        >
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: {},
      qiniuData: {
        token: ''
      },
      //  头像上传token
      avatarUploadToken: ''
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
    handleAvatarExceed() {
      this.$message.error('请不要上传多张头像')
    },
    async beforeAvatarUpload(file) {
      // this.qiniuData.key = file.name
      this.qiniuData.token = this.avatarUploadToken
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt5M = file.size / 1024 / 1024 < 5
      console.log(this)
      if (!isJPG && !isPNG) {
        this.$message.error('图片只能是 JPG/PNG 格式!')
        return false
      }
      if (!isLt5M) {
        this.$message.error('图片大小不能超过 2MB!')
        return false
      }
    },
    // 获取头像上传token
    async getAvatarUploadToken() {
      const token = this.$store.state.token
      const backendUrl = `userimagetoken/?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.avatarUploadToken = res.data
      } else {
        this.$message.error(res.error)
      }
    },
    // 头像上传
    handleAvatarSuccess(res, file, filelist) {
      // 删除七牛云中的头像
      if (this.user.avatar !== '') {
        // this.deleteAvatar(this.user.avatar)
      }
      this.user.avatar = res.url
      // 成功后清空组件上传文件列表
      this.$refs.uploadAvatarRef.clearFiles()
      // 更改头像后直接提交修改
      this.postUserInfo()
    },
    // 根据url获取key值，删除七牛云中的图片
    async deleteAvatar(url) {
      // 从url截取key值
      const splitArray = url.split('/')
      const key = splitArray[splitArray.length - 1]
      const { data: res } = await this.$axios.delete(
        `deleteimagefromqiniu/${key}`
      )
      if (res.code !== 1000) {
        return this.$message.error(res.error)
      }
    },
    // 提交修改
    async postUserInfo() {
      const token = this.$store.state.token
      const backendUrl = `userinfo/?token=${token}`
      const { data: res } = await this.$axios.put(backendUrl, this.user)
      if (res.code === 1000) {
        this.user = res.data
        this.$message.success('个人信息修改成功~')
      } else {
        if (res.error.username) {
          this.$message.error(res.error.username[0])
        }
      }
    }
  },
  created() {
    this.getAvatarUploadToken()
    this.getUserInfo()
  }
}
</script>
<style lang="less" scoped>
.user-profile-detail {
  height: 100%;
  width: 100%;
  // overflow: auto;
  .user-profile-title {
    font-size: 24px;
    font-weight: 700;
    margin: 16px 0;
  }
  .profile-setting-list {
    list-style: none;
    .profile-setting-item {
      padding: 24px 0;
      border-top: 1px solid #f1f1f1;
      display: flex;
      align-items: center;
      .title {
        font-size: 15px;
        color: #333;
        width: 120px;
      }
      .item-input {
        flex: 1;
        border: none;
        outline: none;
        color: #909090;
        font-size: 16px;
      }
      .item-select {
        height: 20px;
        flex: 1;
        border: none;
        outline: none;
        background: #fff;
        color: #909090;
        font-size: 16px;
        // line-height: 2;
      }
    }
    .profile-setting-item:first-child {
      padding: 14.4px 0;
      border-top: 1px solid #f1f1f1;
    }
    .setting-avatar {
      display: flex;
      .avatar-uploader {
        flex: 1;
        display: flex;
        .el-uploader {
          margin-left: 12px;
          flex: 1;
        }
      }
    }
    // .setting-username {
    //   .username-input {
    //   }
    // }
  }
}
</style>
