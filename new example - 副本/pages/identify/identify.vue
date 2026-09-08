<template>
  <view class="identify yl-page">
    <yl-navbar title="植物识别" border>
      <template #right>
        <view class="identify__nav-btn" hover-class="yl-hover" @click="goHistory">
          <uni-icons type="calendar" size="20" color="#1A1F1C"></uni-icons>
        </view>
      </template>
    </yl-navbar>

    <view class="yl-container identify__body">
      <!-- ===================== 选择阶段 ===================== -->
      <block v-if="!results.length">
        <!-- 引导卡片 -->
        <view class="intro yl-anim-up">
          <view class="intro__orb intro__orb--1"></view>
          <view class="intro__orb intro__orb--2"></view>
          <view class="intro__text">
            <text class="intro__title">上传植物照片</text>
            <text class="intro__desc">支持拍照或从相册选择，一次最多 9 张，AI 将给出前 5 个候选物种及置信度</text>
          </view>
          <view class="intro__icon">
            <uni-icons type="scan" size="46" color="#FFFFFF"></uni-icons>
          </view>
        </view>

        <!-- 两个入口 -->
        <view class="pick yl-anim-up yl-delay-1">
          <view class="pick__btn" hover-class="yl-press" hover-stay-time="80" @click="choose('camera')">
            <view class="pick__icon pick__icon--green">
              <uni-icons type="camera-filled" size="30" color="#1DA462"></uni-icons>
            </view>
            <text class="pick__title">拍照识别</text>
            <text class="pick__desc">打开相机现场拍摄</text>
          </view>
          <view class="pick__btn" hover-class="yl-press" hover-stay-time="80" @click="choose('album')">
            <view class="pick__icon pick__icon--blue">
              <uni-icons type="images-filled" size="30" color="#3B82F6"></uni-icons>
            </view>
            <text class="pick__title">相册选择</text>
            <text class="pick__desc">从图库挑选照片</text>
          </view>
        </view>

        <!-- 已选图片 -->
        <view v-if="images.length" class="sel yl-anim-up">
          <view class="sel__head">
            <text class="sel__title">已选择 {{ images.length }} 张</text>
            <view class="sel__clear" hover-class="yl-hover" @click="images = []">
              <uni-icons type="trash" size="14" color="#9AA5A0"></uni-icons>
              <text>清空</text>
            </view>
          </view>
          <view class="sel__grid">
            <view v-for="(img, i) in images" :key="img + i" class="sel__item">
              <image class="sel__img" :src="img" mode="aspectFill" @click="preview(img)"></image>
              <view class="sel__remove" @click.stop="removeImage(i)">
                <uni-icons type="closeempty" size="14" color="#FFFFFF"></uni-icons>
              </view>
              <view v-if="uploading && i === currentIndex" class="sel__mask">
                <view class="yl-spinner sel__spinner"></view>
              </view>
              <view v-else-if="uploading && i < currentIndex" class="sel__done">
                <uni-icons type="checkmarkempty" size="14" color="#FFFFFF"></uni-icons>
              </view>
            </view>
            <view v-if="images.length < 9 && !uploading" class="sel__item sel__add" hover-class="yl-press" @click="choose('album')">
              <uni-icons type="plusempty" size="30" color="#9AA5A0"></uni-icons>
              <text>添加</text>
            </view>
          </view>
        </view>

        <!-- 进度 -->
        <view v-if="uploading" class="progress yl-anim-in">
          <view class="progress__head">
            <text class="progress__text">正在识别第 {{ currentIndex + 1 }} / {{ images.length }} 张</text>
            <text class="progress__pct">{{ overallProgress }}%</text>
          </view>
          <view class="progress__bar">
            <view class="progress__fill" :style="{ width: overallProgress + '%' }"></view>
          </view>
          <text class="progress__hint">{{ fileProgress < 100 ? '上传图片中…' : '模型推理中，请稍候…' }}</text>
        </view>

        <button
          v-if="images.length"
          class="yl-btn yl-btn--primary identify__submit"
          :disabled="uploading"
          hover-class="yl-press"
          @click="start"
        >
          <view v-if="uploading" class="yl-spinner identify__spinner"></view>
          <text>{{ uploading ? '识别中…' : `开始识别（${images.length} 张）` }}</text>
        </button>

        <!-- 小贴士 -->
        <view class="tips yl-anim-up yl-delay-2">
          <view class="tips__row">
            <uni-icons type="checkmarkempty" size="14" color="#1DA462"></uni-icons>
            <text>让植物主体尽量占满画面，背景简洁</text>
          </view>
          <view class="tips__row">
            <uni-icons type="checkmarkempty" size="14" color="#1DA462"></uni-icons>
            <text>对准叶片、孢子体等特征部位，保持对焦清晰</text>
          </view>
          <view class="tips__row">
            <uni-icons type="checkmarkempty" size="14" color="#1DA462"></uni-icons>
            <text>避免逆光与强反光，光线均匀时效果更好</text>
          </view>
        </view>
      </block>

      <!-- ===================== 结果阶段 ===================== -->
      <block v-else>
        <view class="results__head yl-anim-up">
          <view>
            <text class="results__title">识别结果</text>
            <text class="results__sub">共 {{ results.length }} 张 · {{ successCount }} 张成功，已保存至记录</text>
          </view>
          <view class="results__badge">
            <uni-icons type="checkmarkempty" size="14" color="#146C43"></uni-icons>
            <text>完成</text>
          </view>
        </view>

        <view v-for="(r, i) in results" :key="i" class="result yl-anim-up" :class="'yl-delay-' + Math.min(i + 1, 5)">
          <view class="result__top">
            <image class="result__img" :src="r.image" mode="aspectFill" @click="preview(r.image)"></image>

            <view v-if="!r.error" class="result__best">
              <text class="result__label">最可能是</text>
              <text class="result__name">{{ r.best.class }}</text>
              <view class="result__conf">
                <view class="ring" :style="ringStyle(r.best.confidence)">
                  <view class="ring__inner">
                    <text class="ring__pct" :style="{ color: level(r.best.confidence).color }">{{ percent(r.best.confidence) }}%</text>
                  </view>
                </view>
                <view class="result__conf-text">
                  <text class="result__level" :style="{ color: level(r.best.confidence).color }">置信度 · {{ level(r.best.confidence).text }}</text>
                  <text class="result__hint">{{ hintFor(r.best.confidence) }}</text>
                </view>
              </view>
            </view>

            <view v-else class="result__best">
              <text class="result__label">识别失败</text>
              <text class="result__err">{{ r.error }}</text>
              <view class="result__retry" hover-class="yl-press" @click="retry(i)">
                <uni-icons type="refreshempty" size="14" color="#146C43"></uni-icons>
                <text>重试</text>
              </view>
            </view>
          </view>

          <view v-if="r.results.length > 1" class="result__list">
            <text class="result__list-title">全部候选</text>
            <view v-for="(it, j) in r.results" :key="j" class="result__row">
              <view class="result__rank" :class="{ 'is-top': j === 0 }">
                <text>{{ j + 1 }}</text>
              </view>
              <text class="result__class yl-ellipsis">{{ it.class }}</text>
              <view class="result__bar">
                <view class="result__fill" :style="{ width: percent(it.confidence) + '%', background: level(it.confidence).color }"></view>
              </view>
              <text class="result__pct" :style="{ color: level(it.confidence).color }">{{ percent(it.confidence) }}%</text>
            </view>
          </view>
        </view>

        <view class="results__actions">
          <button class="yl-btn yl-btn--light results__btn" hover-class="yl-press" @click="reset">
            <uni-icons type="camera" size="18" color="#146C43"></uni-icons>
            <text class="results__btn-text">再识别一批</text>
          </button>
          <button class="yl-btn yl-btn--primary results__btn" hover-class="yl-press" @click="goHistory">
            <uni-icons type="calendar-filled" size="18" color="#FFFFFF"></uni-icons>
            <text class="results__btn-text">查看识别记录</text>
          </button>
        </view>
      </block>

      <view class="yl-safe-bottom" style="height: 40rpx"></view>
    </view>
  </view>
</template>

<script>
import { uploadImage } from '@/utils/api.js'
import { addRecord, persistImage, confidenceLevel, percent } from '@/utils/history.js'

export default {
  data() {
    return {
      images: [],
      results: [],
      uploading: false,
      currentIndex: 0,
      fileProgress: 0
    }
  },
  computed: {
    overallProgress() {
      if (!this.images.length) return 0
      const per = 100 / this.images.length
      // 上传占每张的 70%，推理占 30%
      const done = this.currentIndex * per
      const cur = Math.min(this.fileProgress, 100) * 0.7 * (per / 100)
      return Math.min(99, Math.round(done + cur))
    },
    successCount() {
      return this.results.filter((r) => !r.error).length
    }
  },
  onLoad() {
    this.consumePending()
  },
  onShow() {
    // 页面实例被复用（如 H5 路由回退）时也能接收首页带入的图片
    this.consumePending()
  },
  methods: {
    percent,
    level: confidenceLevel,
    /** 读取首页快捷入口带入的图片并自动开始识别 */
    consumePending() {
      const app = getApp()
      const pending = app && app.globalData ? app.globalData.pendingImages : []
      if (!Array.isArray(pending) || !pending.length || this.uploading) return
      app.globalData.pendingImages = []
      this.results = []
      this.images = pending.slice(0, 9)
      this.$nextTick(() => this.start())
    },
    hintFor(c) {
      if (c >= 0.8) return '结果可信度较高'
      if (c >= 0.5) return '建议参考其他候选'
      return '可尝试换角度重拍'
    },
    ringStyle(c) {
      const p = percent(c)
      const color = confidenceLevel(c).color
      return { background: `conic-gradient(${color} ${p}%, #EAF0EC 0)` }
    },
    choose(source) {
      const remain = 9 - this.images.length
      if (remain <= 0) {
        uni.showToast({ title: '最多选择 9 张图片', icon: 'none' })
        return
      }
      uni.chooseImage({
        count: source === 'camera' ? 1 : remain,
        sizeType: ['compressed'],
        sourceType: [source],
        success: (res) => {
          this.images = this.images.concat(res.tempFilePaths || []).slice(0, 9)
        },
        fail: () => {}
      })
    },
    removeImage(i) {
      if (this.uploading) return
      this.images.splice(i, 1)
    },
    preview(url) {
      if (!url) return
      uni.previewImage({ urls: [url] })
    },
    normalize(list) {
      const arr = Array.isArray(list) ? list.slice() : []
      arr.sort((a, b) => (Number(b.confidence) || 0) - (Number(a.confidence) || 0))
      return arr.map((it) => ({ class: String(it.class || '未知'), confidence: Number(it.confidence) || 0 }))
    },
    async recognizeOne(path) {
      this.fileProgress = 0
      const res = await uploadImage(path, (p) => {
        this.fileProgress = p
      })
      this.fileProgress = 100
      if (res && res.code === 200 && res.data) {
        const results = this.normalize(res.data.recognition_results)
        if (!results.length) throw new Error('未检测到植物，请换一张更清晰的照片')
        return { results, filename: res.data.filename || '' }
      }
      throw new Error((res && res.message) || '识别失败，请重试')
    },
    async start() {
      if (this.uploading || !this.images.length) return
      this.uploading = true
      this.currentIndex = 0
      const output = []

      for (let i = 0; i < this.images.length; i++) {
        this.currentIndex = i
        const path = this.images[i]
        try {
          const { results, filename } = await this.recognizeOne(path)
          const saved = await persistImage(path)
          addRecord({ image: saved, results, filename })
          output.push({ image: saved, results, best: results[0], error: '' })
        } catch (e) {
          output.push({ image: path, results: [], best: null, error: (e && e.message) || '识别失败' })
        }
      }

      this.uploading = false
      this.results = output
      this.images = []
      uni.pageScrollTo({ scrollTop: 0, duration: 200 })

      const ok = output.filter((r) => !r.error).length
      uni.showToast({
        title: ok === output.length ? '识别完成' : `完成，${output.length - ok} 张失败`,
        icon: ok === output.length ? 'success' : 'none'
      })
    },
    async retry(i) {
      const item = this.results[i]
      if (!item || this.uploading) return
      uni.showLoading({ title: '重新识别…', mask: true })
      try {
        const { results, filename } = await this.recognizeOne(item.image)
        const saved = await persistImage(item.image)
        addRecord({ image: saved, results, filename })
        this.results.splice(i, 1, { image: saved, results, best: results[0], error: '' })
        uni.showToast({ title: '识别成功', icon: 'success' })
      } catch (e) {
        uni.showToast({ title: (e && e.message) || '识别失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    reset() {
      this.results = []
      this.images = []
      this.fileProgress = 0
      this.currentIndex = 0
    },
    goHistory() {
      uni.reLaunch({ url: '/pages/main/main?tab=2' })
    }
  }
}
</script>

<style lang="scss" scoped>
.identify {
  &__body {
    padding-top: 16rpx;
    padding-bottom: 40rpx;
  }

  &__nav-btn {
    width: 72rpx;
    height: 72rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__submit {
    margin-top: 32rpx;
  }

  &__spinner {
    border-color: rgba(255, 255, 255, 0.35);
    border-top-color: #fff;
    margin-right: 14rpx;
  }
}

/* 引导卡片 */
.intro {
  position: relative;
  display: flex;
  align-items: center;
  padding: 40rpx 32rpx;
  border-radius: $yl-radius-xl;
  background: $yl-gradient-hero;
  overflow: hidden;
  box-shadow: $yl-shadow-primary;

  &__orb {
    position: absolute;
    border-radius: 50%;

    &--1 {
      width: 300rpx;
      height: 300rpx;
      right: -80rpx;
      top: -120rpx;
      background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0) 70%);
    }

    &--2 {
      width: 200rpx;
      height: 200rpx;
      left: -60rpx;
      bottom: -80rpx;
      background: radial-gradient(circle at 50% 50%, rgba(111, 211, 154, 0.4), rgba(111, 211, 154, 0) 70%);
    }
  }

  &__text {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  &__title {
    font-size: 38rpx;
    font-weight: 800;
    color: #fff;
  }

  &__desc {
    margin-top: 10rpx;
    font-size: 24rpx;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.82);
    padding-right: 12rpx;
  }

  &__icon {
    position: relative;
    width: 128rpx;
    height: 128rpx;
    border-radius: 40rpx;
    background: rgba(255, 255, 255, 0.18);
    border: 2rpx solid rgba(255, 255, 255, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
}

/* 入口 */
.pick {
  display: flex;
  margin-top: 24rpx;

  &__btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 36rpx 20rpx 30rpx;
    border-radius: $yl-radius-lg;
    background: #fff;
    box-shadow: $yl-shadow;

    &:first-child {
      margin-right: 20rpx;
    }
  }

  &__icon {
    width: 104rpx;
    height: 104rpx;
    border-radius: 32rpx;
    display: flex;
    align-items: center;
    justify-content: center;

    &--green {
      background: $yl-primary-soft;
    }

    &--blue {
      background: $yl-info-soft;
    }
  }

  &__title {
    margin-top: 18rpx;
    font-size: 30rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__desc {
    margin-top: 6rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }
}

/* 已选图片 */
.sel {
  margin-top: 24rpx;
  padding: 28rpx 24rpx 12rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;

  &__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20rpx;
  }

  &__title {
    font-size: 28rpx;
    font-weight: 700;
    color: $yl-text-1;
  }

  &__clear {
    display: flex;
    align-items: center;
    font-size: 22rpx;
    color: $yl-text-3;

    text {
      margin-left: 4rpx;
    }
  }

  &__grid {
    display: flex;
    flex-wrap: wrap;
  }

  &__item {
    position: relative;
    width: calc((100% - 32rpx) / 3);
    height: 200rpx;
    margin-right: 16rpx;
    margin-bottom: 16rpx;
    border-radius: $yl-radius-sm;
    overflow: hidden;
    background: $yl-bg-input;

    &:nth-child(3n) {
      margin-right: 0;
    }
  }

  &__img {
    width: 100%;
    height: 100%;
    display: block;
  }

  &__remove {
    position: absolute;
    right: 8rpx;
    top: 8rpx;
    width: 40rpx;
    height: 40rpx;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__mask {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    background: rgba(14, 59, 46, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__spinner {
    border-color: rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
  }

  &__done {
    position: absolute;
    left: 8rpx;
    bottom: 8rpx;
    width: 36rpx;
    height: 36rpx;
    border-radius: 50%;
    background: $yl-primary;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__add {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2rpx dashed $yl-text-4;
    background: transparent;
    font-size: 22rpx;
    color: $yl-text-3;

    text {
      margin-top: 6rpx;
    }
  }
}

/* 进度 */
.progress {
  margin-top: 24rpx;
  padding: 24rpx 28rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;

  &__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__text {
    font-size: 26rpx;
    color: $yl-text-1;
    font-weight: 600;
  }

  &__pct {
    font-size: 28rpx;
    font-weight: 800;
    color: $yl-primary;
  }

  &__bar {
    height: 16rpx;
    border-radius: 8rpx;
    background: $yl-bg-input;
    overflow: hidden;
    margin-top: 16rpx;
  }

  &__fill {
    height: 100%;
    border-radius: 8rpx;
    background: $yl-gradient;
    transition: width 0.3s ease;
  }

  &__hint {
    display: block;
    margin-top: 12rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }
}

/* 小贴士 */
.tips {
  margin-top: 28rpx;
  padding: 24rpx 28rpx;
  border-radius: $yl-radius-lg;
  background: $yl-primary-soft;

  &__row {
    display: flex;
    align-items: center;
    padding: 8rpx 0;
    font-size: 24rpx;
    color: $yl-primary-dark;

    text {
      margin-left: 10rpx;
    }
  }
}

/* 结果 */
.results {
  &__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20rpx;
  }

  &__title {
    display: block;
    font-size: 40rpx;
    font-weight: 800;
    color: $yl-text-1;
  }

  &__sub {
    display: block;
    margin-top: 6rpx;
    font-size: 24rpx;
    color: $yl-text-3;
  }

  &__badge {
    display: flex;
    align-items: center;
    height: 48rpx;
    padding: 0 18rpx;
    border-radius: $yl-radius-pill;
    background: $yl-primary-soft;
    color: $yl-primary-dark;
    font-size: 22rpx;
    font-weight: 600;

    text {
      margin-left: 6rpx;
    }
  }

  &__actions {
    display: flex;
    margin-top: 12rpx;
  }

  &__btn {
    flex: 1;

    &:first-child {
      margin-right: 20rpx;
    }
  }

  &__btn-text {
    margin-left: 10rpx;
  }
}

.result {
  margin-bottom: 24rpx;
  border-radius: $yl-radius-lg;
  background: #fff;
  box-shadow: $yl-shadow;
  overflow: hidden;

  &__top {
    display: flex;
    padding: 24rpx;
  }

  &__img {
    width: 200rpx;
    height: 200rpx;
    border-radius: $yl-radius;
    flex-shrink: 0;
    background: $yl-bg-input;
  }

  &__best {
    flex: 1;
    min-width: 0;
    padding-left: 24rpx;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  &__label {
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__name {
    margin-top: 4rpx;
    font-size: 40rpx;
    font-weight: 800;
    color: $yl-text-1;
    line-height: 1.2;
  }

  &__conf {
    display: flex;
    align-items: center;
    margin-top: 16rpx;
  }

  &__conf-text {
    display: flex;
    flex-direction: column;
    margin-left: 16rpx;
    min-width: 0;
  }

  &__level {
    font-size: 24rpx;
    font-weight: 700;
  }

  &__hint {
    margin-top: 4rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__err {
    margin-top: 6rpx;
    font-size: 26rpx;
    color: $yl-danger;
    line-height: 1.5;
  }

  &__retry {
    display: inline-flex;
    align-self: flex-start;
    align-items: center;
    height: 56rpx;
    padding: 0 22rpx;
    margin-top: 16rpx;
    border-radius: $yl-radius-pill;
    background: $yl-primary-soft;
    color: $yl-primary-dark;
    font-size: 24rpx;
    font-weight: 600;

    text {
      margin-left: 6rpx;
    }
  }

  &__list {
    padding: 8rpx 24rpx 20rpx;
    border-top: 1rpx solid $yl-border;
  }

  &__list-title {
    display: block;
    padding: 16rpx 0 6rpx;
    font-size: 22rpx;
    color: $yl-text-3;
  }

  &__row {
    display: flex;
    align-items: center;
    padding: 12rpx 0;
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
    width: 190rpx;
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
    transition: width 0.6s ease;
  }

  &__pct {
    width: 76rpx;
    text-align: right;
    font-size: 24rpx;
    font-weight: 700;
    flex-shrink: 0;
  }
}

/* 置信度环 */
.ring {
  width: 108rpx;
  height: 108rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &__inner {
    width: 84rpx;
    height: 84rpx;
    border-radius: 50%;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__pct {
    font-size: 22rpx;
    font-weight: 800;
  }
}
</style>
