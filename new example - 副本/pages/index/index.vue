<template>
	<view class="content">
		
        <image class="logo" src="/static/logo.png" />
		<text class="title1">Welcome</text>
		
		<view v-if="closeInitialElements" :class="{ 'close': closeScaleAnimation }">
			<view style="display: flex;flex-direction: column;align-items: center;">
		    <view class="line1" ></view>
		    <text class="app-name-text" >雨林通</text>
		    <view class="line2" ></view>
			</view>
		</view>
		
		<view 
			class="custom-btn" 
			v-if="showInitialElements" 
			:class="{ 'show': showScaleAnimation }"
		>
			    <view class="custom-btn1" @click="$emit('goToLogin')">
			    登  录
			    </view>
				<view class="custom-btn2" @click="$emit('goToRegister')">
				注 册
				</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 控制初始元素显示与隐藏的标志
				closeInitialElements: true,
				showInitialElements:false,
				//控制标志消失动画
				closeScaleAnimation:false,
				// 控制按钮缩放动画的标志
				showScaleAnimation: false
			}
		},
		onLoad() {
			
		},
		mounted() {

			setTimeout(() =>{
				this.closeScaleAnimation = true;
				setTimeout(() =>{
				this.closeInitialElements = false;
			
				this.showInitialElements = true;
				this.showScaleAnimation = true;	
			
				
			    },2000);
			},1000);
	
		},
		methods: {

		}
	}
</script>

<style>
	  page {
	    margin: 0;
	    padding: 0;
	    height: 100%; 
	  }
	.content {
		display: flex;
		flex-direction: column;
		opacity: 1;
		width: 100vw;
		height: 100vh;
		background: linear-gradient(0deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), linear-gradient(180deg, rgba(0, 255, 242, 0.2) 0%, rgba(90, 252, 3, 0.2) 100%);
		align-items: center;
	}

	.logo {
		margin-top: 25%;
		width:200rpx;
		height:200rpx;
		opacity: 1;
	}

	.title1 {
		
		width: 100%;
		height: 10%;
		text-align: center;
		opacity: 1;
		/** 文本1 */
		font-size: 125rpx;
		font-weight: 400;
		color: rgba(255, 255, 255, 1);
		 -webkit-text-stroke: 0.73rpx rgba(0, 0, 0, 1);/*文字描边*/
		 margin-bottom: 20%;
	}
	
	.app-name-text {
	  height: 183.33rpx;
	  opacity: 1;
	  font-size: 75rpx;
	  font-weight: 400;
	  height:90rpx;
	  color: rgba(63, 177, 53, 1.0);
	   -webkit-text-stroke: 0.21rpx rgba(0, 0, 0, 1);/*文字描边*/
	}

   .line1 {
	   margin-top: 80%;
       width: 270.83rpx; 
       height: 3.13rpx; 
       background-color: rgba(47, 133, 39, 1.0); /* 调整线段颜色 */
    }
	.line2 {
	    width: 270.83rpx; /* 调整线段长度 */
	    height: 3.13rpx; /* 调整线段粗细 */
	    background-color: rgba(47, 133, 39, 1.0); /* 调整线段颜色 */
	 }
	 .custom-btn1 {
	  position: relative; 
	  left: calc(50% - 200rpx);
	
	  width: 400rpx;
	  height: 115rpx;
	  background: linear-gradient(90deg, rgba(57, 212, 75, 0.8) 0%, rgba(23, 172, 9, 0.6) 100%);
	 border-radius: 10rpx;
	 border: 0.8rpx solid rgba(0, 0, 0, 1);
	 box-shadow: 0rpx 2rpx 1rpx  rgba(0, 0, 0, 0.25);
	 filter: blur(1rpx);
	 /*文本*/
	 color: white;
	 font-size: 80rpx;
	 font-weight: 700;
	  display: flex;           /* 启用 Flex 布局 */
	   justify-content: center; /* 水平居中 */
	   align-items: center;     /* 垂直居中 */
	    margin-top: 30%;
	  -webkit-text-stroke: 0.2rpx rgba(0, 0, 0, 1);
	}
	.custom-btn2 {
	  position: relative; 
	  left: calc(50% - 200rpx);
	  
	  width: 400rpx;
	  height: 115rpx;
	  background: radial-gradient(50% 50% at 50% 50%, rgba(212, 212, 212, 0.25) 0%, rgba(255, 255, 255, 0.8) 100%);
	  border-radius: 10rpx;
	  border: 0.8rpx solid rgba(0, 0, 0, 1);
	  box-shadow: 0rpx 2rpx 1rpx  rgba(0, 0, 0, 0.25);
	  filter: blur(1rpx);
	  /*文本*/
	  color: rgba(26, 196, 11, 0.7);
	  font-size: 80rpx;
	  font-weight: 700;
	   display: flex;           /* 启用 Flex 布局 */
	    justify-content: center; /* 水平居中 */
	    align-items: center;     /* 垂直居中 */
	   -webkit-text-stroke: 0.1rpx rgba(0, 0, 0, 1);
	    margin-top: 10%;
	}
	.custom-btn2:active,
	.custom-btn1:active {
	  opacity: 0.8;
	  
	}
/* 标志消失的动画 */
.close {
  
	animation: closesign 2s linear;
}

@keyframes closesign {
	0% {
			transform: scale(1);
			opacity: 1;
		}
		25% {
			transform: scale(1);
			opacity: 0.75;
		}
		50% {
			transform: scale(1);
			opacity: 0.5;
		}
		75% {
			transform: scale(1);
			opacity: 0.25;
		}
	    100% {
			transform: scale(1);
			opacity: 0;
		}
	}
/* 按钮由小变大再变回的动画 */
.show {
    animation: scaleUpDown 2s linear ;
}

@keyframes scaleUpDown {
	0% {
			transform: scale(1);
			opacity: 0.2;
		}
		25% {
			transform: scale(1);
			opacity: 0.4;
		}
		50% {
			transform: scale(1);
			opacity: 0.7;
		}
		100% {
			transform: scale(1);
			opacity: 1;
		}
}
</style>
