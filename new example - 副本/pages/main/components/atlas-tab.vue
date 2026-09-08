<template>
  <view class="atlas">
    <scroll-view
      scroll-y
      class="atlas__scroll"
      :show-scrollbar="false"
      refresher-enabled
      refresher-default-style="black"
      refresher-background="#F4F7F5"
      :refresher-triggered="refreshing"
      lower-threshold="160"
      @refresherrefresh="onRefresh"
      @scrolltolower="loadMore"
    >
      <!-- 头部 -->
      <view class="atlas__header" :style="{ paddingTop: statusBarHeight + 'px' }">
        <view class="atlas__titlebar">
          <view>
            <text class="atlas__title">植物图鉴</text>
            <text class="atlas__sub">{{ subtitle }}</text>
          </view>
          <view v-if="total" class="atlas__count">
            <uni-icons type="images-filled" size="14" color="#146C43"></uni-icons>
            <text>{{ total }} 种</text>
          </view>
        </view>
      </view>

      <!-- 吸顶搜索 / 筛选 -->
      <view class="atlas__sticky">
        <view class="atlas__search" :class="{ 'is-focus': searchFocus }">
          <uni-icons type="search" size="18" :color="searchFocus ? '#1DA462' : '#9AA5A0'"></uni-icons>
          <input
            class="atlas__input"
            v-model="keyword"
            placeholder="搜索中文名 / 拉丁名 / 别名"
            placeholder-class="atlas__placeholder"
            confirm-type="search"
            @focus="searchFocus = true"
            @blur="searchFocus = false"
          />
          <view v-if="keyword" class="atlas__clear" @click="keyword = ''">
            <uni-icons type="clear" size="18" color="#C3CBC7"></uni-icons>
          </view>
        </view>
        <view class="atlas__filter" :class="{ 'is-active': !!category }" hover-class="yl-press" @click="openPicker">
          <uni-icons type="tune-filled" size="18" :color="category ? '#FFFFFF' : '#146C43'"></uni-icons>
          <text class="atlas__filter-text yl-ellipsis">{{ category ? category.name : '分类' }}</text>
        </view>
      </view>

      <!-- 已选分类路径 -->
      <view v-if="category" class="atlas__path">
        <scroll-view scroll-x class="atlas__path-scroll" :show-scrollbar="false">
          <view class="atlas__path-inner">
            <view v-for="(name, i) in category.path" :key="i" class="atlas__crumb" :class="{ 'is-last': i === category.path.length - 1 }">
              <text>{{ name }}</text>
              <uni-icons v-if="i < category.path.length - 1" type="right" size="10" color="#9AA5A0"></uni-icons>
            </view>
          </view>
        </scroll-view>
        <view class="atlas__path-clear" hover-class="yl-hover" @click="clearCategory">
          <uni-icons type="closeempty" size="14" color="#5B6660"></uni-icons>
          <text>清除</text>
        </view>
      </view>

      <!-- 列表 -->
      <view class="atlas__body">
        <!-- 骨架 -->
        <view v-if="loading && page === 1" class="grid">
          <view v-for="n in 6" :key="'sk' + n" class="grid__item">
            <view class="skeleton-card">
              <view class="skeleton-card__cover yl-skeleton"></view>
              <view class="skeleton-card__line yl-skeleton"></view>
              <view class="skeleton-card__line skeleton-card__line--short yl-skeleton"></view>
            </view>
          </view>
        </view>

        <!-- 结果 -->
        <block v-else>
          <view v-if="filtered.length" class="grid">
            <view v-for="p in filtered" :key="p.id" class="grid__item">
              <yl-plant-card :plant="p" @click="openDetail"></yl-plant-card>
            </view>
          </view>

          <yl-empty
            v-else-if="keyword"
            icon="search"
            title="没有匹配的植物"
            :desc="hasMore ? `已加载 ${plants.length} / ${total} 条，加载更多后再试试` : '换个关键词试试吧'"
            :btn-text="hasMore ? '加载更多' : ''"
            @click="loadMore"
          ></yl-empty>

          <yl-empty
            v-else-if="loadError"
            icon="refreshempty"
            title="加载失败"
            :desc="loadError"
            btn-text="重新加载"
            @click="reload"
          ></yl-empty>

          <yl-empty
            v-else
            icon="images"
            title="该分类下暂无植物"
            desc="换一个分类，或清除筛选查看全部植物"
            btn-text="查看全部"
            @click="clearCategory"
          ></yl-empty>

          <!-- 底部状态 -->
          <view v-if="filtered.length" class="atlas__foot">
            <view v-if="loading" class="yl-loading-row">
              <view class="yl-spinner"></view>
              <text>正在加载…</text>
            </view>
            <view v-else-if="hasMore && keyword" class="atlas__more-btn" hover-class="yl-press" @click="loadMore">
              <text>在更多结果中搜索（已加载 {{ plants.length }} / {{ total }}）</text>
            </view>
            <view v-else-if="!hasMore" class="atlas__end">
              <view class="atlas__end-line"></view>
              <text>已展示全部 {{ filtered.length }} 种植物</text>
              <view class="atlas__end-line"></view>
            </view>
          </view>
        </block>
      </view>

      <view class="yl-tab-spacer"></view>
    </scroll-view>

    <yl-category-picker ref="picker" @confirm="onCategory"></yl-category-picker>
  </view>
</template>

<script>
import { getPlants } from '@/utils/api.js'

export default {
  name: 'AtlasTab',
  props: {
    pendingCategory: { type: Object, default: null }
  },
  emits: ['consumed'],
  data() {
    return {
      statusBarHeight: 0,
      keyword: '',
      searchFocus: false,
      category: null,
      plants: [],
      total: 0,
      page: 1,
      pageSize: 30,
      hasMore: true,
      loading: false,
      refreshing: false,
      loadError: '',
      requestSeq: 0
    }
  },
  computed: {
    subtitle() {
      if (this.category) return `${this.category.levelLabel}：${this.category.name}`
      return '按门 · 纲 · 目 · 科 · 属逐级浏览'
    },
    filtered() {
      const k = this.keyword.trim().toLowerCase()
      if (!k) return this.plants
      return this.plants.filter((p) => {
        const fields = [
          p.species_chinese_name,
          p.species_latin_name,
          p.common_names,
          p.genus_chinese_name,
          p.family_chinese_name,
          p.genus_latin_name,
          p.family_latin_name
        ]
        return fields.some((f) => f && String(f).toLowerCase().indexOf(k) !== -1)
      })
    }
  },
  watch: {
    pendingCategory: {
      immediate: true,
      handler(val) {
        if (val) {
          this.applyCategory(val)
          this.$emit('consumed')
        }
      }
    }
  },
  created() {
    try {
      this.statusBarHeight = uni.getSystemInfoSync().statusBarHeight || 0
    } catch (e) {}
    if (!this.pendingCategory) this.reload()
  },
  methods: {
    openPicker() {
      this.$refs.picker && this.$refs.picker.open()
    },
    onCategory(category) {
      this.applyCategory(category)
    },
    applyCategory(category) {
      this.category = category || null
      this.keyword = ''
      this.reload()
    },
    clearCategory() {
      this.category = null
      this.keyword = ''
      this.$refs.picker && this.$refs.picker.reset()
      this.reload()
    },
    reload() {
      this.page = 1
      this.plants = []
      this.total = 0
      this.hasMore = true
      this.loadError = ''
      return this.fetch()
    },
    async onRefresh() {
      this.refreshing = true
      await this.reload()
      this.refreshing = false
    },
    loadMore() {
      if (!this.hasMore || this.loading) return
      this.fetch()
    },
    async fetch() {
      if (this.loading) return
      this.loading = true
      const seq = ++this.requestSeq
      try {
        const params = { page: this.page, pageSize: this.pageSize }
        if (this.category) {
          params.field = this.category.field
          params.value = this.category.value
        }
        const { list, total } = await getPlants(params)
        if (seq !== this.requestSeq) return // 已被新的请求覆盖

        this.plants = this.page === 1 ? list : this.plants.concat(list)
        this.total = total
        this.hasMore = list.length > 0 && this.plants.length < total
        if (this.hasMore) this.page++
        this.loadError = ''
      } catch (e) {
        if (seq !== this.requestSeq) return
        this.loadError = (e && e.message) || '网络异常，请检查服务器地址'
        if (this.page > 1) uni.showToast({ title: this.loadError, icon: 'none' })
      } finally {
        if (seq === this.requestSeq) this.loading = false
      }
    },
    openDetail(plant) {
      const app = getApp()
      if (app && app.globalData) app.globalData.currentPlant = plant
      try {
        uni.setStorageSync('yl_current_plant', plant)
      } catch (e) {}
      uni.navigateTo({ url: `/pages/plant/plantdetail?id=${plant.id}` })
    }
  }
}
</script>

<style lang="scss" scoped>
.atlas {
  width: 100%;
  height: 100vh;

  &__scroll {
    width: 100%;
    height: 100%;
  }

  &__header {
    padding-left: $yl-page-padding;
    padding-right: $yl-page-padding;
    background: $yl-bg;
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

  &__count {
    display: flex;
    align-items: center;
    height: 48rpx;
    padding: 0 18rpx;
    border-radius: $yl-radius-pill;
    background: $yl-primary-soft;
    color: $yl-primary-dark;
    font-size: 22rpx;
    font-weight: 600;
    margin-bottom: 8rpx;

    text {
      margin-left: 6rpx;
    }
  }

  &__sticky {
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    padding: 12rpx $yl-page-padding 16rpx;
    background: rgba(244, 247, 245, 0.95);
    backdrop-filter: blur(12px);
  }

  &__search {
    flex: 1;
    display: flex;
    align-items: center;
    height: 84rpx;
    padding: 0 20rpx 0 24rpx;
    border-radius: $yl-radius-pill;
    background: #fff;
    border: 2rpx solid transparent;
    box-shadow: $yl-shadow-sm;
    transition: all 0.2s ease;

    &.is-focus {
      border-color: $yl-primary;
      box-shadow: 0 0 0 6rpx rgba(29, 164, 98, 0.12);
    }
  }

  &__input {
    flex: 1;
    height: 100%;
    margin-left: 12rpx;
    font-size: 27rpx;
    color: $yl-text-1;
    min-width: 0;
  }

  &__clear {
    width: 48rpx;
    height: 48rpx;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__filter {
    display: flex;
    align-items: center;
    height: 84rpx;
    max-width: 240rpx;
    padding: 0 24rpx;
    margin-left: 16rpx;
    border-radius: $yl-radius-pill;
    background: $yl-primary-soft;
    color: $yl-primary-dark;
    font-size: 26rpx;
    font-weight: 600;
    transition: all 0.2s ease;

    &.is-active {
      background: $yl-gradient;
      color: #fff;
      box-shadow: $yl-shadow-primary;
    }
  }

  &__filter-text {
    margin-left: 8rpx;
    max-width: 160rpx;
  }

  &__path {
    display: flex;
    align-items: center;
    padding: 0 $yl-page-padding 8rpx;
  }

  &__path-scroll {
    flex: 1;
    white-space: nowrap;
    min-width: 0;
  }

  &__path-inner {
    display: inline-flex;
    align-items: center;
  }

  &__crumb {
    display: inline-flex;
    align-items: center;
    font-size: 22rpx;
    color: $yl-text-3;

    text {
      margin-right: 6rpx;
    }

    .uni-icons {
      margin-right: 6rpx;
    }

    &.is-last text {
      color: $yl-primary-dark;
      font-weight: 600;
    }
  }

  &__path-clear {
    display: flex;
    align-items: center;
    height: 44rpx;
    padding: 0 14rpx;
    margin-left: 12rpx;
    border-radius: $yl-radius-pill;
    background: $yl-bg-input;
    font-size: 22rpx;
    color: $yl-text-2;
    flex-shrink: 0;

    text {
      margin-left: 4rpx;
    }
  }

  &__body {
    padding: 8rpx $yl-page-padding 0;
  }

  &__foot {
    padding: 8rpx 0 20rpx;
  }

  &__more-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80rpx;
    border-radius: $yl-radius-pill;
    background: #fff;
    box-shadow: $yl-shadow-sm;
    color: $yl-primary-dark;
    font-size: 24rpx;
    font-weight: 600;
  }

  &__end {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24rpx 0;
    font-size: 22rpx;
    color: $yl-text-3;

    text {
      margin: 0 20rpx;
    }
  }

  &__end-line {
    width: 80rpx;
    height: 1rpx;
    background: $yl-text-4;
  }
}

.grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  &__item {
    width: calc(50% - 12rpx);
    margin-bottom: 24rpx;
  }
}

.skeleton-card {
  background: #fff;
  border-radius: $yl-radius-lg;
  overflow: hidden;
  padding-bottom: 20rpx;

  &__cover {
    width: 100%;
    height: 240rpx;
    border-radius: 0;
  }

  &__line {
    height: 28rpx;
    margin: 20rpx 20rpx 0;

    &--short {
      width: 50%;
      height: 20rpx;
      margin-top: 12rpx;
    }
  }
}
</style>
