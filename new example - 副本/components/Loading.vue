<template>
   <view>
    <view class="password-toast">
    <view  class="toast">
    <view class="circle">
      <view class="mask"></view>
    </view>
    <view class="text">登录中...</view>
  
</view>
</view>
</view>
</template>

<script>
export default {
  name: 'Loading'
}
</script>

<style scoped>
    .toast {
      position: absolute;
      top: 45%;
      left: 50%;
       width: 300rpx;
      height: 250rpx;
      transform: translate(-50%, -50%);
      background-color: rgba(76, 76, 76, 0.9);
      border-radius: 40rpx;
      /* 移除 display: none; */
    }

    .circle {
      width: 100rpx;
      height: 100rpx;
      background: conic-gradient(transparent 10%, #e4e4e4 90%);
      border-radius: 50%;
      position: relative;
      margin: 50rpx auto 20rpx  auto;
      animation: rotate 1s linear infinite;
    }

    .mask {
      width: 85rpx;
      height: 85rpx;
      background-color: rgb(76, 76, 76 ,1);
      border-radius: 50%;
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }

    @keyframes rotate {
      0% {
        transform: rotate(0deg);
        /* 初始状态 */
      }

      100% {
        transform: rotate(360deg);
        /* 结束状态 */
      }
    }

    .text {
   
      width: 100%;
      text-align: center;
      font-size: 14px;
      color: #e4e4e4;
    }
    .password-toast{
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
</style>