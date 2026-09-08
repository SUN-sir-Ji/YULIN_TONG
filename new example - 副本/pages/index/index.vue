<template>
  <view class="splash">
    <!-- 背景装饰 -->
    <view class="splash__bg">
      <view class="splash__orb splash__orb--1"></view>
      <view class="splash__orb splash__orb--2"></view>
      <view class="splash__orb splash__orb--3"></view>
      <view class="splash__leaf splash__leaf--1"></view>
      <view class="splash__leaf splash__leaf--2"></view>
      <view class="splash__leaf splash__leaf--3"></view>
      <view class="splash__grid"></view>
    </view>

    <!-- 品牌区 -->
    <view class="splash__brand" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="splash__logo-wrap yl-anim-pop">
        <view class="splash__logo-glow"></view>
        <view class="splash__logo-tile">
          <image class="splash__logo" src="/static/logo.png" mode="aspectFit"></image>
        </view>
      </view>
      <text class="splash__name yl-anim-up yl-delay-1">雨林通</text>
      <text class="splash__en yl-anim-up yl-delay-2">RAINFOREST LINK</text>
      <text class="splash__slogan yl-anim-up yl-delay-3">拍一拍，认识身边的每一株植物</text>

      <view class="splash__pills yl-anim-up yl-delay-4">
        <view class="splash__pill">
          <uni-icons type="scan" size="14" color="#CDEFDB"></uni-icons>
          <text>AI 智能识别</text>
        </view>
        <view class="splash__pill">
          <uni-icons type="images" size="14" color="#CDEFDB"></uni-icons>
          <text>植物图鉴</text>
        </view>
        <view class="splash__pill">
          <uni-icons type="map" size="14" color="#CDEFDB"></uni-icons>
          <text>分类导航</text>
        </view>
      </view>
    </view>

    <!-- 底部操作区 -->
    <view class="splash__panel yl-safe-bottom" :class="{ 'is-show': ready }">
      <view v-if="autoLogin" class="splash__auto">
        <view class="yl-spinner splash__auto-spinner"></view>
        <text class="splash__auto-text">欢迎回来，正在进入…</text>
      </view>

      <block v-else>
        <text class="splash__panel-title">开始探索</text>
        <text class="splash__panel-desc">登录后可同步识别记录，随时随地查阅植物图鉴</text>

        <button class="yl-btn yl-btn--white splash__btn" hover-class="yl-press" @click="go('/pages/login/login')">
          <uni-icons type="person-filled" size="18" color="#146C43"></uni-icons>
          <text class="splash__btn-text">登 录</text>
        </button>
        <button class="yl-btn yl-btn--outline splash__btn" hover-class="yl-press" @click="go('/pages/login/register')">
          <uni-icons type="personadd" size="18" color="#FFFFFF"></uni-icons>
          <text class="splash__btn-text">注 册 账 号</text>
        </button>

        <view class="splash__guest" hover-class="yl-hover" @click="guest">
          <text>先随便逛逛</text>
          <uni-icons type="right" size="14" color="rgba(255,255,255,0.7)"></uni-icons>
        </view>
      </block>
    </view>
  </view>
</template>

<script>
import { isLoggedIn } from '@/utils/auth.js'

export default {
  data() {
    return {
      statusBarHeight: 0,
      ready: false,
      autoLogin: false
    }
  },
  onLoad() {
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 0
    } catch (e) {}

    this.autoLogin = isLoggedIn()
    setTimeout(() => {
      this.ready = true
    }, 350)

    if (this.autoLogin) {
      setTimeout(() => {
        uni.reLaunch({ url: '/pages/main/main' })
      }, 1400)
    }
  },
  methods: {
    go(url) {
      uni.navigateTo({ url })
    },
    guest() {
      uni.reLaunch({ url: '/pages/main/main' })
    }
  }
}
</script>

<style lang="scss" scoped>
.splash {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: $yl-gradient-hero;
  display: flex;
  flex-direction: column;

  &__bg {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }

  &__orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(2rpx);

    &--1 {
      width: 520rpx;
      height: 520rpx;
      right: -180rpx;
      top: -120rpx;
      background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0) 70%);
    }

    &--2 {
      width: 420rpx;
      height: 420rpx;
      left: -160rpx;
      top: 46%;
      background: radial-gradient(circle at 60% 40%, rgba(111, 211, 154, 0.35), rgba(111, 211, 154, 0) 70%);
    }

    &--3 {
      width: 300rpx;
      height: 300rpx;
      right: -60rpx;
      bottom: 30%;
      background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0) 70%);
    }
  }

  &__leaf {
    position: absolute;
    border-radius: 100% 0 100% 0;
    background: rgba(255, 255, 255, 0.06);
    border: 2rpx solid rgba(255, 255, 255, 0.1);

    &--1 {
      width: 360rpx;
      height: 360rpx;
      left: -120rpx;
      top: 120rpx;
      transform: rotate(35deg);
      animation: yl-float 6s ease-in-out infinite;
    }

    &--2 {
      width: 240rpx;
      height: 240rpx;
      right: 40rpx;
      top: 42%;
      transform: rotate(-25deg);
      animation: yl-float 7s ease-in-out infinite;
      animation-delay: 1s;
    }

    &--3 {
      width: 180rpx;
      height: 180rpx;
      left: 30%;
      top: 58%;
      transform: rotate(60deg);
      animation: yl-float 5s ease-in-out infinite;
      animation-delay: 2s;
    }
  }

  &__grid {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 50%;
    background-image: linear-gradient(rgba(255, 255, 255, 0.05) 1rpx, transparent 1rpx),
      linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1rpx, transparent 1rpx);
    background-size: 80rpx 80rpx;
    mask-image: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
    -webkit-mask-image: linear-gradient(to top, rgba(0, 0, 0, 0.6), transparent);
  }

  &__brand {
    position: relative;
    z-index: 2;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-bottom: 120rpx;
  }

  &__logo-wrap {
    position: relative;
    width: 220rpx;
    height: 220rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 40rpx;
  }

  &__logo-glow {
    position: absolute;
    width: 260rpx;
    height: 260rpx;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0) 70%);
  }

  &__logo-tile {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    border-radius: 48rpx;
    background: $yl-primary-dark;
    box-shadow: 0 24rpx 60rpx rgba(0, 0, 0, 0.3), 0 0 0 6rpx rgba(255, 255, 255, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  &__logo {
    width: 200rpx;
    height: 200rpx;
    display: block;
  }

  &__name {
    font-size: 72rpx;
    font-weight: 800;
    color: #fff;
    letter-spacing: 12rpx;
    text-indent: 12rpx;
    text-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.18);
  }

  &__en {
    margin-top: 8rpx;
    font-size: 22rpx;
    letter-spacing: 8rpx;
    color: rgba(255, 255, 255, 0.72);
  }

  &__slogan {
    margin-top: 28rpx;
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.85);
  }

  &__pills {
    display: flex;
    margin-top: 44rpx;
  }

  &__pill {
    display: flex;
    align-items: center;
    height: 56rpx;
    padding: 0 22rpx;
    margin: 0 8rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.14);
    border: 1rpx solid rgba(255, 255, 255, 0.22);
    font-size: 22rpx;
    color: #e8f7ee;

    text {
      margin-left: 8rpx;
    }
  }

  /* 底部面板 */
  &__panel {
    position: relative;
    z-index: 3;
    padding: 48rpx 48rpx 56rpx;
    background: rgba(14, 59, 46, 0.55);
    backdrop-filter: blur(24px);
    border-top-left-radius: 48rpx;
    border-top-right-radius: 48rpx;
    border-top: 1rpx solid rgba(255, 255, 255, 0.15);
    transform: translateY(100%);
    opacity: 0;
    transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.5s ease;

    &.is-show {
      transform: translateY(0);
      opacity: 1;
    }
  }

  &__panel-title {
    display: block;
    font-size: 36rpx;
    font-weight: 700;
    color: #fff;
  }

  &__panel-desc {
    display: block;
    margin-top: 8rpx;
    margin-bottom: 36rpx;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.7);
  }

  &__btn {
    margin-bottom: 20rpx;
  }

  &__btn-text {
    margin-left: 12rpx;
  }

  &__guest {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 12rpx;
    height: 64rpx;
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.75);

    text {
      margin-right: 4rpx;
    }
  }

  &__auto {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 160rpx;
  }

  &__auto-spinner {
    border-color: rgba(255, 255, 255, 0.25);
    border-top-color: #fff;
    margin-right: 16rpx;
  }

  &__auto-text {
    font-size: 28rpx;
    color: #fff;
  }
}
</style>
