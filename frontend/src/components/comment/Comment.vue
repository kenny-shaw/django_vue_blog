<template>
  <!-- 评论区域 -->
  <div class="comments-container">
    <!-- 当前用户对该文章的评论框 -->
    <div class="my-reply">
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
        <div class="comment-action-box" v-show="myReplyBtnShow">
          <el-button type="primary" size="mini" @click="postComment()"
            >评论</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Clickoutside from 'element-ui/src/utils/clickoutside'
export default {
  data() {
    return {
      user: {},
      // 输入我的评论内容
      inputMyComment: ''
    }
  },
  directives: { Clickoutside }
}
</script>
<style lang="less" scoped></style>
