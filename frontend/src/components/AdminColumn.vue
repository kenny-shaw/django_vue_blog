<template>
  <el-container>
    <!-- 是否删除栏目dialog -->
    <el-dialog
      title="提示"
      :visible.sync="deleteColumnDialogVisible"
      width="30%"
      center
    >
      <span>是否删除栏目？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteColumnDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteColumn">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 头部面包屑导航区域 -->
    <el-header height="30px">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/admin' }"
          >博主中心</el-breadcrumb-item
        >
        <el-breadcrumb-item><a>栏目管理</a></el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>
    <el-main>
      <div class="search-add-box">
        <el-input
          class="search-input "
          placeholder="搜索栏目"
          suffix-icon="icon iconfont iconicon-test12"
          clearable
          @clear="clearSearch"
          v-model="searchColumnContent"
          @keyup.enter.native="searchColumn"
        >
        </el-input>
        <el-button type="primary" size="small" @click="showModalBox"
          >添加栏目</el-button
        >
      </div>
      <div class="table-pagination-container">
        <!-- 表格区域 -->
        <el-table :data="columnList" border stripe>
          <el-table-column type="index" label="#"> </el-table-column>
          <el-table-column prop="title" label="栏目名称"> </el-table-column>
          <el-table-column prop="brief" label="栏目简介"> </el-table-column>
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
                @click="openDeleteColumnDialog(scope.row.id)"
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
      <div class="add-or-update-column-box">
        <a class="el-icon-close close-btn" @click.prevent="closeModalBox"></a>
        <el-form
          ref="columnFormRef"
          :model="columnForm"
          :rules="rules"
          label-width="0px"
        >
          <el-form-item prop="title">
            <el-input
              v-model="columnForm.title"
              placeholder="请输入栏目名称~"
              prefix-icon="icon iconfont iconhuati"
            ></el-input>
          </el-form-item>
          <el-form-item prop="brief">
            <el-input
              v-model="columnForm.brief"
              placeholder="请输入栏目简介~"
              prefix-icon="icon iconfont iconyingpingmoban"
            ></el-input>
          </el-form-item>
          <el-button
            type="primary"
            @click="addColumn"
            class="add-column-button"
            v-if="isAddColumnBtn"
            >新增</el-button
          >
          <el-button
            type="primary"
            @click="updateColumn(curColumnId)"
            class="add-column-button"
            v-if="!isAddColumnBtn"
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
      searchColumnContent: '',
      columnList: [],
      columnForm: {
        title: '',
        brief: ''
      },
      // modal层数是否可见
      isModalBoxVisible: false,
      // 是否为新增用户button
      isAddColumnBtn: '',
      // 当前处理userid
      curColumnId: '',
      // 控制删除用户提书框显示与隐藏
      deleteColumnDialogVisible: false,
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
          { required: true, message: '请输入栏目名称', trigger: 'blur' },
          { max: 64, message: '长度不得超过 64 个字符', trigger: 'blur' }
        ],
        brief: [
          { max: 256, message: '长度不得超过 256 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async getColumnList() {
      const size = this.queryInfo.pageSize
      const page = this.queryInfo.pageNum
      const token = this.$store.state.token
      let backendUrl = ''
      if (this.searchUserContent !== '') {
        backendUrl = `articlecolumns/?token=${token}&text=${this.searchColumnContent}&size=${size}&page=${page}`
      } else {
        backendUrl = `articlecolumns/?token=${token}&size=${size}&page=${page}`
      }
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.total = res.total
        this.columnList = res.data
        this.columnList.forEach(column => {
          column.created = this.$moment(column.created).format('YYYY-MM-DD')
        })
      } else {
        this.$message.error(res.error)
      }
    },
    searchColumn() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getColumnList()
    },
    clearSearch() {
      this.queryInfo = {
        // 当前页数
        pageNum: 1,
        // 当前每页显示多少条数据
        pageSize: 5
      }
      this.getColumnList()
    },
    handleSizeChange(newSize) {
      this.queryInfo.pageSize = newSize
      this.getColumnList()
    },
    handleCurrentChange(newPage) {
      this.queryInfo.pageNum = newPage
      this.getColumnList()
    },
    // 隐藏modal层
    closeModalBox() {
      this.isModalBoxVisible = false
      this.columnForm = {
        title: '',
        brief: ''
      }
      this.$refs.columnFormRef.resetFields()
    },
    showModalBox(column) {
      this.isModalBoxVisible = true
      if ('title' in column) {
        this.columnForm = Object.assign(this.columnForm, column)
        this.curColumnId = column.id
        this.isAddColumnBtn = false
      } else {
        this.isAddColumnBtn = true
      }
    },
    async updateColumn(columnId) {
      this.$refs.columnFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `articlecolumn/${columnId}?token=${token}`
        const { data: res } = await this.$axios.put(backendUrl, this.columnForm)
        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('栏目修改成功')
          this.closeModalBox()
          this.getColumnList()
        } else {
          if (res.error.title) {
            return this.$message.error(res.error.title[0])
          }
          this.$message.error(res.error)
        }
      })
    },
    async addColumn() {
      this.$refs.columnFormRef.validate(async valid => {
        if (!valid) return
        const token = this.$store.state.token
        const backendUrl = `articlecolumn/?token=${token}`
        const { data: res } = await this.$axios.post(
          backendUrl,
          this.columnForm
        )
        if ('detail' in res) {
          this.$message.error(res.detail)
        } else if (res.code === 1000) {
          this.$message.success('新增栏目成功')
          this.closeModalBox()
          this.getColumnList()
        } else {
          if (res.error.title) {
            return this.$message.error(res.error.title[0])
          }
          this.$message.error(res.error)
        }
      })
    },
    openDeleteColumnDialog(columnId) {
      this.curColumnId = columnId
      this.deleteColumnDialogVisible = true
    },
    async deleteColumn() {
      const token = this.$store.state.token
      const backendUrl = `articlecolumn/${this.curColumnId}?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.$message.success('栏目删除成功~')
        this.deleteColumnDialogVisible = false
        this.getColumnList()
      } else {
        this.$message.error(res.error)
      }
    }
  },
  created() {
    this.getColumnList()
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
    .add-or-update-column-box {
      background: #f4f5f5;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 1%;
      box-shadow: 1px 1px 1px #fff;
      // min-height: 500px;
      width: 500px;
      position: relative;
      .close-btn {
        position: absolute;
        top: 3px;
        right: 3px;
        &:hover {
          color: #007fff;
        }
      }
      .el-form {
        margin-top: 10px;
      }
    }
  }
}
</style>
