<template>
  <!-- 整个文章列表区域（包括栏目、文章列表、标签等等等） -->
  <el-container class="article-total-container">
    <!-- 文章列表头部区域，用于展示栏目 -->
    <el-header>
      <!-- 中间专门展示栏目区域，居中，max-height -->
      <div class="article-column-container">
        <el-tabs
          v-model="activeColumnName"
          @tab-click="handleColumnClick"
          tab-position="top"
        >
          <el-tab-pane label="全部" name="全部"></el-tab-pane>
          <el-tab-pane
            :label="column.title"
            v-for="column in columnList"
            :key="column.id"
            :name="column.title"
          ></el-tab-pane>
        </el-tabs>
      </div>
    </el-header>
    <!-- 展示具体文章列表区域 -->
    <el-main>
      <!-- 文章列表中间区域，用于展示文章列表、最热标签、最热文章等等 -->
      <div class="article-container">
        <!-- 具体文章列表区域 -->
        <div class="article-list-container">
          <router-view></router-view>
        </div>
        <!-- 侧边栏区域 -->
        <div class="article-sidebar hidden-xs-only">
          <div class="anniversay-love-box">
            <div class="couple-avatar-box">
              <el-avatar :size="60" :src="this.lover.boyavatar"></el-avatar>
              <el-avatar :size="60" :src="this.lover.girlavatar"></el-avatar>
            </div>

            <div class="anniversay-time">
              <h1>我们在一起已经</h1>
              <h1>{{ anniversayDays }}天</h1>
            </div>
          </div>
          <div class="article-tags-box">
            <div class="article-tags-title">
              <h1 class="title">标签云</h1>
              <a class="all-tag" @click.prevent="toAllTagList">更多标签</a>
            </div>
            <div
              class="article-tags-content"
              v-if="this.articleTagList.length !== 0"
            >
              <el-tag
                class="article-tag "
                type="danger"
                v-for="tag in this.articleTagList"
                :key="tag.id"
                @click.native="toTagDetail(tag.title)"
                >{{ tag.title }}
              </el-tag>

              <!-- <div
                class="article-tag"
                v-for="tag in this.articleTagList"
                :key="tag.id"
              >
                <i class="icon iconfont iconremen"></i>
                <a href="">{{ tag.title }}</a>
              </div> -->
            </div>
            <div class="no-article-tags" v-else>
              <i class="icon iconfont icontanhao1"></i>
              <a href="">暂无标签</a>
            </div>
          </div>
          <div class="hot-articles-box">
            <div class="hot-articles-title">
              <h1 class="title">最热文章</h1>
            </div>
            <div
              class="hot-articles-content"
              v-if="this.hotArticleList.length !== 0"
            >
              <div
                class="hot-article"
                v-for="article in this.hotArticleList"
                :key="article.id"
              >
                <i class="icon iconfont iconremen"></i>
                <a href="#" @click.prevent="toArticleDetail(article.id)">{{
                  article.title
                }}</a>
              </div>
            </div>
            <div class="no-hot-articles" v-else>
              <i class="icon iconfont icontanhao1"></i>
              <a href="">暂无最热文章</a>
            </div>
          </div>
          <div class="beian">
            <p>© 2020-2021 kennyeow.com</p>
            <p>
              版权所有ICP证：<a href="https://beian.miit.gov.cn/" target="blank"
                >鄂ICP备2020015640号</a
              >
            </p>
          </div>
        </div>
      </div>
    </el-main>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      activeColumnName: '全部',
      columnList: [],
      // 最热文章列表
      hotArticleList: [],
      // 标签列表
      articleTagList: [],
      lover: {},
      anniversayDays: ''
    }
  },
  watch: {
    // 监听路由变化，如果存在colomn，则使得直接进入url时激活栏目名称变化
    $route: {
      handler: function(val, oldVal) {
        if (val.params.column) {
          this.activeColumnName = val.params.column
        }
      },
      immediate: true
    }
  },
  methods: {
    // 点击专栏click事件
    handleColumnClick(tab, event) {
      console.log(this.activeColumnName)

      // console.log(event.target.innerHTML)
      // 如果点击的栏目就是当前栏目，则不执行
      // if (this.activeColumnName === event.target.innerHTML) {
      //   return
      // }
      // 如果是所有文章
      if (this.activeColumnName === '全部') {
        return this.$router.push({ path: '/' })
      }
      this.$router.push({
        name: 'column',
        params: { column: this.activeColumnName }
      })
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
    async getHotArticleList() {
      const { data: res } = await this.$axios.get(
        'articles/?sort=popular&size=5'
      )

      if (res.code === 1000) {
        this.hotArticleList = res.data
      } else if (res.code === 1001) {
        this.userHotArticleList = []
      }
    },
    async getArticleTagList() {
      const { data: res } = await this.$axios.get(
        'articletags/?sort=popular&size=10'
      )

      if (res.code === 1000) {
        this.articleTagList = res.data
      } else if (res.code === 1001) {
        this.articleTagList = []
      }
    },
    // 获取情侣信息
    async getLoverDetail() {
      const { data: res } = await this.$axios.get('loverdetail/')
      if (res.code === 1000) {
        this.lover = res.data
      }
      this.anniversayDays = this.$moment().diff(
        this.$moment(res.data.togetherdate),
        'days'
      )
    },
    // 前往所有标签路由
    toAllTagList() {
      this.$router.push({ path: '/tags' })
    },
    toTagDetail(tagTitle) {
      this.$router.push({ path: `/tag/${tagTitle}` })
    },
    // 前往文章详情路由
    toArticleDetail(articleId) {
      this.$router.push({ path: `/post/${articleId}` })
    }
  },
  created() {
    this.getColumnList()
    this.getHotArticleList()
    this.getArticleTagList()
    this.getLoverDetail()
  }
}
</script>
<style lang="less" scoped>
// 文章列表container
.article-total-container {
  width: 100%;
  height: 100%;
  // 头部主要用于展示栏目
  .el-header {
    background: #ffffff;
    height: 40px !important;
    border-bottom: 1px solid #ebecec;
    // 具体栏目div
    .article-column-container {
      max-width: 960px;
      height: 100%;
      margin: auto;
      .el-tabs {
        height: 100% !important;
      }
    }
  }
  .el-main {
    margin: 0;
    padding: 0;

    .article-container {
      max-width: 960px;
      margin: auto;
      padding: 10px 0 0 0;
      background: #ffffff;
      background-clip: content-box;
      height: 100%;
      box-sizing: border-box;
      display: flex;
      justify-content: space-between;
      .article-list-container {
        max-width: 700px;
        width: 100%;
        // height: 100%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
        // background: red;
      }
      .article-sidebar {
        padding-left: 20px;
        width: 240px;
        height: 100%;
        background: #f4f5f5;
        display: flex;
        flex-direction: column;
        .anniversay-love-box {
          width: 100%;
          height: 200px;
          min-width: 240px;
          // background: #ffffff;
          background: pink;
          margin-bottom: 10px;
          width: 100%;
          border-radius: 2%;
          border-radius: 2px;
          box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          .couple-avatar-box {
            margin-bottom: 10px;
            .el-avatar {
              &:nth-child(1) {
                margin-right: 5px;
              }
            }
          }
          .anniversay-time {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            h1 {
              font-size: 15px;
              font-weight: 600;
              color: #31445b;
            }
          }
        }
        .article-tags-box {
          width: 100%;
          margin: 10px 0;
          border-radius: 2%;
          background: #ffffff;
          border-radius: 2px;
          box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
          .article-tags-title {
            padding: 15px;
            box-sizing: border-box;
            border-bottom: 1px solid rgba(230, 230, 231, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
            h1.title {
              color: #31445b;
              margin: 0;
              padding: 0;
              font-size: 16px;
              font-weight: 600;
            }
            a.all-tag {
              font-size: 14px;
              &:hover {
                color: #007fff;
              }
            }
          }
          .article-tags-content {
            width: 100%;
            padding: 15px;
            min-height: 130px;
            .article-tag {
              cursor: pointer;
              margin: 5px 5px 0 0 !important;
            }
            // .article-tag {
            //   display: flex;
            //   align-items: center;
            //   margin-bottom: 10px;
            //   .icon {
            //     color: #ff3838;
            //     margin-right: 10px;
            //   }
            //   a {
            //     color: #31445b;
            //     font-size: 15px;
            //   }
            // }
          }
          .no-article-tags {
            height: 150px;
            padding: 15px;
            .icon {
              color: #ff3838;
              margin-right: 10px;
            }
            a {
              color: #31445b;
              font-size: 15px;
            }
          }
        }
        .hot-articles-box {
          width: 100%;
          margin: 10px 0;
          border-radius: 2%;
          background: #ffffff;
          border-radius: 2px;
          box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
          .hot-articles-title {
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
          .hot-articles-content {
            padding: 15px;
            min-height: 130px;
            .hot-article {
              display: flex;
              align-items: center;
              margin-bottom: 10px;
              .icon {
                color: #ff3838;
                margin-right: 10px;
              }
              a {
                color: #31445b;
                font-size: 15px;
              }
            }
          }
          .no-hot-articles {
            height: 150px;
            padding: 15px;
            .icon {
              color: #ff3838;
              margin-right: 10px;
            }
            a {
              color: #31445b;
              font-size: 15px;
            }
          }
        }
        .beian {
          margin-top: 5px;
          color: #909090;
          a:hover {
            color: #007fff;
          }
        }
      }
    }
  }
}
</style>
