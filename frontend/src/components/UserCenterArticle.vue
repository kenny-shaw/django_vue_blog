<template>
  <!-- 用户文章列表总区域 -->
  <el-container class="user-articles-list-container">
    <el-header height="46px">
      <!-- 用于防止排序选项：最新、最热等-->
      <div class="sort-container">
        <ul>
          <li>
            <a
              href="#"
              :class="{ 'sort-active': isNewest }"
              @click.prevent="toNewestUserArticleList"
              >最新</a
            >
          </li>
          <li>
            <a
              href="#"
              :class="{ 'sort-active': !isNewest }"
              @click.prevent="toPopularUserArticleList"
              >最热</a
            >
          </li>
        </ul>
      </div>
    </el-header>
    <el-main>
      <div
        class="user-articles-list-box"
        v-infinite-scroll="loadMoreUserArticle"
        infinite-scroll-disabled="disabled"
      >
        <div
          class="user-article-box"
          v-for="article in userArticleList"
          :key="article.id"
        >
          <div class="user-article-info-box">
            <!-- 存放作者、时间、栏目标签等信息 -->
            <ul class="user-article-meta-list">
              <li class="user-article-username">
                <a href="#">{{ article.author }}</a>
              </li>
              <li class="user-article-created">
                <a href="#">{{ article.created }}</a>
              </li>
              <li class="user-article-column">
                <a href="#">{{ article.column }}</a>
              </li>
            </ul>
            <div class="user-article-tag-box">
              <el-tag
                size="mini"
                class="user-article-tag"
                v-for="(tag, index) in article.tag"
                :key="index"
                @click="toTagDetail(tag)"
                >{{ tag }}</el-tag
              >
            </div>
            <!-- 文章标题 -->
            <a
              href="#"
              class="user-article-title"
              @click.prevent="toArticleDetail(article.id)"
              >{{ article.title }}</a
            >
            <!-- 文章动作列表，包括点赞、评论等等 -->
            <ul class="user-article-action-list">
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
            class="user-article-avatar-box hidden-xxs-only "
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
  props: ['userid'],
  data() {
    return {
      isNewest: true,
      // 获取到的文章列表
      userArticleList: [],
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
    // 当前是否繁忙状态，true则不执行loadMoreUserArticle
    disabled() {
      return this.loading || this.noMore
    }
  },
  methods: {
    // 获取用户文章列表
    async getUserArticleList(size = this.size, page = 1) {
      // 获取当前token
      const token = this.$store.state.token
      // 要请求的后端URL
      let backendUrl = `userarticles/${this.userid}?token=${token}`
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
      if (res.code === 1000) {
        // 将文章数据存储于userArticleList
        // 如果userArticleList为空，则将res.data赋给userArticleList，
        // 或者size为6，也将res.data赋给userArticleList，解决loadmore与get重复进行的bug
        if (this.userArticleList.length === 0 || size === 6) {
          this.userArticleList = res.data
          this.userArticleList.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
        } else {
          const concatData = res.data

          concatData.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
          this.userArticleList = this.userArticleList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.userArticleList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    // 加载用户的更多文章
    loadMoreUserArticle() {
      console.log('loadmore...')
      this.loading = true
      // 首次加载时，会进行loadmore，判断articleList是否为空
      // 如果为空进行首次加载，加载10条
      if (this.userArticleList.length === 0) {
        console.log('获取6条')
        // 首屏数据load次数+1
        // this.loadMoreFirstPageCount += 1
        // console.log(this.loadMoreFirstPageCount)
        this.getUserArticleList()
      } else {
        this.getUserArticleList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    // 访问用户最新文章路由
    toNewestUserArticleList() {
      // 如果已经是最新文章了，不再重新获取文章列表
      if (this.isNewest === true) {
        return
      }
      this.$router.push({
        name: 'userCenterArticle',
        query: { sort: 'newest' }
      })
    },
    // 访问用户最热文章路由
    toPopularUserArticleList() {
      // 如果已经是最热文章了，不再重新获取文章列表
      if (this.isNewest === false) {
        return
      }
      this.$router.push({
        name: 'userCenterArticle',
        query: { sort: 'popular' }
      })
    },
    // 点赞文章、取消点赞
    async LikeOrCancelLikeArticle(articleId) {
      // 获取当前文章
      const article = this.userArticleList.find(
        article => article.id === articleId
      )
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
    // 前往标签文章列表页
    toTagDetail(tagName) {
      this.$router.push({ path: `/tag/${tagName}` })
    }
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空文章列表
      this.userArticleList = []
      // 加载更多文章首个页数配置重置为6
      this.loadMorePage = 4

      // 是否在加载文章状态重置为false
      this.loading = false
      // 是否为没有更多文章状态重置为false
      this.noMore = false
      // 路由变化，重新获取文章列表

      this.getUserArticleList()
    }
  }
}
</script>
<style lang="less" scoped>
// 控制最新最热变色
.sort-active {
  color: #409eff !important;
}
.user-articles-list-container {
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
    .user-articles-list-box {
      height: 100%;
      overflow: auto;
      .user-article-box {
        min-height: 115px;
        padding: 20px 30px;
        box-sizing: border-box;
        border-bottom: 1px solid rgba(178, 186, 194, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        .user-article-info-box {
          max-width: 568px;
          flex: 1;

          ul.user-article-meta-list {
            a {
              font-size: 12px;
            }
            margin: 0;
            padding: 0;
            list-style: none;
            display: flex;
            align-items: center;
            li.user-article-username,
            li.user-article-created {
              position: relative;
              // 小圆点
              &::after {
                content: '·';
                margin: 0 0.4em;
                color: #b2bac2;
              }
            }
          }
          .user-article-tag-box {
            width: 100%;
            display: flex;
            .user-article-tag {
              cursor: pointer;
              margin: 5px 5px 0 0;
            }
            // justify-content: space-around;
          }
          a.user-article-title {
            font-size: 17px;
            font-weight: 600;
            color: #2e3135;
            line-height: 2;
            &:hover {
              text-decoration: underline;
            }
          }
          ul.user-article-action-list {
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
        .user-article-avatar-box {
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
