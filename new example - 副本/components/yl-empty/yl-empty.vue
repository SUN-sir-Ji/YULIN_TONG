<template>
  <view class="yl-empty" :class="{ 'yl-empty--compact': compact }">
    <view class="yl-empty__illus">
      <view class="yl-empty__blob yl-empty__blob--1"></view>
      <view class="yl-empty__blob yl-empty__blob--2"></view>
      <view class="yl-empty__icon">
        <uni-icons :type="icon" size="40" color="#1DA462"></uni-icons>
      </view>
    </view>
    <text class="yl-empty__title">{{ title }}</text>
    <text v-if="desc" class="yl-empty__desc">{{ desc }}</text>
    <view v-if="btnText" class="yl-empty__btn" hover-class="yl-press" @click="$emit('click')">
      <text>{{ btnText }}</text>
    </view>
    <slot></slot>
  </view>
</template>

<script>
export default {
  name: 'YlEmpty',
  props: {
    icon: { type: String, default: 'info' },
    title: { type: String, default: '暂无内容' },
    desc: { type: String, default: '' },
    btnText: { type: String, default: '' },
    compact: { type: Boolean, default: false }
  },
  emits: ['click']
}
</script>

<style lang="scss" scoped>
.yl-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 96rpx 48rpx;

  &--compact {
    padding: 48rpx 32rpx;
  }

  &__illus {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 28rpx;
  }

  &__blob {
    position: absolute;
    border-radius: 50%;

    &--1 {
      width: 180rpx;
      height: 180rpx;
      background: $yl-primary-soft;
    }

    &--2 {
      width: 110rpx;
      height: 110rpx;
      right: 0;
      bottom: 6rpx;
      background: rgba(111, 211, 154, 0.35);
      animation: yl-float 3s ease-in-out infinite;
    }
  }

  &__icon {
    position: relative;
    width: 120rpx;
    height: 120rpx;
    border-radius: 36rpx;
    background: #fff;
    box-shadow: $yl-shadow;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__title {
    font-size: 30rpx;
    font-weight: 600;
    color: $yl-text-1;
  }

  &__desc {
    margin-top: 12rpx;
    font-size: 24rpx;
    color: $yl-text-3;
    text-align: center;
    line-height: 1.6;
  }

  &__btn {
    margin-top: 36rpx;
    height: 76rpx;
    padding: 0 48rpx;
    border-radius: $yl-radius-pill;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 26rpx;
    font-weight: 600;
    background: $yl-gradient;
    box-shadow: $yl-shadow-primary;
  }
}
</style>
