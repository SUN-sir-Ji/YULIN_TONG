<template>
  <view class="yl-picker" :class="{ 'is-show': visible }" v-if="rendered">
    <view class="yl-picker__mask" @click="close" @touchmove.stop.prevent></view>

    <view class="yl-picker__sheet yl-safe-bottom" @touchmove.stop>
      <view class="yl-picker__handle"></view>

      <!-- 头部 -->
      <view class="yl-picker__head">
        <view>
          <text class="yl-picker__title">植物分类导航</text>
          <text class="yl-picker__sub">门 → 纲 → 目 → 科 → 属，逐级浏览</text>
        </view>
        <view class="yl-picker__close" hover-class="yl-hover" @click="close">
          <uni-icons type="closeempty" size="20" color="#5B6660"></uni-icons>
        </view>
      </view>

      <!-- 面包屑 -->
      <scroll-view scroll-x class="yl-picker__crumbs" :scroll-into-view="crumbScrollId" scroll-with-animation>
        <view class="yl-picker__crumbs-inner">
          <view class="yl-picker__crumb" :class="{ 'is-current': path.length === 0 }" id="crumb-root" @click="jumpTo(-1)">
            <uni-icons type="home-filled" size="14" :color="path.length === 0 ? '#1DA462' : '#9AA5A0'"></uni-icons>
            <text class="yl-picker__crumb-text">全部</text>
          </view>
          <block v-for="(node, i) in path" :key="node.id">
            <uni-icons type="right" size="12" color="#C3CBC7"></uni-icons>
            <view
              class="yl-picker__crumb"
              :class="{ 'is-current': i === path.length - 1 }"
              :id="'crumb-' + i"
              @click="jumpTo(i)"
            >
              <text class="yl-picker__crumb-text">{{ node.name }}</text>
            </view>
          </block>
        </view>
      </scroll-view>

      <!-- 当前层级说明 -->
      <view class="yl-picker__level">
        <text class="yl-tag">{{ levelLabel }}</text>
        <text class="yl-picker__level-tip">{{ levelTip }}</text>
      </view>

      <!-- 列表 -->
      <scroll-view scroll-y class="yl-picker__list" :scroll-top="listScrollTop">
        <view v-if="loading" class="yl-picker__loading">
          <view v-for="n in 6" :key="n" class="yl-picker__skeleton yl-skeleton"></view>
        </view>

        <view v-else-if="items.length === 0" class="yl-picker__empty">
          <uni-icons type="info" size="30" color="#C3CBC7"></uni-icons>
          <text>该分类下暂无子分类</text>
        </view>

        <view v-else>
          <view
            v-for="item in items"
            :key="item.id"
            class="yl-picker__row"
            hover-class="yl-picker__row--hover"
            hover-stay-time="80"
            @click="onRowTap(item)"
          >
            <view class="yl-picker__row-icon" :style="{ background: levelColor.bg }">
              <text :style="{ color: levelColor.color }">{{ levelShort }}</text>
            </view>
            <view class="yl-picker__row-body">
              <text class="yl-picker__row-name">{{ item.name }}</text>
              <text class="yl-picker__row-latin">{{ item.value }}</text>
            </view>
            <view class="yl-picker__row-select" hover-class="yl-hover" @click.stop="select(item)">
              <text>查看</text>
            </view>
            <view v-if="item.hasChildren !== false && depth < 4" class="yl-picker__row-arrow">
              <uni-icons type="right" size="16" color="#C3CBC7"></uni-icons>
            </view>
          </view>
        </view>
        <view style="height: 24rpx"></view>
      </scroll-view>

      <!-- 底部操作 -->
      <view class="yl-picker__foot">
        <view v-if="path.length" class="yl-picker__foot-btn yl-picker__foot-btn--ghost" hover-class="yl-press" @click="jumpTo(path.length - 2)">
          <uni-icons type="left" size="16" color="#5B6660"></uni-icons>
          <text>上一级</text>
        </view>
        <view class="yl-picker__foot-btn yl-picker__foot-btn--primary" hover-class="yl-press" @click="confirmCurrent">
          <text>{{ path.length ? `查看「${current.name}」下的植物` : '查看全部植物' }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
/**
 * yl-category-picker 分类导航弹层
 * 数据来源：/api/plants/categories?parent_id=N（懒加载 + 缓存）
 * 层级：0 门 phylum / 1 纲 class / 2 目 order / 3 科 family / 4 属 genus
 *
 * 使用：this.$refs.picker.open() ；@confirm="(category) => ..."
 * category: { id, name, value, level, field, path: [...] } ；全部 => null
 */
import { getPlantCategories } from '@/utils/api.js'

const LEVELS = [
  { key: 'phylum', label: '门', field: 'phylum_latin_name', color: '#1DA462', bg: '#E3F6EA', tip: '选择一个「门」，或点击行进入下一级' },
  { key: 'class', label: '纲', field: 'class_latin_name', color: '#3B82F6', bg: '#E8F0FE', tip: '选择一个「纲」，或继续进入「目」' },
  { key: 'order', label: '目', field: 'order_latin_name', color: '#8B5CF6', bg: '#F1EBFF', tip: '选择一个「目」，或继续进入「科」' },
  { key: 'family', label: '科', field: 'family_latin_name', color: '#F5A524', bg: '#FFF4DF', tip: '选择一个「科」，或继续进入「属」' },
  { key: 'genus', label: '属', field: 'genus_latin_name', color: '#E5484D', bg: '#FDECEC', tip: '点击「属」直接查看该属植物' }
]

export default {
  name: 'YlCategoryPicker',
  emits: ['confirm', 'close'],
  data() {
    return {
      rendered: false,
      visible: false,
      loading: false,
      path: [], // 已进入的节点 [{id,name,value,level}]
      items: [],
      cache: {}, // parentId -> items
      listScrollTop: 0,
      crumbScrollId: ''
    }
  },
  computed: {
    depth() {
      return this.path.length
    },
    current() {
      return this.path[this.path.length - 1] || null
    },
    levelMeta() {
      return LEVELS[Math.min(this.depth, 4)]
    },
    levelLabel() {
      return `当前层级：${this.levelMeta.label}`
    },
    levelShort() {
      return this.levelMeta.label
    },
    levelTip() {
      return this.levelMeta.tip
    },
    levelColor() {
      return { color: this.levelMeta.color, bg: this.levelMeta.bg }
    }
  },
  methods: {
    open() {
      this.rendered = true
      this.$nextTick(() => {
        setTimeout(() => {
          this.visible = true
        }, 20)
      })
      if (this.items.length === 0 && this.path.length === 0) this.load(0)
    },
    close() {
      this.visible = false
      this.$emit('close')
      setTimeout(() => {
        if (!this.visible) this.rendered = false
      }, 300)
    },
    async load(parentId) {
      const key = String(parentId)
      if (this.cache[key]) {
        this.items = this.cache[key]
        return
      }
      this.loading = true
      try {
        const list = await getPlantCategories(parentId)
        this.cache[key] = list
        this.items = list
      } catch (e) {
        this.items = []
        uni.showToast({ title: (e && e.message) || '获取分类失败', icon: 'none' })
      } finally {
        this.loading = false
      }
    },
    buildCategory(node, level) {
      const meta = LEVELS[level]
      return {
        id: node.id,
        name: node.name,
        value: node.value,
        level,
        levelLabel: meta.label,
        field: meta.field,
        path: this.path.slice(0, level).map((p) => p.name).concat(node.name)
      }
    },
    onRowTap(item) {
      // 属为最末级：直接选中
      if (this.depth >= 4 || item.hasChildren === false) {
        this.select(item)
        return
      }
      this.path.push({ id: item.id, name: item.name, value: item.value, level: this.depth })
      this.listScrollTop = this.listScrollTop === 0 ? 0.1 : 0
      this.$nextTick(() => {
        this.crumbScrollId = 'crumb-' + (this.path.length - 1)
      })
      this.load(item.id)
    },
    jumpTo(index) {
      // index = -1 回到根
      this.path = this.path.slice(0, index + 1)
      const parentId = index < 0 ? 0 : this.path[index].id
      this.crumbScrollId = index < 0 ? 'crumb-root' : 'crumb-' + index
      this.load(parentId)
    },
    select(item) {
      const category = this.buildCategory(item, this.depth)
      this.$emit('confirm', category)
      this.close()
    },
    confirmCurrent() {
      if (!this.current) {
        this.$emit('confirm', null)
        this.close()
        return
      }
      const node = this.current
      const category = {
        id: node.id,
        name: node.name,
        value: node.value,
        level: node.level,
        levelLabel: LEVELS[node.level].label,
        field: LEVELS[node.level].field,
        path: this.path.map((p) => p.name)
      }
      this.$emit('confirm', category)
      this.close()
    },
    reset() {
      this.path = []
      this.items = this.cache['0'] || []
    }
  }
}
</script>

<style lang="scss" scoped>
.yl-picker {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 1200;

  &__mask {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    background: $yl-mask;
    opacity: 0;
    transition: opacity 0.28s ease;
  }

  &__sheet {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 78vh;
    background: #fff;
    border-top-left-radius: 40rpx;
    border-top-right-radius: 40rpx;
    display: flex;
    flex-direction: column;
    transform: translateY(100%);
    transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
    box-shadow: 0 -10rpx 40rpx rgba(0, 0, 0, 0.08);
  }

  &.is-show &__mask {
    opacity: 1;
  }

  &.is-show &__sheet {
    transform: translateY(0);
  }

  &__handle {
    width: 72rpx;
    height: 8rpx;
    border-radius: 4rpx;
    background: #e3e8e5;
    margin: 16rpx auto 0;
  }

  &__head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 24rpx 32rpx 12rpx;
  }

  &__title {
    display: block;
    font-size: 34rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__sub {
    display: block;
    margin-top: 6rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__close {
    width: 64rpx;
    height: 64rpx;
    border-radius: 50%;
    background: $yl-bg-input;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__crumbs {
    width: 100%;
    white-space: nowrap;
    padding: 8rpx 0;
  }

  &__crumbs-inner {
    display: inline-flex;
    align-items: center;
    padding: 0 32rpx;
  }

  &__crumb {
    display: inline-flex;
    align-items: center;
    height: 52rpx;
    padding: 0 18rpx;
    border-radius: $yl-radius-pill;
    background: $yl-bg-input;
    margin: 0 8rpx;
    font-size: 24rpx;
    color: $yl-text-2;

    &.is-current {
      background: $yl-primary-soft;
      color: $yl-primary-dark;
      font-weight: 600;
    }

    .uni-icons {
      margin-right: 6rpx;
    }
  }

  &__level {
    display: flex;
    align-items: center;
    padding: 12rpx 32rpx 8rpx;
  }

  &__level-tip {
    margin-left: 16rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__list {
    flex: 1;
    height: 0;
    padding: 0 24rpx;
  }

  &__loading {
    padding: 8rpx 0;
  }

  &__skeleton {
    height: 108rpx;
    margin: 12rpx 0;
    border-radius: $yl-radius;
  }

  &__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 96rpx 0;
    color: $yl-text-3;
    font-size: 24rpx;

    text {
      margin-top: 16rpx;
    }
  }

  &__row {
    display: flex;
    align-items: center;
    padding: 20rpx 16rpx;
    margin: 8rpx 0;
    border-radius: $yl-radius;
    transition: background 0.15s ease;

    &--hover {
      background: $yl-bg;
    }
  }

  &__row-icon {
    width: 72rpx;
    height: 72rpx;
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    font-weight: 700;
    margin-right: 20rpx;
    flex-shrink: 0;
  }

  &__row-body {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }

  &__row-name {
    font-size: 29rpx;
    font-weight: 600;
    color: $yl-text-1;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  &__row-latin {
    margin-top: 4rpx;
    font-size: 22rpx;
    font-style: italic;
    color: $yl-text-3;
    text-transform: capitalize;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  &__row-select {
    height: 52rpx;
    padding: 0 22rpx;
    border-radius: $yl-radius-pill;
    display: flex;
    align-items: center;
    font-size: 22rpx;
    color: $yl-primary-dark;
    background: $yl-primary-soft;
    margin-left: 12rpx;
    flex-shrink: 0;
  }

  &__row-arrow {
    margin-left: 10rpx;
    flex-shrink: 0;
  }

  &__foot {
    display: flex;
    align-items: center;
    padding: 16rpx 32rpx 20rpx;
    border-top: 1rpx solid $yl-border;
  }

  &__foot-btn {
    height: 88rpx;
    border-radius: $yl-radius-pill;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    font-weight: 600;

    &--ghost {
      width: 200rpx;
      margin-right: 16rpx;
      color: $yl-text-2;
      background: $yl-bg-input;

      text {
        margin-left: 6rpx;
      }
    }

    &--primary {
      flex: 1;
      color: #fff;
      background: $yl-gradient;
      box-shadow: $yl-shadow-primary;
      padding: 0 24rpx;

      text {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
  }
}
</style>
