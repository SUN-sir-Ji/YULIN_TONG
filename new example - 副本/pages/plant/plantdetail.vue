<template>
  <view class="detail yl-page">
    <yl-navbar title="" transparent light float :placeholder="false">
      <template #right>
        <view class="detail__share" hover-class="yl-hover" @click="copyName">
          <uni-icons type="paperclip" size="20" color="#FFFFFF"></uni-icons>
        </view>
      </template>
    </yl-navbar>

    <block v-if="plant">
      <!-- 头图 -->
      <view class="detail__hero" :style="coverStyle">
        <image v-if="imageUrl && !imgError" class="detail__img" :src="imageUrl" mode="aspectFill" @error="imgError = true" @click="preview"></image>
        <view v-else class="detail__ph">
          <view class="detail__leaf detail__leaf--1"></view>
          <view class="detail__leaf detail__leaf--2"></view>
          <view class="detail__leaf detail__leaf--3"></view>
          <text class="detail__initial">{{ initial }}</text>
        </view>
        <view class="detail__hero-mask"></view>

        <view class="detail__hero-text yl-anim-up">
          <view class="detail__chips">
            <view v-if="plant.genus_chinese_name" class="detail__chip">
              <text>{{ plant.genus_chinese_name }}</text>
            </view>
            <view v-if="plant.family_chinese_name" class="detail__chip detail__chip--ghost">
              <text>{{ plant.family_chinese_name }}</text>
            </view>
          </view>
          <text class="detail__name">{{ plant.species_chinese_name }}</text>
          <text class="detail__latin">{{ plant.species_latin_name }}</text>
        </view>
      </view>

      <view class="detail__body">
        <!-- 分类阶元 -->
        <view class="tax yl-anim-up yl-delay-1">
          <view class="tax__head">
            <text class="tax__title">分类阶元</text>
            <text class="tax__sub">Taxonomy</text>
          </view>
          <scroll-view scroll-x class="tax__scroll" :show-scrollbar="false">
            <view class="tax__inner">
              <view v-for="(t, i) in taxonomy" :key="t.key" class="tax__item">
                <view class="tax__rank" :style="{ background: t.bg, color: t.color }">
                  <text>{{ t.label }}</text>
                </view>
                <text class="tax__cn yl-ellipsis">{{ t.cn || '—' }}</text>
                <text class="tax__la yl-ellipsis">{{ t.la || '' }}</text>
                <view v-if="i < taxonomy.length - 1" class="tax__link"></view>
              </view>
            </view>
          </scroll-view>
        </view>

        <!-- 别名 -->
        <view v-if="aliases.length" class="sec yl-anim-up yl-delay-2">
          <view class="sec__head">
            <view class="sec__icon" style="background: #FFF4DF">
              <uni-icons type="flag-filled" size="18" color="#F5A524"></uni-icons>
            </view>
            <text class="sec__title">别名</text>
          </view>
          <view class="sec__chips">
            <view v-for="(a, i) in aliases" :key="i" class="yl-tag yl-tag--accent sec__chip">
              <text>{{ a }}</text>
            </view>
          </view>
        </view>

        <!-- 各描述段落 -->
        <view v-for="(s, i) in sections" :key="s.key" class="sec yl-anim-up" :class="'yl-delay-' + Math.min(i + 2, 5)">
          <view class="sec__head">
            <view class="sec__icon" :style="{ background: s.bg }">
              <uni-icons :type="s.icon" size="18" :color="s.color"></uni-icons>
            </view>
            <text class="sec__title">{{ s.title }}</text>
          </view>
          <text class="sec__content">{{ s.text }}</text>
        </view>

        <view v-if="!sections.length && !aliases.length" class="detail__nodata">
          <uni-icons type="info" size="18" color="#9AA5A0"></uni-icons>
          <text>暂无更多描述信息</text>
        </view>

        <view style="height: 180rpx"></view>
      </view>

      <!-- 底部操作 -->
      <view class="detail__bottom yl-safe-bottom">
        <view class="detail__bottom-inner">
          <button class="yl-btn yl-btn--light detail__btn" hover-class="yl-press" @click="back">
            <uni-icons type="images" size="18" color="#146C43"></uni-icons>
            <text class="detail__btn-text">返回图鉴</text>
          </button>
          <button class="yl-btn yl-btn--primary detail__btn" hover-class="yl-press" @click="goIdentify">
            <uni-icons type="scan" size="18" color="#FFFFFF"></uni-icons>
            <text class="detail__btn-text">识别相似植物</text>
          </button>
        </view>
      </view>
    </block>

    <view v-else class="detail__empty">
      <view :style="{ height: navHeight + 'px' }"></view>
      <yl-empty icon="images" title="未找到植物信息" desc="请从图鉴列表重新进入" btn-text="返回图鉴" @click="back"></yl-empty>
    </view>
  </view>
</template>

<script>
import { getBaseUrl } from '@/utils/apiConfig.js'

const PALETTES = [
  ['#1DA462', '#0E3B2E'],
  ['#2FB77A', '#146C43'],
  ['#3B9C8A', '#1B4F4A'],
  ['#4BA96B', '#1F5F3E'],
  ['#26A69A', '#00695C'],
  ['#66BB6A', '#2E7D32']
]

const TAX = [
  { key: 'kingdom', label: '界', color: '#5B6660', bg: '#F1F5F3' },
  { key: 'phylum', label: '门', color: '#1DA462', bg: '#E3F6EA' },
  { key: 'class', label: '纲', color: '#3B82F6', bg: '#E8F0FE' },
  { key: 'order', label: '目', color: '#8B5CF6', bg: '#F1EBFF' },
  { key: 'family', label: '科', color: '#F5A524', bg: '#FFF4DF' },
  { key: 'genus', label: '属', color: '#E5484D', bg: '#FDECEC' }
]

const SECTIONS = [
  { key: 'morphological_features', title: '形态特征', icon: 'eye-filled', color: '#1DA462', bg: '#E3F6EA' },
  { key: 'growth_environment', title: '生长环境', icon: 'location-filled', color: '#3B82F6', bg: '#E8F0FE' },
  { key: 'distribution', title: '分布区域', icon: 'map-filled', color: '#8B5CF6', bg: '#F1EBFF' },
  { key: 'growth_habits', title: '生长习性', icon: 'calendar-filled', color: '#26A69A', bg: '#E0F4F2' },
  { key: 'usage_value', title: '用途价值', icon: 'star-filled', color: '#F5A524', bg: '#FFF4DF' }
]

function isEmptyText(v) {
  if (v === null || v === undefined) return true
  const s = String(v).trim()
  return !s || s === '无' || s === '暂无' || s.toLowerCase() === 'null' || s.toLowerCase() === 'none'
}

export default {
  data() {
    return {
      plant: null,
      imgError: false,
      navHeight: 44
    }
  },
  computed: {
    initial() {
      const n = (this.plant && (this.plant.species_chinese_name || this.plant.species_latin_name)) || '?'
      return String(n).trim().charAt(0)
    },
    imageUrl() {
      const p = this.plant && this.plant.image_path
      if (!p) return ''
      if (/^https?:\/\//i.test(p)) return p
      return getBaseUrl() + '/' + String(p).replace(/^\/+/, '')
    },
    coverStyle() {
      const key = (this.plant && (this.plant.species_latin_name || this.plant.species_chinese_name)) || ''
      let hash = 0
      for (let i = 0; i < key.length; i++) hash = (hash * 31 + key.charCodeAt(i)) >>> 0
      const [a, b] = PALETTES[hash % PALETTES.length]
      return { background: `linear-gradient(160deg, ${a} 0%, ${b} 100%)` }
    },
    taxonomy() {
      const p = this.plant || {}
      return TAX.map((t) => ({
        ...t,
        cn: p[`${t.key}_chinese_name`] || '',
        la: p[`${t.key}_latin_name`] || ''
      }))
    },
    aliases() {
      const v = this.plant && this.plant.common_names
      if (isEmptyText(v)) return []
      return String(v)
        .split(/[,，、;；\/\n]/)
        .map((s) => s.trim())
        .filter((s) => s && s !== '无')
    },
    sections() {
      const p = this.plant || {}
      return SECTIONS.filter((s) => !isEmptyText(p[s.key])).map((s) => ({ ...s, text: String(p[s.key]).trim() }))
    }
  },
  onLoad(options) {
    try {
      const info = uni.getSystemInfoSync()
      this.navHeight = (info.statusBarHeight || 0) + 44
    } catch (e) {}

    const app = getApp()
    let plant = app && app.globalData ? app.globalData.currentPlant : null
    if (!plant) {
      try {
        plant = uni.getStorageSync('yl_current_plant') || null
      } catch (e) {}
    }
    if (plant && options && options.id && String(plant.id) !== String(options.id)) {
      // 与路由参数不一致时视为无效
      plant = null
    }
    this.plant = plant
  },
  methods: {
    preview() {
      if (this.imageUrl) uni.previewImage({ urls: [this.imageUrl] })
    },
    copyName() {
      if (!this.plant) return
      const text = `${this.plant.species_chinese_name || ''} ${this.plant.species_latin_name || ''}`.trim()
      uni.setClipboardData({
        data: text,
        success: () => uni.showToast({ title: '已复制植物名称', icon: 'none' })
      })
    },
    back() {
      const pages = getCurrentPages()
      if (pages.length > 1) uni.navigateBack()
      else uni.reLaunch({ url: '/pages/main/main?tab=1' })
    },
    goIdentify() {
      uni.navigateTo({ url: '/pages/identify/identify' })
    }
  }
}
</script>

<style lang="scss" scoped>
.detail {
  position: relative;

  &__share {
    width: 72rpx;
    height: 72rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__hero {
    position: relative;
    width: 100%;
    height: 620rpx;
    overflow: hidden;
  }

  &__img {
    width: 100%;
    height: 100%;
    display: block;
  }

  &__ph {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  &__initial {
    position: relative;
    z-index: 2;
    font-size: 220rpx;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.85);
    text-shadow: 0 16rpx 50rpx rgba(0, 0, 0, 0.25);
    margin-top: -80rpx;
  }

  &__leaf {
    position: absolute;
    border-radius: 100% 0 100% 0;
    background: rgba(255, 255, 255, 0.1);
    border: 2rpx solid rgba(255, 255, 255, 0.12);

    &--1 {
      width: 460rpx;
      height: 460rpx;
      right: -160rpx;
      top: -140rpx;
      transform: rotate(25deg);
    }

    &--2 {
      width: 320rpx;
      height: 320rpx;
      left: -120rpx;
      bottom: -40rpx;
      transform: rotate(-35deg);
      background: rgba(255, 255, 255, 0.07);
    }

    &--3 {
      width: 160rpx;
      height: 160rpx;
      left: 30%;
      top: 26%;
      transform: rotate(60deg);
      background: rgba(255, 255, 255, 0.06);
      animation: yl-float 5s ease-in-out infinite;
    }
  }

  &__hero-mask {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 60%;
    background: linear-gradient(to top, rgba(10, 30, 20, 0.85), rgba(10, 30, 20, 0));
    pointer-events: none;
  }

  &__hero-text {
    position: absolute;
    left: $yl-page-padding;
    right: $yl-page-padding;
    bottom: 64rpx;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  &__chips {
    display: flex;
    margin-bottom: 16rpx;
  }

  &__chip {
    height: 44rpx;
    padding: 0 18rpx;
    margin-right: 12rpx;
    border-radius: $yl-radius-pill;
    background: #fff;
    color: $yl-primary-dark;
    font-size: 22rpx;
    font-weight: 700;
    display: flex;
    align-items: center;

    &--ghost {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      border: 1rpx solid rgba(255, 255, 255, 0.4);
      font-weight: 500;
    }
  }

  &__name {
    font-size: 56rpx;
    font-weight: 800;
    color: #fff;
    line-height: 1.2;
    text-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.25);
  }

  &__latin {
    margin-top: 8rpx;
    font-size: 26rpx;
    font-style: italic;
    color: rgba(255, 255, 255, 0.82);
  }

  &__body {
    position: relative;
    margin-top: -40rpx;
    padding: 32rpx $yl-page-padding 0;
    border-top-left-radius: 40rpx;
    border-top-right-radius: 40rpx;
    background: $yl-bg;
  }

  &__nodata {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 48rpx 0;
    font-size: 24rpx;
    color: $yl-text-3;

    text {
      margin-left: 8rpx;
    }
  }

  &__bottom {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(16px);
    box-shadow: 0 -8rpx 30rpx rgba(14, 59, 46, 0.08);
  }

  &__bottom-inner {
    display: flex;
    padding: 20rpx $yl-page-padding;
  }

  &__btn {
    flex: 1;
    height: 88rpx;

    &:first-child {
      margin-right: 20rpx;
      flex: 0 0 240rpx;
    }
  }

  &__btn-text {
    margin-left: 10rpx;
  }

  &__empty {
    padding-top: 80rpx;
  }
}

/* 分类阶元 */
.tax {
  padding: 28rpx 0 24rpx 28rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;

  &__head {
    display: flex;
    align-items: baseline;
    margin-bottom: 20rpx;
  }

  &__title {
    font-size: 32rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__sub {
    margin-left: 12rpx;
    font-size: 22rpx;
    color: $yl-text-4;
    letter-spacing: 2rpx;
  }

  &__scroll {
    width: 100%;
    white-space: nowrap;
  }

  &__inner {
    display: inline-flex;
    align-items: flex-start;
    padding-right: 28rpx;
  }

  &__item {
    position: relative;
    width: 168rpx;
    margin-right: 24rpx;
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
  }

  &__rank {
    width: 68rpx;
    height: 68rpx;
    border-radius: 22rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26rpx;
    font-weight: 800;
  }

  &__cn {
    width: 100%;
    margin-top: 12rpx;
    text-align: center;
    font-size: 25rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__la {
    width: 100%;
    margin-top: 2rpx;
    text-align: center;
    font-size: 20rpx;
    font-style: italic;
    color: $yl-text-3;
  }

  &__link {
    position: absolute;
    top: 32rpx;
    right: -24rpx;
    width: 24rpx;
    height: 4rpx;
    background: $yl-border;
  }
}

/* 描述区块 */
.sec {
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

  &__icon {
    width: 56rpx;
    height: 56rpx;
    border-radius: 18rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16rpx;
  }

  &__title {
    font-size: 30rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__content {
    display: block;
    font-size: 27rpx;
    line-height: 1.85;
    color: $yl-text-2;
    text-align: justify;
  }

  &__chips {
    display: flex;
    flex-wrap: wrap;
  }

  &__chip {
    margin: 0 12rpx 12rpx 0;
    height: 52rpx;
    font-size: 24rpx;
  }
}
</style>
