<template>
  <view class="homepage-container">
    <view class="content">
      <!-- 顶部标题区域 -->
      <view class="header">
        <view class="logout-container">
          <image class="leave-btn" src="/static/leave.png" @click="handleLogout" />
          <text class="logout-text">退出登录</text>
        </view>
        <text class="title">植物识别</text>
        <text class="menu-dots">...</text>
      </view>

      <!-- 拍照区域 -->
      <view class="camera-section">
        <view class="user-info">
          <view class="avatar">
            <image class="avatar-img" src="/static/plantlogin.png" mode="aspectFit"></image>
          </view>
          <view class="user-text">
            <text class="welcome-title">欢迎使用雨林通</text>
            <text class="welcome-subtitle">Welcome back to PlantID</text>
          </view>
        </view>
      </view>

      <!-- 主要功能区域 -->
      <view class="main-features">
        <view class="features-header">
          <text class="features-title">主要功能</text>
          <text class="features-subtitle">Main Features</text>
        </view>
        <view class="features-grid">
          <view class="feature-item" @click="goToPlantHome">
            <view class="feature-icon green-bg">
              <image src="/static/plant-book.png" class="feature-icon-img" />
            </view>
            <text class="feature-text">植物图鉴</text>
            <text class="feature-text-en">Plant Atlas</text>
          </view>
          <view class="feature-item" @click="goToIdentify">
            <view class="feature-icon blue-bg">
              <image src="/static/identify.png" class="feature-icon-img" />
            </view>
            <text class="feature-text">植物识别</text>
            <text class="feature-text-en">Plant ID</text>
          </view>
          <view class="feature-item" @click="goToPlantHome">
            <view class="feature-icon orange-bg">
              <image src="/static/mine.png" class="feature-icon-img" />
            </view>
            <text class="feature-text">用户管理</text>
            <text class="feature-text-en">My Profile</text>
          </view>
          <view class="feature-item" @click="goToAbout">
            <view class="feature-icon purple-bg">
              <image src="/static/about.png" class="feature-icon-img" />
            </view>
            <text class="feature-text">关于我们</text>
            <text class="feature-text-en">About Us</text>
          </view>
        </view>
      </view>

     
    </view>
  </view>
</template>

<script>
  export default {
    data() {
      return {
       
      }
    },
    methods: {
      // 切换标签页
      switchTab(tabName) {
        this.activeTab = tabName;
      },
      
      // 退出登录
      handleLogout() {
        // 弹出退出账号成功提示
        uni.showToast({
          title: '退出账号成功',
          icon: 'success',
          duration: 2000
        });
        
        // 延迟跳转到登录页
        setTimeout(() => {
          this.$emit('goToLogin');
        }, 1500);
      },
      
      // 拍照功能
      takePhoto() {
        // 拍照相关逻辑
        console.log('拍照');
      },
      
      // 选择照片功能
      choosePhoto() {
        // 选择照片相关逻辑
        console.log('选择照片');
      },
      
      // 跳转到植物图鉴
      goToPlantHome() {
        this.$emit('goToPlantHome');
      },
      
      // 跳转到植物识别
      goToIdentify() {
        this.$emit('goToIdentify');
      },
      
      // 跳转到关于页面
      goToAbout() {
        this.$emit('goToAbout');
      }
    }
  }
</script>

<style lang="scss">
  // 导入uni.scss变量
  @import '../../uni.scss';
  
  // 全局样式重置
  page {
    background-color: #f5f7fa;
  }
  
  .homepage-container {
    width: 100%;
    min-height: 100vh;
  }
  

  .content {
    position: relative;
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(
      0deg, 
      rgba(255, 255, 255, 0.4), 
      rgba(255, 255, 255, 0.4)
    ), linear-gradient(
      180deg, 
      rgba(0, 255, 242, 0.2) 0%, 
      rgba(90, 252, 3, 0.2) 100%
    );
    padding-bottom: 30rpx;
  }
  
  // 顶部标题区域
  .header {
    position: relative;
    width: 100%;
    height: 140rpx;
    display: flex;
    align-items: center;
    padding: 0 30rpx;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(10rpx);
  }
  
  .logout-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .leave-btn {
    width: 70rpx;
    height: 70rpx;
    opacity: 0.8;
    transition: all 0.3s ease;
  }
  
  .leave-btn:active {
    opacity: 1;
    transform: scale(0.95);
  }
  
  .logout-text {
    font-size: 24rpx;
    color: #666;
    margin-top: 8rpx;
  }
  
  .title {
    flex: 1;
    font-size: 56rpx;
    font-weight: 600;
    color: #4caf50;
    text-align: center;
    letter-spacing: 2rpx;
  }
  
  .menu-dots {
    font-size: 48rpx;
    font-weight: 600;
    color: #666;
    line-height: 1;
  }
  
  // 拍照区域
  .camera-section {
    margin: 40rpx auto 0;
    width: 620rpx;
    border-radius: 32rpx;
    background: rgba(255, 255, 255, 0.95);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50rpx 30rpx;
    box-sizing: border-box;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
  }
  
  .camera-section:active {
    box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.12);
  }
  
  .user-info {
    display: flex;
    align-items: center;
  }
  
  .avatar {
    width: 140rpx;
    height: 140rpx;
    border-radius: 70rpx;
    background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 30rpx;
    box-shadow: 0 6rpx 20rpx rgba(76, 175, 80, 0.2);
    position: relative;
    overflow: hidden;
  }
  
  .avatar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0) 100%);
    pointer-events: none;
  }
  
  .avatar-img {
    width: 100rpx;
    height: 100rpx;
    border-radius: 50rpx;
    z-index: 1;
  }
  
  .user-text {
    display: flex;
    flex-direction: column;
  }
  
  .welcome-title {
    font-size: 48rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 8rpx;
  }
  
  .welcome-subtitle {
    font-size: 30rpx;
    color: #888;
    font-weight: 400;
  }
  
  // 主要功能区域
  .main-features {
    margin: 60rpx auto 0;
    width: 620rpx;
    padding: 0 30rpx;
    box-sizing: border-box;
  }
  
  .features-header {
    margin-bottom: 36rpx;
  }
  
  .features-title {
    font-size: 40rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 8rpx;
    display: block;
    letter-spacing: 1rpx;
  }
  
  .features-subtitle {
    font-size: 28rpx;
    color: #999;
    display: block;
    font-weight: 400;
  }
  
  // 功能网格
  .features-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    width: 100%;
    box-sizing: border-box;
  }
  
  .feature-item {
    width: 48%;
    background: white;
    border-radius: 24rpx;
    padding: 36rpx 24rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    margin-bottom: 24rpx;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
  }
  
  .feature-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6rpx;
    background: linear-gradient(90deg, #4caf50, #81c784);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .feature-item:active {
    transform: translateY(4rpx) scale(0.98);
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.03);
  }
  
  .feature-item:active::before {
    opacity: 1;
  }
  
  .feature-icon {
    width: 120rpx;
    height: 120rpx;
    border-radius: 24rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20rpx;
    position: relative;
    overflow: hidden;
  }
  
  .feature-icon::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0) 100%);
    pointer-events: none;
  }
  
  .green-bg {
    background-color: #e8f5e9;
  }
  
  .blue-bg {
    background-color: #e3f2fd;
  }
  
  .orange-bg {
    background-color: #fff3e0;
  }
  
  .purple-bg {
    background-color: #f3e5f5;
  }
  
  .feature-icon-img {
    width: 64rpx;
    height: 64rpx;
    z-index: 1;
  }
  
  .feature-text {
    font-size: 34rpx;
    font-weight: 500;
    color: #333;
    margin-bottom: 6rpx;
  }
  
  .feature-text-en {
    font-size: 26rpx;
    color: #999;
  }
  
  // 内容区域
  .content-section {
    margin: 60rpx auto 60rpx;
    width: 620rpx;
    border-radius: 32rpx;
    background: white;
    display: flex;
    flex-direction: column;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
    overflow: hidden;
  }
  
  // 标签切换
  .tabs {
    display: flex;
    width: 100%;
    height: 110rpx;
    background: #f8f9fa;
    border-bottom: 2rpx solid #e9ecef;
  }
  
  .tab {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32rpx;
    transition: all 0.3s ease;
    color: #666;
    position: relative;
  }
  
  .tab::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 30%;
    width: 40%;
    height: 6rpx;
    background: #4caf50;
    transform: scaleX(0);
    transition: all 0.3s ease;
    border-radius: 3rpx;
  }
  
  .tab.active {
    font-size: 36rpx;
    font-weight: 600;
    color: #4caf50;
  }
  
  .tab.active::after {
    transform: scaleX(1);
  }
  
  // 标签内容
  .tab-content {
    flex: 1;
    width: 100%;
    height: 500rpx;
    overflow-y: auto;
    background: white;
  }
  
  // 列表项通用样式
  .hot-plants-list, .recent-recognitions-list {
    padding: 20rpx;
  }
  
  .plant-item, .recognition-item {
    margin-bottom: 20rpx;
    padding: 30rpx;
    border-radius: 20rpx;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .plant-item::before, .recognition-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 8rpx;
    height: 100%;
    background: linear-gradient(180deg, #4caf50, #81c784);
  }
  
  .plant-item:active, .recognition-item:active {
    transform: translateX(8rpx);
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  }
 
</style>
