<template>
  <view class="about yl-page">
    <yl-navbar title="关于雨林通" border></yl-navbar>

    <view class="yl-container about__body">
      <!-- 品牌卡片 -->
      <view class="brand yl-anim-up">
        <view class="brand__orb brand__orb--1"></view>
        <view class="brand__orb brand__orb--2"></view>
        <view class="brand__logo">
          <image class="brand__logo-img" src="/static/logo.png" mode="aspectFit"></image>
        </view>
        <text class="brand__name">雨林通</text>
        <text class="brand__en">RAINFOREST LINK</text>
        <view class="brand__version">
          <text>Version {{ version }}</text>
        </view>
        <text class="brand__slogan">拍一拍，认识身边的每一株植物</text>
      </view>

      <!-- 简介 -->
      <view class="card yl-anim-up yl-delay-1">
        <view class="card__head">
          <text class="card__title">应用简介</text>
        </view>
        <text class="card__text">
          雨林通是一款基于深度学习的植物识别应用。上传或拍摄植物照片，YOLO 模型会给出最可能的物种及置信度；同时内置按「门 → 纲 → 目 → 科 → 属」组织的植物图鉴，可逐级浏览并查看形态特征、生长环境、分布与用途等资料。
        </text>
      </view>

      <!-- 核心功能 -->
      <view class="card yl-anim-up yl-delay-2">
        <view class="card__head">
          <text class="card__title">核心功能</text>
        </view>
        <view v-for="f in features" :key="f.title" class="feature">
          <view class="feature__icon" :style="{ background: f.bg }">
            <uni-icons :type="f.icon" size="20" :color="f.color"></uni-icons>
          </view>
          <view class="feature__body">
            <text class="feature__title">{{ f.title }}</text>
            <text class="feature__desc">{{ f.desc }}</text>
          </view>
        </view>
      </view>

      <!-- 技术栈 -->
      <view class="card yl-anim-up yl-delay-3">
        <view class="card__head">
          <text class="card__title">技术栈</text>
        </view>
        <view class="stack">
          <view v-for="s in stack" :key="s" class="stack__chip">
            <text>{{ s }}</text>
          </view>
        </view>
      </view>

      <!-- 链接 -->
      <view class="card yl-anim-up yl-delay-4">
        <view class="card__head">
          <text class="card__title">项目与反馈</text>
        </view>
        <view class="link" hover-class="yl-hover" @click="copy(repo, '仓库地址已复制')">
          <view class="link__icon" style="background: #F1F5F3">
            <uni-icons type="link" size="18" color="#1A1F1C"></uni-icons>
          </view>
          <view class="link__body">
            <text class="link__title">GitHub 开源仓库</text>
            <text class="link__value yl-ellipsis">{{ repo }}</text>
          </view>
          <uni-icons type="paperclip" size="16" color="#9AA5A0"></uni-icons>
        </view>
        <view class="link" hover-class="yl-hover" @click="copy(baseUrl, '服务器地址已复制')">
          <view class="link__icon" style="background: #E8F0FE">
            <uni-icons type="cloud-upload-filled" size="18" color="#3B82F6"></uni-icons>
          </view>
          <view class="link__body">
            <text class="link__title">当前服务器</text>
            <text class="link__value yl-ellipsis">{{ baseUrl }}</text>
          </view>
          <uni-icons type="paperclip" size="16" color="#9AA5A0"></uni-icons>
        </view>
      </view>

      <view class="about__footer">
        <text>© {{ year }} 雨林通 · RAINFOREST LINK</text>
        <text>仅供学习与研究使用</text>
      </view>
      <view class="yl-safe-bottom"></view>
    </view>
  </view>
</template>

<script>
import { getBaseUrl } from '@/utils/apiConfig.js'

export default {
  data() {
    return {
      version: '2.0.0',
      year: new Date().getFullYear(),
      repo: 'https://github.com/SUN-sir-Ji/YULIN_TONG',
      baseUrl: '',
      features: [
        { title: 'AI 植物识别', desc: '基于 Ultralytics YOLO 的物种识别，返回 Top 5 候选与置信度', icon: 'scan', color: '#1DA462', bg: '#E3F6EA' },
        { title: '植物图鉴', desc: '五级分类导航，支持在结果中按中文名 / 拉丁名 / 别名搜索', icon: 'images-filled', color: '#3B82F6', bg: '#E8F0FE' },
        { title: '识别记录', desc: '识别结果自动保存到本机，随时回顾候选列表', icon: 'calendar-filled', color: '#F5A524', bg: '#FFF4DF' },
        { title: '账号体系', desc: '邮箱验证码注册、用户 ID 登录与找回密码', icon: 'person-filled', color: '#8B5CF6', bg: '#F1EBFF' }
      ],
      stack: ['uni-app · Vue 3', 'uni-ui / uni-icons', 'FastAPI + Uvicorn', 'SQLAlchemy 2.x', 'MySQL 5.7', 'Ultralytics YOLO', 'JWT 鉴权']
    }
  },
  onLoad() {
    this.baseUrl = getBaseUrl()
  },
  methods: {
    copy(text, tip) {
      uni.setClipboardData({
        data: text,
        success: () => uni.showToast({ title: tip || '已复制', icon: 'none' })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.about {
  &__body {
    padding-top: 16rpx;
    padding-bottom: 40rpx;
  }

  &__footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 40rpx;
    font-size: 22rpx;
    line-height: 1.8;
    color: $yl-text-4;
  }
}

.brand {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 56rpx 32rpx 44rpx;
  border-radius: $yl-radius-xl;
  background: $yl-gradient-hero;
  overflow: hidden;
  box-shadow: $yl-shadow-primary;

  &__orb {
    position: absolute;
    border-radius: 50%;

    &--1 {
      width: 360rpx;
      height: 360rpx;
      right: -120rpx;
      top: -140rpx;
      background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0) 70%);
    }

    &--2 {
      width: 260rpx;
      height: 260rpx;
      left: -100rpx;
      bottom: -100rpx;
      background: radial-gradient(circle at 50% 50%, rgba(111, 211, 154, 0.4), rgba(111, 211, 154, 0) 70%);
    }
  }

  &__logo {
    position: relative;
    width: 168rpx;
    height: 168rpx;
    border-radius: 40rpx;
    background: $yl-primary-dark;
    box-shadow: 0 20rpx 50rpx rgba(0, 0, 0, 0.3), 0 0 0 6rpx rgba(255, 255, 255, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  &__logo-img {
    width: 168rpx;
    height: 168rpx;
    display: block;
  }

  &__name {
    margin-top: 28rpx;
    font-size: 48rpx;
    font-weight: 800;
    color: #fff;
    letter-spacing: 8rpx;
    text-indent: 8rpx;
  }

  &__en {
    margin-top: 4rpx;
    font-size: 20rpx;
    letter-spacing: 6rpx;
    color: rgba(255, 255, 255, 0.72);
  }

  &__version {
    margin-top: 20rpx;
    height: 44rpx;
    padding: 0 20rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.2);
    border: 1rpx solid rgba(255, 255, 255, 0.35);
    display: flex;
    align-items: center;
    font-size: 22rpx;
    color: #fff;
  }

  &__slogan {
    margin-top: 20rpx;
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.85);
  }
}

.card {
  margin-top: 24rpx;
  padding: 28rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;

  &__head {
    display: flex;
    align-items: center;
    margin-bottom: 16rpx;
  }

  &__title {
    font-size: 30rpx;
    font-weight: 700;
    color: $yl-text-1;
    position: relative;
    padding-left: 18rpx;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 6rpx;
      bottom: 6rpx;
      width: 8rpx;
      border-radius: 4rpx;
      background: $yl-gradient;
    }
  }

  &__text {
    display: block;
    font-size: 27rpx;
    line-height: 1.85;
    color: $yl-text-2;
    text-align: justify;
  }
}

.feature {
  display: flex;
  align-items: flex-start;
  padding: 18rpx 0;
  border-bottom: 1rpx solid $yl-border;

  &:last-child {
    border-bottom: none;
    padding-bottom: 4rpx;
  }

  &__icon {
    width: 64rpx;
    height: 64rpx;
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20rpx;
    flex-shrink: 0;
  }

  &__body {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  &__title {
    font-size: 28rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__desc {
    margin-top: 4rpx;
    font-size: 24rpx;
    line-height: 1.6;
    color: $yl-text-3;
  }
}

.stack {
  display: flex;
  flex-wrap: wrap;

  &__chip {
    height: 56rpx;
    padding: 0 22rpx;
    margin: 0 12rpx 12rpx 0;
    border-radius: $yl-radius-pill;
    background: $yl-bg-input;
    color: $yl-text-2;
    font-size: 24rpx;
    display: flex;
    align-items: center;
  }
}

.link {
  display: flex;
  align-items: center;
  padding: 18rpx 0;
  border-bottom: 1rpx solid $yl-border;

  &:last-child {
    border-bottom: none;
    padding-bottom: 4rpx;
  }

  &__icon {
    width: 64rpx;
    height: 64rpx;
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20rpx;
    flex-shrink: 0;
  }

  &__body {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    margin-right: 12rpx;
  }

  &__title {
    font-size: 27rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__value {
    margin-top: 4rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }
}
</style>
