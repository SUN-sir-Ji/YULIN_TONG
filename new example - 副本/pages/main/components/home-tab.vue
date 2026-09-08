<template>
  <scroll-view scroll-y class="home" :show-scrollbar="false" enhanced>
    <!-- 顶部沉浸区 -->
    <view class="home__hero" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="home__orb home__orb--1"></view>
      <view class="home__orb home__orb--2"></view>
      <view class="home__leaf"></view>

      <view class="home__topbar">
        <view class="home__greet">
          <text class="home__hello">{{ greeting }}</text>
          <text class="home__user">{{ displayName }}</text>
        </view>
        <view class="home__avatar" hover-class="yl-press" @click="$emit('switch', 3)">
          <text v-if="user" class="home__avatar-text">{{ avatarChar }}</text>
          <uni-icons v-else type="person-filled" size="22" color="#FFFFFF"></uni-icons>
        </view>
      </view>

      <view class="home__search" hover-class="yl-hover" @click="$emit('switch', 1)">
        <uni-icons type="search" size="18" color="#9AA5A0"></uni-icons>
        <text class="home__search-text">搜索植物中文名 / 拉丁名…</text>
        <view class="home__search-btn">
          <uni-icons type="scan" size="16" color="#FFFFFF"></uni-icons>
        </view>
      </view>

      <!-- 识别主卡片 -->
      <view class="hero-card" hover-class="yl-press" hover-stay-time="100" @click="goIdentify()">
        <view class="hero-card__text">
          <view class="hero-card__tag">
            <text>AI · YOLO</text>
          </view>
          <text class="hero-card__title">拍照识别植物</text>
          <text class="hero-card__desc">拍一张或从相册选择，秒级得到识别结果与置信度</text>
          <view class="hero-card__btn">
            <text>立即识别</text>
            <uni-icons type="right" size="14" color="#146C43"></uni-icons>
          </view>
        </view>
        <view class="hero-card__visual">
          <view class="hero-card__ring hero-card__ring--1"></view>
          <view class="hero-card__ring hero-card__ring--2"></view>
          <view class="hero-card__cam">
            <uni-icons type="camera-filled" size="42" color="#FFFFFF"></uni-icons>
          </view>
          <view class="hero-card__spark hero-card__spark--1"></view>
          <view class="hero-card__spark hero-card__spark--2"></view>
        </view>
      </view>
    </view>

    <view class="home__content yl-container">
      <!-- 快捷入口 -->
      <view class="quick yl-anim-up">
        <view v-for="a in actions" :key="a.key" class="quick__item" hover-class="yl-press" hover-stay-time="80" @click="onAction(a.key)">
          <view class="quick__icon" :style="{ background: a.bg }">
            <uni-icons :type="a.icon" size="26" :color="a.color"></uni-icons>
          </view>
          <text class="quick__text">{{ a.text }}</text>
        </view>
      </view>

      <!-- 分类速览 -->
      <view class="yl-section yl-anim-up yl-delay-1">
        <view class="yl-section__head">
          <text class="yl-section__title">分类速览</text>
          <view class="yl-section__more" hover-class="yl-hover" @click="$emit('switch', 1)">
            <text>全部图鉴</text>
            <uni-icons type="right" size="12" color="#9AA5A0"></uni-icons>
          </view>
        </view>

        <scroll-view scroll-x class="cats" :show-scrollbar="false">
          <view class="cats__inner">
            <block v-if="catsLoading">
              <view v-for="n in 4" :key="'s' + n" class="cats__item cats__item--skeleton yl-skeleton"></view>
            </block>
            <block v-else-if="categories.length">
              <view
                v-for="(c, i) in categories"
                :key="c.id"
                class="cats__item"
                :style="{ background: catBg(i) }"
                hover-class="yl-press"
                hover-stay-time="80"
                @click="pickCategory(c)"
              >
                <view class="cats__badge">
                  <text>门</text>
                </view>
                <text class="cats__char">{{ c.name.charAt(0) }}</text>
                <text class="cats__name yl-ellipsis">{{ c.name }}</text>
                <text class="cats__latin yl-ellipsis">{{ c.value }}</text>
              </view>
            </block>
            <view v-else class="cats__empty" @click="loadCategories">
              <uni-icons type="refreshempty" size="20" color="#9AA5A0"></uni-icons>
              <text>分类加载失败，点击重试</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 最近识别 -->
      <view v-if="recent.length" class="yl-section yl-anim-up yl-delay-2">
        <view class="yl-section__head">
          <text class="yl-section__title">最近识别</text>
          <view class="yl-section__more" hover-class="yl-hover" @click="$emit('switch', 2)">
            <text>查看全部</text>
            <uni-icons type="right" size="12" color="#9AA5A0"></uni-icons>
          </view>
        </view>
        <scroll-view scroll-x class="recent" :show-scrollbar="false">
          <view class="recent__inner">
            <view v-for="r in recent" :key="r.id" class="recent__item" hover-class="yl-press" hover-stay-time="80" @click="$emit('switch', 2)">
              <view class="recent__cover">
                <image v-if="r.image && !broken[r.id]" class="recent__img" :src="r.image" mode="aspectFill" @error="broken[r.id] = true"></image>
                <view v-else class="recent__img recent__img--ph">
                  <uni-icons type="image" size="28" color="#9AA5A0"></uni-icons>
                </view>
                <view class="recent__conf" :style="{ background: level(r.best.confidence).color }">
                  <text>{{ percent(r.best.confidence) }}%</text>
                </view>
              </view>
              <text class="recent__name yl-ellipsis">{{ r.best.class }}</text>
              <text class="recent__time">{{ relativeTime(r.time) }}</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 植物小知识 -->
      <view class="yl-section yl-anim-up yl-delay-3">
        <view class="yl-section__head">
          <text class="yl-section__title">植物小知识</text>
        </view>
        <view class="tips">
          <view v-for="(t, i) in tips" :key="i" class="tips__item">
            <view class="tips__icon" :style="{ background: t.bg }">
              <uni-icons :type="t.icon" size="22" :color="t.color"></uni-icons>
            </view>
            <view class="tips__body">
              <text class="tips__title">{{ t.title }}</text>
              <text class="tips__desc">{{ t.desc }}</text>
            </view>
          </view>
        </view>
      </view>

      <view class="yl-tab-spacer"></view>
    </view>
  </scroll-view>
</template>

<script>
import { getPlantCategories } from '@/utils/api.js'
import { getUserInfo } from '@/utils/auth.js'
import { getRecords, relativeTime, confidenceLevel, percent } from '@/utils/history.js'

const CAT_BGS = [
  'linear-gradient(135deg, #1DA462 0%, #146C43 100%)',
  'linear-gradient(135deg, #3B82F6 0%, #1E4FB8 100%)',
  'linear-gradient(135deg, #8B5CF6 0%, #5B34C4 100%)',
  'linear-gradient(135deg, #F5A524 0%, #D97706 100%)',
  'linear-gradient(135deg, #26A69A 0%, #00695C 100%)',
  'linear-gradient(135deg, #EC6B8A 0%, #B83258 100%)'
]

export default {
  name: 'HomeTab',
  emits: ['switch', 'category'],
  data() {
    return {
      statusBarHeight: 0,
      user: null,
      categories: [],
      catsLoading: true,
      recent: [],
      broken: {},
      actions: [
        { key: 'camera', text: '拍照识别', icon: 'camera-filled', color: '#1DA462', bg: '#E3F6EA' },
        { key: 'album', text: '相册识别', icon: 'images-filled', color: '#3B82F6', bg: '#E8F0FE' },
        { key: 'atlas', text: '植物图鉴', icon: 'map-filled', color: '#8B5CF6', bg: '#F1EBFF' },
        { key: 'history', text: '识别记录', icon: 'calendar-filled', color: '#F5A524', bg: '#FFF4DF' }
      ],
      tips: [
        {
          icon: 'camera',
          color: '#1DA462',
          bg: '#E3F6EA',
          title: '拍摄技巧',
          desc: '尽量让植物占满画面、对焦清晰，避免逆光与手抖，识别准确率会更高。'
        },
        {
          icon: 'map',
          color: '#3B82F6',
          bg: '#E8F0FE',
          title: '分类阶元',
          desc: '图鉴按「门 → 纲 → 目 → 科 → 属」五级分类组织，可在分类导航中逐级浏览。'
        },
        {
          icon: 'star',
          color: '#F5A524',
          bg: '#FFF4DF',
          title: '苔藓与角苔',
          desc: '苔藓植物没有真正的根与维管束，常生于阴湿环境，是雨林生态的重要组成。'
        }
      ]
    }
  },
  computed: {
    greeting() {
      const h = new Date().getHours()
      if (h < 6) return '夜深了'
      if (h < 9) return '早上好'
      if (h < 12) return '上午好'
      if (h < 14) return '中午好'
      if (h < 18) return '下午好'
      return '晚上好'
    },
    displayName() {
      return this.user ? `用户 ${this.user.username}` : '欢迎来到雨林通'
    },
    avatarChar() {
      const s = String((this.user && this.user.username) || '')
      return s.slice(-2) || '林'
    }
  },
  created() {
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 0
    } catch (e) {}
    this.refresh()
    this.loadCategories()
  },
  methods: {
    relativeTime,
    percent,
    level: confidenceLevel,
    refresh() {
      this.user = getUserInfo()
      this.recent = getRecords().slice(0, 8)
    },
    async loadCategories() {
      this.catsLoading = true
      try {
        this.categories = await getPlantCategories(0)
      } catch (e) {
        this.categories = []
      } finally {
        this.catsLoading = false
      }
    },
    catBg(i) {
      return CAT_BGS[i % CAT_BGS.length]
    },
    pickCategory(c) {
      this.$emit('category', {
        id: c.id,
        name: c.name,
        value: c.value,
        level: 0,
        levelLabel: '门',
        field: 'phylum_latin_name',
        path: [c.name]
      })
    },
    goIdentify(images) {
      const app = getApp()
      if (app && app.globalData) app.globalData.pendingImages = images || []
      uni.navigateTo({ url: '/pages/identify/identify' })
    },
    onAction(key) {
      if (key === 'atlas') return this.$emit('switch', 1)
      if (key === 'history') return this.$emit('switch', 2)
      const sourceType = key === 'camera' ? ['camera'] : ['album']
      uni.chooseImage({
        count: key === 'camera' ? 1 : 9,
        sizeType: ['compressed'],
        sourceType,
        success: (res) => this.goIdentify(res.tempFilePaths || []),
        fail: () => {}
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  width: 100%;
  height: 100vh;

  &__hero {
    position: relative;
    overflow: hidden;
    padding-left: $yl-page-padding;
    padding-right: $yl-page-padding;
    padding-bottom: 48rpx;
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
      right: -140rpx;
      top: -160rpx;
      background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0) 70%);
    }

    &--2 {
      width: 300rpx;
      height: 300rpx;
      left: -120rpx;
      bottom: -60rpx;
      background: radial-gradient(circle at 50% 50%, rgba(111, 211, 154, 0.35), rgba(111, 211, 154, 0) 70%);
    }
  }

  &__leaf {
    position: absolute;
    width: 260rpx;
    height: 260rpx;
    right: 60rpx;
    top: 20rpx;
    border-radius: 100% 0 100% 0;
    background: rgba(255, 255, 255, 0.05);
    border: 2rpx solid rgba(255, 255, 255, 0.1);
    transform: rotate(30deg);
    pointer-events: none;
  }

  &__topbar {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 112rpx;
    margin-top: 8rpx;
  }

  &__greet {
    display: flex;
    flex-direction: column;
  }

  &__hello {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.75);
  }

  &__user {
    margin-top: 4rpx;
    font-size: 38rpx;
    font-weight: 700;
    color: #fff;
  }

  &__avatar {
    width: 84rpx;
    height: 84rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.18);
    border: 2rpx solid rgba(255, 255, 255, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
  }

  &__avatar-text {
    color: #fff;
    font-size: 26rpx;
    font-weight: 700;
  }

  &__search {
    position: relative;
    display: flex;
    align-items: center;
    height: 88rpx;
    margin-top: 16rpx;
    padding: 0 12rpx 0 28rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.12);
  }

  &__search-text {
    flex: 1;
    margin-left: 14rpx;
    font-size: 26rpx;
    color: $yl-text-3;
  }

  &__search-btn {
    width: 64rpx;
    height: 64rpx;
    border-radius: 50%;
    background: $yl-gradient;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__content {
    position: relative;
    margin-top: -20rpx;
    padding-top: 40rpx;
  }
}

/* 识别主卡片 */
.hero-card {
  position: relative;
  display: flex;
  align-items: center;
  margin-top: 28rpx;
  padding: 36rpx 32rpx;
  border-radius: $yl-radius-xl;
  background: rgba(255, 255, 255, 0.14);
  border: 1rpx solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(14px);
  overflow: hidden;

  &__text {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    z-index: 2;
  }

  &__tag {
    height: 40rpx;
    padding: 0 16rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.22);
    display: flex;
    align-items: center;
    font-size: 20rpx;
    color: #fff;
    letter-spacing: 2rpx;
  }

  &__title {
    margin-top: 16rpx;
    font-size: 40rpx;
    font-weight: 800;
    color: #fff;
  }

  &__desc {
    margin-top: 10rpx;
    font-size: 24rpx;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.8);
    padding-right: 20rpx;
  }

  &__btn {
    margin-top: 24rpx;
    height: 64rpx;
    padding: 0 26rpx;
    border-radius: $yl-radius-pill;
    background: #fff;
    display: flex;
    align-items: center;
    font-size: 26rpx;
    font-weight: 700;
    color: $yl-primary-dark;
    box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.15);

    text {
      margin-right: 6rpx;
    }
  }

  &__visual {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  &__ring {
    position: absolute;
    border-radius: 50%;
    border: 2rpx solid rgba(255, 255, 255, 0.35);

    &--1 {
      width: 180rpx;
      height: 180rpx;
      animation: yl-float 4s ease-in-out infinite;
    }

    &--2 {
      width: 230rpx;
      height: 230rpx;
      border-style: dashed;
      opacity: 0.6;
    }
  }

  &__cam {
    width: 128rpx;
    height: 128rpx;
    border-radius: 50%;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.1));
    border: 2rpx solid rgba(255, 255, 255, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.2);
  }

  &__spark {
    position: absolute;
    border-radius: 50%;
    background: #fff;

    &--1 {
      width: 14rpx;
      height: 14rpx;
      right: 10rpx;
      top: 30rpx;
      opacity: 0.9;
    }

    &--2 {
      width: 8rpx;
      height: 8rpx;
      left: 6rpx;
      bottom: 40rpx;
      opacity: 0.7;
    }
  }
}

/* 快捷入口 */
.quick {
  display: flex;
  justify-content: space-between;
  padding: 28rpx 16rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  &__icon {
    width: 96rpx;
    height: 96rpx;
    border-radius: 30rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__text {
    margin-top: 14rpx;
    font-size: 24rpx;
    color: $yl-text-1;
    font-weight: 500;
  }
}

/* 分类速览 */
.cats {
  width: 100%;
  white-space: nowrap;

  &__inner {
    display: inline-flex;
    padding-right: 32rpx;
  }

  &__item {
    position: relative;
    width: 220rpx;
    height: 240rpx;
    margin-right: 20rpx;
    border-radius: $yl-radius-lg;
    padding: 22rpx;
    display: inline-flex;
    flex-direction: column;
    justify-content: flex-end;
    overflow: hidden;
    color: #fff;
    box-shadow: $yl-shadow;
    flex-shrink: 0;

    &--skeleton {
      box-shadow: none;
    }
  }

  &__badge {
    position: absolute;
    right: 18rpx;
    top: 18rpx;
    width: 44rpx;
    height: 44rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.22);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20rpx;
  }

  &__char {
    position: absolute;
    left: 18rpx;
    top: 10rpx;
    font-size: 96rpx;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.18);
    line-height: 1;
  }

  &__name {
    position: relative;
    font-size: 28rpx;
    font-weight: 700;
  }

  &__latin {
    position: relative;
    margin-top: 4rpx;
    font-size: 20rpx;
    font-style: italic;
    text-transform: capitalize;
    color: rgba(255, 255, 255, 0.78);
  }

  &__empty {
    display: inline-flex;
    align-items: center;
    height: 120rpx;
    padding: 0 32rpx;
    border-radius: $yl-radius;
    background: #fff;
    color: $yl-text-3;
    font-size: 24rpx;

    text {
      margin-left: 10rpx;
    }
  }
}

/* 最近识别 */
.recent {
  width: 100%;
  white-space: nowrap;

  &__inner {
    display: inline-flex;
    padding-right: 32rpx;
  }

  &__item {
    width: 200rpx;
    margin-right: 20rpx;
    display: inline-flex;
    flex-direction: column;
    flex-shrink: 0;
  }

  &__cover {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    border-radius: $yl-radius;
    overflow: hidden;
    background: #fff;
    box-shadow: $yl-shadow-sm;
  }

  &__img {
    width: 100%;
    height: 100%;
    display: block;

    &--ph {
      display: flex;
      align-items: center;
      justify-content: center;
      background: $yl-bg-input;
    }
  }

  &__conf {
    position: absolute;
    right: 10rpx;
    top: 10rpx;
    height: 36rpx;
    padding: 0 12rpx;
    border-radius: $yl-radius-pill;
    display: flex;
    align-items: center;
    font-size: 20rpx;
    font-weight: 700;
    color: #fff;
  }

  &__name {
    margin-top: 12rpx;
    font-size: 26rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__time {
    margin-top: 2rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }
}

/* 小知识 */
.tips {
  background: #fff;
  border-radius: $yl-radius-lg;
  box-shadow: $yl-shadow;
  padding: 8rpx 28rpx;

  &__item {
    display: flex;
    align-items: flex-start;
    padding: 24rpx 0;
    border-bottom: 1rpx solid $yl-border;

    &:last-child {
      border-bottom: none;
    }
  }

  &__icon {
    width: 72rpx;
    height: 72rpx;
    border-radius: 22rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-right: 20rpx;
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
    margin-top: 6rpx;
    font-size: 24rpx;
    line-height: 1.6;
    color: $yl-text-2;
  }
}
</style>
