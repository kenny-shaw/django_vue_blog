<template>
  <el-container>
    <!-- 头部面包屑导航区域 -->
    <el-header height="30px">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/admin' }"
          >博主中心</el-breadcrumb-item
        >
        <el-breadcrumb-item><a>情侣管理</a></el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <div class="table-container">
        <!-- 表格区域 -->
        <el-table :data="lover" border stripe>
          <el-table-column type="index" label="#"> </el-table-column>
          <el-table-column prop="boy" label="男生"> </el-table-column>
          <el-table-column prop="girl" label="女生"> </el-table-column>
          <el-table-column prop="boyavatar" label="男生头像">
            <template slot-scope="scope">
              <div class="avatar-uploader">
                <el-avatar
                  shape="square"
                  :size="60"
                  :src="scope.row.boyavatar"
                ></el-avatar>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="girlavatar" label="女生头像">
            <template slot-scope="scope">
              <div class="avatar-uploader">
                <el-avatar
                  shape="square"
                  :size="60"
                  :src="scope.row.girlavatar"
                ></el-avatar>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="togetherdate" label="在一起时间">
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                @click="showModalBox(scope.row)"
                >编辑</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-main>
    <div class="modal-box" v-if="isModalBoxVisible">
      <div class="update-lover-box">
        <div class="boyavatar-uploader">
          <el-avatar
            shape="square"
            :size="72"
            :src="loverForm.boyavatar"
            :key="loverForm.boyavatar"
            fit="cover"
          ></el-avatar>
          <el-upload
            action="http://up.qiniup.com"
            :limit="1"
            :on-exceed="handleAvatarExceed"
            :show-file-list="false"
            :on-success="handleBoyAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :data="qiniuData"
            ref="uploadBoyAvatarRef"
          >
            <el-button size="mini" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">
              只能上传jpg/png/jepg文件，且不超过5M
            </div>
          </el-upload>
          <a class="el-icon-close close-btn" @click.prevent="closeModalBox"></a>
        </div>
        <div class="girlavatar-uploader">
          <el-avatar
            shape="square"
            :size="72"
            :src="loverForm.girlavatar"
            :key="loverForm.girlavatar"
            fit="cover"
          ></el-avatar>
          <el-upload
            action="http://up.qiniup.com"
            :limit="1"
            :on-exceed="handleAvatarExceed"
            :show-file-list="false"
            :on-success="handleGirlAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :data="qiniuData"
            ref="uploadGirlAvatarRef"
          >
            <el-button size="mini" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">
              只能上传jpg/png/jepg文件，且不超过5M
            </div>
          </el-upload>
        </div>
        <el-form ref="loverFormRef" :model="loverForm" label-width="0px">
          <el-form-item>
            <el-input
              v-model="loverForm.boy"
              placeholder="请输入男孩名字~"
              prefix-icon="icon iconfont iconicon-test35"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="loverForm.girl"
              placeholder="请输入女孩名字~"
              prefix-icon="icon iconfont iconicon-test35"
            ></el-input> </el-form-item
          ><el-form-item>
            <el-input
              v-model="loverForm.togetherdate"
              placeholder="请输入在一起日期（eg 2019-11-12）~"
              prefix-icon="icon iconfont iconicon-test35"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="updateLover"
            class="update-lover-button"
            >修改</el-button
          >
        </el-form>
      </div>
    </div>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      lover: [],
      qiniuData: {},
      loverForm: {
        boy: '',
        girl: '',
        boyavatar: '',
        girlavatar: '',
        togetherdate: ''
      },
      // modal层数是否可见
      isModalBoxVisible: false,
      avatarUploadToken: ''
    }
  },
  methods: {
    async getLoverDetail() {
      const backendUrl = 'loverdetail/'
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.lover = [res.data]
        console.log(this.lover)
      } else {
        this.$message.error(res.error)
      }
    },
    // 隐藏modal层
    closeModalBox() {
      this.isModalBoxVisible = false
      this.loverForm = {
        boy: '',
        girl: '',
        boyavatar: '',
        girlavatar: '',
        togetherdate: ''
      }
      this.$refs.loverFormRef.resetFields()
    },
    showModalBox(lover) {
      this.isModalBoxVisible = true
      this.loverForm = Object.assign(this.loverForm, lover)
    },
    async updateLover() {
      const token = this.$store.state.token
      const backendUrl = `loverupdate/?token=${token}`
      const { data: res } = await this.$axios.put(backendUrl, this.loverForm)
      if ('detail' in res) {
        this.$message.error(res.detail)
      } else if (res.code === 1000) {
        this.$message.success('情侣信息修改成功')
        this.closeModalBox()
        this.getLoverDetail()
      } else {
        this.$message.error('情侣信息修改失败')
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
      const backendUrl = `bloggerimageuploadtoken/?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.avatarUploadToken = res.data
      } else {
        this.$message.error(res.error)
      }
    },
    // 男孩头像上传
    async handleBoyAvatarSuccess(res, file, filelist) {
      // 删除七牛云中的头像

      if (this.loverForm.boyavatar !== '') {
        console.log(this.loverForm.boyavatar)
        // this.deleteAvatar(this.userForm.avatar)
      }
      this.loverForm.boyavatar = res.url
      // 成功后清空组件上传文件列表
      this.$refs.uploadBoyAvatarRef.clearFiles()
      // 更改头像后直接提交修改

      const token = this.$store.state.token
      const backendUrl = `loverupdate/?token=${token}`
      const { data: res1 } = await this.$axios.put(backendUrl, {
        boyavatar: this.loverForm.boyavatar
      })
      if (res1.code !== 1000) {
        if ('detail' in res1) {
          this.$message.error(res1.detail)
        } else {
          this.$message.error('上传头像失败')
        }
      } else {
        this.getLoverDetail()
      }

      // this.postUserInfo()
    },
    // 女孩头像上传
    async handleGirlAvatarSuccess(res, file, filelist) {
      // 删除七牛云中的头像

      if (this.loverForm.girlavatar !== '') {
        console.log(this.loverForm.girlavatar)
        // this.deleteAvatar(this.userForm.avatar)
      }
      this.loverForm.girlavatar = res.url
      // 成功后清空组件上传文件列表
      this.$refs.uploadGirlAvatarRef.clearFiles()
      // 更改头像后直接提交修改

      const token = this.$store.state.token
      const backendUrl = `loverupdate/?token=${token}`
      const { data: res1 } = await this.$axios.put(backendUrl, {
        girlavatar: this.loverForm.girlavatar
      })
      if (res1.code !== 1000) {
        if ('detail' in res1) {
          this.$message.error(res1.detail)
        } else {
          this.$message.error('上传头像失败')
        }
      } else {
        this.getLoverDetail()
      }

      // this.postUserInfo()
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
    }
  },
  created() {
    this.getLoverDetail()
    this.getAvatarUploadToken()
  }
}
</script>
<style lang="less" scoped>
.el-header,
.el-main {
  margin: 0;
  padding: 0;
}
.el-select {
  width: 100%;
}
.el-container {
  padding: 30px;
  .el-header {
    display: flex;
    justify-content: center;
    .el-breadcrumb {
      flex: 1;
    }
  }
  .el-main {
    display: flex;
    flex-direction: column;
    .table-container {
      background: #fff;
      border-radius: 4px;
      border: 1px solid #ebeef5;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
      color: #303133;
      box-sizing: border-box;
      padding: 20px;
      flex: 1;
      margin-bottom: 5px;
      max-height: 90%;

      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      .el-table {
        overflow: auto;
        border: 1px solid #ebeef5;
        &::before {
          height: 0;
          // position: fixed;
        }
      }
    }
  }
  .modal-box {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 400;
    display: flex;
    align-items: center;
    justify-content: center;
    .update-lover-box {
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;
      min-height: 500px;
      width: 500px;

      .boyavatar-uploader,
      .girlavatar-uploader {
        display: flex;
        align-items: flex-end;
        margin-bottom: 12px;
        position: relative;
        .close-btn {
          position: absolute;
          top: 0;
          right: 0;
          &:hover {
            color: #007fff;
          }
        }
        .el-avatar {
          margin-right: 12px;
        }
      }
    }
  }
}
</style>
