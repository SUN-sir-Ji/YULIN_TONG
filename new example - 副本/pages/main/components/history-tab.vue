<template>
  <scroll-view scroll-y class="history" :show-scrollbar="false">
    <view class="history__header" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="history__titlebar">
        <view>
          <text class="history__title">识别记录</text>
          <text class="history__sub">{{ records.length ? `共 ${records.length} 条，保存在本机` : '记录保存在本机，最多保留 60 条' }}</text>
        </view>
        <view v-if="records.length" class="history__clear" hover-class="yl-hover" @click="clearAll">
          <uni-icons type="trash" size="16" color="#E5484D"></uni-icons>
          <text>清空</text>
        </view>
      </view>

      <!-- 概览 -->
      <view v-if="records.length" class="overview">
        <view class="overview__item">
          <text class="overview__num">{{ stats.count }}</text>
          <text class="overview__label">识别次数</text>
        </view>
        <view class="overview__divider"></view>
        <view class="overview__item">
          <text class="overview__num">{{ stats.species }}</text>
          <text class="overview__label">识别物种</text>
        </view>
        <view class="overview__divider"></view>
        <view class="overview__item">
          <text class="overview__num">{{ highRate }}%</text>
          <text class="overview__label">高置信占比</text>
        </view>
      </view>
    </view>

    <view class="yl-container">
      <yl-empty
        v-if="!records.length"
        icon="camera"
        title="还没有识别记录"
        desc="拍一张植物照片，试试 AI 识别吧"
        btn-text="去识别"
        @click="goIdentify"
      ></yl-empty>

      <view v-else class="list">
        <block v-for="group in grouped" :key="group.label">
          <view class="list__date">
            <text>{{ group.label }}</text>
          </view>

          <view
            v-for="r in group.items"
            :key="r.id"
            class="record"
            :class="{ 'is-open': openId === r.id }"
            hover-class="record--hover"
            hover-stay-time="80"
            @click="toggle(r.id)"
          >
            <view class="record__main">
              <view class="record__cover">
                <image v-if="r.image && !broken[r.id]" class="record__img" :src="r.image" mode="aspectFill" @error="broken[r.id] = true"></image>
                <view v-else class="record__img record__img--ph">
                  <uni-icons type="image" size="26" color="#9AA5A0"></uni-icons>
                </view>
              </view>

              <view class="record__body">
                <text class="record__name yl-ellipsis">{{ r.best.class }}</text>
                <view class="record__meta">
                  <uni-icons type="calendar" size="12" color="#9AA5A0"></uni-icons>
                  <text class="record__time">{{ relativeTime(r.time) }}</text>
                  <text v-if="r.results.length > 1" class="record__dot">·</text>
                  <text v-if="r.results.length > 1" class="record__time">{{ r.results.length }} 个候选</text>
                </view>
              </view>

              <view class="record__conf" :style="{ color: level(r.best.confidence).color, background: level(r.best.confidence).bg }">
                <text>{{ percent(r.best.confidence) }}%</text>
              </view>
              <view class="record__arrow">
                <uni-icons :type="openId === r.id ? 'up' : 'down'" size="14" color="#C3CBC7"></uni-icons>
              </view>
            </view>

            <!-- 展开详情 -->
            <view v-if="openId === r.id" class="record__detail yl-anim-in">
              <view v-for="(it, i) in r.results" :key="i" class="record__row">
                <view class="record__rank" :class="{ 'is-top': i === 0 }">
                  <text>{{ i + 1 }}</text>
                </view>
                <text class="record__class yl-ellipsis">{{ it.class }}</text>
                <view class="record__bar">
                  <view class="record__fill" :style="{ width: percent(it.confidence) + '%', background: level(it.confidence).color }"></view>
                </view>
                <text class="record__pct" :style="{ color: level(it.confidence).color }">{{ percent(it.confidence) }}%</text>
              </view>

              <view class="record__actions">
                <view class="record__action" hover-class="yl-hover" @click.stop="preview(r)">
                  <uni-icons type="eye" size="16" color="#5B6660"></uni-icons>
                  <text>查看原图</text>
                </view>
                <view class="record__action record__action--danger" hover-class="yl-hover" @click.stop="remove(r.id)">
                  <uni-icons type="trash" size="16" color="#E5484D"></uni-icons>
                  <text>删除</text>
                </view>
              </view>
            </view>
          </view>
        </block>
      </view>
    </view>

    <view class="yl-tab-spacer"></view>
  </scroll-view>
</template>

<script>
import { getRecords, removeRecord, clearRecords, relativeTime, confidenceLevel, percent, getStats } from '@/utils/history.js'

export default {
  name: 'HistoryTab',
  data() {
    return {
      statusBarHeight: 0,
      records: [],
      stats: { count: 0, species: 0 },
      openId: '',
      broken: {}
    }
  },
  computed: {
    highRate() {
      if (!this.records.length) return 0
      const high = this.records.filter((r) => r.best && r.best.confidence >= 0.8).length
      return Math.round((high / this.records.length) * 100)
    },
    grouped() {
      const groups = []
      const map = {}
      const today = new Date().toDateString()
      const yesterday = new Date(Date.now() - 86400000).toDateString()
      this.records.forEach((r) => {
        const d = new Date(r.time)
        const ds = d.toDateString()
        let label
        if (ds === today) label = '今天'
        else if (ds === yesterday) label = '昨天'
        else label = `${d.getMonth() + 1} 月 ${d.getDate()} 日`
        if (!map[label]) {
          map[label] = { label, items: [] }
          groups.push(map[label])
        }
        map[label].items.push(r)
      })
      return groups
    }
  },
  created() {
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 0
    } catch (e) {}
    this.refresh()
  },
  methods: {
    relativeTime,
    percent,
    level: confidenceLevel,
    refresh() {
      this.records = getRecords()
      this.stats = getStats()
    },
    toggle(id) {
      this.openId = this.openId === id ? '' : id
    },
    preview(r) {
      if (!r.image) return
      uni.previewImage({ urls: [r.image] })
    },
    remove(id) {
      uni.showModal({
        title: '删除记录',
        content: '确定删除这条识别记录吗？',
        confirmColor: '#E5484D',
        success: (res) => {
          if (res.confirm) {
            this.records = removeRecord(id)
            this.stats = getStats()
            uni.showToast({ title: '已删除', icon: 'none' })
          }
        }
      })
    },
    clearAll() {
      uni.showModal({
        title: '清空记录',
        content: '将删除本机保存的全部识别记录，且无法恢复。',
        confirmColor: '#E5484D',
        success: (res) => {
          if (res.confirm) {
            clearRecords()
            this.refresh()
            uni.showToast({ title: '已清空', icon: 'none' })
          }
        }
      })
    },
    goIdentify() {
      uni.navigateTo({ url: '/pages/identify/identify' })
    }
  }
}
</script>

<style lang="scss" scoped>
.history {
  width: 100%;
  height: 100vh;

  &__header {
    padding-left: $yl-page-padding;
    padding-right: $yl-page-padding;
  }

  &__titlebar {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 128rpx;
    padding-bottom: 16rpx;
  }

  &__title {
    display: block;
    font-size: 44rpx;
    font-weight: 800;
    color: $yl-text-1;
  }

  &__sub {
    display: block;
    margin-top: 4rpx;
    font-size: 24rpx;
    color: $yl-text-3;
  }

  &__clear {
    display: flex;
    align-items: center;
    height: 52rpx;
    padding: 0 18rpx;
    margin-bottom: 8rpx;
    border-radius: $yl-radius-pill;
    background: $yl-danger-soft;
    color: $yl-danger;
    font-size: 22rpx;
    font-weight: 600;

    text {
      margin-left: 6rpx;
    }
  }
}

.overview {
  display: flex;
  align-items: center;
  margin: 8rpx 0 24rpx;
  padding: 28rpx 0;
  border-radius: $yl-radius-lg;
  background: $yl-gradient;
  box-shadow: $yl-shadow-primary;

  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
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

  &__divider {
    width: 1rpx;
    height: 56rpx;
    background: rgba(255, 255, 255, 0.25);
  }
}

.list {
  &__date {
    display: flex;
    align-items: center;
    padding: 20rpx 0 14rpx;
    font-size: 24rpx;
    font-weight: 600;
    color: $yl-text-2;

    &::before {
      content: '';
      width: 10rpx;
      height: 10rpx;
      border-radius: 50%;
      background: $yl-primary;
      margin-right: 12rpx;
    }
  }
}

.record {
  background: #fff;
  border-radius: $yl-radius-lg;
  box-shadow: $yl-shadow-sm;
  margin-bottom: 20rpx;
  overflow: hidden;
  transition: box-shadow 0.2s ease;

  &--hover {
    background: #fbfdfc;
  }

  &.is-open {
    box-shadow: $yl-shadow;
  }

  &__main {
    display: flex;
    align-items: center;
    padding: 20rpx;
  }

  &__cover {
    width: 120rpx;
    height: 120rpx;
    border-radius: $yl-radius-sm;
    overflow: hidden;
    flex-shrink: 0;
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

  &__body {
    flex: 1;
    min-width: 0;
    padding: 0 20rpx;
    display: flex;
    flex-direction: column;
  }

  &__name {
    font-size: 30rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__meta {
    display: flex;
    align-items: center;
    margin-top: 8rpx;
  }

  &__time {
    margin-left: 6rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__dot {
    margin: 0 8rpx;
    color: $yl-text-4;
  }

  &__conf {
    height: 48rpx;
    padding: 0 16rpx;
    border-radius: $yl-radius-pill;
    display: flex;
    align-items: center;
    font-size: 24rpx;
    font-weight: 700;
    flex-shrink: 0;
  }

  &__arrow {
    margin-left: 12rpx;
    flex-shrink: 0;
  }

  &__detail {
    padding: 4rpx 24rpx 20rpx;
    border-top: 1rpx solid $yl-border;
  }

  &__row {
    display: flex;
    align-items: center;
    padding: 14rpx 0;
  }

  &__rank {
    width: 36rpx;
    height: 36rpx;
    border-radius: 10rpx;
    background: $yl-bg-input;
    color: $yl-text-3;
    font-size: 20rpx;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &.is-top {
      background: $yl-primary;
      color: #fff;
    }
  }

  &__class {
    width: 200rpx;
    margin-left: 14rpx;
    font-size: 26rpx;
    color: $yl-text-1;
    flex-shrink: 0;
  }

  &__bar {
    flex: 1;
    height: 14rpx;
    border-radius: 7rpx;
    background: $yl-bg-input;
    overflow: hidden;
    margin: 0 16rpx;
  }

  &__fill {
    height: 100%;
    border-radius: 7rpx;
    transition: width 0.5s ease;
  }

  &__pct {
    width: 76rpx;
    text-align: right;
    font-size: 24rpx;
    font-weight: 700;
    flex-shrink: 0;
  }

  &__actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 12rpx;
  }

  &__action {
    display: flex;
    align-items: center;
    height: 56rpx;
    padding: 0 20rpx;
    margin-left: 12rpx;
    border-radius: $yl-radius-pill;
    background: $yl-bg-input;
    font-size: 22rpx;
    color: $yl-text-2;

    text {
      margin-left: 6rpx;
    }

    &--danger {
      background: $yl-danger-soft;
      color: $yl-danger;
    }
  }
}
</style>
