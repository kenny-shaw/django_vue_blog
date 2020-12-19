<template>
  <!-- 总居中区域 -->
  <el-container>
    <!-- 文章区域、包括文章内容、评论等 -->
    <div class="article-container">
      <!-- 头部区域，放置作者、标题、标题图 -->
      <div class="article-info-header">
        <!-- 作者相关信息、头像、名字、文章修改时间、阅读量 -->
        <div class="author-info-container">
          <!-- 作者头像 -->
          <el-avatar
            :size="40"
            :src="author.avatar"
            :key="author.avatar"
            @click.native="toHome"
          ></el-avatar>
          <div class="author-info-box">
            <!-- 作者名 -->
            <a class="author-name">{{ article.author }}</a>
            <div class="article-meta-box">
              <span class="article-created">{{ article.updated }}</span>
              <span class="article-views">阅读 {{ article.total_views }}</span>
              <span
                class="dot"
                v-if="article.author_id === this.$store.state.userid"
                >·</span
              >
              <a
                class="article-edit"
                v-if="article.author_id === this.$store.state.userid"
                @click.prevent="toEditor"
                >编辑</a
              >
            </div>
          </div>
        </div>
        <!-- 文章标题图 -->

        <el-image
          :src="article.avatar"
          fit="cover"
          class="article-avatar"
          v-if="article.avatar"
        ></el-image>

        <!-- 文章标题 -->
        <h1 class="article-title">{{ article.title }}</h1>
      </div>

      <!-- 文章主体区域，用于放置文章内容 -->
      <!-- article-content-container  -->
      <div
        class="article-content-container markdown-body"
        v-html="article.content_html"
      >
        <!-- <mavon-editor
          class="editor-preview"
          v-model="article.content"
          :subfield="false"
          :boxShadow="false"
          defaultOpen="preview"
          :toolbarsFlag="false"
          :navigation="false"
          previewBackground="#fff"
          ref="editorRef"
        >
        </mavon-editor> -->
      </div>
      <!-- 文章评论区域 -->
      <div class="article-comments-container">
        <!-- 当前用户的评论框 -->
        <div class="my-reply" v-clickoutside="hideMyReplyBtn">
          <!-- 当前用户头像 -->
          <el-avatar
            :size="32"
            :src="user.avatar"
            :key="user.avatar"
            class="hidden-xs-only"
          ></el-avatar>
          <!-- 评论表单区域 -->
          <div class="comment-form-box">
            <!-- input -->
            <el-input
              v-model="inputMyComment"
              @focus="showMyReplyBtn"
              placeholder="输入评论..."
            ></el-input>
            <!-- 评论按钮及后续富文本区域 -->
            <div class="comment-action-box" v-if="myReplyBtnShow">
              <a
                class="icon iconfont iconsmile"
                @click="isShowEmojiPanel = !isShowEmojiPanel"
              ></a>
              <el-button type="primary" size="mini" @click="postComment()"
                >评论</el-button
              >
              <emoji-panel
                @emojiClick="appendEmoji"
                v-if="isShowEmojiPanel"
              ></emoji-panel>
            </div>
          </div>
        </div>
        <!-- 评论列表区域 -->
        <div class="comments-list-container no-margin-left">
          <!-- 根评论区域 -->
          <div
            class="parent-comment-box"
            v-for="comment in commentList"
            :key="comment.id"
          >
            <!-- 评论者头像 -->
            <el-avatar
              :size="32"
              :src="comment.user_avatar"
              :key="comment.user_avatar"
            ></el-avatar>
            <!-- 评论内容区域 -->
            <div class="parent-comment-content-box">
              <!-- 评论者信息 -->
              <div class="meta-box">
                <a class="comment-username">{{ comment.user }}</a>
                <a class="user-job-company"
                  >{{ comment.user_job }} @ {{ comment.user_company }}</a
                >
              </div>
              <!-- 评论内容 -->
              <div class="comment-content-box" v-html="comment.content"></div>
              <!-- 发表时间、点赞、回复 -->
              <div class="comment-time-action-box">
                <!-- 发表时间 -->
                <div class="comment-reply-time">{{ comment.created }}</div>
                <!-- 评论点赞回复删除 -->
                <div class="comment-action-box">
                  <div
                    :class="[
                      'like-action',
                      { 'is-liked ': comment.likedbycuruser }
                    ]"
                    @click="likeOrCancelLikeComment(comment.id)"
                  >
                    <a class="icon iconfont icondianzan1"></a>
                    <a class="like-counts">{{ comment.comment_likes }}</a>
                  </div>
                  <div
                    class="reply-action hideReplyBoxClass"
                    @click="activateOrDeactivateReplyBox(comment.id)"
                  >
                    <a class="icon iconfont iconpinglun1"></a>
                    <a class="reply-title">回复</a>
                  </div>
                  <div
                    class="delete-action"
                    v-if="
                      comment.user === user.username ||
                        user.role === '博主' ||
                        article.username === user.username
                    "
                    @click="deleteComment(comment.id)"
                  >
                    <a class="icon iconfont iconicon_delete_fill"></a>
                  </div>
                </div>
              </div>
              <div
                class="parent-comment-reply-box hideReplyBoxClass"
                v-if="activeReplyBoxId === comment.id"
                v-clickoutside="hideReplyBox"
              >
                <!-- input -->
                <el-input
                  v-model="inputSubComment"
                  placeholder="输入评论..."
                  @focus="closeEmojiPanel"
                >
                </el-input>
                <!-- 评论按钮及后续富文本区域 -->
                <div class="parent-comment-action-box">
                  <a
                    class="icon iconfont iconsmile"
                    @click="isShowEmojiPanel = !isShowEmojiPanel"
                  ></a>
                  <el-button
                    type="primary"
                    size="mini"
                    @click="postComment(comment.id)"
                    >评论</el-button
                  >
                  <emoji-panel
                    @emojiClick="appendEmoji"
                    v-if="isShowEmojiPanel"
                  ></emoji-panel>
                </div>
              </div>
              <div
                class="sub-comments-list-container"
                v-if="comment.children.length > 0"
              >
                <div
                  class="sub-comment-box"
                  v-for="subComment in comment.children"
                  :key="subComment.id"
                >
                  <!-- 子评论者头像 -->
                  <el-avatar
                    :size="32"
                    :src="subComment.user_avatar"
                    :key="subComment.user_avatar"
                  ></el-avatar>
                  <div class="sub-comment-content-box">
                    <!-- 评论者信息 -->
                    <div class="meta-box">
                      <a class="comment-username">{{ subComment.user }}</a>
                      <a class="user-job-company"
                        >{{ subComment.user_job }} @
                        {{ subComment.user_company }}</a
                      >
                    </div>
                    <!-- 评论内容 -->
                    <div class="comment-content-box">
                      <span>回复&nbsp;</span>
                      <a class="reply-to">{{ subComment.reply_to }}</a>
                      :&nbsp;
                      <span v-html="subComment.content"></span>
                    </div>
                    <!-- 发表时间、点赞、回复 -->
                    <div class="comment-time-action-box">
                      <!-- 发表时间 -->
                      <div class="comment-reply-time">
                        {{ subComment.created }}
                      </div>
                      <!-- 评论点赞回复删除 -->
                      <div class="comment-action-box">
                        <div
                          :class="[
                            'like-action',
                            { 'is-liked ': subComment.likedbycuruser }
                          ]"
                          @click="likeOrCancelLikeComment(subComment.id)"
                        >
                          <a class="icon iconfont icondianzan1"></a>
                          <a class="like-counts">{{
                            subComment.comment_likes
                          }}</a>
                        </div>
                        <div
                          class="reply-action hideReplyBoxClass"
                          @click="activateOrDeactivateReplyBox(subComment.id)"
                        >
                          <a class="icon iconfont iconpinglun1"></a>
                          <a class="reply-title">回复</a>
                        </div>
                        <div
                          class="delete-action"
                          v-if="
                            subComment.user === user.username ||
                              user.role === '博主' ||
                              article.username === user.username
                          "
                          @click="deleteComment(subComment.id)"
                        >
                          <a class="icon iconfont iconicon_delete_fill"></a>
                        </div>
                      </div>
                    </div>
                    <!-- 回复子评论 -->
                    <div
                      class="sub-comment-reply-box hideReplyBoxClass"
                      v-if="activeReplyBoxId === subComment.id"
                      v-clickoutside="hideReplyBox"
                    >
                      <!-- input -->
                      <el-input
                        v-model="inputSubComment"
                        placeholder="输入评论..."
                        @focus="closeEmojiPanel"
                      ></el-input>
                      <!-- 评论按钮及后续富文本区域 -->
                      <div class="sub-comment-action-box">
                        <a
                          class="icon iconfont iconsmile"
                          @click="isShowEmojiPanel = !isShowEmojiPanel"
                        ></a>
                        <el-button
                          type="primary"
                          size="mini"
                          @click="postComment(subComment.id)"
                          >评论</el-button
                        >
                        <emoji-panel
                          @emojiClick="appendEmoji"
                          v-if="isShowEmojiPanel"
                        ></emoji-panel>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 侧边栏区域，放置作者等相关信息 -->
    <div class="article-sidebar hidden-md-and-down">
      <div class="author-about-box">
        <div class="author-about-title-box">
          <h1 class="title">关于作者</h1>
        </div>
        <div class="author-about-content-box">
          <div class="author-detail-box">
            <!-- 作者头像 -->
            <el-avatar
              :size="40"
              :src="author.avatar"
              :key="author.avatar"
              @click.native="toHome"
            ></el-avatar>
            <div class="author-info-box">
              <!-- 作者名 -->
              <a class="author-name">{{ author.username }}</a>
              <a class="author-job-company"
                >{{ author.job }} @ {{ author.company }}</a
              >
            </div>
          </div>
          <div class="author-total-articles">
            <i class="icon iconfont iconchuangzuo1"></i>
            <a href="">共发布{{ author.article_counts }}篇文章</a>
          </div>
          <div class="author-total-likes">
            <i class="icon iconfont iconaixin1"></i>
            <a href="">共获得{{ author.obtained_total_likes }}点赞</a>
          </div>
          <div class="author-total-views">
            <i class="icon iconfont iconyanjing1"></i>
            <a href="">共获得{{ author.obtained_total_views }}浏览量</a>
          </div>
        </div>
      </div>
    </div>
    <!-- 放置点赞评论收藏悬挂框 -->
    <div class="article-suspended-panel">
      <div
        :class="['like-btn', { 'is-liked ': article.likedbycuruser }]"
        @click="LikeOrCancelLikeArticle"
      >
        <a class="icon iconfont icondianzan1"></a>
        <div class="counts">{{ article.article_likes }}</div>
      </div>
      <div class="comment-btn">
        <a class="icon iconfont iconpinglun1"></a>
        <div class="counts">{{ article.article_comments }}</div>
      </div>
      <div class="favorite-btn">
        <a
          :class="[
            'icon',
            'iconfont',
            'iconshoucang1',
            { 'is-collected': this.hasBeenCollectedByCurUser }
          ]"
          class="icon iconfont iconshoucang1"
          @click.prevent="showFavoritePopup"
        ></a>
        <!-- 弹出的收藏框、用于收藏文章 -->
        <div
          class="favorite-popup-container"
          v-if="favoritePopupShow"
          v-clickoutside="hideFavoritePopupAndInputBtn"
        >
          <!-- 弹出框的标题 -->
          <div class="favorite-popup-title">
            添加到收藏夹
          </div>
          <ul class="favorite-list">
            <li
              class="favorite-item"
              v-for="favorite in favoriteList"
              :key="favorite.id"
              @click="
                collectArticleOrCancel(
                  favorite.id,
                  favorite.favoritedbycurfavorite
                )
              "
            >
              <div class="favorite-item-brief">
                <div class="favorite-title">{{ favorite.title }}</div>
                <div class="favorite-article-counts">
                  {{ favorite.article_counts }}
                </div>
              </div>
              <div
                class="favorited-icon"
                v-if="favorite.favoritedbycurfavorite"
              >
                <i class="icon iconfont iconicon-test45"></i>
              </div>
            </li>
          </ul>
          <div class="favorite-action-box">
            <a
              class="new-favorite-btn"
              v-if="!newFavoriteInputShow"
              @click.prevent="showFavoriteInputBtn"
              >新建文件夹</a
            >
            <div class="new-favorite-input-btn" v-if="newFavoriteInputShow">
              <input
                type="text"
                v-if="true"
                class="new-favorite-input"
                v-model="newFavoriteTitle"
              />
              <el-button type="primary" size="mini" @click="createNewFavorite"
                >新建</el-button
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-container>
</template>
<script>
// const clickoutside = {
//   // 初始化指令
//   bind(el, binding, vnode) {
//     function documentHandler(e) {
//       // 这里判断点击的元素是否是本身，是本身，则返回
//       if (el.contains(e.target)) {
//         return false
//       }
//       // 判断指令中是否绑定了函数
//       if (binding.expression) {
//         // 如果绑定了函数 则调用那个函数，此处binding.value就是handleClose方法
//         binding.value(e)
//       }
//     }
//     // 给当前元素绑定个私有变量，方便在unbind中可以解除事件监听
//     el.vueClickOutside = documentHandler
//     document.addEventListener('click', documentHandler)
//   },
//   update() {},
//   unbind(el, binding) {
//     // 解除事件监听
//     document.removeEventListener('click', el.vueClickOutside)
//     delete el.vueClickOutside
//   }
// }
// import Clickoutside from '../plugins/clickoutside'
import Clickoutside from 'element-ui/src/utils/clickoutside'
import EmojiPanel from './EmojiPanel.vue'

export default {
  props: ['id'],
  components: {
    EmojiPanel
  },
  data() {
    return {
      // 文章
      article: {},
      // 作者
      author: {},
      user: {},
      // 输入我的评论内容
      inputMyComment: '',
      // 输入的回复他人的评论内容
      inputSubComment: '',
      // 控制文章一级回复评论按钮的显示隐藏
      myReplyBtnShow: false,
      // 评论列表
      commentList: [],
      // 激活的回复框id，为comment的id
      activeReplyBoxId: '',
      // 获取到的收藏夹列表
      favoriteList: [],
      // 控制新增收藏夹输入框和button隐藏和显示
      newFavoriteInputShow: false,
      favoritePopupShow: false,
      hasBeenCollectedByCurUser: false,
      // 新增收藏夹title
      newFavoriteTitle: '',
      // 是否显示表情框
      isShowEmojiPanel: false
    }
  },
  directives: { Clickoutside },
  methods: {
    closeEmojiPanel() {
      this.isShowEmojiPanel = false
    },
    appendEmoji(text) {
      // 如果是当前用户评论当前文章
      if (this.myReplyBtnShow === true) {
        this.inputMyComment = `${this.inputMyComment}[emoji:${text}]`
      } else {
        console.log('231')

        this.inputSubComment = `${this.inputSubComment}[emoji:${text}]`
      }
    },
    // 转换将[emoji:smile]转换成相应的表情字符
    emoji(word) {
      const type = word.substring(7, word.length - 1)
      return `<span class="comment-content-emoji emoji-${type} " ></span>`
    },
    showEmojiPanel() {
      this.isShowEmojiPanel = true
    },
    // 获取文章详情
    async getArticle() {
      const token = this.$store.state.token
      const backendUrl = `articles/${this.id}?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)

      if (res.code === 1000) {
        this.article = Object.assign({}, res.data)
        console.log(this.article)
        this.article.updated = this.$moment(this.article.updated).format(
          'YYYY-MM-DD'
        )
        await this.getAuthorInfo()
      } else {
        this.$message.error(res.error)
      }
    },
    // 点赞文章、取消点赞
    async LikeOrCancelLikeArticle() {
      // 获取当前token
      const token = this.$store.state.token
      if (!token) {
        return this.$message.warning('请登录后进行点赞~')
      }
      // 要请求的后端URL
      const backendUrl = `likearticle/${this.id}?token=${token}`
      // 如果未点赞，则进行点赞，
      if (this.article.likedbycuruser === 0) {
        const { data: res } = await this.$axios.post(backendUrl)
        if (res.code === 1000) {
          this.article.likedbycuruser = 1
          this.article.article_likes += 1
        } else {
          this.$message.error(res.error)
        }
      } else {
        console.log('取消点赞')
        // 如果已点赞，则取消点赞
        const { data: res } = await this.$axios.delete(backendUrl)
        if (res.code === 1000) {
          this.article.likedbycuruser = 0
          this.article.article_likes -= 1
        } else {
          this.$message.error(res.error)
        }
      }
    },
    async getAuthorInfo() {
      const { data: res } = await this.$axios.get(
        `usergeneralinfo/${this.article.author_id}`
      )
      if (res.code === 1000) {
        this.author = Object.assign({}, res.data)
        this.author.date_joined = this.$moment(res.data).format('YYYY-MM-DD')
      } else {
        return this.$message.error(res.error)
      }
    },
    // 获取当前用户信息
    async getUserInfo() {
      const token = this.$store.state.token
      const backendUrl = `userinfo/?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.user = res.data
      } else {
        // this.$message.error(res.error)
      }
    },
    // 展示myReply用户评论按钮
    showMyReplyBtn() {
      this.activeReplyBoxId = ''
      this.myReplyBtnShow = true
      // 关掉表情面板
      this.isShowEmojiPanel = false
    },
    // 隐藏myReply用户评论按钮
    hideMyReplyBtn() {
      this.myReplyBtnShow = false
      // // 同时关闭表情框
      // this.isShowEmojiPanel = false
    },
    // 获取评论列表
    async getCommentList() {
      const token = this.$store.state.token
      const backendUrl = `articlecomments/${this.id}?token=${token}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.commentList = res.data
        this.commentList.forEach(comment => {
          // 将时间转换为formnow
          comment.created = this.$moment(comment.created).fromNow()
          comment.content = comment.content.replace(
            /\[emoji:.*?\]/g,
            this.emoji
          )
          // 子评论时间转换
          if (comment.children.length > 0) {
            comment.children.forEach(subComment => {
              // 将时间转换为formnow
              subComment.created = this.$moment(subComment.created).fromNow()
              subComment.content = subComment.content.replace(
                /\[emoji:.*?\]/g,
                this.emoji
              )
            })
          }
        })
      } else if (res.code === 1001) {
        this.commentList = []
      } else {
        this.$message.error(res.error)
      }
    },
    activateOrDeactivateReplyBox(commentId) {
      console.log(this.activeReplyBoxId)
      console.log(commentId)

      // 将表情框重置为隐藏
      this.isShowEmojiPanel = false
      if (this.activeReplyBoxId === commentId) {
        this.activeReplyBoxId = ''
      } else {
        this.inputSubComment = ''
        this.activeReplyBoxId = commentId
      }
      console.log(this.activeReplyBoxId)
    },
    hideReplyBox() {
      this.activeReplyBoxId = ''
    },
    async postComment(commentId = 0) {
      const token = this.$store.state.token
      if (!token) {
        return this.$router.push('/login')
      }
      let backendUrl = `articlecomment/${this.id}`
      let res = {}
      if (commentId === 0) {
        if (this.inputMyComment.trim() === '') {
          return this.$message.error('评论不能为空')
        }
        backendUrl = `${backendUrl}/?token=${token}`
        const { data: resTmp } = await this.$axios.post(backendUrl, {
          content: this.inputMyComment
        })
        res = resTmp
      } else {
        if (this.inputSubComment.trim() === '') {
          return this.$message.error('评论不能为空')
        }
        backendUrl = `${backendUrl}/${commentId}?token=${token}`
        const { data: resTmp } = await this.$axios.post(backendUrl, {
          content: this.inputSubComment
        })
        res = resTmp
      }
      if (res.code === 1000) {
        // 重新获取列表
        this.getCommentList()
        // 清空内容
        this.inputMyComment = ''
        this.inputSubComment = ''
        // 关闭回复框
        this.activeReplyBoxId = ''
        this.myReplyBtnShow = false
        // 关闭表情框
        this.isShowEmojiPanel = false
      } else {
        this.$message.error(res.error)
      }
    },
    async deleteComment(commentId) {
      const token = this.$store.state.token
      const backendUrl = `articlecomment/${commentId}?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.getCommentList()
      } else {
        this.$message.error(res.error)
      }
    },
    // 点赞评论、取消点赞
    async likeOrCancelLikeComment(commentId) {
      // 获取当前token
      const token = this.$store.state.token
      if (!token) {
        return this.$message.warning('请登录后进行点赞~')
      }
      const commentBackendUrl = `comments/${commentId}?token=${token}`
      const backendUrl = `likecomment/${commentId}?token=${token}`
      // 获取当前评论
      const { data: commentRes } = await this.$axios.get(commentBackendUrl)
      if (commentRes.code === 1000) {
        const comment = commentRes.data
        if (comment.likedbycuruser === 0) {
          const { data: res } = await this.$axios.post(backendUrl)
          if (res.code === 1000) {
            this.getCommentList()
          } else {
            this.$message.error(res.error)
          }
        } else {
          // 取消点赞
          const { data: res } = await this.$axios.delete(backendUrl)
          if (res.code === 1000) {
            this.getCommentList()
          } else {
            this.$message.error(res.error)
          }
        }
      } else {
        this.$message.error(commentRes.error)
      }
    },
    async getFavoriteList() {
      const userId = this.$store.state.userid
      const backendUrl = `userfavorites/${userId}/${this.id}?size=100&page=1`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.favoriteList = res.data
        this.hasBeenCollectedByCurUser = this.favoriteList.some(favorite => {
          return favorite.favoritedbycurfavorite === 1
        })
      } else if (res.code === 1001) {
        this.favoriteList = []
      } else {
        // this.$message.error(res.error)
      }
    },
    async getUserFavoriteList(size = this.size, page = 1) {
      const backendUrl = `userfavorites/${this.userid}?size=${size}&page=${page}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        // 将用户收藏夹列表存储于userFavoriteList
        // 如果userFavoriteList为空，则将res.data赋给userFavoriteList，
        // 或者size为6，也将res.data赋给userFavoriteList，解决loadmore与get重复进行的bug
        if (this.userFavoriteList.length === 0 || size === 6) {
          this.userFavoriteList = res.data
          this.userFavoriteList.forEach(favorite => {
            // 将时间转换为formnow
            favorite.createdorupdated = this.$moment(
              favorite.createdorupdated
            ).fromNow()
          })
        } else {
          const concatData = res.data
          // 将文章id映射和是否被当前用户点赞存储于isLiked，
          // 以及存储id映射和当前文章点赞数量存储于likeCounts，用于前端无刷新更新点赞状态和点赞数量
          concatData.forEach(favorite => {
            // 将时间转换为formnow
            favorite.createdorupdated = this.$moment(
              favorite.createdorupdated
            ).fromNow()
          })
          this.userFavoriteList = this.userFavoriteList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.userFavoriteList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    // 显示新增收藏夹的输入框和按钮
    showFavoriteInputBtn() {
      this.newFavoriteInputShow = true
    },
    // 显示收藏夹弹出框
    showFavoritePopup() {
      this.favoritePopupShow = true
    },
    // 隐藏收藏夹弹出框以及新增收藏家的输入框和按钮
    hideFavoritePopupAndInputBtn() {
      this.favoritePopupShow = false
      this.newFavoriteInputShow = false
    },
    // 收藏文章或取消收藏
    async collectArticleOrCancel(favoriteId, favoritedByCurFavorite) {
      const token = this.$store.state.token
      const backendUrl = `favoritearticle/${favoriteId}/${this.id}?token=${token}`
      let res = {}
      console.log(favoritedByCurFavorite)
      if (favoritedByCurFavorite === 0) {
        const { data: res1 } = await this.$axios.post(backendUrl)
        res = res1
      } else {
        const { data: res2 } = await this.$axios.delete(backendUrl)
        res = res2
      }
      console.log(res)

      if (res.code === 1000) {
        this.getFavoriteList()
      } else {
        this.$message.error(res.error)
      }
    },
    // 新建收藏夹
    async createNewFavorite() {
      if (this.newFavoriteTitle === '') {
        return this.$message.error('请输入收藏夹名称~')
      }
      const token = this.$store.state.token
      if (!token) {
        return this.$message.warning('请登录后进行新建收藏夹~')
      }
      const backendUrl = `favorite/?token=${token}`
      const { data: res } = await this.$axios.post(backendUrl, {
        title: this.newFavoriteTitle
      })
      if (res.code === 1000) {
        this.getFavoriteList()
        this.newFavoriteTitle = ''
      } else {
        this.$message.error(res.error)
      }
    },
    // 前往编辑路由
    toEditor() {
      this.$router.push({ path: `/editor/${this.id}` })
    }
  },
  created() {
    this.getArticle()
    if (this.$store.state.token) {
      this.getUserInfo()
    }
    this.getCommentList()
    this.getFavoriteList()
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      this.getArticle()
      this.getCommentList()
      this.getFavoriteList()
    }
  }
}
</script>
<style lang="less" scoped>
// 已点赞
.is-liked {
  a {
    color: #ee5253;
  }
}
.is-collected {
  color: #ffc347;
}
.el-header,
.el-main {
  margin: 0;
  padding: 0;
}
.el-container {
  min-height: 100%;
  max-width: 960px;
  padding-top: 20px;
  width: 100%;
  margin: auto;
  // 文章主体区域
  .article-container {
    background: #fff;
    max-width: 700px;
    width: 100%;
    box-sizing: border-box;
    padding: 24px 24px 0 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    // 头部作者、标题图、标题区域
    .article-info-header {
      .author-info-container {
        display: flex;
        .el-avatar {
          margin-right: 12px;
        }
        .author-info-box {
          flex: 1;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          margin-bottom: 24px;
          .author-name {
            font-size: 16px;
            font-weight: 700;
            color: #333;
          }
          .article-meta-box {
            .article-created {
              font-size: 13px;
              color: #909090;
              letter-spacing: 1px;
            }
            .article-views {
              margin-left: 6px;
              font-size: 13px;
              color: #909090;
            }
            .dot {
              font-size: 16px;
              color: #909090;
              margin: 0 6px;
            }
            .article-edit {
              color: #1264b6;
              cursor: pointer;
              font-size: 13px;
              &:hover {
                text-decoration: underline;
              }
            }
          }
        }
      }

      .article-avatar {
        width: 100%;
        height: auto;
        max-height: 400px;
      }

      .article-title {
        margin: 20px 0;
        font-size: 30px;
        font-weight: 700;
        line-height: 1.5;
        color: #333;
      }
    }
    // 文章主体部分
    .article-content-container {
      flex: 1;
      // background: pink;
    }
    // 文章评论部分
    .article-comments-container {
      margin-top: 10px;
      border-top: 1px solid #ebebeb;
      padding: 10px 25px;
      .my-reply {
        background-color: #fafbfc;

        padding: 16px 12px;
        display: flex;
        border-radius: 3px;
        .el-avatar {
          margin-right: 12px;
        }
        .comment-form-box {
          flex: 1;
          .comment-action-box {
            margin-top: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            .icon {
              &:hover {
                color: #007fff;
              }
            }
          }
        }
      }

      .comments-list-container {
        margin-left: 50px;
        .parent-comment-box {
          margin-top: 10px;
          display: flex;
          .el-avatar {
            margin-right: 10px;
          }
          .parent-comment-content-box {
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f1f1;
            flex: 1;
            .meta-box {
              .comment-username {
                font-size: 16px;
                font-weight: 700;
                color: #333;
                margin-right: 5px;
              }
              .user-job-company {
                text-decoration: none;
                cursor: pointer;
                color: #8a9aa9;
                font-size: 14px;
              }
            }
            .comment-content-box {
              font-size: 13px;
              margin-top: 7px;
              color: #505050;
              overflow: hidden;
              display: flex;
              align-items: center;
            }
            .comment-time-action-box {
              margin-top: 7px;
              display: flex;
              justify-content: space-between;
              align-items: center;
              .comment-reply-time {
                font-size: 13px;
                color: #8a9aa9;
              }
              .comment-action-box {
                display: flex;
                justify-content: flex-end;
                align-items: center;
                font-size: 12px;
                .like-action {
                  margin-right: 12px;
                  &:hover {
                    a {
                      color: #ee5253;
                    }
                  }
                }

                .reply-action {
                  .reply-title {
                    margin-left: 4px;
                  }
                }
                .delete-action {
                  margin-left: 12px;
                  &:hover {
                    a {
                      color: #007fff;
                    }
                  }
                }
              }
            }
            .parent-comment-reply-box {
              margin-top: 13px;
              padding: 12px;
              background-color: #fafbfc;
              .parent-comment-action-box {
                margin-top: 8px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: relative;
                .icon {
                  &:hover {
                    color: #007fff;
                  }
                }
              }
            }
            .sub-comments-list-container {
              margin: 14px 0;
              background-color: #fafbfc;
              border-radius: 3px;
              .sub-comment-box {
                padding: 10px 0 0 12px;
                display: flex;
                .el-avatar {
                  margin-right: 10px;
                }
                .sub-comment-content-box {
                  flex: 1;
                  padding-bottom: 10px;
                  border-bottom: 1px solid #f1f1f1;
                  .meta-box {
                    .comment-username {
                      font-size: 16px;
                      font-weight: 700;
                      color: #333;
                      margin-right: 5px;
                    }
                    .user-job-company {
                      text-decoration: none;
                      cursor: pointer;
                      color: #8a9aa9;
                      font-size: 14px;
                    }
                  }
                  .comment-content-box {
                    font-size: 13px;
                    margin-top: 7px;
                    color: #505050;
                    overflow: hidden;
                    span {
                      display: flex;
                      align-items: center;
                    }
                    .reply-to {
                      text-decoration: none;
                      cursor: pointer;
                      color: #406599;
                    }
                  }
                  .comment-time-action-box {
                    margin-top: 7px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    .comment-reply-time {
                      font-size: 13px;
                      color: #8a9aa9;
                    }
                    .comment-action-box {
                      display: flex;
                      justify-content: flex-end;
                      align-items: center;
                      font-size: 12px;
                      .like-action {
                        margin-right: 12px;
                        &:hover {
                          a {
                            color: #ee5253;
                          }
                        }
                      }
                      .reply-action {
                        .reply-title {
                          margin-left: 4px;
                        }
                      }
                      .delete-action {
                        margin-left: 12px;
                        &:hover {
                          a {
                            color: #007fff;
                          }
                        }
                      }
                    }
                  }
                }
                .sub-comment-reply-box {
                  margin-top: 13px;
                  padding: 12px;
                  background-color: #fff;
                  .sub-comment-action-box {
                    margin-top: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    position: relative;
                    .icon {
                      &:hover {
                        color: #007fff;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  // 侧边栏区域
  .article-sidebar {
    // background: #fff;
    padding-left: 20px;
    background-clip: content-box;
    width: 240px;
    // height: 100%;
    // background: #f4f5f5;
    display: flex;
    flex-direction: column;
    .author-about-box {
      // margin-top: 24px;
      width: 240px;
      position: absolute;
      background: #ffffff;
      border-radius: 2px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      .author-about-title-box {
        padding: 15px;
        box-sizing: border-box;
        border-bottom: 1px solid rgba(230, 230, 231, 0.5);
        h1.title {
          color: #31445b;
          margin: 0;
          padding: 0;
          font-size: 16px;
          font-weight: 600;
        }
      }
      .author-about-content-box {
        padding: 15px;
        .author-detail-box {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          .el-avatar {
            margin-right: 12px;
          }
          .author-info-box {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            .author-name {
              font-size: 16px;
              font-weight: 700;
              color: #333;
            }
            .author-job-company {
              font-size: 14px;
            }
          }
        }
        .author-total-articles,
        .author-total-likes,
        .author-total-views {
          display: flex;
          align-items: center;
          .icon {
            color: #ee5253;
            margin-right: 10px;
          }
          a {
            color: #31445b;
            font-size: 15px;
          }
        }
        .author-total-likes {
          margin: 10px 0;
        }
        .author-total-articles {
          .icon {
            color: #1b9cfc;
          }
        }
        .author-total-views {
          .icon {
            color: #ff9f1a;
          }
        }
      }
    }
  }
  // 左侧增加的面板，用于点赞评论收藏等
  .article-suspended-panel {
    position: fixed;
    margin-left: -80px;
    // top: 192px;
    top: 50%;
    transform: translate(0, -100%);

    .like-btn,
    .comment-btn,
    .favorite-btn {
      position: relative;
      background: #fff;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.04);
      margin-bottom: 10px;
      cursor: pointer;
      .iconfont {
        font-size: 20px;
      }
      .counts {
        position: absolute;
        top: 0;
        left: 75%;
        font-size: 12px;
        background-color: #b2bac2;
        color: #fff;
        padding: 1px 5px;
        border-radius: 8px;
      }
    }
    .favorite-btn {
      position: relative;
      z-index: 2000;
      .favorite-popup-container {
        position: absolute;
        left: 100%;
        top: 0;
        width: 200px;
        background: #fff;
        margin-left: 12px;
        width: 336px;
        border: 1px solid #eceeef;
        border-radius: 3px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
        z-index: 100000000;
        .favorite-popup-title {
          padding: 10px;
          font-size: 14px;
          font-weight: 700;
          display: flex;
          justify-content: center;
          align-items: center;
          color: #000;
        }
        .favorite-list {
          list-style: none;
          border: 1px solid #eceeef;
          border-right: none;
          border-left: none;
          .favorite-item {
            min-height: 35px;
            box-sizing: border-box;
            padding: 6px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            .favorite-item-brief {
              display: flex;
              align-items: center;
              .favorite-title {
                margin: 0 12px;
                font-size: 13px;
                overflow: hidden;
                text-overflow: ellipsis;
                color: #000;
                display: flex;
                align-items: center;
              }
              .favorite-article-counts {
                // padding: 1px 8px;
                // width: 15px;
                // height: 15px;
                padding: 1px 5px;
                border-radius: 8px;
                line-height: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #b9bec2;
                background-color: #f2f2f2;
                border-radius: 50%;
              }
            }
            .favorited-icon {
              color: #83c73a;
            }
          }
        }
        .favorite-action-box {
          padding: 0 12px;
          height: 40px;
          display: flex;
          align-items: center;

          .new-favorite-btn {
            &:hover {
              color: #007fff;
            }
          }
          .new-favorite-input-btn {
            display: flex;
            align-items: center;
            height: 100%;
            width: 100%;
            .new-favorite-input {
              height: 100%;
              flex: 1;
              outline: none;
              border: none;
            }
          }
        }
      }
    }
    // 已点赞样式
    .is-liked {
      a {
        color: #ee5253;
      }
      div {
        background-color: #ee5253 !important;
      }
    }
  }
}

/* 小屏幕时媒体查询评论左margin消失 */
@media screen and (max-width: 768px) {
  .no-margin-left {
    margin: 0 !important ;
  }
}
@import '../assets/css/emoji.css'; // 导入精灵图样式
</style>
