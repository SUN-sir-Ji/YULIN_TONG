<template>
	<view>
		<view class="content">
            <image class="logo" src="\static\logo.png" />
			<view class="rectangle">
	            <text class="title">Welcome to Login</text>
			    <view class="input">
                <!-- 用户名输入框 -->
                <input 
                    class="input-box1" 
                    placeholder="用户名" 
                    v-model="username" 
                />
                <!-- 密码输入框 -->
                <input 
                    class="input-box2" 
                    placeholder="密码" 
                    v-model="password" 
			    type="password" 
                />
                
                </view>
                <view class="find-password" @click="goToFindPassword">忘记密码</view>
			    <view class="sign-in-button" @click="handleLogin"> 登     录</view>
	            <view class="rejister-box" >
			        <text >没有账号？点击</text>
				    <view class="rejister-page" @click="goToRegister">注册</view>
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
                // 定义用户名和密码
				username: '',
				password: '',
                // 加载状态
                isLoading: false
			}
		},
		methods: {
            // 登录处理函数
            handleLogin() {
                // 表单验证
                if (!this.validateForm()) {
                    return;
                }
                
                this.isLoading = true;
                
                // 调用登录API
                this.loginApi().then(res => {
                    this.isLoading = false;
                    // 处理登录结果
                    if (res.code === 200 && res.message === 'success') {
                        // 登录成功，保存用户信息
                        this.saveLoginState(res.data);
                        // 跳转到首页
                        this.$emit('goToHomepage');
                    } else {
                        // 登录失败，显示错误信息
                        uni.showToast({
                            title: res.message || '登录失败，请重试',
                            icon: 'none',
                            duration: 2000
                        });
                    }
                }).catch(err => {
                    this.isLoading = false;
                    // 网络错误处理
                    uni.showToast({
                        title: '网络连接失败，请检查网络',
                        icon: 'none',
                        duration: 2000
                    });
                    console.error('登录请求失败:', err);
                });
            },
            
            // 表单验证
            validateForm() {
                if (!this.username.trim()) {
                    uni.showToast({
                        title: '请输入用户名',
                        icon: 'none'
                    });
                    return false;
                }
                
                if (!this.password) {
                    uni.showToast({
                        title: '请输入密码',
                        icon: 'none'
                    });
                    return false;
                }
                
                if (this.password.length < 6) {
                    uni.showToast({
                        title: '密码长度不能少于6位',
                        icon: 'none'
                    });
                    return false;
                }
                
                return true;
            },
            
            // 登录API调用 - 适配提供的接口文档
            // 在loginApi方法中修改API地址
            loginApi() {
                return new Promise((resolve, reject) => {
                    //固定为FastAPI后端的实际地址，请根据实际情况修改
                    const apiUrl = API_CONFIG.baseUrl + API_CONFIG.login;
                    
                    uni.request({
                        url: apiUrl,
                        method: 'POST',
                        data: {
                            username: this.username,
                            password: this.password
                            // 已删除remember参数
                        },
                        header: {
                            'content-type': 'application/json'
                        },
                        success: (res) => {
                            resolve(res.data);
                        },
                        fail: (err) => {
                            reject(err);
                        }
                    });
                });
            },
            
            // 保存登录状态
            saveLoginState(userData) {
                // 根据接口文档的响应数据结构保存信息
                if (userData) {
                    // 存储用户基本信息
                    const userInfo = {
                        userId: userData.userId,
                        username: userData.username
                    };
                    uni.setStorageSync('userInfo', userInfo);
                    
                    // 存储token
                    if (userData.token) {
                        uni.setStorageSync('token', userData.token);
                    }
                    
                    // 记录登录状态
                    uni.setStorageSync('isLoggedIn', true);
                }
            },
            
            // 页面跳转方法
            goToFindPassword() {
                this.$emit('goToFindPassword');
            },
            
            goToRegister() {
                this.$emit('goToRegister');
            },
            
            goToIndex() {
                this.$emit('goToIndex');
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
    
    /* 已删除记住我和checkbox相关样式 */
    
    /* 其他原有样式保持不变 */
    .title
	{   
		display: flex;
		margin: auto;
	    margin-top: 10%;
		margin-bottom: 20%;
        width: 450rpx;
        opacity: 1;
        color: rgba(0, 0, 0, 1);
        /** 文本1 */
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
		width:200rpx;
		height:200rpx;
		opacity: 1;
	}
	.rectangle {
	 margin-top: 5%;
	 width: 75%;
	 padding:10rpx;
	 opacity: 1;
	 border-radius: 55rpx;
	 background: rgba(241, 240, 240, 0.347);
	 border: 0.2rpx solid rgba(0, 0, 0, 1);
	}
	.input-box1 {
		display: flex;
		text-align: center;
		margin: auto;
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
		margin: auto;
	    margin-top: 10rpx;
		width: 480rpx;
		height: 80rpx;
		opacity: 1;
        border-radius: 30rpx;
        background: rgba(255, 255, 255, 0.9);
		padding: 0 20rpx;
		   box-sizing: border-box;
		}	
	.sign-in-button{
		display: flex;
		text-align: center;
		margin: auto;
	    margin-top: 20%;
	  width: 400rpx;
	  height: 85rpx;
	  background: linear-gradient(0deg, rgba(80, 224, 18, 0.68), rgba(80, 224, 18, 0.68)), radial-gradient(38.73% 48.73% at 50% 51.168476563545674%, rgba(94, 201, 48, 0.9) 0%, rgba(81, 247, 10, 0.87) 3.24%, rgba(37, 199, 16, 0.9) 100%);
	 border-radius: 45rpx;
	 border: 0.8rpx solid rgba(0, 0, 0, 1);
	 box-shadow: 0rpx 2rpx 1rpx  rgba(0, 0, 0, 0.25);
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
	.sign-in-button:active {
		opacity: 0.8;
	}	
	.find-password{
		text-align: center;
		margin:auto;
	    margin-top: 15rpx;
        color: rgba(86, 85, 85, 0.553);
	    font-size: 31rpx;
	    font-weight: 700;
	}
	.rejister-box{
        color: rgba(6, 5, 5, 0.772);
	    font-size: 30rpx;
	    font-weight: 700rpx;
		display: flex;
		align-items: center; 
		margin-left: 20%;
		margin-top: 10%;
		opacity: 0.8;
	}
  .rejister-page{
		margin-left: 15rpx;
		color: rgba(168, 6, 6, 0.772);
	    font-size: 40rpx;
	    font-weight: 700;
  }
  .back-button {
        margin-top: 10%;
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		background-color: rgba(80, 224, 18, 0.68);
		border: 0.8rpx solid rgba(0, 0, 0, 1);
		box-shadow: 0rpx 2rpx 1rpx  rgba(0, 0, 0, 0.25);
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
	}

</style>
