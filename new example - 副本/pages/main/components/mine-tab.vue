<template>
  <scroll-view scroll-y class="mine" :show-scrollbar="false">
    <!-- 头部 -->
    <view class="mine__hero" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="mine__orb mine__orb--1"></view>
      <view class="mine__orb mine__orb--2"></view>

      <view class="mine__user">
        <view class="mine__avatar">
          <text v-if="user" class="mine__avatar-text">{{ avatarChar }}</text>
          <uni-icons v-else type="person-filled" size="40" color="#FFFFFF"></uni-icons>
          <view class="mine__avatar-dot"></view>
        </view>
        <view class="mine__info">
          <text class="mine__name">{{ user ? `用户 ${user.username}` : '未登录' }}</text>
          <text class="mine__sub">{{ user ? `ID：${user.userId}` : '登录后可同步识别记录' }}</text>
          <view v-if="user" class="mine__badge">
            <uni-icons type="vip-filled" size="12" color="#F5A524"></uni-icons>
            <text>雨林探索者</text>
          </view>
        </view>
        <view v-if="!user" class="mine__login" hover-class="yl-press" @click="toLogin">
          <text>登录 / 注册</text>
        </view>
      </view>

      <view class="stats">
        <view class="stats__item" hover-class="yl-hover" @click="$emit('switch', 2)">
          <text class="stats__num">{{ stats.count }}</text>
          <text class="stats__label">识别次数</text>
        </view>
        <view class="stats__item" hover-class="yl-hover" @click="$emit('switch', 2)">
          <text class="stats__num">{{ stats.species }}</text>
          <text class="stats__label">识别物种</text>
        </view>
        <view class="stats__item">
          <text class="stats__num">{{ days }}</text>
          <text class="stats__label">使用天数</text>
        </view>
      </view>
    </view>

    <view class="yl-container mine__content">
      <!-- 功能菜单 -->
      <view class="menu">
        <view class="menu__item" hover-class="menu__item--hover" @click="$emit('switch', 2)">
          <view class="menu__icon" style="background: #E3F6EA">
            <uni-icons type="calendar-filled" size="20" color="#1DA462"></uni-icons>
          </view>
          <text class="menu__text">识别记录</text>
          <text class="menu__value">{{ stats.count }} 条</text>
          <uni-icons type="right" size="14" color="#C3CBC7"></uni-icons>
        </view>
        <view class="menu__item" hover-class="menu__item--hover" @click="$emit('switch', 1)">
          <view class="menu__icon" style="background: #F1EBFF">
            <uni-icons type="map-filled" size="20" color="#8B5CF6"></uni-icons>
          </view>
          <text class="menu__text">植物图鉴</text>
          <text class="menu__value">分类浏览</text>
          <uni-icons type="right" size="14" color="#C3CBC7"></uni-icons>
        </view>
      </view>

      <view class="menu">
        <view class="menu__item" hover-class="menu__item--hover" @click="editServer">
          <view class="menu__icon" style="background: #E8F0FE">
            <uni-icons type="cloud-upload-filled" size="20" color="#3B82F6"></uni-icons>
          </view>
          <text class="menu__text">服务器地址</text>
          <text class="menu__value yl-ellipsis">{{ baseUrlShort }}</text>
          <uni-icons type="right" size="14" color="#C3CBC7"></uni-icons>
        </view>
        <view class="menu__item" hover-class="menu__item--hover" @click="clearCache">
          <view class="menu__icon" style="background: #FFF4DF">
            <uni-icons type="trash-filled" size="20" color="#F5A524"></uni-icons>
          </view>
          <text class="menu__text">清除本地缓存</text>
          <text class="menu__value">记录与偏好</text>
          <uni-icons type="right" size="14" color="#C3CBC7"></uni-icons>
        </view>
        <view class="menu__item" hover-class="menu__item--hover" @click="toAbout">
          <view class="menu__icon" style="background: #E3F6EA">
            <uni-icons type="info-filled" size="20" color="#1DA462"></uni-icons>
          </view>
          <text class="menu__text">关于雨林通</text>
          <text class="menu__value">v2.0.0</text>
          <uni-icons type="right" size="14" color="#C3CBC7"></uni-icons>
        </view>
      </view>

      <button v-if="user" class="yl-btn yl-btn--danger mine__logout" hover-class="yl-press" @click="logout">
        <uni-icons type="closeempty" size="18" color="#E5484D"></uni-icons>
        <text class="mine__logout-text">退出登录</text>
      </button>

      <view class="mine__footer">
        <text>雨林通 RAINFOREST LINK</text>
        <text>FastAPI + YOLO + uni-app</text>
      </view>
    </view>

    <view class="yl-tab-spacer"></view>
  </scroll-view>
</template>

<script>
import { getUserInfo, logout as doLogout, getLoginTime } from '@/utils/auth.js'
import { getStats, clearRecords } from '@/utils/history.js'
import { getBaseUrl, setBaseUrl } from '@/utils/apiConfig.js'

export default {
  name: 'MineTab',
  emits: ['switch'],
  data() {
    return {
      statusBarHeight: 0,
      user: null,
      stats: { count: 0, species: 0 },
      baseUrl: ''
    }
  },
  computed: {
    avatarChar() {
      const s = String((this.user && this.user.username) || '')
      return s.slice(-2) || '林'
    },
    baseUrlShort() {
      return (this.baseUrl || '').replace(/^https?:\/\//, '')
    },
    days() {
      const t = getLoginTime()
      if (!t) return this.user ? 1 : 0
      return Math.max(1, Math.floor((Date.now() - t) / 86400000) + 1)
    }
  },
  created() {
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 0
    } catch (e) {}
    this.refresh()
  },
  methods: {
    refresh() {
      this.user = getUserInfo()
      this.stats = getStats()
      this.baseUrl = getBaseUrl()
    },
    toLogin() {
      uni.navigateTo({ url: '/pages/login/login' })
    },
    toAbout() {
      uni.navigateTo({ url: '/pages/about/about' })
    },
    editServer() {
      uni.showModal({
        title: '服务器地址',
        content: this.baseUrl,
        editable: true,
        placeholderText: '例如 http://192.168.1.10:8000',
        confirmText: '保存',
        success: (res) => {
          if (!res.confirm) return
          if (typeof res.content !== 'string') {
            uni.showToast({ title: '当前平台不支持在线修改，请编辑 utils/apiConfig.js', icon: 'none', duration: 2500 })
            return
          }
          this.baseUrl = setBaseUrl(res.content)
          uni.showToast({ title: '已保存：' + this.baseUrlShort, icon: 'none' })
        }
      })
    },
    clearCache() {
      uni.showModal({
        title: '清除本地缓存',
        content: '将清除识别记录、记住的账号等本地数据（不会退出登录）。',
        confirmColor: '#E5484D',
        success: (res) => {
          if (!res.confirm) return
          clearRecords()
          uni.removeStorageSync('yl_remember_username')
          uni.removeStorageSync('yl_current_plant')
          this.refresh()
          uni.showToast({ title: '已清除', icon: 'success' })
        }
      })
    },
    logout() {
      uni.showModal({
        title: '退出登录',
        content: '确定要退出当前账号吗？',
        confirmColor: '#E5484D',
        success: (res) => {
          if (!res.confirm) return
          doLogout()
          uni.showToast({ title: '已退出登录', icon: 'none' })
          setTimeout(() => uni.reLaunch({ url: '/pages/index/index' }), 500)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.mine {
  width: 100%;
  height: 100vh;

  &__hero {
    position: relative;
    overflow: hidden;
    padding-left: $yl-page-padding;
    padding-right: $yl-page-padding;
    padding-bottom: 40rpx;
    background: $yl-gradient-hero;
    border-bottom-left-radius: 48rpx;
    border-bottom-right-radius: 48rpx;
  }

  &__orb {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;

    &--1 {
      width: 420rpx;
      height: 420rpx;
      right: -160rpx;
      top: -180rpx;
      background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0) 70%);
    }

    &--2 {
      width: 280rpx;
      height: 280rpx;
      left: -100rpx;
      bottom: -80rpx;
      background: radial-gradient(circle at 50% 50%, rgba(111, 211, 154, 0.35), rgba(111, 211, 154, 0) 70%);
    }
  }

  &__user {
    position: relative;
    display: flex;
    align-items: center;
    padding: 56rpx 0 36rpx;
  }

  &__avatar {
    position: relative;
    width: 136rpx;
    height: 136rpx;
    border-radius: 44rpx;
    background: rgba(255, 255, 255, 0.18);
    border: 3rpx solid rgba(255, 255, 255, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 12rpx 30rpx rgba(0, 0, 0, 0.18);
  }

  &__avatar-text {
    font-size: 44rpx;
    font-weight: 800;
    color: #fff;
  }

  &__avatar-dot {
    position: absolute;
    right: -4rpx;
    bottom: -4rpx;
    width: 28rpx;
    height: 28rpx;
    border-radius: 50%;
    background: $yl-primary-light;
    border: 4rpx solid #fff;
  }

  &__info {
    flex: 1;
    min-width: 0;
    margin-left: 28rpx;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  &__name {
    font-size: 38rpx;
    font-weight: 800;
    color: #fff;
  }

  &__sub {
    margin-top: 6rpx;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.75);
  }

  &__badge {
    display: flex;
    align-items: center;
    height: 40rpx;
    margin-top: 14rpx;
    padding: 0 16rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.18);
    border: 1rpx solid rgba(255, 255, 255, 0.3);
    font-size: 20rpx;
    color: #fff;

    text {
      margin-left: 6rpx;
    }
  }

  &__login {
    height: 68rpx;
    padding: 0 28rpx;
    border-radius: $yl-radius-pill;
    background: #fff;
    color: $yl-primary-dark;
    font-size: 26rpx;
    font-weight: 700;
    display: flex;
    align-items: center;
    box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.15);
  }

  &__content {
    margin-top: 28rpx;
  }

  &__logout {
    margin-top: 32rpx;
  }

  &__logout-text {
    margin-left: 10rpx;
  }

  &__footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 48rpx;
    font-size: 22rpx;
    color: $yl-text-4;
    line-height: 1.8;
  }
}

.stats {
  position: relative;
  display: flex;
  padding: 28rpx 0;
  border-radius: $yl-radius-lg;
  background: rgba(255, 255, 255, 0.14);
  border: 1rpx solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(14px);

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-right: 1rpx solid rgba(255, 255, 255, 0.2);

    &:last-child {
      border-right: none;
    }
  }

  &__num {
    font-size: 44rpx;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
  }

  &__label {
    margin-top: 8rpx;
    font-size: 22rpx;
    color: rgba(255, 255, 255, 0.78);
  }
}

.menu {
  background: #fff;
  border-radius: $yl-radius-lg;
  box-shadow: $yl-shadow;
  padding: 8rpx 28rpx;
  margin-bottom: 24rpx;

  &__item {
    display: flex;
    align-items: center;
    height: 112rpx;
    border-bottom: 1rpx solid $yl-border;

    &:last-child {
      border-bottom: none;
    }

    &--hover {
      opacity: 0.7;
    }
  }

  &__icon {
    width: 68rpx;
    height: 68rpx;
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 22rpx;
    flex-shrink: 0;
  }

  &__text {
    flex: 1;
    font-size: 29rpx;
    color: $yl-text-1;
    font-weight: 500;
  }

  &__value {
    max-width: 280rpx;
    margin-right: 12rpx;
    font-size: 24rpx;
    color: $yl-text-3;
  }
}
</style>
