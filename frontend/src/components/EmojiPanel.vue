<template>
  <div class="emoji-panel-wrap" v-clickoutside="closeEmojiPanel">
    <span
      class="emoji-item-common"
      v-for="(item, index) in emojis"
      :key="index"
      :class="['emoji-' + item]"
      @click="handleEmojiClick(item)"
    ></span>
  </div>
</template>
<script>
import Clickoutside from 'element-ui/src/utils/clickoutside'
export default {
  data() {
    return {
      // 控制panel显示或隐藏
      flag: false,
      emojis: [
        'angry',
        'anguished',
        'astonished',
        'blush',
        'cold_sweat',
        'confounded',
        'confused',
        'cry',
        'disappointed',
        'disappointed_relieved',
        'dizzy_face',
        'expressionless',
        'fearful',
        'flushed',
        'frowning',
        'grimacing',
        'grin',
        'grinning',
        'heart_eyes',
        'hushed',
        'innocent',
        'joy',
        'kissing_closed_eyes',
        'kissing_heart',
        'laughing',
        'neutral_face',
        'no_mouth',
        'open_mouth',
        'pensive',
        'persevere',
        'relaxed',
        'relieved',
        'sleepy',
        'smile',
        'smiley',
        'smirk',
        'sob',
        'stuck_out_tongue',
        'sunglasses',
        'sweat',
        'sweat_smile',
        'scream',
        'wink',
        'unamused',
        'satisfied',
        'worried',
        'stuck_out_tongue_closed_eyes',
        'weary',
        'yum',
        'tired_face',
        'triumph',
        'stuck_out_tongue_winking_eye'
      ]
    }
  },

  directives: { Clickoutside },
  methods: {
    closeEmojiPanel() {
      if (this.flag === false) {
        this.flag = true
      } else {
        this.$emit('onClose')
      }
    },
    handleEmojiClick(text) {
      this.$emit('emojiClick', text)
    }
  }
}
</script>
<style lang="less" scoped>
.emoji-panel-wrap {
  box-sizing: border-box;
  border: 1px solid #cccccc;
  border-radius: 5px;
  background-color: #ffffff;
  position: absolute;
  left: 0px;
  right: 30%;
  top: 32px;
  padding: 10px 0 5px 5px;
  .emoji-item-common {
    background: url('../assets/image/emoji_sprite.png');
    display: inline-block;
    zoom: 0.5;

    &:hover {
      cursor: pointer;
      // zoom: 0.6;
    }
  }
}
</style>
