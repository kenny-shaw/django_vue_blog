<template>
  <!-- tag列表总区域 -->
  <el-container class="tags-page-container">
    <!-- tag列表头部区域 -->
    <el-header height="46px">
      <!-- 居中区域  max960 auto-->
      <div class="tags-page-header-middle">
        <a href="#">全部标签</a>
      </div>
    </el-header>
    <!-- 展示tag列表的sort和主区域 -->
    <el-main>
      <el-container class="tags-sort-list-container">
        <!-- 排序区域 -->
        <el-header class="tags-sort-header" height="46px">
          <div class="sort-container">
            <ul>
              <li>
                <a
                  href="#"
                  :class="{ 'sort-active': isNewest }"
                  @click.prevent="toNewestTagList"
                  >最新</a
                >
              </li>
              <li>
                <a
                  href="#"
                  :class="{ 'sort-active': !isNewest }"
                  @click.prevent="toPopularTagList"
                  >最热</a
                >
              </li>
            </ul>
          </div>
        </el-header>
        <!-- 主区域 -->
        <el-main
          class="tags-list-box"
          v-infinite-scroll="loadMoreTag"
          infinite-scroll-disabled="disabled"
        >
          <el-row :gutter="10">
            <el-col :xs="12" :sm="6" v-for="tag in tagList" :key="tag.id">
              <div class="tag-box">
                <div class="tag-avatar-box">
                  <el-avatar
                    :size="40"
                    :src="tag.avatar"
                    shape="square"
                  ></el-avatar>
                </div>
                <div class="tag-title-box">{{ tag.title }}</div>
                <div class="tag-meta-box">
                  <ul class="tag-meta-list">
                    <li class="tag-article-counts">
                      <a href="#">{{ tag.article_counts }}篇文章</a>
                    </li>
                    <li class="tag-created">
                      <a href="#">{{ tag.created }}</a>
                    </li>
                  </ul>
                </div>
                <el-button
                  type="success"
                  size="mini"
                  @click="toTagArticle(tag.title)"
                  >查看文章</el-button
                >
              </div>
            </el-col>
          </el-row>
          <!-- <div class="tag-box">
            123
          </div> -->
        </el-main>
      </el-container>
    </el-main>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      isNewest: true,
      // 获取到的标签列表
      tagList: [],
      // 当前是否在加载标签状态
      loading: false,
      // 是否为没有更多标签状态
      noMore: false,
      // 首屏加载的标签数量
      size: 20,
      // 加载更多标签时，每次加载的数量
      loadMoreSize: 4,
      loadMorePage: 6
    }
  },
  computed: {
    // 当前是否繁忙状态，true则不执行loadMoreUserLikeArticle
    disabled() {
      return this.loading || this.noMore
    }
  },
  methods: {
    // 获取标签列表
    async getTagList(size = this.size, page = 1) {
      let backendUrl = 'articletags/'
      // 获取排序方式
      const sortQuery = this.$route.query.sort
      if (sortQuery === 'popular') {
        this.isNewest = false
        backendUrl = `${backendUrl}?sort=popular`
      } else {
        this.isNewest = true
        backendUrl = `${backendUrl}?sort=newest`
      }
      backendUrl = `${backendUrl}&size=${size}&page=${page}`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        // 将tag数据存储于tagList
        // 如果tagList为空，则将res.data赋给tagList，
        // 或者size为6，也将res.data赋给tagList，解决loadmore与get重复进行的bug
        if (this.tagList.length === 0 || size === this.size) {
          this.tagList = res.data
          this.tagList.forEach(tag => {
            // 将时间转换为formnow
            tag.created = this.$moment(tag.created).fromNow()
          })
        } else {
          const concatData = res.data

          concatData.forEach(tag => {
            // 将时间转换为formnow
            tag.created = this.$moment(tag.created).fromNow()
          })
          this.tagList = this.tagList.concat(concatData)
        }
      } else if (res.code === 1001) {
        // 不存在数据时，将数组置位空
        this.tagList = []
      } else if (res.code === 1002) {
        // 分页无数据时，noMore改为True
        this.noMore = true
      } else {
        this.$message.error(res.error)
      }
    },
    loadMoreTag() {
      this.loading = true
      // 首次加载时，会进行loadmore，判断tagList是否为空
      // 如果为空进行首次加载
      if (this.tagList.length === 0) {
        this.getTagList()
      } else {
        this.getTagList(this.loadMoreSize, this.loadMorePage)
        this.loadMorePage += 1
      }
      this.loading = false
    },
    // 前往最新标签路由
    toNewestTagList() {
      // 如果已经是最新标签了，不再重新获取标签列表
      if (this.isNewest === true) {
        return
      }
      this.$router.push({
        name: 'tags',
        query: { sort: 'newest' }
      })
    },
    // 前往最热标签路由
    toPopularTagList() {
      // 如果已经是最热标签了，不再重新获取标签列表
      if (this.isNewest === false) {
        return
      }
      this.$router.push({
        name: 'tags',
        query: { sort: 'popular' }
      })
    },
    // 前往标签文章列表路由
    toTagArticle(tagTitle) {
      this.$router.push({ name: 'tag', params: { tagTitle: tagTitle } })
    }
  },
  watch: {
    // 监听路由，路由发生变化时，获得数据
    $route(val) {
      console.log('route change')
      // 每次路由变化，清空标签列表
      this.tagList = []
      // 加载更多标签首个页数配置重置为6
      this.loadMorePage = 6

      // 是否在加载标签状态重置为false
      this.loading = false
      // 是否为没有更多标签状态重置为false
      this.noMore = false
      // 路由变化，重新获取标签列表
      this.getTagList()
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
.tags-page-container {
  height: 100%;
  width: 100%;
  .el-header {
    background: #ffffff;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    .tags-page-header-middle {
      max-width: 960px;
      height: 100%;
      margin: auto;
      display: flex;
      align-items: center;
      a {
        font-size: 14px;
        font-weight: 600;
        height: 100%;
        line-height: 46px;
        color: #007fff;
        cursor: pointer;
        border-bottom: 2px solid #007fff;
        box-sizing: border-box;
      }
    }
  }
  .el-main {
    .tags-sort-list-container {
      max-width: 960px;
      height: 100%;
      margin: auto;
      padding: 10px 0 0 0;
      background: #fff;
      box-sizing: border-box;
      background-clip: content-box;
      .tags-sort-header {
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
      .tags-list-box {
        padding: 20px;
        .el-row {
          .el-col {
            .tag-box {
              min-height: 200px;
              box-sizing: border-box;
              padding: 20px 10px;
              margin-bottom: 10px;
              // border: 1px solid #f1f1f1;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12),
                0 0 6px rgba(0, 0, 0, 0.04);
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              .tag-avatar-box {
                display: flex;
                justify-content: center;
              }
              .tag-title-box {
                padding-top: 5px;
                font-size: 18px;
                line-height: 24px;
                color: #333;
              }
              .tag-meta-box {
                // color: #909090;
                // font-size: 14px;
                // line-height: 24px;
                ul.tag-meta-list {
                  a {
                    color: #909090;
                    font-size: 14px;
                    line-height: 24px;
                    // font-size: 12px;
                  }
                  margin: 0;
                  padding: 0;
                  list-style: none;
                  display: flex;
                  li.tag-article-counts {
                    position: relative;
                    // 小圆点
                    &::after {
                      content: '·';
                      margin: 0 0.2em;
                      color: #b2bac2;
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
</style>
