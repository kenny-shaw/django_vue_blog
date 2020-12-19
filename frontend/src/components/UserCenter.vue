<template>
  <!-- 用户中心 -->
  <div class="user-center-container">
    <!-- 左侧主体区域 -->
    <el-container class="user-major-container">
      <!-- 用户简略信息展示部分（头像、用户名、职业、简介等） -->
      <el-header class="user-briefinfo-box">
        <div class="user-avatar-box">
          <el-avatar
            :size="90"
            :src="user.avatar"
            :key="user.avatar"
          ></el-avatar>
        </div>
        <div class="user-info-box">
          <div class="username-edituser">
            <h1 class="username">{{ user.username }}</h1>
            <a
              class="user-edit hidden-xxs-up"
              v-if="this.$store.state.userid === user.id"
              @click.prevent="toUserSetting"
              >编辑</a
            >
          </div>

          <div class="user-job">
            <i class="icon iconfont iconicon_boss_fill"></i>
            <a href="#">{{ user.job }}</a>
          </div>
          <div class="user-company">
            <i class="icon iconfont iconicon_homepage_fill"></i>
            <a href="#">{{ user.company }}</a>
          </div>
          <div class="user-brief">
            <i class="icon iconfont iconicon_namecard_fill"></i
            ><a href="">{{ user.brief }}</a>
          </div>
        </div>
        <div
          class="user-action-box hidden-xxs-only"
          v-if="this.$store.state.userid === user.id"
        >
          <el-button type="primary" plain @click="toUserSetting"
            >编辑个人资料</el-button
          >
        </div>
      </el-header>
      <el-main>
        <!-- 用户详细容器，包括文章、点赞、收藏夹等 -->
        <el-container class="user-detail-container">
          <!-- 用户详细容器的导航部分 -->
          <el-header class="user-detail-container-header">
            <el-tabs
              v-model="activeUserCenterName"
              @tab-click="handleUserCenterClick"
            >
              <el-tab-pane label="文章" name="article"></el-tab-pane>
              <el-tab-pane label="喜欢" name="like"></el-tab-pane>
              <el-tab-pane label="收藏夹" name="favorite"></el-tab-pane>
            </el-tabs>
          </el-header>

          <!-- 用户详细容器的主体部分 -->
          <el-main class="user-detail-container-body">
            <router-view
              :userid="this.id"
              :favorites_count="this.user.favorite_counts"
            ></router-view>
          </el-main>
        </el-container>
      </el-main>
    </el-container>
    <!-- 右侧简单区域、包括个人成就、加入时间、等等 -->
    <div class="user-minor-container hidden-xs-only">
      <!-- 用户成就（包括发表文章数、文章总点赞、总浏览量等等） -->
      <div class="user-achievement-box">
        <div class="user-achievement-title-box">
          <h1 class="title">个人成就</h1>
        </div>
        <div class="user-achievement-content-box">
          <div class="user-total-articles">
            <i class="icon iconfont iconchuangzuo1"></i>
            <a href="">共发布{{ user.article_counts }}篇文章</a>
          </div>
          <div class="user-total-likes">
            <i class="icon iconfont iconaixin1"></i>
            <a href="">共获得{{ user.obtained_total_likes }}点赞</a>
          </div>
          <div class="user-total-views">
            <i class="icon iconfont iconyanjing1"></i>
            <a href="">共获得{{ user.obtained_total_views }}浏览量</a>
          </div>
        </div>
      </div>
      <!-- 其他的一些信息，如加入时间、用户身份等等 -->
      <div class="user-otherinfo-box">
        <!-- 收藏夹 -->
        <div class="user-favorites-count" @click="toUserFavoriteList">
          <a>收藏夹</a>
          <a>{{ user.favorite_counts }}</a>
        </div>
        <!-- 喜欢 -->
        <div class="user-likes-count" @click="toUserLikeList">
          <a>点赞</a>
          <a>{{ user.like_articles_count }}</a>
        </div>
        <div class="user-role">
          <a>用户角色</a>
          <a>{{ user.role }}</a>
        </div>
        <div class="join-date">
          <a>加入时间</a>
          <a>{{ user.date_joined }}</a>
        </div>
      </div>

      <div class="user-hot-articles-box">
        <div class="user-hot-articles-title">
          <h1 class="title">用户最热文章</h1>
        </div>
        <div
          class="user-hot-articles-content"
          v-if="this.userHotArticleList.length !== 0"
        >
          <div
            class="user-hot-article"
            v-for="article in this.userHotArticleList"
            :key="article.id"
          >
            <i class="icon iconfont iconremen"></i>
            <a href="" @click.prevent="toArticleDetail(article.id)">{{
              article.title
            }}</a>
          </div>
        </div>
        <div class="user-no-hot-articles" v-else>
          <i class="icon iconfont icontanhao1"></i>
          <a href="">用户暂无最热文章</a>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['id'],
  data() {
    return {
      // 获取到的用户基本信息
      user: {},
      userHotArticleList: [],
      activeUserCenterName: 'article'
    }
  },
  methods: {
    // 获取用户信息
    async getUserInfo() {
      const { data: res } = await this.$axios.get(`usergeneralinfo/${this.id}`)
      if (res.code === 1000) {
        this.user = res.data
        this.user.date_joined = this.$moment(res.data).format('YYYY-MM-DD')
      } else {
        return this.$message.error(res.error)
      }
    },
    // 获取用户最热文章
    async getUserHotArticleList() {
      const backendUrl = `userarticles/${this.id}?size=5&sort=popular`
      const { data: res } = await this.$axios.get(backendUrl)
      if (res.code === 1000) {
        this.userHotArticleList = res.data
      } else if (res.code === 1001) {
        this.userHotArticleList = []
      }
    },
    handleUserCenterClick(tab, event) {
      if (this.activeUserCenterName === 'article') {
        return this.$router.push({
          path: `/user/${this.id}/articles`
        })
      } else if (this.activeUserCenterName === 'like') {
        return this.$router.push({
          path: `/user/${this.id}/likes`
        })
      } else if (this.activeUserCenterName === 'favorite') {
        return this.$router.push({
          path: `/user/${this.id}/favorites`
        })
      }
    },
    // 前往用户收藏夹路由
    toUserFavoriteList() {
      this.$router.push({ path: 'favorites' })
    },
    // 前往用户点赞路由
    toUserLikeList() {
      this.$router.push({ path: 'likes' })
    },
    // 前往文章详情路由
    toArticleDetail(articleId) {
      this.$router.push({ path: `/post/${articleId}` })
    },
    // 前往编辑个人资料路由
    toUserSetting() {
      this.$router.push({ path: '/user/settings' })
    }
  },

  created() {
    // this.getUserInfo()
    // this.getUserHotArticleList()
  },
  watch: {
    // 监听路由实现数据加载以及
    $route: {
      handler: function(val, oldVal) {
        // console.log(val)

        if (val.name === 'userCenterArticle' || val.name === 'userCenterHome') {
          this.activeUserCenterName = 'article'
        } else if (val.name === 'userCenterLike') {
          this.activeUserCenterName = 'like'
        } else if (val.name === 'userCenterFavorite') {
          this.activeUserCenterName = 'favorite'
        }
        this.getUserInfo()
        this.getUserHotArticleList()
      },
      immediate: true
    }
  }
}
</script>
<style lang="less" scoped>
.el-main {
  padding: 0;
}
.user-center-container {
  height: 100%;
  max-width: 960px;
  width: 100%;
  margin: auto;
  padding: 20px 0 0 0;
  box-sizing: border-box;
  background: #f4f5f5;
  background-clip: content-box;
  display: flex;
  justify-content: space-between;
  .user-major-container {
    height: 100%;
    max-width: 700px;
    width: 100%;
    display: flex;
    flex-direction: column;
    // background: green;

    .user-briefinfo-box {
      height: 156px !important;
      background: #ffffff;
      padding: 30px;
      display: flex;
      align-items: center;
      border-radius: 2px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      .user-avatar-box {
        margin-right: 30px;
      }
      .user-info-box {
        flex: 1;
        display: flex;
        flex-direction: column;
        .username-edituser {
          display: flex;
          align-items: center;

          .username {
            margin: 0;
            padding: 0;
            font-size: 26px;
            line-height: 30px;
            font-weight: 600;
            margin-bottom: 5px;
          }
          .user-edit {
            margin-left: 10px;
            color: #1264b6;
            cursor: pointer;
            font-size: 14px;
            &:hover {
              text-decoration: underline;
            }
          }
        }

        .user-job,
        .user-company,
        .user-brief {
          display: flex;
          align-items: center;
          .icon {
            color: #72777b;
            margin-right: 10px;
          }
          a {
            font-size: 14px;
          }
        }
        .user-company {
          margin: 2px 0;
        }
      }
      .user-action-box {
        height: 100%;
      }
    }

    .user-detail-container {
      background: #ffffff;
      height: 100%;
      padding-top: 12px;
      box-sizing: border-box;
      background-clip: content-box;
      border-radius: 2px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      display: flex;
      flex-direction: column;
      .user-detail-container-header {
        height: 40px !important;
        padding: 0 10px;
        .el-tabs {
          height: 100% !important;
        }
      }
      .user-detail-container-body {
        padding: 0;
        flex: 1;
        height: 100%;
      }
    }
  }
  .user-minor-container {
    min-width: 240px;
    margin-left: 20px;
    // background: blue;
    .user-achievement-box {
      background: #ffffff;
      border-radius: 2px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      .user-achievement-title-box {
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
      .user-achievement-content-box {
        padding: 15px;
        .user-total-articles,
        .user-total-likes,
        .user-total-views {
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
        .user-total-likes {
          margin: 10px 0;
        }
        .user-total-articles {
          .icon {
            color: #1b9cfc;
          }
        }
        .user-total-views {
          .icon {
            color: #ff9f1a;
          }
        }
      }
    }
    .user-otherinfo-box {
      margin-top: 20px;
      font-size: 16px;
      div {
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 5px;
        border-top: 1px solid rgba(230, 230, 231, 0.7);
        a {
          color: #000000;
        }
      }
      .join-date {
        border-bottom: 1px solid rgba(230, 230, 231, 0.7);
      }
    }
    .user-hot-articles-box {
      margin-top: 20px;
      background: #ffffff;
      border-radius: 2px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      .user-hot-articles-title {
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
      .user-hot-articles-content {
        padding: 15px;
        min-height: 130px;
        .user-hot-article {
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
      .user-no-hot-articles {
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
  }
}
</style>
