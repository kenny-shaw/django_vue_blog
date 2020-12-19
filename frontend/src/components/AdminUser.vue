<template>
  <el-container>
    <!-- 是否删除用户dialog -->
    <el-dialog
      title="提示"
      :visible.sync="deleteUserDialogVisible"
      width="30%"
      center
    >
      <span>是否删除用户？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteUserDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteUser">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 头部面包屑导航区域 -->
    <el-header height="30px">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/admin' }"
          >博主中心</el-breadcrumb-item
        >
        <el-breadcrumb-item><a>用户管理</a></el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <div class="search-add-box">
        <el-input
          class="search-input "
          placeholder="搜索用户"
          suffix-icon="icon iconfont iconicon-test12"
          clearable
          @clear="clearSearch"
          v-model="searchUserContent"
          @keyup.enter.native="searchUser"
        >
        </el-input>
        <el-button type="primary" size="small" @click="showModalBox"
          >添加用户</el-button
        >
      </div>
      <div class="table-pagination-container">
        <!-- 表格区域 -->
        <el-table :data="userList" border stripe>
          <el-table-column type="index" label="#"> </el-table-column>
          <el-table-column prop="username" label="用户名"> </el-table-column>
          <el-table-column prop="email" label="邮箱"> </el-table-column>
          <el-table-column prop="gender" label="性别">
            <template slot-scope="scope">
              <p v-if="scope.row.gender === 1">保密</p>
              <p v-if="scope.row.gender === 2">男</p>
              <p v-if="scope.row.gender === 3">女</p>
            </template>
          </el-table-column>
          <el-table-column prop="avatar" label="头像">
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
          <el-table-column prop="role" label="权限">
            <template slot-scope="scope">
              <p v-if="scope.row.role === 1">普通用户</p>
              <p v-if="scope.row.role === 2">管理员</p>
              <p v-if="scope.row.role === 3">博主</p>
            </template>
          </el-table-column>
          <el-table-column prop="brief" label="简介"> </el-table-column>
          <el-table-column prop="job" label="职业"> </el-table-column>
          <el-table-column prop="company" label="公司"> </el-table-column>
          <el-table-column prop="date_joined" label="加入时间">
          </el-table-column>
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
                @click="openDeleteUserDialog(scope.row.id)"
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
      <div class="add-or-update-user-box">
        <div class="avatar-uploader">
          <el-avatar
            shape="square"
            :size="72"
            :src="userForm.avatar"
            :key="userForm.avatar"
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
          ref="userFormRef"
          :model="userForm"
          :rules="rules"
          label-width="0px"
        >
          <el-form-item prop="username">
            <el-input
              v-model="userForm.username"
              placeholder="请输入用户名~"
              prefix-icon="icon iconfont iconicon-test35"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password" v-if="isAddUserBtn">
            <el-input
              v-model="userForm.password"
              placeholder="请输入密码~"
              show-password
              prefix-icon="icon iconfont iconicon-test26"
            ></el-input>
          </el-form-item>
          <el-form-item prop="updatepassword" v-if="!isAddUserBtn">
            <el-input
              v-model="userForm.updatepassword"
              placeholder="如不修改密码，无需填写~"
              show-password
              prefix-icon="icon iconfont iconicon-test26"
            ></el-input>
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="userForm.email"
              placeholder="请输入邮箱~"
              prefix-icon="icon iconfont iconicon-test33"
            ></el-input>
          </el-form-item>
          <el-form-item prop="gender">
            <el-select v-model="userForm.gender" placeholder="请选择">
              <el-option label="保密" :value="1"> </el-option>
              <el-option label="男" :value="2"> </el-option>
              <el-option label="女" :value="3"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="role">
            <el-select v-model="userForm.role" placeholder="请选择">
              <el-option label="普通用户" :value="1"> </el-option>
              <el-option label="管理员" :value="2"> </el-option>
              <el-option label="博主" :value="3"> </el-option>
            </el-select>
          </el-form-item>

          <el-form-item prop="brief">
            <el-input
              v-model="userForm.brief"
              placeholder="请输入简介~"
              prefix-icon="icon iconfont iconicon_namecard"
            ></el-input>
          </el-form-item>
          <el-form-item prop="job">
            <el-input
              v-model="userForm.job"
              placeholder="请输入职位~"
              prefix-icon="icon iconfont iconicon_boss"
            ></el-input>
          </el-form-item>
          <el-form-item prop="company">
            <el-input
              v-model="userForm.company"
              placeholder="请输入公司~"
              prefix-icon="icon iconfont iconicon_homepage"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="addUser"
            class="add-user-button"
            v-if="isAddUserBtn"
            >新增</el-button
          >
          <el-button
            type="primary"
            @click="updateUser(curUserId)"
            class="add-user-button"
            v-if="!isAddUserBtn"
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
      searchUserContent: '',
      userList: [],
      qiniuData: {},
      userForm: {
        username: '',
        password: '',
        // 供更新密码规则校验使用
        updatepassword: '',
        avatar: '',
        email: undefined,
        gender: undefined,
        role: undefined,
        brief: '',
        job: '',
        company: ''
      },
      // modal层数是否可见
      isModalBoxVisible: false,
      // 是否为新增用户button
      isAddUserBtn: '',
      // 当前处理userid
      curUserId: '',
      // 博主上传图片token
      avatarUploadToken: '',
      // 控制删除用户提书框显示与隐藏
      deleteUserDialogVisible: false,
      queryInfo: {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      },
      // 所有用户数
      total: 0,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        updatepassword: [
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          // { required: true, message: '请输入邮箱', trigger: 'blur' },

          {
            pattern: /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
            message: '请输入正确的邮箱',
            trigger: 'blur'
          }
        ],
        brief: [{ max: 256, message: '长度要小于256个字符', trigger: 'blur' }],
        job: [{ max: 128, message: '长度要小于128个字符', trigger: 'blur' }],
        company: [{ max: 128, message: '长度要小于128个字符', trigger: 'blur' }]
      }
    }
  },
  methods: {
    async getUserList() {
      const size = this.queryInfo.pageSize
      const page = this.queryInfo.pageNum
      const token = this.$store.state.token
      let backendUrl = ''
      if (this.searchUserContent !== '') {
        backendUrl = `accountadmin/?token=${token}&text=${this.searchUserContent}&size=${size}&page=${page}`
      } else {
        backendUrl = `accountadmin/?token=${token}&size=${size}&page=${page}`
      }
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.total = res.total
        this.userList = res.data
        this.userList.forEach(user => {
          user.date_joined = this.$moment(user.date_joined).format('YYYY-MM-DD')
        })
      } else {
        this.$message.error(res.error)
      }
    },
    searchUser() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getUserList()
    },
    clearSearch() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getUserList()
    },
    handleSizeChange(newSize) {
      this.queryInfo.pageSize = newSize
      this.getUserList()
    },
    handleCurrentChange(newPage) {
      this.queryInfo.pageNum = newPage
      this.getUserList()
    },
    // 隐藏modal层
    closeModalBox() {
      this.isModalBoxVisible = false
      this.userForm = {
        username: '',
        password: '',
        updatepassword: '',
        avatar: '',
        email: undefined,
        gender: undefined,
        role: undefined,
        brief: '',
        job: '',
        company: ''
      }
      this.$refs.userFormRef.resetFields()
    },
    showModalBox(user) {
      this.isModalBoxVisible = true
      if ('username' in user) {
        this.userForm = Object.assign(this.userForm, user)
        // 不将加密后的密码填充到form中
        this.userForm.password = undefined
        console.log(this.userForm)

        this.curUserId = user.id
        this.isAddUserBtn = false
      } else {
        this.isAddUserBtn = true
      }
    },
    async updateUser(userId) {
      // 如果密码为空字符串，将密码重置为undefined，这样提交的时候不会更改密码
      if (
        'updatepassword' in this.userForm &&
        typeof this.userForm.updatepassword === 'string' &&
        this.userForm.updatepassword.trim() === ''
      ) {
        this.userForm.updatepassword = undefined
      }
      this.userForm.password = this.userForm.updatepassword
      // 防止邮箱重复,如果是空字符串，则重置为undefined
      if (
        'email' in this.userForm &&
        typeof this.userForm.email === 'string' &&
        this.userForm.email.trim() === ''
      ) {
        this.userForm.email = undefined
      }
      this.$refs.userFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `accountadmin/${userId}?token=${token}`
        const { data: res } = await this.$axios.put(backendUrl, this.userForm)
        console.log(res)

        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('用户修改成功')
          this.closeModalBox()
          this.getUserList()
        } else {
          if (res.error.username) {
            return this.$message.error(res.error.username[0])
          } else if (res.error.email) {
            return this.$message.error(res.error.email[0])
          } else if (res.error.password) {
            return this.$message.error(res.error.password[0])
          }
          this.$message.error(res.error)
        }
      })
    },
    async addUser() {
      this.$refs.userFormRef.validate(async valid => {
        if (!valid) return
        // 防止邮箱重复,如果是空字符串，则重置为undefined
        if (
          'email' in this.userForm &&
          typeof this.userForm.email === 'string' &&
          this.userForm.email.trim() === ''
        ) {
          this.userForm.email = undefined
        }
        const token = this.$store.state.token
        const backendUrl = `accountadmin/?token=${token}`
        const { data: res } = await this.$axios.post(backendUrl, this.userForm)
        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('新增用户成功')
          this.closeModalBox()
          this.getUserList()
        } else {
          if (res.error.username) {
            return this.$message.error(res.error.username[0])
          } else if (res.error.email) {
            return this.$message.error(res.error.email[0])
          } else if (res.error.password) {
            return this.$message.error(res.error.password[0])
          }

          this.$message.error(res.error)
        }
      })
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
    // 头像上传
    async handleAvatarSuccess(res, file, filelist) {
      // 删除七牛云中的头像
      console.log(this.userForm.avatar)

      if (this.userForm.avatar !== '') {
        console.log(this.userForm.avatar)
        // this.deleteAvatar(this.userForm.avatar)
      }
      this.userForm.avatar = res.url
      // 成功后清空组件上传文件列表
      this.$refs.uploadAvatarRef.clearFiles()
      // 更改头像后直接提交修改
      if (this.curUserId !== '') {
        const token = this.$store.state.token
        const backendUrl = `accountadmin/${this.curUserId}?token=${token}`
        const { data: res } = await this.$axios.put(backendUrl, {
          avatar: this.userForm.avatar
        })
        if (res.code !== 1000) {
          if ('detail' in res) {
            this.$message.error(res.detail)
          } else {
            this.$message.error('上传头像失败')
          }
        } else {
          this.getUserList()
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
    openDeleteUserDialog(userId) {
      this.curUserId = userId
      this.deleteUserDialogVisible = true
    },
    async deleteUser() {
      const token = this.$store.state.token
      const backendUrl = `accountadmin/${this.curUserId}?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.$message.success('用户删除成功~')
        this.deleteUserDialogVisible = false
        this.getUserList()
      } else {
        this.$message.error(res.error)
      }
    }
  },
  created() {
    this.getUserList()
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
    .add-or-update-user-box {
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;
      min-height: 500px;
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
