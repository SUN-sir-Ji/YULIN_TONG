<template>
  <view class="yl-tabbar">
    <view class="yl-tabbar__panel">
      <view class="yl-tabbar__inner">
        <block v-for="item in items" :key="item.key">
          <!-- 中间凸起的识别按钮 -->
          <view v-if="item.center" class="yl-tabbar__item yl-tabbar__item--center" @click="$emit('scan')">
            <view class="yl-tabbar__scan" hover-class="yl-press" hover-stay-time="120">
              <view class="yl-tabbar__scan-ring"></view>
              <uni-icons type="scan" size="30" color="#FFFFFF"></uni-icons>
            </view>
            <text class="yl-tabbar__label yl-tabbar__label--center">{{ item.text }}</text>
          </view>

          <view
            v-else
            class="yl-tabbar__item"
            :class="{ 'is-active': current === item.index }"
            hover-class="yl-hover"
            hover-stay-time="80"
            @click="onTap(item.index)"
          >
            <view class="yl-tabbar__icon">
              <uni-icons
                :type="current === item.index ? item.iconActive : item.icon"
                size="24"
                :color="current === item.index ? activeColor : inactiveColor"
              ></uni-icons>
              <view v-if="item.badge && badges[item.key]" class="yl-tabbar__badge">{{ badges[item.key] }}</view>
            </view>
            <text class="yl-tabbar__label">{{ item.text }}</text>
            <view class="yl-tabbar__dot" :class="{ 'is-active': current === item.index }"></view>
          </view>
        </block>
      </view>
      <view class="yl-tabbar__safe"></view>
    </view>
  </view>
</template>

<script>
/**
 * yl-tabbar 自定义底部导航
 * 首页 / 图鉴 / [识别] / 记录 / 我的
 */
export default {
  name: 'YlTabbar',
  props: {
    current: { type: Number, default: 0 },
    badges: { type: Object, default: () => ({}) }
  },
  emits: ['change', 'scan'],
  data() {
    return {
      activeColor: '#1DA462',
      inactiveColor: '#9AA5A0',
      items: [
        { key: 'home', index: 0, text: '首页', icon: 'home', iconActive: 'home-filled' },
        { key: 'atlas', index: 1, text: '图鉴', icon: 'images', iconActive: 'images-filled' },
        { key: 'scan', center: true, text: '识别' },
        { key: 'history', index: 2, text: '记录', icon: 'calendar', iconActive: 'calendar-filled', badge: true },
        { key: 'mine', index: 3, text: '我的', icon: 'person', iconActive: 'person-filled' }
      ]
    }
  },
  methods: {
    onTap(index) {
      if (index === this.current) return
      this.$emit('change', index)
    }
  }
}
</script>

<style lang="scss" scoped>
.yl-tabbar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 950;
  pointer-events: none;

  &__panel {
    pointer-events: auto;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(20px);
    border-top-left-radius: 36rpx;
    border-top-right-radius: 36rpx;
    box-shadow: 0 -8rpx 40rpx rgba(14, 59, 46, 0.1);
  }

  &__inner {
    display: flex;
    align-items: flex-end;
    height: $yl-tabbar-height;
    padding: 0 12rpx;
  }

  &__safe {
    height: constant(safe-area-inset-bottom);
    height: env(safe-area-inset-bottom);
  }

  &__item {
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;

    &--center {
      justify-content: flex-end;
      padding-bottom: 10rpx;
    }
  }

  &__icon {
    position: relative;
    height: 48rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
  }

  &__item.is-active &__icon {
    transform: translateY(-4rpx);
  }

  &__label {
    margin-top: 4rpx;
    font-size: 22rpx;
    color: $yl-text-3;
    line-height: 1;
    transition: color 0.2s ease;

    &--center {
      margin-top: 8rpx;
      color: $yl-primary-dark;
      font-weight: 600;
    }
  }

  &__item.is-active &__label {
    color: $yl-primary;
    font-weight: 600;
  }

  &__dot {
    position: absolute;
    bottom: 6rpx;
    width: 0;
    height: 6rpx;
    border-radius: 3rpx;
    background: $yl-primary;
    transition: width 0.25s ease;

    &.is-active {
      width: 28rpx;
    }
  }

  &__badge {
    position: absolute;
    top: -6rpx;
    right: -22rpx;
    min-width: 30rpx;
    height: 30rpx;
    padding: 0 8rpx;
    border-radius: 15rpx;
    background: $yl-danger;
    color: #fff;
    font-size: 18rpx;
    line-height: 30rpx;
    text-align: center;
    border: 2rpx solid #fff;
  }

  /* 中间凸起按钮 */
  &__scan {
    position: relative;
    width: 108rpx;
    height: 108rpx;
    border-radius: 50%;
    margin-top: -60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $yl-gradient;
    box-shadow: 0 14rpx 30rpx rgba(29, 164, 98, 0.45);
    transition: transform 0.15s ease;
  }

  &__scan-ring {
    position: absolute;
    left: -10rpx;
    top: -10rpx;
    right: -10rpx;
    bottom: -10rpx;
    border-radius: 50%;
    border: 10rpx solid rgba(255, 255, 255, 0.96);
    z-index: -1;
  }
}
</style>
