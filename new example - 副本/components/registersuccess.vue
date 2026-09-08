<template>
    <view>
    <view class="register-toast">
    <view  class="toast">
      
      <view class="back" @click="$emit('goToLogin'); $emit('registersuccess')">
        <text class="close-icon">×</text>
			    
			</view>
    <view class="text">注册成功！</view>
  </view>
  </view>
</view>
</template>

<script>
export default {
  
}
</script>

<style scoped>
.register-toast{
   /* 使用 fixed 定位覆盖整个视口 */
   position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* 调高背景颜色透明度，这里使用半透明黑色 */
    background-color: rgba(0, 0, 0, 0.5); 
    /* 确保遮罩层在底层元素之上 */
    z-index: 998; 
}
    .toast {
      position: absolute;
      top: 40%;
      left: calc(50% - 200rpx);
       width: 400rpx;
      height: 250rpx;
      background-color: rgba(254, 252, 252, 0.9);
      border-radius: 40rpx;
      border: 0.8rpx solid rgba(0, 0, 0, 1);
      /* 移除 display: none; */
    }
    .text {
     position: absolute;
     left: 20%;
      top: 40%;
      width: 100%;
      font-size: 25px;
      color: #000000;
    }
  
    .back {
      position: absolute;
      right: 20rpx;
      top: 20rpx;
      width: 40rpx;
      height: 40rpx;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
    }
    .close-icon {
      font-size: 40rpx;
      color: #000000;
    }
</style>