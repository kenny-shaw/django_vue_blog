<template>
  <!-- 收藏夹总区域 -->
  <el-container class="tag-articles-list-container">
    <!-- 收藏夹头部区域、放置标题简介等 -->
    <el-header height="150px" class="tag-articles-list-header">
      <h1 class="tag-title">{{ tag.title }}</h1>
      <ul class="tag-meta">
        <li>
          <a href="#">{{ tag.article_counts }}篇文章</a>
        </li>
        <li>
          <a href="#">{{ tag.created }}</a>
        </li>
      </ul>
    </el-header>

    <!-- 主体区域 -->
    <el-main>
      <!-- 主体居中区域 -->
      <el-container>
        <!-- 头部区域，放置删除返回等 -->
        <el-header class="tag-action-box" height="30px">
          <div class="tag-return-box" @click.stop="toMoreTag">
            <a>返回更多标签</a>
          </div>
          <!-- 后续博主可以开放 -->
          <!-- <div
            class="favorite-delete-box"
            @click="favoriteDeleteDialogVisible = true"
          >
            <a href="#">删除</a>
            <a href="#" class="icon iconfont iconicon_delete_fill"></a>
          </div> -->
        </el-header>
        <!-- 文章列表区域 -->
        <el-main>
          <el-container class="tag-sort-articles-container">
            <el-header height="46px">
              <!-- 用于防止排序选项：最新、最热等-->
              <div class="sort-container">
                <ul>
                  <li>
                    <a
                      href="#"
                      :class="{ 'sort-active': isNewest }"
                      @click.prevent="toNewestTagArticleList"
                      >最新</a
                    >
                  </li>
                  <li>
                    <a
                      href="#"
                      :class="{ 'sort-active': !isNewest }"
                      @click.prevent="toPopularTagArticleList"
                      >最热</a
                    >
                  </li>
                </ul>
              </div>
            </el-header>
            <el-main
              class="tag-articles-list-box"
              v-infinite-scroll="loadMoreTagArticle"
              infinite-scroll-disabled="disabled"
            >
              <!-- 文章区域，用于v-for -->
              <div
                class="tag-article-box"
                v-for="article in tagArticleList"
                :key="article.id"
              >
                <div class="article-info-box">
                  <!-- 存放作者、时间、栏目标签等信息 -->
                  <ul class="article-meta-list">
                    <li class="article-username">
                      <a
                        href="#"
                        @click.prevent="toUserCenter(article.author_id)"
                        >{{ article.author }}</a
                      >
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
                      >{{ tag }}</el-tag
                    >
                  </div>
                  <!-- 文章标题 -->
                  <a
                    href="#"
                    class="article-title"
                    @click.prevent="toArticleDetail(article.id)"
                    >{{ article.title }}</a
                  >
                  <!-- 文章动作列表，包括点赞、评论等等 -->
                  <ul class="article-action-list">
                    <!-- 点赞 -->
                    <li
                      :class="[
                        'like-box',
                        { 'is-liked ': article.likedbycuruser }
                      ]"
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
                      <a class="comment-count ">{{
                        article.article_comments
                      }}</a>
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
    </el-main>
  </el-container>
</template>
<script>
export default {
  props: ['tagTitle'],
  data() {
    return {
      // 存放标签的详细信息
      tag: {},
      isNewest: true,
      // 获取到的标签文章列表
      tagArticleList: [],
      // 当前是否在加载文章状态
      loading: false,
      // 是否为没有更多文章状态
      noMore: false,
      // 首屏加载的文章数量
      size: 6,
      // 加载更多文章时，每次加载的数量
      loadMoreSize: 2,
      loadMorePage: 4
      // 控制提示是否删除收藏夹的dialog显示与隐藏
      // favoriteDeleteDialogVisible: false
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
    async getTagArticleList(size = this.size, page = 1) {
      // 获取当前token
      const token = this.$store.state.token
      // 要请求的后端URL
      let backendUrl = `articles/?token=${token}&tag=${this.tagTitle}`
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
        // 将文章数据存储于tagArticleList
        // 如果tagArticleList为空，则将res.data赋给tagArticleList，
        // 或者size为6，也将res.data赋给tagArticleList，解决loadmore与get重复进行的bug
        if (this.tagArticleList.length === 0 || size === 6) {
          this.tagArticleList = res.data
          this.tagArticleList.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
        } else {
          const concatData = res.data

          concatData.forEach(article => {
            // 将时间转换为formnow
            article.created = this.$moment(article.created).fromNow()
          })
          this.tagArticleList = this.tagArticleList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.tagArticleList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    // 加载用户的更多文章
    loadMoreTagArticle() {
      console.log('loadmore...')
      this.loading = true
      // 首次加载时，会进行loadmore，判断userLikeArticleList是否为空
      // 如果为空进行首次加载，加载6条
      if (this.tagArticleList.length === 0) {
        this.getTagArticleList()
      } else {
        this.getTagArticleList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    async getTagDetail() {
      console.log(this.tagTitle)
      const backendUrl = `articletags/${this.tagTitle}`
      console.log(backendUrl)

      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.tag = res.data
        this.tag.created = this.$moment(this.tag.created).fromNow()
      } else {
        this.$message.error(res.error)
      }
    },
    // 返回用户收藏夹列表
    toMoreTag() {
      this.$router.push({ path: '/tags' })
    },
    // // 删除tag
    // async deleteFavorite(favoriteId, userId) {
    //   const token = this.$store.state.token
    //   const backendUrl = `favorite/${favoriteId}?token=${token}`
    //   const { data: res } = await this.$axios.delete(backendUrl)
    //   if (res.code === 1000) {
    //     this.$message.success('删除收藏夹成功')
    //     this.$router.push({ path: `/user/${userId}/favorites` })
    //   } else {
    //     this.$message.error(res.error)
    //   }
    // },
    // 点赞文章、取消点赞
    async LikeOrCancelLikeArticle(articleId) {
      // 获取当前文章
      const article = this.tagArticleList.find(
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
    // 访问最新文章路由
    toNewestTagArticleList() {
      // 如果已经是最新文章了，不再重新获取文章列表
      if (this.isNewest === true) {
        return
      }
      this.$router.push({
        name: 'tag',
        query: { sort: 'newest' },
        params: { tagTitle: this.tagTitle }
      })
    },
    // 访问最热文章路由
    toPopularTagArticleList() {
      // 如果已经是最热文章了，不再重新获取文章列表
      if (this.isNewest === false) {
        return
      }
      this.$router.push({
        name: 'tag',
        query: { sort: 'popular' },
        params: { tagTitle: this.tagTitle }
      })
    },
    // 前往文章详情路由
    toArticleDetail(articleId) {
      this.$router.push({ path: `/post/${articleId}` })
    },
    toUserCenter(userId) {
      this.$router.push({ path: `/user/${userId}` })
    }
  },
  created() {
    this.getTagDetail()
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空文章列表
      this.tagArticleList = []
      // 加载更多文章首个页数配置重置为6
      this.loadMorePage = 4

      // 是否在加载文章状态重置为false
      this.loading = false
      // 是否为没有更多文章状态重置为false
      this.noMore = false
      // 路由变化，重新获取文章列表
      this.getTagDetail()
      this.getTagArticleList()
    }
  }
}
</script>
<style lang="less" scoped>
.sort-active {
  color: #409eff !important;
}
.el-main,
.el-header {
  margin: 0;
  padding: 0;
}
.tag-articles-list-container {
  height: 100%;
  width: 100%;
  .tag-articles-list-header {
    margin: 0;
    padding: 0;
    background: #f8f9fa;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .tag-title {
      font-family: PingFangSC-Semibold, PingFang SC;
      font-size: 24px;
      font-weight: 600;
      color: #666;
      margin-bottom: 5px;
    }

    .tag-meta {
      list-style: none;
      display: flex;
      align-items: center;
      font-size: 14px;
      white-space: nowrap;
      overflow: hidden;
      li {
        &:nth-child(1) {
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
  // 主体全屏区域
  .el-main {
    height: 100%;
    // 主体居中区域
    .el-container {
      max-width: 960px;
      width: 100%;
      height: 100%;
      margin: auto;
      .tag-action-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        .tag-return-box,
        .tag-delete-box {
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
      // 文章排序和主体区域的main
      .el-main {
        height: 100%;
        width: 100%;
        background: #ffffff;
        // 文章排序和主体区域的container
        .tag-sort-articles-container {
          .el-header {
            // 排序区域
            .sort-container {
              padding-left: 20px;
              height: 100%;
              box-sizing: border-box;
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
          // 文章列表真正区域
          .tag-articles-list-box {
            height: 100%;
            overflow: auto;
            .tag-article-box {
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
  }
}
</style>
