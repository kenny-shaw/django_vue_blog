<template>
  <!-- 用户收藏夹列表总区域 -->
  <el-container class="user-favorites-list-container">
    <!-- 收藏夹列表头部区域，放置收藏夹简介 数量等-->
    <el-header height="46px">
      <div class="user-favorites-list-brief">
        <a href="">收藏夹</a>
        <a href="">{{ this.favorites_count }}</a>
      </div>
    </el-header>
    <!-- 收藏夹主体区域，放置各个收藏夹 -->
    <el-main>
      <div
        class="user-favorites-list-box"
        v-infinite-scroll="loadMoreUserFavorite"
        infinite-scroll-disabled="disabled"
      >
        <!-- 收藏夹box，用于v-for -->
        <div
          class="user-favorite-box"
          v-for="favorite in userFavoriteList"
          :key="favorite.id"
          @click="toFavoriteArticleList(favorite.id)"
        >
          <div class="user-favorite-title">{{ favorite.title }}</div>
          <div class="user-favorite-brief">{{ favorite.brief }}</div>
          <div>
            <ul class="user-favorite-meta">
              <li>
                <a href="#">{{ favorite.user }}</a>
              </li>
              <li>
                <a href="#">{{ favorite.createdorupdated }}</a>
              </li>
              <li>
                <a href="#">{{ favorite.article_counts }}篇文章</a>
              </li>
            </ul>
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
  props: ['userid', 'favorites_count'],
  data() {
    return {
      // 获取到的收藏夹列表
      userFavoriteList: [],
      // 当前是否在加载收藏夹状态
      loading: false,
      // 是否为没有更多收藏夹状态
      noMore: false,
      // 首屏加载的收藏夹数量
      size: 6,
      // 加载更多收藏夹时，每次加载的数量以及起始页数
      loadMoreSize: 2,
      loadMorePage: 4
    }
  },
  computed: {
    // 当前是否繁忙状态，true则不执行loadMoreUserFavorite
    disabled() {
      return this.loading || this.noMore
    }
  },
  methods: {
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
    loadMoreUserFavorite() {
      this.loading = true
      // 首次加载时，会进行loadmore，判断userFavoriteList是否为空
      // 如果为空进行首次加载，加载6条
      if (this.userFavoriteList.length === 0) {
        console.log('获取6条')
        this.getUserFavoriteList()
      } else {
        this.getUserFavoriteList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    // 前往收藏夹文章列表详情
    toFavoriteArticleList(favoriteId) {
      this.$router.push({ path: `/favorite/${favoriteId}` })
    }
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空收藏夹列表
      this.userFavoriteList = []
      // 加载更多收藏夹首个页数配置重置为6
      this.loadMorePage = 4

      // 是否在加载收藏夹状态重置为false
      this.loading = false
      // 是否为没有更多收藏夹状态重置为false
      this.noMore = false
      // 路由变化，重新获取用户收藏夹
      this.getUserFavoriteList()
    }
  }
}
</script>
<style lang="less" scoped>
.user-favorites-list-container {
  height: 100%;
  width: 100%;
  .el-header {
    padding: 0;
    .user-favorites-list-brief {
      padding: 0 20px;
      height: 100%;
      border-bottom: 1px solid hsla(0, 0%, 59.2%, 0.1);
      display: flex;
      align-items: center;
      justify-content: space-between;
      a {
        color: black;
        &:nth-child(1) {
          font-size: 15px;
          font-weight: 600;
        }
      }
    }
  }
  .el-main {
    margin: 0;
    padding: 0;
    height: 100%;
    .user-favorites-list-box {
      height: 100%;
      overflow: auto;
      .user-favorite-box {
        padding: 15px 30px;
        box-sizing: border-box;
        border-bottom: 1px solid rgba(178, 186, 194, 0.15);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        cursor: pointer;
        // align-items: center;
        .user-favorite-title {
          font-size: 16px;
          font-weight: 500;
          line-height: 1.4;
          color: #2e3135;
          cursor: pointer;
        }
        .user-favorite-brief {
          font-size: 14px;
          font-weight: 500;
          line-height: 1.4;
          text-decoration: none;
          color: #909090;
          cursor: pointer;
          margin: 2px 0;
        }
        ul.user-favorite-meta {
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
