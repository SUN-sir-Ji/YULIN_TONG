<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <view class="back-btn" @click="$emit('goToHomepage1')">
        <uni-icons type="left" size="48rpx" color="#333"></uni-icons>
      </view>
      <view class="title">关于我们</view>
      <view class="empty-space"></view>
    </view>

    <!-- 主体内容 -->
    <view class="content">
      <!-- App Logo和名称 -->
      <view class="app-info">
        <image 
          class="app-logo" 
          src="/static/logo.png" 
          mode="widthFix"
          alt="应用程序logo"
        ></image>
        <view class="app-name">我的应用</view>
        <view class="app-version">版本 v1.0.0</view>
      </view>

      <!-- 应用简介 -->
      <view class="app-intro">
        <view class="section-title">应用简介</view>
        <view class="intro-content">
          这是一款功能强大的移动应用，为用户提供便捷的服务和优质的体验。我们致力于不断优化产品，为用户创造更大价值。
        </view>
      </view>

      <!-- 下载二维码 -->
      <view class="qrcode-section">
        <view class="section-title">下载二维码</view>
        <view class="qrcode-container">
          <image 
            class="qrcode" 
            src="/static/qrcode.png" 
            mode="widthFix"
            alt="应用下载二维码"
          ></image>
          <view class="qrcode-desc">扫码下载最新版本</view>
        </view>
      </view>

      <!-- 其他信息 -->
      <view class="other-info">
        <view class="contact-item">
          <uni-icons type="phone" size="32rpx" color="#666" class="info-icon"></uni-icons>
          <text class="info-text">客服电话：400-123-4567</text>
        </view>
        <view class="contact-item">
          <uni-icons type="email" size="32rpx" color="#666" class="info-icon"></uni-icons>
          <text class="info-text">邮箱：contact@example.com</text>
        </view>
      </view>
    </view>

    <!-- 页脚 -->
    <view class="footer">
      <text class="copyright">© 2023 我的应用 版权所有</text>
    </view>
  </view>
</template>

<script>
import uniIcons from '@/uni_modules/uni-icons/components/uni-icons/uni-icons.vue';

export default {
  components: {
    uniIcons
  },
  data() {
    return {
      // 可以从后端接口获取的动态数据
      appInfo: {
        name: '我的应用',
        version: 'v1.0.0',
        intro: '', // 可从接口获取
        qrcodeUrl: '' // 可从接口获取
      }
    };
  },
  onLoad() {
    // 页面加载时获取数据
    // 暂时注释，避免请求不存在的接口导致错误
    // this.fetchAboutData();
  },
  methods: {
    // 返回主页
    navigateBack() {
      // 假设主页在pages/index/index.vue
      uni.navigateTo({
        url: '/pages/index/index'
      });
      // 如果是从主页跳转过来的，也可以使用uni.navigateBack()
      // uni.navigateBack({ delta: 1 });
    },
    
    // 从后端接口获取关于页面数据
    fetchAboutData() {
      // 调用后端接口获取数据
      uni.request({
        url: 'https://api.example.com/about', // 后端接口地址
        method: 'GET',
        success: (res) => {
          if (res.statusCode === 200 && res.data.success) {
            this.appInfo = res.data.data;
          } else {
            uni.showToast({
              title: '获取数据失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('接口请求失败', err);
          uni.showToast({
            title: '网络错误',
            icon: 'none'
          });
        }
      });
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* 导航栏样式 */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 160rpx;
  padding: 0 32rpx;
  background-color: #fff;
  border-bottom: 2rpx solid #eee;
}

.back-btn {
  width: 88rpx;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  font-weight: 500;
  color: #333;
}

.empty-space {
  width: 88rpx;
  height: 88rpx;
}

/* 主体内容样式 */
.content {
  flex: 1;
  padding: 40rpx 32rpx;
}

/* 应用信息样式 */
.app-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;
  padding: 40rpx 0;
  background-color: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.app-logo {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 30rpx;
  border-radius: 32rpx;
}

.app-name {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.app-version {
  font-size: 28rpx;
  color: #666;
}

/* 通用区块标题样式 */
.section-title {
  font-size: 32rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 24rpx;
  padding-left: 8rpx;
  border-left: 6rpx solid #007aff;
}

/* 应用简介样式 */
.app-intro {
  margin-bottom: 60rpx;
  padding: 32rpx;
  background-color: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.intro-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  text-align: justify;
}

/* 二维码区域样式 */
.qrcode-section {
  margin-bottom: 60rpx;
  padding: 32rpx;
  background-color: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.qrcode-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qrcode {
  width: 320rpx;
  height: 320rpx;
  margin-bottom: 20rpx;
  padding: 20rpx;
  background-color: #fff;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
}

.qrcode-desc {
  font-size: 28rpx;
  color: #666;
}

/* 其他信息样式 */
.other-info {
  margin-bottom: 60rpx;
  padding: 32rpx;
  background-color: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.info-icon {
  margin-right: 20rpx;
}

.info-text {
  font-size: 28rpx;
  color: #666;
}

/* 页脚样式 */
.footer {
  padding: 30rpx 0;
  text-align: center;
}

.copyright {
  font-size: 24rpx;
  color: #999;
}
</style>
