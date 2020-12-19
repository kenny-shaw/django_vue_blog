<template>
  <el-container @click.native="avatarPanelVisible = false">
    <el-header height="46px">
      <!-- 文章标题部分 -->
      <input
        type="text"
        class="input-article-title"
        placeholder="请输入文章标题..."
        v-model="article.title"
        maxlength="128"
      />
      <!-- 文章栏目部分 -->
      <el-select v-model="article.column" placeholder="请选择栏目">
        <el-option
          v-for="column in columnList"
          :key="column.id"
          :label="column.title"
          :value="column.title"
        >
        </el-option>
      </el-select>
      <!-- 添加标签 -->
      <el-tag
        :key="tag"
        v-for="tag in article.tag"
        closable
        :disable-transitions="false"
        @close="handleTagClose(tag)"
      >
        {{ tag }}
      </el-tag>
      <el-input
        class="input-new-tag"
        v-if="inputTagVisible"
        v-model="inputTagValue"
        ref="saveTagInput"
        size="small"
        @keyup.enter.native="handleTagInputConfirm"
        @blur="handleTagInputConfirm"
      >
      </el-input>
      <el-button
        v-else
        class="button-new-tag"
        size="small"
        @click="showTagInput"
        >+ New Tag</el-button
      >
      <!-- 上传标题图部分 -->
      <div
        class="article-avatar-box"
        @click.stop="avatarPanelVisible = !avatarPanelVisible"
      >
        <a
          :class="[
            'toggle-icon-button',
            'icon',
            'iconfont',
            'iconicon-test32',
            { 'avatar-uploaded': article.avatar }
          ]"
        ></a>
        <div
          class="upload-avatar-panel"
          v-if="avatarPanelVisible"
          @click.stop="avatarPanelVisible = true"
        >
          <div class="panel-title">
            <a>添加封面大图</a>
            <i
              class="icon iconfont iconicon_delete_fill"
              v-if="article.avatar"
              @click="deleteAvatar()"
            ></i>
          </div>
          <!-- 标题图上传框 -->
          <el-upload
            class="avatar-uploader"
            action="http://up.qiniup.com"
            :show-file-list="false"
            :data="qiniuData"
            :on-remove="handleAvatarRemove"
            :before-upload="beforeAvatarUpload"
            :on-success="handleAvatarSuccess"
            :on-error="handleAvatarError"
            :limit="1"
            :on-exceed="handleAvatarExceed"
            ref="uploadAvatarRef"
          >
            <el-image
              v-if="article.avatar"
              :src="article.avatar"
              class="avatar"
              fit="cover"
            ></el-image>
            <!-- <img v-if="avatar" :src="avatar" class="avatar" /> -->
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </div>
      </div>
      <!-- 发布文章按钮 -->
      <el-button type="primary" class="post-article-button" @click="postArticle"
        >发布文章</el-button
      >
      <!-- 用户头像 -->
      <el-avatar
        :size="35"
        :src="user.avatar"
        @click.native="toHome"
      ></el-avatar>
    </el-header>
    <el-main>
      <mavon-editor
        :toolbars="toolbars"
        @imgAdd="handleEditorImageAdd"
        @imgDel="handleEditorImageDel"
        v-model="article.content"
        @change="change"
        ref="editorRef"
      >
      </mavon-editor>
    </el-main>
  </el-container>
</template>
<script>
export default {
  props: ['id'],
  data() {
    return {
      // mavonEditor自定义工具栏
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        mark: true, // 标记
        superscript: true, // 上角标
        subscript: true, // 下角标
        quote: true, // 引用
        ol: true, // 有序列表
        ul: true, // 无序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        code: false, // code
        table: true, // 表格
        fullscreen: true, // 全屏编辑
        readmodel: true, // 沉浸式阅读
        htmlcode: true, // 展示html源码
        help: true, // 帮助
        /* 1.3.5 */
        undo: true, // 上一步
        redo: true, // 下一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        /* 1.4.2 */
        navigation: true, // 导航目录
        /* 2.1.8 */
        alignleft: true, // 左对齐
        aligncenter: true, // 居中
        alignright: true, // 右对齐
        /* 2.2.1 */
        subfield: true, // 单双栏模式
        preview: true // 预览
      },
      // 文章
      article: {
        // 输入的原生md内容
        content: '',
        // 原生md转换为的html内容，后端同时将其转为text
        content_html: '',
        // 用于在后台将html转换为text，用于搜索
        content_text: '',
        // 输入的文章标题
        title: '',
        // 选中的栏目column
        column: '',
        // 标签列表
        tag: [],
        // 文章标题图url
        avatar: ''
      },
      // 标签输入框是否可见
      inputTagVisible: false,
      // 标签输入框绑定的值
      inputTagValue: '',
      // 用户信息
      user: {},
      // 获取到的栏目列表
      columnList: [],
      // 用户上传图片的token
      userImageToken: '',
      // 控制上传标题图的面板显示
      avatarPanelVisible: false,
      // 标题图上传七牛云所需的data
      qiniuData: {
        token: ''
      },
      //  图片上传token
      imageUploadToken: ''
    }
  },
  methods: {
    // 监听markdown变化
    change(value, render) {
      console.log(this)

      console.log(render)
    },
    // 上传图片接口pos 表示第几个图片
    async handleEditorImageAdd(pos, $file) {
      const formdata = new FormData()
      formdata.append('file', $file)
      formdata.append('token', this.imageUploadToken)
      // formdata.append('key', $file.name)
      console.log(formdata.get('token'))

      const { data: res } = await this.$axios({
        url: 'http://up.qiniup.com',
        method: 'post',
        data: formdata,
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      if (res.code === 1000) {
        const url = res.url
        this.$refs.editorRef.$img2Url(pos, url)
      } else {
        this.$message.error('图片上传失败')
      }
    },
    // 文章图片删除函数
    async handleEditorImageDel(pos, $file) {
      // 从url截取key值
      const url = pos[0]
      const splitArray = url.split('/')
      const key = splitArray[splitArray.length - 1]
      console.log(pos[0])
      // const key = pos[1].name
      const { data: res } = await this.$axios.delete(
        `deleteimagefromqiniu/${key}`
      )
      if (res.code !== 1000) {
        this.$message.error(res.error)
      }
    },
    async getColumnList() {
      const { data: res } = await this.$axios.get('articlecolumns/?size=100')
      if (res.code === 1000) {
        this.columnList = res.data
        // console.log(this.columnList)
      } else if (res.code === 1001) {
        this.columnList = []
      } else {
        this.$message.error(res.error)
      }
    },
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
    async getImageUploadtoken() {
      const token = this.$store.state.token
      const backendUrl = `userimagetoken/?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.imageUploadToken = res.data
      } else {
        this.$message.error(res.error)
      }
    },
    // 关闭标签的相应事件
    handleTagClose(tag) {
      this.article.tag.splice(this.article.tag.indexOf(tag), 1)
    },
    // 点击新建标签相应事件
    showTagInput() {
      this.inputTagVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    // 回车或者确认新增tag
    handleTagInputConfirm() {
      // 最多3个标签
      if (this.article.tag.length >= 3) {
        this.inputTagVisible = false
        this.inputTagValue = ''
        return this.$message.error('最多添加三个标签哦~')
      }
      // 获取输入的值
      let inputTagValue = this.inputTagValue
      if (inputTagValue) {
        // 去除前后空格
        inputTagValue = inputTagValue.trim()
        // 确保没有重复标签
        const sameValueInTagList = this.article.tag.find(
          tag => tag === inputTagValue
        )
        if (sameValueInTagList) {
          return this.$message.error('无法添加相同的标签哦~')
        }
        this.article.tag.push(inputTagValue)
      }
      this.inputTagVisible = false
      this.inputTagValue = ''
    },
    // 标题图上传前控制上传类型、大小
    // 将文件名赋给key值，并获取上传token
    async beforeAvatarUpload(file) {
      // this.qiniuData.key = file.name
      this.qiniuData.token = this.imageUploadToken
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2
      console.log(this)
      if (!isJPG && !isPNG) {
        this.$message.error('图片只能是 JPG/PNG 格式!')
        return false
      }
      if (!isLt2M) {
        this.$message.error('图片大小不能超过 2MB!')
        return false
      }
    },
    // 文章标题图上传
    async handleAvatarSuccess(res, file, filelist) {
      this.article.avatar = res.url

      // 成功后清空组件上传文件列表
      this.$refs.uploadAvatarRef.clearFiles()
      // 直接更新文章
      // this.postArticle()
      // 如果是更新文章，则直接进行更新
      if (this.id) {
        const token = this.$store.state.token
        const backendUrl = `article/${this.id}?token=${token}`
        const { data: res1 } = await this.$axios.put(backendUrl, this.article)
        if (res1.code !== 1000) {
          return this.$message.error(res.error)
        }
      }
    },
    handleAvatarError() {
      this.$message.error('标题图上传失败')
    },
    handleAvatarRemove() {},
    handleAvatarExceed() {
      this.$message.error('请先删除已上传标题图')
    },
    // 删除七牛云中的图片，以及本地filelist，清空avatar
    async deleteAvatar() {
      // 获得已上传的key值
      // 从avatar截取key值
      // const splitArray = this.article.avatar.split('/')
      // const key = splitArray[splitArray.length - 1]
      // const { data: res } = await this.$axios.delete(
      //   `deleteimagefromqiniu/${key}`
      // )
      // if (res.code !== 1000) {
      //   return this.$message.error(res.error)
      // }
      // 清空组件上传文件列表
      this.$refs.uploadAvatarRef.clearFiles()
      // 重置标题图url
      this.article.avatar = ''
      // 如果是更新文章，则直接进行更新
      // if (this.id) {
      //   const token = this.$store.state.token
      //   const backendUrl = `article/${this.id}?token=${token}`
      //   const { data: res1 } = await this.$axios.put(backendUrl, this.article)
      //   if (res1.code !== 1000) {
      //     return this.$message.error(res.error)
      //   }
      // }
    },
    async getArticleDetail() {
      console.log(typeof this.id)
      const token = this.$store.state.token
      // const articleId = this.$route.query.articleId
      const backendUrl = `articles/${this.id}?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        const article = res.data
        if (article.author !== this.$store.state.username) {
          this.$message.error('您无权修改他人文章~')
          return this.$router.push({ path: '/' })
        } else {
          // eslint-disable-next-line camelcase
          const { content, content_html, title, column, tag, avatar } = article
          this.article = { content, content_html, title, column, tag, avatar }
          console.log(this.article)
        }
      } else {
        return this.$message.error(res.error)
      }
    },
    async postArticle() {
      this.article.content_html = this.$refs.editorRef.d_render
      console.log(this.article)

      const token = this.$store.state.token
      // const articleId = this.$route.query.articleId
      let backendUrl = ''
      let res = {}
      // 根据是否有articleId来判断进行post或是put
      if (this.id) {
        backendUrl = `article/${this.id}?token=${token}`
        const { data: res1 } = await this.$axios.put(backendUrl, this.article)
        res = res1
      } else {
        backendUrl = `article/?token=${token}`
        const { data: res2 } = await this.$axios.post(backendUrl, this.article)
        res = res2
      }
      if (res.code === 1000) {
        this.$message.success('文章发布成功')
        this.$router.push({ path: '/' })
      } else {
        return this.$message.error(res.error)
      }
    },
    // 前往主頁路由
    toHome() {
      console.log('1')
      this.$router.push({ path: '/' })
    }
  },
  created() {
    this.getColumnList()
    this.getUserInfo()
    // 获取图片上传token
    this.getImageUploadtoken()
    if (this.id) {
      this.getArticleDetail()
    }
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      if (this.id) {
        this.getArticleDetail()
      } else {
        // 重置article
        this.article = {
          // 输入的原生md内容
          content: '',
          // 原生md转换为html内容，由于后端最后要转为text，因此起名为content_html
          content_html: '',
          // 输入的文章标题
          title: '',
          // 选中的栏目column
          column: '',
          // 标签列表
          tag: [],
          // 文章标题图url
          avatar: ''
        }
      }
    }
  }
}
</script>
<style lang="less" scoped>
.avatar-uploaded {
  color: #3399ff !important;
}
.el-container {
  height: 100%;
  width: 100%;
  .el-header {
    margin: 0;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    .input-article-title {
      flex: 1;
      border: none;
      outline: none;
      height: 100%;
      font-size: 20px;
      font-weight: 600;
      color: #000;
    }
    .el-select {
      margin: 0 15px;
    }
    .el-tag {
      margin-left: 10px;
    }
    .button-new-tag {
      margin: 0 15px;
      height: 32px;
      line-height: 30px;
      padding-top: 0;
      padding-bottom: 0;
    }
    .input-new-tag {
      width: 90px;
      margin-left: 15px;
      vertical-align: bottom;
    }
    .article-avatar-box {
      margin: 0 15px;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      .toggle-icon-button {
        color: #ccd1d8;
        font-size: 28px;
        &:hover {
          color: #3399ff;
        }
      }
      .upload-avatar-panel {
        // display: none;
        position: absolute;
        margin-top: 16px;
        padding: 24px;
        top: 100%;
        left: 50%;
        transform: translate(-50%);
        font-size: 14px;
        white-space: nowrap;
        color: #909090;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 2px;
        z-index: 10000;
        &::before {
          content: '';
          position: absolute;
          left: 50%;
          transform: rotate(45deg);
          box-sizing: border-box;
          width: 12px;
          height: 12px;
          background: #fff;
          border: 1px solid #ddd;
          border-right: none;
          border-bottom: none;
          margin-left: -6px;
          top: -7px;
        }
        .panel-title {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 14px;
          a,
          .icon {
            font-size: 18px;
            font-weight: 700;
            color: rgba(119, 127, 141, 0.8);
            cursor: pointer;
          }
          .icon {
            &:hover {
              color: #409eff;
            }
          }
        }
        .avatar-uploader {
          border: 1px dashed #d9d9d9;
          border-radius: 6px;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          &:hover {
            border-color: #409eff;
          }
          .avatar-uploader-icon {
            font-size: 28px;
            color: #8c939d;
            width: 178px;
            height: 178px;
            line-height: 178px;
            text-align: center;
          }
          .avatar {
            width: 178px;
            height: 178px;
          }
        }
      }
    }
    //发布文章按钮
    .post-article-button {
      margin: 0 15px;
    }
    // 用户头像
    .el-avatar {
      cursor: pointer;
      // margin-right: 15px;
    }
  }
  .el-main {
    margin: 0;
    padding: 0;
    .markdown-body {
      width: 100%;
      height: 100%;
    }
  }
}
</style>
