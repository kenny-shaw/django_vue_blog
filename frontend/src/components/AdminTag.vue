<template>
  <el-container>
    <!-- 是否删除标签dialog -->
    <el-dialog
      title="提示"
      :visible.sync="deleteTagDialogVisible"
      width="30%"
      center
    >
      <span>是否删除标签？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteTagDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteTag">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 头部面包屑导航区域 -->
    <el-header height="30px">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/admin' }"
          >博主中心</el-breadcrumb-item
        >
        <el-breadcrumb-item><a>标签管理</a></el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <div class="search-add-box">
        <el-input
          class="search-input "
          placeholder="搜索标签"
          suffix-icon="icon iconfont iconicon-test12"
          clearable
          @clear="clearSearch"
          v-model="searchTagContent"
          @keyup.enter.native="searchTag"
        >
        </el-input>
        <el-button type="primary" size="small" @click="showModalBox"
          >添加用户</el-button
        >
      </div>
      <div class="table-pagination-container">
        <!-- 表格区域 -->
        <el-table :data="tagList" border stripe>
          <el-table-column type="index" label="#"> </el-table-column>
          <el-table-column prop="title" label="标签名称"></el-table-column>
          <el-table-column prop="avatar" label="标签图片">
            <template slot-scope="scope">
              <div class="avatar-uploader">
                <el-avatar
                  shape="square"
                  :size="60"
                  :src="scope.row.avatar"
                ></el-avatar>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="created" label="创建时间"> </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                @click="showModalBox(scope.row)"
                >编辑</el-button
              >
              <el-button
                size="mini"
                type="danger"
                @click="openDeleteTagDialog(scope.row.id)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页区域 -->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.pageNum"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="queryInfo.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div>
    </el-main>
    <div class="modal-box" v-if="isModalBoxVisible">
      <div class="add-or-update-tag-box">
        <div class="avatar-uploader">
          <el-avatar
            shape="square"
            :size="72"
            :src="tagForm.avatar"
            :key="tagForm.avatar"
            fit="cover"
          ></el-avatar>
          <el-upload
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
          <a class="el-icon-close close-btn" @click.prevent="closeModalBox"></a>
        </div>
        <el-form
          ref="tagFormRef"
          :model="tagForm"
          :rules="rules"
          label-width="0px"
        >
          <el-form-item prop="title">
            <el-input
              v-model="tagForm.title"
              placeholder="请输入标签名称~"
              prefix-icon="icon iconfont iconicon-test35"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="addTag"
            class="add-tag-button"
            v-if="isAddTagBtn"
            >新增</el-button
          >
          <el-button
            type="primary"
            @click="updateTag(curTagId)"
            class="add-tag-button"
            v-if="!isAddTagBtn"
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
      searchTagContent: '',
      tagList: [],
      qiniuData: {},
      tagForm: {
        title: '',
        avatar: ''
      },
      // modal层数是否可见
      isModalBoxVisible: false,
      // 是否为新增标签button
      isAddTagBtn: '',
      // 当前处理userid
      curTagId: '',
      // 博主上传图片token
      avatarUploadToken: '',
      // 控制删除用户提书框显示与隐藏
      deleteTagDialogVisible: false,
      queryInfo: {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      },
      // 所有用户数
      total: 0,
      rules: {
        title: [
          { required: true, message: '请输入标签名称', trigger: 'blur' },
          { max: 64, message: '长度不得超过 64 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async getTagList() {
      const size = this.queryInfo.pageSize
      const page = this.queryInfo.pageNum
      const token = this.$store.state.token
      let backendUrl = ''
      if (this.searchTagContent !== '') {
        console.log(size)

        backendUrl = `articletags/?token=${token}&text=${this.searchTagContent}&size=${size}&page=${page}`
      } else {
        backendUrl = `articletags/?token=${token}&size=${size}&page=${page}`
      }
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.total = res.total
        this.tagList = res.data
        this.tagList.forEach(tag => {
          tag.created = this.$moment(tag.created).format('YYYY-MM-DD')
        })
      } else {
        this.$message.error(res.error)
      }
    },
    searchTag() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getTagList()
    },
    clearSearch() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getTagList()
    },
    handleSizeChange(newSize) {
      this.queryInfo.pageSize = newSize
      this.getTagList()
    },
    handleCurrentChange(newPage) {
      this.queryInfo.pageNum = newPage
      this.getTagList()
    },
    // 隐藏modal层
    closeModalBox() {
      this.isModalBoxVisible = false
      this.tagForm = {
        title: '',
        avatar: ''
      }
      this.$refs.tagFormRef.resetFields()
    },
    showModalBox(tag) {
      this.isModalBoxVisible = true
      if ('title' in tag) {
        this.tagForm = Object.assign(this.tagForm, tag)
        this.curTagId = tag.id
        this.isAddTagBtn = false
      } else {
        this.isAddTagBtn = true
      }
    },
    async updateTag(tagId) {
      this.$refs.tagFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `articletag/${tagId}?token=${token}`
        const { data: res } = await this.$axios.put(backendUrl, this.tagForm)
        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('标签修改成功')
          this.closeModalBox()
          this.getTagList()
        } else {
          if (res.error.title) {
            return this.$message.error(res.error.title[0])
          }
          this.$message.error(res.error)
        }
      })
    },
    async addTag() {
      this.$refs.tagFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `articletag/?token=${token}`
        const { data: res } = await this.$axios.post(backendUrl, this.tagForm)
        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('新增标签成功')
          this.closeModalBox()
          this.getTagList()
        } else {
          if (res.error.title) {
            return this.$message.error(res.error.title[0])
          }
          this.$message.error(res.error)
        }
      })
    },
    handleAvatarExceed() {
      this.$message.error('请不要上传标签图片')
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
    // 头像上传
    async handleAvatarSuccess(res, file, filelist) {
      // 删除七牛云中的头像

      if (this.tagForm.avatar !== '') {
        // this.deleteAvatar(this.tagForm.avatar)
      }
      this.tagForm.avatar = res.url
      // 成功后清空组件上传文件列表
      this.$refs.uploadAvatarRef.clearFiles()
      // 更改头像后直接提交修改
      if (this.curTagId !== '') {
        const token = this.$store.state.token
        const backendUrl = `articletag/${this.curTagId}?token=${token}`
        const { data: res1 } = await this.$axios.put(backendUrl, {
          avatar: this.tagForm.avatar
        })
        if (res1.code !== 1000) {
          if ('detail' in res1) {
            this.$message.error(res.detail)
          } else {
            this.$message.error('上传标签图片失败')
          }
        } else {
          this.getTagList()
        }
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
    },
    openDeleteTagDialog(tagId) {
      this.curTagId = tagId
      this.deleteTagDialogVisible = true
    },
    async deleteTag() {
      const token = this.$store.state.token
      const backendUrl = `articletag/${this.curTagId}?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.$message.success('标签删除成功~')
        this.deleteTagDialogVisible = false
        this.getTagList()
      } else {
        this.$message.error(res.error)
      }
    }
  },
  created() {
    this.getTagList()
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
    .search-add-box {
      margin-bottom: 15px;
      .el-input {
        max-width: 240px;
        margin-right: 12px;
      }
    }
    .table-pagination-container {
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
    .add-or-update-tag-box {
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;
      // min-height: 500px;
      width: 500px;

      .avatar-uploader {
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
