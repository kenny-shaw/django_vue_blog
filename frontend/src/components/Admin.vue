<template>
  <el-container>
    <el-aside :width="isAdminNavCollapse ? '64px' : '200px'">
      <a
        href=""
        :class="[
          'icon',
          'iconfont',
          isAdminNavCollapse ? 'toggle-btn' : 'toggle-btn-border',
          isAdminNavCollapse ? 'iconicon-test61' : 'iconicon-test59'
        ]"
        @click.prevent="toggleAdminNav"
      ></a>
      <el-menu
        :default-active="activeAdminNavIndex"
        :collapse="isAdminNavCollapse"
        :collapse-transition="false"
        :router="true"
      >
        <!-- <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>用户管理</span>
          </template>

          <el-menu-item index="1-1">选项1</el-menu-item>
          <el-menu-item index="1-2">选项2</el-menu-item>
        </el-submenu> -->
        <el-menu-item index="/admin/user">
          <i class="el-icon-user-solid"></i>
          <span slot="title">用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/tag">
          <i class="el-icon-menu"></i>
          <span slot="title">标签管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/column">
          <i
            :class="[
              'icon',
              'iconfont',
              'iconhuati1',
              isAdminNavCollapse ? 'icon-collapesed' : 'no-icon-collapesed'
            ]"
          ></i>
          <span slot="title">栏目管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/lover">
          <i
            :class="[
              'icon',
              'iconfont',
              'iconaixin1',
              isAdminNavCollapse ? 'icon-collapesed' : 'no-icon-collapesed'
            ]"
          ></i>
          <span slot="title">情侣管理</span>
        </el-menu-item>
        <el-menu-item index="4">
          <i
            :class="[
              'icon',
              'iconfont',
              'iconchuangzuo1',
              isAdminNavCollapse ? 'icon-collapesed' : 'no-icon-collapesed'
            ]"
          ></i>
          <span slot="title">文章管理</span>
        </el-menu-item>
      </el-menu></el-aside
    >
    <el-main><router-view></router-view></el-main>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      // 默认激活的导航
      activeAdminNavIndex: '1',
      isAdminNavCollapse: true
    }
  },
  methods: {
    toggleAdminNav() {
      this.isAdminNavCollapse = !this.isAdminNavCollapse
    },
    handleAdminNavOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handlehandleAdminNavClose(key, keyPath) {
      console.log(key, keyPath)
    }
  },
  watch: {
    $route: {
      handler: function(val, oldVal) {
        if (val.path === '/admin/user' || val.path === '/admin') {
          this.activeAdminNavIndex = '/admin/user'
        } else if (val.path === '/admin/tag') {
          this.activeAdminNavIndex = '/admin/tag'
        } else if (val.path === '/admin/column') {
          this.activeAdminNavIndex = '/admin/column'
        } else if (val.path === '/admin/lover') {
          this.activeAdminNavIndex = '/admin/lover'
        }
      },
      immediate: true
    }
  }
}
</script>
<style lang="less" scoped>
.el-main {
  margin: 0;
  padding: 0;
}
.el-container {
  height: 100%;
  .el-aside {
    display: flex;
    flex-direction: column;
    .toggle-btn {
      background: #fff;
      font-size: 24px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .toggle-btn-border {
      background: #fff;
      font-size: 24px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-right: solid 1px #e6e6e6;
    }
    .el-menu {
      // height: 100%;
      flex: 1;
      .el-menu-item {
        i.icon-collapesed {
          font-size: 18px;
          line-height: 1;
          margin: 0;
          padding: 0 3px;
        }
        i.no-icon-collapesed {
          font-size: 18px;
          line-height: 1;
          margin: 0 5px 0 0;
          padding: 0 3px;
        }
      }
    }
  }
}
</style>
