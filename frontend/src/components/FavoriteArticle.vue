<template>
  <!-- 收藏夹总区域 -->
  <el-container class="favorite-articles-list-container">
    <!-- 收藏夹头部区域、放置标题简介等 -->
    <el-header height="150px" class="favorite-articles-list-header">
      <h1 class="favorite-title">{{ favorite.title }}</h1>
      <h1 class="favorite-brief">{{ favorite.brief }}</h1>
      <ul class="favorite-meta">
        <li>
          <a href="">{{ favorite.user }}</a>
        </li>
        <li>
          <a href="">{{ favorite.createdorupdated }}</a>
        </li>
        <li>
          <a href="">{{ favorite.article_counts }}篇文章</a>
        </li>
      </ul>
    </el-header>
    <!-- 询问是否删除收藏夹dialog区域 -->
    <el-dialog
      title="提示"
      :visible.sync="favoriteDeleteDialogVisible"
      width="30%"
      center
    >
      <span>是否确认删除该收藏夹？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="favoriteDeleteDialogVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="deleteFavorite(id, favorite.user_id)"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <!-- 主体区域 -->
    <el-main class="favorite-articles-list-main">
      <!-- 主体居中区域 -->
      <el-container class="favorite-articles-list-main-middle">
        <!-- 头部区域，放置删除返回等 -->
        <el-header class="favorite-action-box" height="30px">
          <div
            class="favorite-return-box"
            @click="toUserMoreFavorite(favorite.user_id)"
          >
            <a href="#" class="icon iconfont iconicon-test66"></a>
            <a href="#">返回 {{ favorite.user }} 更多收藏</a>
          </div>
          <div
            class="favorite-delete-box"
            @click="favoriteDeleteDialogVisible = true"
          >
            <a href="#">删除</a>
            <a href="#" class="icon iconfont iconicon_delete_fill"></a>
          </div>
        </el-header>
        <!-- 文章列表区域 -->
        <el-main
          class="favorite-articles-list-box"
          v-infinite-scroll="loadMoreFavoriteArticle"
          infinite-scroll-disabled="disabled"
        >
          <!-- 文章区域，用于v-for -->
          <div
            class="favorite-article-box"
            v-for="article in favoriteArticleList"
            :key="article.id"
          >
            <div class="article-info-box">
              <!-- 存放作者、时间、栏目标签等信息 -->
              <ul class="article-meta-list">
                <li class="article-username">
                  <a href="#">{{ article.author }}</a>
                </li>
                <li class="article-created">
                  <a href="#">{{ article.created }}</a>
                </li>
                <li class="article-column">
                  <a href="#">{{ article.column }}</a>
                </li>
              </ul>
              <div class="article-tag-box">
                <el-tag
                  size="mini"
                  class="article-tag"
                  v-for="(tag, index) in article.tag"
                  @click="toTagDetail(tag)"
                  :key="index"
                  >{{ tag }}</el-tag
                >
              </div>
              <!-- 文章标题 -->
              <a href="#" class="article-title">{{ article.title }}</a>
              <!-- 文章动作列表，包括点赞、评论等等 -->
              <ul class="article-action-list">
                <!-- 点赞 -->
                <li
                  :class="['like-box', { 'is-liked ': article.likedbycuruser }]"
                  @click="LikeOrCancelLikeArticle(article.id)"
                >
                  <a
                    href="#"
                    class="
                  icon
                  iconfont
                  icondianzan1
                  like-icon
                "
                  ></a>
                  <a class="like-count ">{{ article.article_likes }}</a>
                </li>
                <!-- 评论 -->
                <li class="comment-box">
                  <a
                    href="#"
                    class="
                  icon
                  iconfont
                  iconpinglun1
                  comment-icon
                "
                  ></a>
                  <a class="comment-count ">{{ article.article_comments }}</a>
                </li>
              </ul>
            </div>
            <!-- 文章标题图 -->
            <div
              class="article-avatar-box hidden-xxs-only "
              v-if="article.avatar"
            >
              <el-avatar
                shape="square"
                :size="60"
                :src="article.avatar"
              ></el-avatar>
            </div>
          </div>
          <div class="load-more-info-box">
            <p v-if="loading">加载中...</p>
            <p v-if="noMore">没有更多了</p>
          </div>
        </el-main>
      </el-container>
    </el-main>
  </el-container>
</template>
<script>
export default {
  props: ['id'],
  data() {
    return {
      // 存放收藏夹的详细信息
      favorite: {},
      // isNewest: true,
      // 获取到的收藏夹文章列表
      favoriteArticleList: [],
      // 当前是否在加载文章状态
      loading: false,
      // 是否为没有更多文章状态
      noMore: false,
      // 首屏加载的文章数量
      size: 6,
      // 加载更多文章时，每次加载的数量
      loadMoreSize: 2,
      loadMorePage: 4,
      // 控制提示是否删除收藏夹的dialog显示与隐藏
      favoriteDeleteDialogVisible: false
    }
  },
  computed: {
    // 当前是否繁忙状态，true则不执行loadMoreUserLikeArticle
    disabled() {
      return this.loading || this.noMore
    }
  },
  methods: {
    // 获取收藏夹文章列表
    async getFavoriteArticleList(size = this.size, page = 1) {
      // 获取当前token
      const token = this.$store.state.token
      // 要请求的后端URL
      let backendUrl = `favoritearticles/${this.id}?token=${token}`
      backendUrl = `${backendUrl}&size=${size}&page=${page}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        // 将文章数据存储于favoriteArticleList
        // 如果favoriteArticleList为空，则将res.data赋给favoriteArticleList，
        // 或者size为6，也将res.data赋给favoriteArticleList，解决loadmore与get重复进行的bug
        if (this.favoriteArticleList.length === 0 || size === 6) {
          this.favoriteArticleList = res.data
          this.favoriteArticleList.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
        } else {
          const concatData = res.data

          concatData.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
          this.favoriteArticleList = this.favoriteArticleList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.favoriteArticleList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    // 加载用户的更多文章
    loadMoreFavoriteArticle() {
      console.log('loadmore...')
      this.loading = true
      // 首次加载时，会进行loadmore，判断userLikeArticleList是否为空
      // 如果为空进行首次加载，加载6条
      if (this.favoriteArticleList.length === 0) {
        console.log('获取6条')
        this.getFavoriteArticleList()
      } else {
        this.getFavoriteArticleList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    async getFavoriteDetail() {
      const backendUrl = `favoritedetail/${this.id}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.favorite = res.data
        this.favorite.createdorupdated = this.$moment(
          this.favorite.createdorupdated
        ).fromNow()
      } else {
        this.$message.error(res.error)
      }
    },
    // 返回用户收藏夹列表
    toUserMoreFavorite(userId) {
      this.$router.push({ path: `/user/${userId}/favorites` })
    },
    // 删除收藏夹
    async deleteFavorite(favoriteId, userId) {
      const token = this.$store.state.token
      const backendUrl = `favorite/${favoriteId}?token=${token}`
      const { data: res } = await this.$axios.delete(backendUrl)
      if (res.code === 1000) {
        this.$message.success('删除收藏夹成功')
        this.$router.push({ path: `/user/${userId}/favorites` })
      } else {
        this.$message.error(res.error)
      }
    },
    // 点赞文章、取消点赞
    async LikeOrCancelLikeArticle(articleId) {
      // 获取当前文章
      const article = this.favoriteArticleList.find(
        article => article.id === articleId
      )
      // 获取当前token
      const token = this.$store.state.token
      if (!token) {
        return this.$message.warning('请登录后进行点赞~')
      }
      // 要请求的后端URL
      const backendUrl = `likearticle/${articleId}?token=${token}`
      // 如果未点赞，则进行点赞，
      if (article.likedbycuruser === 0) {
        const { data: res } = await this.$axios.post(backendUrl)
        if (res.code === 1000) {
          article.likedbycuruser = 1
          article.article_likes += 1
        } else {
          this.$message.error(res.error)
        }
      } else {
        console.log('取消点赞')
        // 如果已点赞，则取消点赞
        const { data: res } = await this.$axios.delete(backendUrl)
        if (res.code === 1000) {
          article.likedbycuruser = 0
          article.article_likes -= 1
        } else {
          this.$message.error(res.error)
        }
      }
    },
    // 前往标签文章列表页
    toTagDetail(tagName) {
      this.$router.push({ path: `/tag/${tagName}` })
    }
  },
  created() {
    this.getFavoriteDetail()
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空文章列表
      this.favoriteArticleList = []
      // 加载更多文章首个页数配置重置为6
      this.loadMorePage = 4

      // 是否在加载文章状态重置为false
      this.loading = false
      // 是否为没有更多文章状态重置为false
      this.noMore = false
      // 路由变化，重新获取文章列表
      this.getFavoriteDetail()
      this.getFavoriteArticleList()
    }
  }
}
</script>
<style lang="less" scoped>
.el-main,
.el-header {
  margin: 0;
  padding: 0;
}
.favorite-articles-list-container {
  height: 100%;
  width: 100%;
  .favorite-articles-list-header {
    margin: 0;
    padding: 0;
    background: #f8f9fa;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .favorite-title {
      font-family: PingFangSC-Semibold, PingFang SC;
      font-size: 24px;
      font-weight: 600;
      color: #666;
    }
    .favorite-brief {
      font-size: 14px;
      margin: 5px 0;
      font-weight: normal;
      color: #909090;
    }
    .favorite-meta {
      list-style: none;
      display: flex;
      align-items: center;
      font-size: 14px;
      white-space: nowrap;
      overflow: hidden;
      li {
        &:nth-child(1),
        &:nth-child(2) {
          position: relative;
          &::after {
            content: '·';
            margin: 0 0.4em;
            color: #b2bac2;
          }
        }
      }
    }
  }
  .favorite-articles-list-main {
    height: 100%;
    .favorite-articles-list-main-middle {
      max-width: 960px;
      width: 100%;
      height: 100%;
      margin: auto;
      .favorite-action-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        .favorite-return-box,
        .favorite-delete-box {
          &:hover {
            a {
              color: #007fff;
            }
          }
          a {
            font-size: 14px;
          }
        }
      }
      .favorite-articles-list-box {
        height: 100%;
        overflow: auto;
        .favorite-article-box {
          background: #ffffff;
          min-height: 115px;
          padding: 20px 30px;
          box-sizing: border-box;
          border-bottom: 1px solid rgba(178, 186, 194, 0.15);
          display: flex;
          justify-content: space-between;
          align-items: center;

          .article-info-box {
            max-width: 568px;
            flex: 1;

            ul.article-meta-list {
              a {
                font-size: 12px;
              }
              margin: 0;
              padding: 0;
              list-style: none;
              display: flex;
              align-items: center;
              li.article-username,
              li.article-created {
                position: relative;
                // 小圆点
                &::after {
                  content: '·';
                  margin: 0 0.4em;
                  color: #b2bac2;
                }
              }
            }
            .article-tag-box {
              width: 100%;
              display: flex;
              .article-tag {
                cursor: pointer;
                margin: 5px 5px 0 0;
              }
              // justify-content: space-around;
            }
            a.article-title {
              font-size: 17px;
              font-weight: 600;
              color: #2e3135;
              line-height: 2;
              &:hover {
                text-decoration: underline;
              }
            }
            ul.article-action-list {
              margin: 0;
              padding: 0;
              list-style: none;
              display: flex;
              align-items: center;
              li {
                color: #f7f8fa;
                margin-top: 5px;
                height: 24px;
                padding: 0 5px;
                border-radius: 1px;
                border: 1px solid #edeeef;
                cursor: pointer;
                display: flex;
                justify-content: center;
                align-items: center;
              }
              li.like-box {
                a.like-icon {
                  margin-right: 3px;
                }
                a.like-count {
                  font-weight: 600;
                  font-size: 14px;
                }
              }
              li.comment-box {
                a.comment-icon {
                  margin-right: 3px;
                }
                a.comment-count {
                  font-weight: 600;
                  font-size: 14px;
                }
              }
              li.is-liked {
                a {
                  color: #ee5253;
                }
              }
            }
          }
          .article-avatar-box {
            width: 60px;
            height: 60px;
          }
        }
        .load-more-info-box {
          font-size: 16px;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 50px;
        }
      }
    }
  }
}
</style>
