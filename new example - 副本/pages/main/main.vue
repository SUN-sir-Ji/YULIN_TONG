<template>
  <view class="main">
    <view class="main__body">
      <home-tab v-if="visited[0]" v-show="current === 0" ref="home" @switch="switchTab" @category="openCategory"></home-tab>
      <atlas-tab v-if="visited[1]" v-show="current === 1" ref="atlas" :pending-category="pendingCategory" @consumed="pendingCategory = null"></atlas-tab>
      <history-tab v-if="visited[2]" v-show="current === 2" ref="history"></history-tab>
      <mine-tab v-if="visited[3]" v-show="current === 3" ref="mine" @switch="switchTab"></mine-tab>
    </view>

    <yl-tabbar :current="current" :badges="badges" @change="switchTab" @scan="goIdentify"></yl-tabbar>
  </view>
</template>

<script>
/**
 * 主容器页：首页 / 图鉴 / 记录 / 我的
 * 各 Tab 以组件形式常驻（首次进入时挂载），切换无闪烁。
 */
import HomeTab from './components/home-tab.vue'
import AtlasTab from './components/atlas-tab.vue'
import HistoryTab from './components/history-tab.vue'
import MineTab from './components/mine-tab.vue'

export default {
  components: { HomeTab, AtlasTab, HistoryTab, MineTab },
  data() {
    return {
      current: 0,
      visited: [true, false, false, false],
      pendingCategory: null,
      badges: {}
    }
  },
  onLoad(options) {
    const tab = Number(options && options.tab)
    if (!Number.isNaN(tab) && tab >= 0 && tab <= 3) this.switchTab(tab)
  },
  onShow() {
    // 从识别页返回时刷新记录 / 首页最近识别 / 我的统计
    this.$nextTick(() => {
      ;['home', 'history', 'mine'].forEach((key) => {
        const ref = this.$refs[key]
        if (ref && typeof ref.refresh === 'function') ref.refresh()
      })
    })
  },
  methods: {
    switchTab(index) {
      if (!this.visited[index]) this.visited[index] = true
      this.current = index
    },
    openCategory(category) {
      this.pendingCategory = category
      this.switchTab(1)
    },
    goIdentify() {
      uni.navigateTo({ url: '/pages/identify/identify' })
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: $yl-bg;

  &__body {
    width: 100%;
    height: 100%;
  }
}
</style>
