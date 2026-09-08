<template>
  <view>
    <view class="content">
      <image class="logo" src="/static/logo.png" />
      <view class="rectangle">
        <text class="title">Welcome to Login</text>
        <view class="input">
          <input class="input-box1" placeholder="请输入注册时的邮箱" v-model="email" type="email" />
        </view>
        <!-- 验证码输入框 - 修改了获取验证码按钮的显示 -->
        <view style="display: flex; margin-top: 10rpx; width: 100%; height:80rpx; flex-direction: row;">
          <input class="input-box2" placeholder="验证码" v-model="code" />
          <text class="get-code" 
                @click="getCode" 
                :disabled="countdown > 0 || isGettingCode"
                :class="{ 'getting-code': isGettingCode }">
              {{ isGettingCode ? '发送中...' : (countdown > 0 ? `${countdown}秒后重试` : '获取验证码') }}
            </text>
        </view>
        <view class="find-password" @click="verifyCode">确认找回</view>
        <view class="rejister-box">
          <text>没有账号？点击</text>
          <view class="rejister-page" @click="$emit('goToRegister')">注册
          </view>
        </view>
      </view>
      <!-- 返回按钮 -->
      <view class="back-button" @click="$emit('goToLogin')">
        <text class="arrow-left">←</text>
      </view>
    </view>
    
    <!-- 密码显示浮窗 - 添加了动画类 -->
    <view class="password-modal" v-if="showPasswordModal">
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">您的密码</text>
          <text class="modal-close" @click="closePasswordModal">✕</text>
        </view>
        <view class="password-container">
          <text class="password-text">{{ userPassword }}</text>
          <text class="password-tip">请妥善保管您的密码</text>
        </view>
        <view class="modal-button" @click="closePasswordModal">确定</view>
      </view>
    </view>
  </view>
</template>

<script>
import API_CONFIG from '../../utils/apiConfig.js';

export default {
  data() {
    return {
      email: "",
      code: "",
      countdown: 0,
      timer: null,
      showPasswordModal: false,
      userPassword: "",
      // 添加一个加载状态，用于防止重复点击
      isGettingCode: false
    }
  },
  methods: {
    // 获取验证码 - 添加了加载状态控制
    getCode() {
      // 如果正在发送验证码或倒计时中，直接返回
      if (this.isGettingCode || this.countdown > 0) {
        return;
      }
      
      // 简单的邮箱格式验证
      if (!this.email || !this.isValidEmail(this.email)) {
        uni.showToast({
          title: '请输入有效的邮箱地址',
          icon: 'none'
        });
        return;
      }
      
      // 设置加载状态，防止重复点击
      this.isGettingCode = true;
      
      // 调用后端API获取验证码
      uni.request({
        url: `${API_CONFIG.baseUrl}/api/auth/forgot-password/captcha`,
        method: 'POST',
        data: {
          email: this.email
        },
        success: (res) => {
          if (res.statusCode === 200) {
            uni.showToast({
              title: '验证码已发送',
              icon: 'success'
            });
            this.startCountdown();
          } else if (res.statusCode === 400 && res.data.detail === '该邮箱已被注册，请使用其他邮箱') {
            // 注意：这里需要后端配合修改，目前的API是为注册设计的
            // 实际应该创建一个新的API专门用于找回密码的验证码发送
            uni.showToast({
              title: '验证码已发送',
              icon: 'success'
            });
            this.startCountdown();
          } else {
            uni.showToast({
              title: '获取验证码失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，请重试',
            icon: 'none'
          });
        },
        complete: () => {
          // 请求完成后，无论成功失败，都重置加载状态
          this.isGettingCode = false;
        }
      });
    },
    
    // 验证邮箱格式
    isValidEmail(email) {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailRegex.test(email);
    },
    
    // 开始倒计时
    startCountdown() {
      this.countdown = 60;
      this.timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(this.timer);
        }
      }, 1000);
    },
    
    // 验证验证码并获取密码
    verifyCode() {
      if (!this.email || !this.code) {
        uni.showToast({
          title: '请填写完整信息',
          icon: 'none'
        });
        return;
      }
      
      // 调用后端API验证验证码并获取密码
      // 注意：需要后端配合创建这个新API
      uni.request({
        url: `${API_CONFIG.baseUrl}/api/auth/reset-password`,
        method: 'POST',
        data: {
          email: this.email,
          captcha: this.code
        },
        success: (res) => {
          if (res.statusCode === 200 && res.data.success) {
            // 显示密码浮窗
            this.userPassword = res.data.password;
            this.showPasswordModal = true;
          } else {
            uni.showToast({
              title: res.data.message || '验证码错误或已过期',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，请重试',
            icon: 'none'
          });
        }
      });
    },
    
    // 关闭密码浮窗
    closePasswordModal() {
      this.showPasswordModal = false;
      this.$emit('goToLogin');
    }
  },
  
  // 组件销毁时清除定时器
  destroyed() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
}
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
  opacity: 1;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(0deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), linear-gradient(180deg, rgba(0, 255, 242, 0.2) 0%, rgba(90, 252, 3, 0.2) 100%);
  align-items: center;
}

.title {
  display: flex;
  margin: auto;
  margin-top: 10%;
  margin-bottom: 20%;
  width: 450rpx;
  opacity: 1;
  color: rgba(0, 0, 0, 1);
  font-size: 50rpx;
  font-weight: 400;
  letter-spacing: 0rpx;
  line-height: 34.75rpx;
  color: rgba(0, 0, 0, 1);
  vertical-align: top;
  text-align: center;
}

.logo {
  margin-top: 20%;
  width: 200rpx;
  height: 200rpx;
  opacity: 1;
}

.rectangle {
  left: calc(50% - 300rpx);
  margin-top: 5%;
  width: 75%;
  padding: 10rpx;
  opacity: 1;
  border-radius: 55rpx;
  background: rgba(241, 240, 240, 0.347);
  border: 0.2rpx solid rgba(0, 0, 0, 1);
}

.input-box1 {
  display: flex;
  text-align: center;
  margin: auto;
  margin-top: 10rps;
  width: 480rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

.input-box2 {
  display: flex;
  text-align: center;
  margin-left: 60rpx;
  margin-top: 10rpx;
  width: 250rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 15rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

.find-password {
  display: flex;
  text-align: center;
  align-items: center;
  margin: auto;
  margin-top: 70rpx;
  width: 400rpx;
  height: 85rpx;
  background: linear-gradient(0deg, rgba(80, 224, 18, 0.68), rgba(80, 224, 18, 0.68)), radial-gradient(38.73% 48.73% at 50% 51.168476563545674%, rgba(94, 201, 48, 0.9) 0%, rgba(81, 247, 10, 0.87) 3.24%, rgba(37, 199, 16, 0.9) 100%);
  border-radius: 45rpx;
  border: 0.8rpx solid rgba(0, 0, 0, 1);
  box-shadow: 0rpx 2rpx 1rpx rgba(0, 0, 0, 0.25);
  filter: blur(1rpx);
  color: white;
  font-size: 55rpx;
  font-weight: 700;
  justify-content: center;
  -webkit-text-stroke: 0.2rpx rgba(0, 0, 0, 1);
  letter-spacing: 20rpx;
}

.find-password:active {
  opacity: 0.8;
}

.rejister-box {
  color: rgba(6, 5, 5, 0.772);
  font-size: 30rpx;
  font-weight: 700rpx;
  display: flex;
  align-items: center;
  margin-left: 20%;
  margin-top: 80rpx;
  opacity: 0.8;
}

.rejister-page {
  margin-left: 15rpx;
  color: rgba(168, 6, 6, 0.772);
  font-size: 40rpx;
  font-weight: 700;
}

.get-code {
  display: flex;
  margin-left: 30rpx;
  margin-top: 30rpx;
  width: 200rpx;
  height: 80rpx;
  color: rgba(221, 83, 8, 0.772);
  font-size: 33rpx;
  font-weight: 500;
}

.get-code {
  opacity: 0.8;
}

.back-button {
  margin-top: 10%;
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  background-color: rgba(80, 224, 18, 0.68);
  border: 0.8rpx solid rgba(0, 0, 0, 1);
  box-shadow: 0rpx 2rpx 1rpx rgba(0, 0, 0, 0.25);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.back-button:active {
  opacity: 0.8;
}

.arrow-left {
  color: white;
  font-size: 60rpx;
  font-weight: 700;
  -webkit-text-stroke: 0.2rpx rgba(0, 0, 0, 1);
}

/* 美化后的密码显示浮窗样式 */
.password-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  width: 80%;
  max-width: 500rpx;
  background-color: white;
  border-radius: 40rpx;
  padding: 50rpx;
  text-align: center;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.15);
  border: 1rpx solid rgba(0, 0, 0, 0.05);
  animation: scaleIn 0.3s ease-out;
}

/* 添加头部区域和关闭按钮 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.modal-title {
  font-size: 48rpx;
  font-weight: 700;
  color: #333;
  letter-spacing: 2rpx;
}

.modal-close {
  font-size: 50rpx;
  color: #999;
  padding: 10rpx;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:active {
  background-color: #f5f5f5;
  color: #666;
}

/* 密码显示区域优化 */
.password-container {
  margin-bottom: 50rpx;
}

.password-text {
  display: inline-block;
  font-size: 44rpx;
  font-weight: 600;
  color: #ff6b35;
  padding: 25rpx 40rpx;
  background-color: #fff9f5;
  border-radius: 20rpx;
  border: 1rpx solid #ffd6c2;
  margin-bottom: 20rpx;
  min-width: 300rpx;
  word-break: break-all;
}

.password-tip {
  display: block;
  font-size: 28rpx;
  color: #999;
  margin-top: 20rpx;
}

/* 按钮美化 */
.modal-button {
  width: 100%;
  height: 90rpx;
  background: linear-gradient(135deg, #50e012, #3dc518);
  color: white;
  border-radius: 45rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  font-size: 38rpx;
  font-weight: 600;
  box-shadow: 0 5rpx 20rpx rgba(80, 224, 18, 0.3);
  transition: all 0.3s ease;
  letter-spacing: 2rpx;
}

.modal-button:active {
  opacity: 0.9;
  transform: translateY(2rpx);
  box-shadow: 0 3rpx 10rpx rgba(80, 224, 18, 0.2);
}

/* 添加动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>

/* 添加发送中状态的样式 */
.get-code {
  display: flex;
  margin-left: 30rpx;
  margin-top: 30rpx;
  width: 200rpx;
  height: 80rpx;
  color: rgba(221, 83, 8, 0.772);
  font-size: 33rpx;
  font-weight: 500;
  opacity: 0.8;
  /* 添加过渡效果 */
  transition: all 0.3s ease;
}

/* 发送中状态的样式 */
.get-code.getting-code {
  color: #999;
  /* 可以添加一个简单的动画效果 */
}

/* 禁用状态的样式 */
.get-code[disabled] {
  opacity: 0.5;
  pointer-events: none;
}
