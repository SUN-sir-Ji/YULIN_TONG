<template>
  <view>
    <view class="content">
      <image class="logo" src="/static/logo.png" />
      <view class="rectangle">
        <text class="title">Welcome to Login</text>
        <view class="input">
          <!-- 用户名输入框 -->
          <input 
            class="input-box1" 
            placeholder="请输入纯数字作为用户ID（将作为登录用户名）" 
            v-model="username" 
            @input="validateUsername"
            maxlength="20"
          />
          <!-- 用户名验证提示 -->
          <text v-if="usernameError" class="error-text">{{ usernameError }}</text>
          
          <!-- 密码输入框 -->
          <input 
            class="input-box2" 
            placeholder="密码" 
            v-model="password" 
            password 
          />
          
          <!-- 邮箱输入框 -->
          <input 
            class="input-box3" 
            placeholder="邮箱" 
            v-model="email" 
          />
          
          <!-- 验证码输入框 -->
          <view class="verification-code-container">
            <input 
              class="input-box4" 
              placeholder="验证码" 
              v-model="captcha" 
            />
            <text class="get-code" @click="getCode" :disabled="countdown > 0">{{ countdown > 0 ? `${countdown}秒后重发` : '获取验证码' }}</text>
          </view>
        </view>

        <!-- 注册按钮 -->
        <view class="sign-in-button" @click="register" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注    册' }}
        </view>

        <!-- 登录链接 -->
        <view class="rejister-box">
          <text>已有账号？点击</text>
          <view class="rejister-page" @click="goToLogin">
            登录
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import API_CONFIG from '../../utils/apiConfig.js';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      captcha: '',
      countdown: 0,
      isLoading: false,
      usernameError: '',
      validationTimer: null
    }
  },
  methods: {
    // 注册方法
    register() {
      // 表单验证
      if (!this.validateForm()) {
        return;
      }

      this.isLoading = true;

      // 调用注册接口
      uni.request({
        url: API_CONFIG.baseUrl + '/api/auth/register',
        method: 'POST',
        data: {
          username: this.username,
          password: this.password,
          email: this.email,
          captcha: this.captcha
        },
        success: (res) => {
          console.log('注册响应:', res);
          // 检查后端响应格式并显示具体原因
          if (res.statusCode === 200) {
            if (res.data && res.data.status === 200) {
              // 注册成功
              uni.showToast({
                title: '注册成功',
                icon: 'success',
                duration: 2000
              });
              // 延迟跳转到登录页
              setTimeout(() => {
                this.goToLogin();
              }, 2000);
            } else {
              // 注册失败，显示具体原因
              let errorMsg = '注册失败，请重试';
              if (res.data && res.data.message) {
                errorMsg = res.data.message;
              } else if (res.data && res.data.error) {
                errorMsg = res.data.error;
              }
              
              uni.showToast({
                title: errorMsg,
                icon: 'none'
              });
            }
          } else {
            // 根据不同的HTTP状态码显示不同的错误信息
            let errorMsg = '注册失败，请重试';
            if (res.statusCode === 400) {
              errorMsg = res.data?.message || '请求参数错误';
            } else if (res.statusCode === 401) {
              errorMsg = '验证码错误或已过期';
            } else if (res.statusCode === 409) {
              errorMsg = '用户名或邮箱已被注册';
            } else if (res.statusCode === 500) {
              errorMsg = '服务器内部错误，请稍后重试';
            }
            
            uni.showToast({
              title: errorMsg,
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('注册请求失败:', err);
          uni.showToast({
            title: '网络异常，请检查网络连接',
            icon: 'none'
          });
        },
        complete: () => {
          this.isLoading = false;
        }
      });
    },

    // 获取验证码方法
    getCode() {
      // 邮箱格式验证
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        uni.showToast({
          title: '请先输入有效的邮箱地址',
          icon: 'none'
        });
        return;
      }

      // 调用发送验证码接口
      uni.request({
        url: API_CONFIG.baseUrl + '/api/auth/get-captcha',
        method: 'POST',
        data: {
          email: this.email
        },
        success: (res) => {
          console.log('验证码请求响应:', res);
          if (res.statusCode === 200) {
            if (res.data && res.data.status === 200) {
              uni.showToast({
                title: '验证码已发送',
                icon: 'success'
              });
              // 开始倒计时
              this.startCountdown();
            } else {
              // 显示后端返回的具体错误信息
              uni.showToast({
                title: res.data?.message || '发送失败，请重试',
                icon: 'none'
              });
            }
          } else if (res.statusCode === 400) {
            uni.showToast({
              title: '该邮箱已被注册，请使用其他邮箱',
              icon: 'none'
            });
          } else if (res.statusCode === 500) {
            uni.showToast({
              title: '服务器错误，请稍后再试',
              icon: 'none'
            });
          } else {
            uni.showToast({
              title: '未知错误，请重试',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('获取验证码请求失败:', err);
          uni.showToast({
            title: '网络异常，请检查网络连接',
            icon: 'none'
          });
        }
      });
    },
    
    // 验证码倒计时
    startCountdown() {
      this.countdown = 60;
      const timer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(timer);
        }
      }, 1000);
    },

    // 表单验证
    validateForm() {
      // 用户名验证
      if (!this.username || this.username.trim().length === 0) {
        uni.showToast({
          title: '请输入用户名',
          icon: 'none'
        });
        return false;
      }
      
      // 验证用户名是否为纯数字
      const numberRegex = /^\d+$/;
      if (!numberRegex.test(this.username)) {
        uni.showToast({
          title: '用户名必须为纯数字',
          icon: 'none'
        });
        return false;
      }

      // 用户名长度验证
      if (this.username.length < 4 || this.username.length > 20) {
        uni.showToast({
          title: '用户名长度必须在4-20位之间',
          icon: 'none'
        });
        return false;
      }

      // 密码验证
      if (!this.password || this.password.length < 6) {
        uni.showToast({
          title: '密码长度不能少于6位',
          icon: 'none'
        });
        return false;
      }

      // 邮箱格式验证
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        uni.showToast({
          title: '请输入有效的邮箱地址',
          icon: 'none'
        });
        return false;
      }

      // 验证码验证
      if (!this.captcha || this.captcha.trim().length === 0) {
        uni.showToast({
          title: '请输入验证码',
          icon: 'none'
        });
        return false;
      }

      return true;
    },

    // 实时验证用户名
    validateUsername() {
      // 清除之前的定时器
      if (this.validationTimer) {
        clearTimeout(this.validationTimer);
      }
      
      // 设置延迟验证，避免频繁验证
      this.validationTimer = setTimeout(() => {
        if (this.username) {
          const numberRegex = /^\d+$/;
          if (!numberRegex.test(this.username)) {
            this.usernameError = '用户名必须为纯数字';
          } else if (this.username.length < 4 || this.username.length > 20) {
            this.usernameError = '用户名长度必须在4-20位之间';
          } else {
            this.usernameError = '';
          }
        } else {
          this.usernameError = '';
        }
      }, 300);
    },

    // 跳转到登录页面
    goToLogin() {
      this.$emit('goToLogin');
    }
  },
  
  // 组件销毁时清除定时器
  destroyed() {
    if (this.validationTimer) {
      clearTimeout(this.validationTimer);
    }
  }
}
</script>

<style>
/* 页面容器样式 */
.content {
  display: flex;
  flex-direction: column;
  opacity: 1;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(0deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), linear-gradient(180deg, rgba(0, 255, 242, 0.2) 0%, rgba(90, 252, 3, 0.2) 100%);
  align-items: center;
}

/* 标题样式 */
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

/* Logo样式 */
.logo {
  margin-top: 20%;
  width: 200rpx;
  height: 200rpx;
  opacity: 1;
}

/* 矩形容器样式 */
.rectangle {
  margin-top: 5%;
  width: 75%;
  padding: 10rpx;
  opacity: 1;
  border-radius: 55rpx;
  background: rgba(241, 240, 240, 0.347);
  border: 0.2rpx solid rgba(0, 0, 0, 1);
  align-items: center;
}

/* 输入框容器样式 */
.input {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 用户名输入框样式 */
.input-box1 {
  margin-bottom: 10rpx;
  width: 480rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

/* 密码输入框样式 */
.input-box2 {
  margin-bottom: 10rpx;
  width: 480rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

/* 邮箱输入框样式 */
.input-box3 {
  margin-bottom: 10rpx;
  width: 480rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

/* 验证码输入框样式 */
.input-box4 {
  width: 250rpx;
  height: 80rpx;
  opacity: 1;
  border-radius: 10rpx;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 20rpx;
  box-sizing: border-box;
}

/* 获取验证码按钮样式 */
.get-code {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200rpx;
  height: 80rpx;
  color: rgba(221, 83, 8, 0.772);
  font-size: 33rpx;
  font-weight: 500;
}

/* 验证码容器样式 */
.verification-code-container {
  display: flex;
  align-items: center;
  gap: 20rpx;
  width: 100%;
  justify-content: center;
}

/* 注册按钮样式 */
.sign-in-button {
  display: flex;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20rpx;
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
  display: flex;
  justify-content: center;
  align-items: center;
  -webkit-text-stroke: 0.2rpx rgba(0, 0, 0, 1);
  letter-spacing: 20rpx;
}

/* 注册按钮点击效果 */
.sign-in-button:active {
  opacity: 0.8;
}

/* 注册按钮禁用效果 */
.sign-in-button[disabled] {
  opacity: 0.6;
}

/* 登录链接容器样式 */
.rejister-box {
  color: rgba(6, 5, 5, 0.772);
  font-size: 30rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  margin-left: 20%;
  margin-top: 10%;
  opacity: 0.8;
}

/* 登录链接样式 */
.rejister-page {
  margin-left: 15rpx;
  color: rgba(168, 6, 6, 0.772);
  font-size: 40rpx;
  font-weight: 700;
}

/* 错误提示样式 */
.error-text {
  color: #e64340;
  font-size: 24rpx;
  margin-bottom: 10rpx;
  width: 480rpx;
  text-align: left;
  padding-left: 20rpx;
}
</style>