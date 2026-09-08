<template>
  <view class="yl-navbar" :class="{ 'yl-navbar--fixed': fixed, 'yl-navbar--border': border }">
    <view class="yl-navbar__bar" :class="{ 'yl-navbar--transparent': transparent }" :style="barStyle">
      <view class="yl-navbar__side yl-navbar__side--left">
        <view
          v-if="back"
          class="yl-navbar__btn"
          :class="{ 'yl-navbar__btn--light': light, 'yl-navbar__btn--float': float }"
          hover-class="yl-hover"
          @click="handleBack"
        >
          <uni-icons type="left" size="22" :color="iconColor"></uni-icons>
        </view>
        <slot name="left"></slot>
      </view>

      <view class="yl-navbar__center">
        <slot name="title">
          <text class="yl-navbar__title" :style="{ color: textColor }">{{ title }}</text>
        </slot>
      </view>

      <view class="yl-navbar__side yl-navbar__side--right" :style="{ minWidth: rightWidth + 'px' }">
        <slot name="right"></slot>
      </view>
    </view>

    <view v-if="fixed && placeholder" class="yl-navbar__placeholder" :style="{ height: totalHeight + 'px' }"></view>
  </view>
</template>

<script>
/**
 * yl-navbar 自定义导航栏
 * - 自动处理状态栏高度 / 微信小程序胶囊避让
 * - 支持透明（沉浸式）、浅色图标、悬浮返回按钮
 */
export default {
  name: 'YlNavbar',
  props: {
    title: { type: String, default: '' },
    back: { type: Boolean, default: true },
    fixed: { type: Boolean, default: true },
    placeholder: { type: Boolean, default: true },
    transparent: { type: Boolean, default: false },
    light: { type: Boolean, default: false },
    float: { type: Boolean, default: false },
    border: { type: Boolean, default: false },
    bgColor: { type: String, default: '' },
    color: { type: String, default: '' },
    backTo: { type: String, default: '' }
  },
  emits: ['back'],
  data() {
    return {
      statusBarHeight: 0,
      navHeight: 44,
      rightWidth: 44
    }
  },
  computed: {
    totalHeight() {
      return this.statusBarHeight + this.navHeight
    },
    barStyle() {
      const style = {
        paddingTop: this.statusBarHeight + 'px',
        height: this.totalHeight + 'px'
      }
      if (this.bgColor) style.background = this.bgColor
      return style
    },
    iconColor() {
      if (this.color) return this.color
      return this.light ? '#FFFFFF' : '#1A1F1C'
    },
    textColor() {
      return this.iconColor
    }
  },
  created() {
    try {
      const info = uni.getSystemInfoSync()
      this.statusBarHeight = info.statusBarHeight || 0
    } catch (e) {}

    // #ifdef MP-WEIXIN
    try {
      const rect = uni.getMenuButtonBoundingClientRect()
      const info = uni.getSystemInfoSync()
      if (rect && rect.height) {
        this.navHeight = rect.height + (rect.top - this.statusBarHeight) * 2
        this.rightWidth = info.windowWidth - rect.left + 8
      }
    } catch (e) {}
    // #endif
  },
  methods: {
    handleBack() {
      this.$emit('back')
      if (this.backTo) {
        uni.reLaunch({ url: this.backTo })
        return
      }
      const pages = getCurrentPages()
      if (pages.length > 1) {
        uni.navigateBack({ delta: 1 })
      } else {
        uni.reLaunch({ url: '/pages/main/main' })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.yl-navbar {
  width: 100%;

  &__bar {
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
    padding-left: 16rpx;
    padding-right: 16rpx;
    background: $yl-bg;
    transition: background 0.25s ease;
  }

  &--fixed &__bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 900;
  }

  &--border &__bar {
    border-bottom: 1rpx solid $yl-border;
  }

  &--transparent {
    background: transparent !important;
  }

  &__side {
    display: flex;
    align-items: center;
    min-width: 88rpx;
    height: 100%;

    &--right {
      justify-content: flex-end;
    }
  }

  &__center {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 0 8rpx;
  }

  &__title {
    font-size: 34rpx;
    font-weight: 600;
    color: $yl-text-1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__btn {
    width: 72rpx;
    height: 72rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    &--float {
      background: rgba(255, 255, 255, 0.92);
      box-shadow: 0 6rpx 18rpx rgba(0, 0, 0, 0.12);
    }

    &--light.yl-navbar__btn--float {
      background: rgba(255, 255, 255, 0.18);
      backdrop-filter: blur(10px);
      box-shadow: none;
    }
  }

  &__placeholder {
    width: 100%;
  }
}
</style>
