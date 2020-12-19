<template>
  <!-- 文章列表总区域 -->
  <el-container class="all-articles-list-container">
    <el-header height="46px">
      <!-- 用于防止排序选项：最新、最热等-->
      <div class="sort-container">
        <ul>
          <li>
            <a
              href="#"
              :class="{ 'sort-active': isNewest }"
              @click.prevent="toNewestArticleList"
              >最新</a
            >
          </li>
          <li>
            <a
              href="#"
              :class="{ 'sort-active': !isNewest }"
              @click.prevent="toPopularArticleList"
              >最热</a
            >
          </li>
        </ul>
      </div>
    </el-header>
    <el-main>
      <div
        class="articles-list-box"
        v-infinite-scroll="loadMoreArticle"
        infinite-scroll-disabled="disabled"
      >
        <div
          class="article-box"
          v-for="article in articleList"
          :key="article.id"
        >
          <div class="article-info-box">
            <!-- 存放作者、时间、栏目标签等信息 -->
            <ul class="article-meta-list">
              <li class="article-username">
                <a href="#" @click.prevent="toUserCenter(article.author_id)">{{
                  article.author
                }}</a>
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
                :key="index"
                @click="toTagDetail(tag)"
                >{{ tag }}</el-tag
              >
            </div>
            <!-- 文章标题 -->
            <a
              class="article-title"
              @click.stop="toArticleDetail(article.id)"
              >{{ article.title }}</a
            >
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
                <a href="#" class="like-count ">{{ article.article_likes }}</a>
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
      </div>
    </el-main>
  </el-container>
</template>
<script>
export default {
  // params传参方式接收到的column参数
  props: ['column'],
  data() {
    return {
      // 用于sort方式的高亮
      isNewest: true,
      // 获取到的文章列表
      articleList: [],
      // 当前是否在加载文章状态
      loading: false,
      // 是否为没有更多文章状态
      noMore: false,
      // 首屏加载的文章数量
      size: 6,
      // 加载更多文章时，每次加载的数量
      loadMoreSize: 2,
      loadMorePage: 4
    }
  },
  computed: {
    // 当前是否繁忙状态，true则不执行loadMoreArticle
    disabled() {
      return this.loading || this.noMore
    }
  },
  methods: {
    async getArticleList(size = this.size, page = 1) {
      console.log('size' + size)
      // 获取当前token
      const token = this.$store.state.token
      // 要请求的后端URL
      let backendUrl = `articles/?token=${token}`

      if (this.column) {
        backendUrl = `${backendUrl}&column=${this.column}`
      }
      // 获取排序方式
      const sortQuery = this.$route.query.sort

      if (sortQuery === 'popular') {
        this.isNewest = false
        backendUrl = `${backendUrl}&sort=popular`
      } else {
        this.isNewest = true
        backendUrl = `${backendUrl}&sort=newest`
      }
      backendUrl = `${backendUrl}&size=${size}&page=${page}`
      const { data: res } = await this.$axios.get(backendUrl)
      console.log(backendUrl)

      if (res.code === 1000) {
        // 将文章数据存储于articleList
        // 如果articleList为空，则将res.data赋给articleList，
        // 或者size为6，也将res.data赋给articleList，解决loadmore与get重复进行的bug
        if (this.articleList.length === 0 || size === 6) {
          this.articleList = res.data
          this.articleList.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
        } else {
          const concatData = res.data
          concatData.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
          this.articleList = this.articleList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.articleList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    // 加载更多文章
    loadMoreArticle() {
      console.log('loadmore...')
      this.loading = true
      // 首次加载时，会进行loadmore，判断articleList是否为空
      // 如果为空进行首次加载，加载6条
      if (this.articleList.length === 0) {
        this.getArticleList()
      } else {
        this.getArticleList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    // 访问最新文章路由
    toNewestArticleList() {
      // 如果已经是最新文章了，不再重新获取文章列表
      if (this.isNewest === true) {
        return
      }
      if (!this.column) {
        this.$router.push({ path: '/', query: { sort: 'newest' } })
      } else {
        this.$router.push({
          name: 'column',
          query: { sort: 'newest' },
          params: { column: this.column }
        })
      }
    },
    // 访问最热文章路由
    toPopularArticleList() {
      // 如果已经是最热文章了，不再重新获取文章列表
      if (this.isNewest === false) {
        return
      }
      if (!this.column) {
        this.$router.push({ path: '/', query: { sort: 'popular' } })
      } else {
        this.$router.push({
          name: 'column',
          query: { sort: 'popular' },
          params: { column: this.column }
        })
      }
    },
    // 点赞文章、取消点赞
    async LikeOrCancelLikeArticle(articleId) {
      // 获取当前文章
      const article = this.articleList.find(article => article.id === articleId)
      // 获取当前token
      const token = this.$store.state.token
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
    // 前往文章详情路由
    toArticleDetail(articleId) {
      this.$router.push({ path: `/post/${articleId}` })
    },
    toUserCenter(userId) {
      this.$router.push({ path: `/user/${userId}` })
    },
    // 前往标签文章列表页
    toTagDetail(tagName) {
      this.$router.push({ path: `/tag/${tagName}` })
    }
  },
  created() {
    // 首次加载会进行loadMoreArticle,将获取数据放到该函数中
    // this.getArticleList()
  },
  // beforeDestroy() {
  //   // 每次路由变化，清空文章列表
  //   this.articleList = []
  //   // 加载更多文章首个页数配置重置为6
  //   this.loadMorePage = 6

  //   // 是否在加载文章状态重置为false
  //   this.loading = false
  //   // 是否为没有更多文章状态重置为false
  //   this.noMore = false
  //   // 路由变化，重新获取文章列表
  // },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空文章列表
      this.articleList = []
      // 加载更多文章首个页数配置重置为4
      this.loadMorePage = 4

      // 是否在加载文章状态重置为false
      this.loading = false
      // 是否为没有更多文章状态重置为false
      this.noMore = false
      // 路由变化，重新获取文章列表
      // this.$router.go(0)
      // console.log(this.loadMoreFirstPageCount)
      // if (this.loadMoreFirstPageCount <= 1) {
      this.getArticleList()
      // }
      // this.loadMoreFirstPageCount = 0
      // this.loadMoreArticle()
    }
  }
  // 组件内router函数，用于统一路由内刷新页面
  // beforeRouteUpdate(to, from, next) {
  //   console.log(1)
  //   next()
  //   this.getArticleList()
  // }
}
</script>
<style lang="less" scoped>
// 控制最新最热变色
.sort-active {
  color: #409eff !important;
}
.all-articles-list-container {
  // background: yellow;
  height: 100%;
  width: 100%;
  // 头部区域
  .el-header {
    padding: 0;
    // 排序区域
    .sort-container {
      padding-left: 20px;
      height: 100%;
      border-bottom: 1px solid hsla(0, 0%, 59.2%, 0.1);
      display: flex;
      align-items: center;
      ul {
        list-style: none;
        display: flex;
        margin: 0;
        padding: 0;
        font-size: 14px;
        li {
          box-sizing: border-box;
          &:nth-child(1) {
            padding-right: 10px;
            border-right: 1px solid hsla(0, 0%, 59.2%, 0.2);
          }
          &:nth-child(2) {
            padding: 0 10px;
          }
        }
      }
    }
  }
  .el-main {
    margin: 0;
    padding: 0;
    height: 100%;
    .articles-list-box {
      height: 100%;
      overflow: auto;
      .article-box {
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
</style>
