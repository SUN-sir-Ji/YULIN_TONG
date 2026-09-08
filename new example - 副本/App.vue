<script>
import { getBaseUrl } from '@/utils/apiConfig.js'

export default {
  // 全局数据：页面间传递临时对象（如当前查看的植物、待识别的图片）
  globalData: {
    currentPlant: null,
    pendingImages: [],
    statusBarHeight: 0
  },
  onLaunch() {
    try {
      const info = uni.getSystemInfoSync()
      this.globalData.statusBarHeight = info.statusBarHeight || 0
    } catch (e) {}
    console.log('[雨林通] 启动，API 地址：', getBaseUrl())
  },
  onShow() {},
  onHide() {}
}
</script>

<style lang="scss">
/* =====================================================
 * 雨林通 · 全局样式
 * ===================================================== */

page {
  background-color: $yl-bg;
  color: $yl-text-1;
  font-size: $yl-font;
  line-height: 1.5;
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB',
    'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
  -webkit-font-smoothing: antialiased;
}

view,
text,
scroll-view,
image,
input,
button {
  box-sizing: border-box;
}

/* ---------- 通用按压反馈（配合 hover-class 使用） ---------- */
.yl-hover {
  opacity: 0.72;
}

.yl-press {
  transform: scale(0.97);
  opacity: 0.9;
}

/* ---------- 页面容器 ---------- */
.yl-page {
  min-height: 100vh;
  background-color: $yl-bg;
}

.yl-container {
  padding: 0 $yl-page-padding;
}

/* ---------- 卡片 ---------- */
.yl-card {
  background-color: $yl-bg-card;
  border-radius: $yl-radius-lg;
  box-shadow: $yl-shadow;
  padding: $yl-gap-md;
}

/* ---------- 按钮 ---------- */
.yl-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 96rpx;
  border-radius: $yl-radius-pill;
  font-size: 32rpx;
  font-weight: 600;
  letter-spacing: 2rpx;
  border: none;
  margin: 0;
  padding: 0;
  line-height: 1;
  transition: transform 0.15s ease, opacity 0.15s ease;

  &::after {
    border: none;
  }

  &--primary {
    color: #fff;
    background: $yl-gradient;
    box-shadow: $yl-shadow-primary;
  }

  &--light {
    color: $yl-primary-dark;
    background: $yl-primary-soft;
  }

  &--white {
    color: $yl-primary-dark;
    background: #fff;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.12);
  }

  &--outline {
    color: #fff;
    background: transparent;
    border: 2rpx solid rgba(255, 255, 255, 0.7);
  }

  &--ghost {
    color: $yl-text-2;
    background: $yl-bg-input;
  }

  &--danger {
    color: $yl-danger;
    background: $yl-danger-soft;
  }

  &--sm {
    height: 72rpx;
    font-size: 26rpx;
    padding: 0 32rpx;
    width: auto;
  }

  &[disabled],
  &.is-disabled {
    opacity: 0.5;
    box-shadow: none;
  }
}

/* ---------- 区块标题 ---------- */
.yl-section {
  margin-top: $yl-gap-lg;

  &__head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: $yl-gap;
  }

  &__title {
    font-size: 34rpx;
    font-weight: 700;
    color: $yl-text-1;
    position: relative;
    padding-left: 20rpx;

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 8rpx;
      bottom: 8rpx;
      width: 8rpx;
      border-radius: 4rpx;
      background: $yl-gradient;
    }
  }

  &__more {
    font-size: 24rpx;
    color: $yl-text-3;
    display: flex;
    align-items: center;
  }
}

/* ---------- 标签 ---------- */
.yl-tag {
  display: inline-flex;
  align-items: center;
  height: 44rpx;
  padding: 0 18rpx;
  border-radius: $yl-radius-pill;
  font-size: 22rpx;
  color: $yl-primary-dark;
  background: $yl-primary-soft;

  &--accent {
    color: #b36b00;
    background: $yl-accent-soft;
  }

  &--info {
    color: #1e5bc6;
    background: $yl-info-soft;
  }

  &--danger {
    color: $yl-danger;
    background: $yl-danger-soft;
  }

  &--purple {
    color: #6b3fd1;
    background: $yl-purple-soft;
  }

  &--grey {
    color: $yl-text-2;
    background: $yl-bg-input;
  }
}

/* ---------- 文本工具 ---------- */
.yl-ellipsis {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.yl-ellipsis-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.yl-latin {
  font-style: italic;
  color: $yl-text-3;
}

/* ---------- 输入框占位符（placeholder-class 需全局样式） ---------- */
.field__placeholder,
.atlas__placeholder,
.yl-placeholder {
  color: $yl-text-3;
  font-size: 27rpx;
}

/* ---------- 安全区 ---------- */
.yl-safe-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}

/* Tab 页底部留白（避免被底部导航遮挡） */
.yl-tab-spacer {
  height: 180rpx;
  height: calc(180rpx + constant(safe-area-inset-bottom));
  height: calc(180rpx + env(safe-area-inset-bottom));
}

/* ---------- 进场动画 ---------- */
@keyframes yl-fade-up {
  from {
    opacity: 0;
    transform: translateY(32rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes yl-fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes yl-pop {
  0% {
    opacity: 0;
    transform: scale(0.85);
  }
  70% {
    transform: scale(1.04);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes yl-spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes yl-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-14rpx);
  }
}

.yl-anim-up {
  animation: yl-fade-up 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.yl-anim-in {
  animation: yl-fade-in 0.4s ease both;
}

.yl-anim-pop {
  animation: yl-pop 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.yl-delay-1 {
  animation-delay: 0.08s;
}
.yl-delay-2 {
  animation-delay: 0.16s;
}
.yl-delay-3 {
  animation-delay: 0.24s;
}
.yl-delay-4 {
  animation-delay: 0.32s;
}
.yl-delay-5 {
  animation-delay: 0.4s;
}

/* ---------- 骨架屏 ---------- */
@keyframes yl-skeleton {
  0% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0 50%;
  }
}

.yl-skeleton {
  background: linear-gradient(90deg, #eef2ef 25%, #f7faf8 37%, #eef2ef 63%);
  background-size: 400% 100%;
  animation: yl-skeleton 1.4s ease infinite;
  border-radius: $yl-radius-sm;
}

/* ---------- 加载指示 ---------- */
.yl-spinner {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  border: 4rpx solid rgba(29, 164, 98, 0.2);
  border-top-color: $yl-primary;
  animation: yl-spin 0.8s linear infinite;
}

.yl-loading-row {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28rpx 0;
  color: $yl-text-3;
  font-size: 24rpx;

  .yl-spinner {
    margin-right: 14rpx;
  }
}
</style>
