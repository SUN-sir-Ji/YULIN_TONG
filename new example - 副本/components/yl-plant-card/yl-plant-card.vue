<template>
  <view class="yl-plant-card" :class="{ 'yl-plant-card--row': mode === 'row' }" hover-class="yl-plant-card--hover" hover-stay-time="80" @click="$emit('click', plant)">
    <!-- 封面 -->
    <view class="yl-plant-card__cover" :style="coverStyle">
      <image
        v-if="imageUrl && !imgError"
        class="yl-plant-card__img"
        :src="imageUrl"
        mode="aspectFill"
        lazy-load
        @error="imgError = true"
      ></image>
      <view v-else class="yl-plant-card__placeholder">
        <text class="yl-plant-card__initial">{{ initial }}</text>
        <view class="yl-plant-card__leaf yl-plant-card__leaf--1"></view>
        <view class="yl-plant-card__leaf yl-plant-card__leaf--2"></view>
      </view>
      <view v-if="familyName" class="yl-plant-card__chip">
        <text>{{ familyName }}</text>
      </view>
    </view>

    <!-- 文本 -->
    <view class="yl-plant-card__body">
      <text class="yl-plant-card__name yl-ellipsis">{{ plant.species_chinese_name || '未命名' }}</text>
      <text class="yl-plant-card__latin yl-ellipsis">{{ plant.species_latin_name || '' }}</text>
      <view v-if="mode === 'row'" class="yl-plant-card__meta">
        <text class="yl-plant-card__meta-item yl-ellipsis">{{ metaText }}</text>
      </view>
    </view>
    <view v-if="mode === 'row'" class="yl-plant-card__arrow">
      <uni-icons type="right" size="16" color="#C3CBC7"></uni-icons>
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
  ['#5CB85C', '#2E6B2E'],
  ['#26A69A', '#00695C'],
  ['#66BB6A', '#2E7D32'],
  ['#43A047', '#1B5E20']
]

export default {
  name: 'YlPlantCard',
  props: {
    plant: { type: Object, required: true },
    mode: { type: String, default: 'grid' } // grid | row
  },
  emits: ['click'],
  data() {
    return { imgError: false }
  },
  computed: {
    initial() {
      const name = this.plant.species_chinese_name || this.plant.species_latin_name || '?'
      return name.trim().charAt(0)
    },
    familyName() {
      return this.plant.family_chinese_name || this.plant.genus_chinese_name || ''
    },
    metaText() {
      const parts = [this.plant.phylum_chinese_name, this.plant.class_chinese_name, this.plant.order_chinese_name].filter(Boolean)
      return parts.join(' · ')
    },
    imageUrl() {
      const p = this.plant.image_path
      if (!p) return ''
      if (/^https?:\/\//i.test(p)) return p
      return getBaseUrl() + '/' + String(p).replace(/^\/+/, '')
    },
    coverStyle() {
      const key = this.plant.species_latin_name || this.plant.species_chinese_name || ''
      let hash = 0
      for (let i = 0; i < key.length; i++) hash = (hash * 31 + key.charCodeAt(i)) >>> 0
      const [a, b] = PALETTES[hash % PALETTES.length]
      return { background: `linear-gradient(145deg, ${a} 0%, ${b} 100%)` }
    }
  },
  watch: {
    plant() {
      this.imgError = false
    }
  }
}
</script>

<style lang="scss" scoped>
.yl-plant-card {
  background: #fff;
  border-radius: $yl-radius-lg;
  overflow: hidden;
  box-shadow: $yl-shadow-sm;
  transition: transform 0.15s ease, box-shadow 0.15s ease;

  &--hover {
    transform: translateY(2rpx) scale(0.985);
    box-shadow: $yl-shadow;
  }

  &__cover {
    position: relative;
    width: 100%;
    height: 240rpx;
    overflow: hidden;
  }

  &__img {
    width: 100%;
    height: 100%;
    display: block;
  }

  &__placeholder {
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
    font-size: 88rpx;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.92);
    text-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.18);
  }

  &__leaf {
    position: absolute;
    border-radius: 100% 0 100% 0;
    background: rgba(255, 255, 255, 0.12);

    &--1 {
      width: 220rpx;
      height: 220rpx;
      right: -70rpx;
      top: -60rpx;
      transform: rotate(20deg);
    }

    &--2 {
      width: 160rpx;
      height: 160rpx;
      left: -50rpx;
      bottom: -70rpx;
      transform: rotate(-30deg);
      background: rgba(255, 255, 255, 0.08);
    }
  }

  &__chip {
    position: absolute;
    left: 14rpx;
    bottom: 14rpx;
    z-index: 3;
    height: 40rpx;
    padding: 0 16rpx;
    border-radius: $yl-radius-pill;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    font-size: 20rpx;
    color: $yl-primary-dark;
    font-weight: 600;
    max-width: 80%;

    text {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  &__body {
    padding: 18rpx 20rpx 22rpx;
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  &__name {
    font-size: 29rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__latin {
    margin-top: 4rpx;
    font-size: 22rpx;
    font-style: italic;
    color: $yl-text-3;
  }

  &__meta {
    margin-top: 8rpx;
  }

  &__meta-item {
    font-size: 22rpx;
    color: $yl-text-3;
  }

  /* 横向列表模式 */
  &--row {
    display: flex;
    align-items: center;
    padding: 16rpx;
    border-radius: $yl-radius;
  }

  &--row &__cover {
    width: 150rpx;
    height: 150rpx;
    border-radius: $yl-radius-sm;
    flex-shrink: 0;
  }

  &--row &__initial {
    font-size: 56rpx;
  }

  &--row &__chip {
    display: none;
  }

  &--row &__body {
    flex: 1;
    padding: 0 20rpx;
  }

  &--row &__arrow {
    flex-shrink: 0;
  }
}
</style>
