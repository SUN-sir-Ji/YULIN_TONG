<template>
  <view class="content">
    <!-- 标题和返回按钮区域 --> 
    <view class="header-container">
      <view class="back-button" @click="$emit('goToHomepage1')">
        <image src="/static/back.png" class="back-icon"></image>
      </view>
      <!-- 标题 -->
      <view class="title">图片识别</view>
      <view class="header-placeholder"></view> <!-- 占位元素，保持标题居中 -->
    </view>
    
    <!-- 上传区域 -->
    <view class="upload-container">
      <!-- 上传按钮 -->
      <view class="upload-btn-wrapper">
        <view class="upload-btn" @click="chooseImage">
          <view class="upload-icon-wrapper">
            <image src="/static/photo.png" class="upload-icon"></image>
          </view>
          <text class="upload-text">点击上传图片</text>
          <text class="upload-subtext">支持JPG、PNG格式，最多9张</text>
        </view>
      </view>
      
      <!-- 已选择的图片预览 -->
      <!-- 在image-list-title下方添加滑动提示箭头 -->
      <view class="image-list" v-if="imageList.length > 0">
        <text class="image-list-title">已选择 {{ imageList.length }} 张图片</text>
        <!-- 添加滑动提示 -->
        <text class="swipe-hint" v-if="imageList.length > 3">← 左右滑动查看更多 →</text>
        <view class="images-wrapper">
          <!-- 图片项内容保持不变 -->
          <view class="image-item" v-for="(image, index) in imageList" :key="index">
            <image :src="image" class="preview-image" mode="aspectFill"></image>
            <view class="delete-btn" @click="deleteImage(index)">
              <text class="delete-icon">×</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 上传进度条 -->
      <view class="progress-container" v-if="uploading">
        <view class="progress-header">
          <text class="progress-text">上传中...</text>
          <text class="progress-percentage">{{ uploadProgress }}%</text>
        </view>
        <view class="progress-bar">
          <view class="progress-track"></view>
          <view class="progress-fill" :style="{ width: uploadProgress + '%' }"></view>
          <view class="progress-ball" :style="{ left: uploadProgress + '%' }"></view>
        </view>
      </view>
      
      <!-- 上传到服务器按钮 -->
      <button class="submit-btn" @click="uploadImages" :disabled="imageList.length === 0 || uploading">
        <text class="submit-btn-text">{{ uploading ? '上传中...' : '开始识别' }}</text>
      </button>
    </view>
    
    <!-- 上传历史记录 -->
    <view class="history-container" v-if="uploadHistory.length > 0">
      <view class="history-header">
        <text class="history-title">最近上传</text>
        <text class="history-tip">点击图片查看识别结果</text>
      </view>
      <view class="history-list">
        <view class="history-item" v-for="(item, index) in uploadHistory" :key="index" @click="showHistoryResult(index)">
          <image :src="item.url" class="history-image" mode="aspectFill"></image>
          <view class="history-overlay">
            <text class="history-info">{{ item.time }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 识别结果展示区域 -->
    <view class="recognition-container" v-if="selectedResult || recognitionResults.length > 0">
      <text class="recognition-title">识别结果</text>
      <view class="recognition-list">
        <view class="recognition-card" v-if="selectedResult">
          <view class="card-header">
            <image :src="selectedResult.imageUrl" class="card-image" mode="aspectFill"></image>
            <view class="card-info">

            </view>
          </view>
          <view class="card-results">
            <view class="result-item" v-for="item in selectedResult.results" :key="item.class">
              <text class="result-class">{{ item.class }}</text>
              <view class="confidence-wrapper">
                <text class="confidence-text">{{ (item.confidence * 100).toFixed(0) }}%</text>
                <view class="confidence-bar">
                  <view class="confidence-fill" :style="{ width: (item.confidence * 100) + '%', backgroundColor: getConfidenceColor(item.confidence) }"></view>
                </view>
              </view>
            </view>
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
        // 存储选择的图片列表
        imageList: [],
        // 上传进度
        uploadProgress: 0,
        // 是否正在上传
        uploading: false,
        // 上传历史记录
        uploadHistory: [],
        
        // 所有历史识别结果
        recognitionResults: [],
        // 当前上传的识别结果
        currentRecognitionResults: [],
        // 当前选中的识别结果（用于显示点击历史图片后的结果）
        selectedResult: null
      };
    },
    onLoad() {
      // 页面加载时，从本地存储获取历史记录
      this.loadHistory();
    },
    methods: {
      // 返回按钮功能
      
      // 选择图片
      chooseImage() {
        // 计算还能选择多少张图片（最多9张）
        const maxCount = 9 - this.imageList.length;
        
        if (maxCount <= 0) {
          uni.showToast({
            title: '最多只能上传9张图片',
            icon: 'none'
          });
          return;
        }
        
        uni.chooseImage({
          count: maxCount,
          sizeType: ['compressed'], // 压缩图片
          sourceType: ['album', 'camera'], // 从相册选择或拍照
          success: (res) => {
            // 将选择的图片添加到列表中
            this.imageList = [...this.imageList, ...res.tempFilePaths];
          },
          fail: (err) => {
            console.error('选择图片失败:', err);
          }
        });
      },
      
      // 删除图片
      deleteImage(index) {
        uni.showModal({
          title: '提示',
          content: '确定要删除这张图片吗？',
          success: (res) => {
            if (res.confirm) {
              this.imageList.splice(index, 1);
            }
          }
        });
      },
      
      // 上传图片到服务器
      uploadImages() {
        if (this.imageList.length === 0) {
          uni.showToast({
            title: '请先选择图片',
            icon: 'none'
          });
          return;
        }
        
        // 清空当前上传的识别结果
        this.currentRecognitionResults = [];
        // 清空选中的结果，确保显示新上传的结果
        this.selectedResult = null;
        
        this.uploading = true;
        this.uploadProgress = 0;
        
        uni.showLoading({
          title: '正在上传...'
        });
        
        // 获取存储的token
        const token = uni.getStorageSync('token');
        
        // 逐个上传图片
        let uploadedCount = 0;
        //固定为FastAPI后端的实际地址，确保与后端的配置一致
        const apiUrl = API_CONFIG.baseUrl + API_CONFIG.uploadImage;

        this.imageList.forEach((filePath, index) => {
          uni.uploadFile({
            url:apiUrl,
            filePath: filePath,
            name: 'file',
            header: {
              'Authorization': `Bearer ${token}`
            },
            success: (uploadFileRes) => {
              // 在 uploadFile 的 success 回调中添加
              console.log('上传成功:', uploadFileRes.data);
              const responseData = JSON.parse(uploadFileRes.data);
              console.log('解析后的数据:', responseData);
              console.log('是否包含识别结果:', !!responseData.data?.recognition_results);
              
              // 保存识别结果
              if (responseData.code === 200 && responseData.data.recognition_results) {
                // 添加到所有历史识别结果中
                this.recognitionResults.push({
                  imageUrl: filePath,
                  results: responseData.data.recognition_results,
                  filename: responseData.data.filename,
                  // 添加时间戳，用于与历史记录关联
                  timestamp: Date.now()
                });
                
                // 添加到当前上传的识别结果中
                this.currentRecognitionResults.push({
                  imageUrl: filePath,
                  results: responseData.data.recognition_results,
                  filename: responseData.data.filename,
                  timestamp: Date.now()
                });
              }
              
              uploadedCount++;
              
              // 更新进度
              this.uploadProgress = Math.floor((uploadedCount / this.imageList.length) * 100);
              
              // 如果所有图片上传完成
              if (uploadedCount === this.imageList.length) {
                this.handleUploadComplete();
              }
            },
            fail: (err) => {
              console.error('上传失败:', err);
              this.uploading = false;
              this.uploadProgress = 0;
              uni.hideLoading();
              
              uni.showToast({
                title: '上传失败，请重试',
                icon: 'none'
              });
            }
          });
        });
      },
      
      // 处理上传完成
      handleUploadComplete() {  
        this.uploading = false;
        uni.hideLoading();
        
        // 保存上传历史（传入当前识别结果）
        this.saveHistory(this.currentRecognitionResults);
        
        // 如果有识别结果，显示识别结果弹窗
        if (this.currentRecognitionResults.length > 0) {
          this.showRecognitionResults();
          // 设置选中的结果为最新上传的第一个结果
          this.selectedResult = this.currentRecognitionResults[0];
        }
        
        uni.showToast({
          title: '上传成功',
          icon: 'success'
        });
        
        // 清空已选择的图片
        this.imageList = [];
      },
      
      // 保存上传历史（修改版本：接收识别结果作为参数）
      saveHistory(recognitionResults) {
        // 获取当前时间
        const now = new Date();
        const timeStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
        
        // 为每张图片创建历史记录，并关联识别结果
        const newHistory = this.imageList.map((url, index) => {
          // 获取该图片对应的识别结果
          const result = recognitionResults[index] || {};
          
          return {
            url: url,
            time: timeStr,
            timestamp: Date.now(),
            // 添加唯一ID用于关联
            id: `history_${Date.now()}_${index}`,
            // 直接存储识别结果，避免后续查找
            recognitionData: result.results || []
          };
        });
        
        // 合并到历史记录中，并限制最多显示10条
        this.uploadHistory = [...newHistory, ...this.uploadHistory].slice(0, 10);
        
        // 保存到本地存储
        uni.setStorageSync('uploadHistory', this.uploadHistory);
      },
      
      // 从本地存储加载历史记录
      loadHistory() {
        const history = uni.getStorageSync('uploadHistory');
        if (history) {
          this.uploadHistory = history;
        }
      },
      
      // 显示历史记录的识别结果（修改版本）
      showHistoryResult(index) {
        // 获取点击的历史图片项
        const historyItem = this.uploadHistory[index];
        
        if (historyItem && historyItem.recognitionData && historyItem.recognitionData.length > 0) {
          // 直接从historyItem中获取识别结果
          this.selectedResult = {
            imageUrl: historyItem.url,
            results: historyItem.recognitionData,
            filename: '历史图片'
          };
        } else {
          // 如果没有直接存储的识别结果，尝试通过其他方式查找
          const result = this.recognitionResults.find(r => 
            r.imageUrl === historyItem.url || 
            (r.timestamp && historyItem.timestamp && Math.abs(r.timestamp - historyItem.timestamp) < 1000)
          );
          
          if (result) {
            this.selectedResult = result;
          } else {
            uni.showToast({
              title: '未找到对应识别结果',
              icon: 'none'
            });
          }
        }
      },
      
      // 添加缺失的showRecognitionResults方法
      showRecognitionResults() {
        // 这个方法在handleUploadComplete中被调用，但功能已经通过设置selectedResult实现
        // 可以在这里添加任何额外的显示逻辑
        console.log('显示识别结果');
      },
      
      // 添加缺失的getConfidenceColor方法
      getConfidenceColor(confidence) {
        // 根据置信度返回不同的颜色
        if (confidence >= 0.9) {
          return '#07c160'; // 绿色 - 高置信度
        } else if (confidence >= 0.7) {
          return '#52c41a'; // 深绿色 - 中高置信度
        } else if (confidence >= 0.5) {
          return '#faad14'; // 橙色 - 中等置信度
        } else {
          return '#ff7a45'; // 橙色 - 低置信度
        }
      }
    }
  };
</script>

<style scoped>
  .content {
    padding: 30rpx;
    background-color: #f5f5f5;
    min-height: 100vh;
    background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  }
  
  .title {
    font-size: 56rpx;
    font-weight: bold;
    text-align: center;
    margin-bottom: 60rpx;
    color: #333;
    text-shadow: 2rpx 2rpx 4rpx rgba(0, 0, 0, 0.1);
  }
  
  .upload-container {
    background-color: #fff;
    border-radius: 30rpx;
    padding: 40rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
  }
  
  .upload-container:active {
    box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.05);
    transform: translateY(2rpx);
  }
  
  .upload-btn-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 30rpx;
  }
  
  .upload-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 450rpx;
    height: 300rpx;
    border: 4rpx dashed #ddd;
    border-radius: 20rpx;
    background-color: #f9f9f9;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .upload-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(7, 193, 96, 0.1), transparent);
    transition: all 0.5s ease;
  }
  
  .upload-btn:active {
    border-color: #07c160;
    background-color: rgba(7, 193, 96, 0.05);
    transform: scale(0.98);
  }
  
  .upload-btn:active::before {
    left: 100%;
  }
  
  .upload-icon-wrapper {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: #07c160;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20rpx;
    box-shadow: 0 5rpx 15rpx rgba(7, 193, 96, 0.3);
  }
  
  .upload-icon {
    width: 60rpx;
    height: 60rpx;
    filter: brightness(0) invert(1);
  }
  
  .upload-text {
    font-size: 32rpx;
    color: #333;
    font-weight: 500;
    margin-bottom: 8rpx;
  }
  
  .upload-subtext {
    font-size: 24rpx;
    color: #999;
  }
  
  .image-list {
    margin-bottom: 30rpx;
  }
  
  .image-list-title {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 20rpx;
    display: block;
  }
  
  .images-wrapper {
    display: flex;
    gap: 20rpx;
    overflow-x: auto;
    padding-right: 20rpx;
    
  }
  
  .image-item {
    position: relative;
    width: 200rpx;
    height: 200rpx;
    border-radius: 15rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    flex-shrink: 0;
  }
  
  .image-item:active {
    transform: scale(0.95);
  }
  
  .preview-image {
    width: 100%;
    height: 100%;
  }
  /* 添加滑动提示文字样式 */
.swipe-hint {
  font-size: 24rpx;
  color: #999;
  display: block;
  margin-bottom: 15rpx;
  text-align: center;
  /* 添加轻微的动画效果吸引用户注意 */
  animation: fadeInOut 2s ease-in-out infinite;
}

/* 淡入淡出动画 */
@keyframes fadeInOut {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
  .delete-btn {
    position: absolute;
    top: 10rpx;
    right: 10rpx;
    width: 60rpx;
    height: 60rpx;
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }
  
  .delete-btn:active {
    background-color: #ee0a24;
    transform: scale(1.1);
  }
  
  .delete-icon {
    color: #fff;
    font-size: 40rpx;
    font-weight: bold;
  }
  
  .progress-container {
    margin: 30rpx 0;
  }
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15rpx;
  }
  
  .progress-text {
    font-size: 28rpx;
    color: #666;
  }
  
  .progress-percentage {
    font-size: 28rpx;
    font-weight: bold;
    color: #07c160;
  }
  
  .progress-bar {
    width: 100%;
    height: 20rpx;
    background-color: #f0f0f0;
    border-radius: 10rpx;
    overflow: hidden;
    position: relative;
  }
  
  .progress-track {
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, #e6f7ff, #f6ffed);
  }
  
  .progress-fill {
    position: absolute;
    height: 100%;
    background: linear-gradient(90deg, #07c160, #52c41a);
    transition: width 0.3s ease;
  }
  
  .progress-ball {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 30rpx;
    height: 30rpx;
    background-color: #fff;
    border: 6rpx solid #07c160;
    border-radius: 50%;
    box-shadow: 0 2rpx 8rpx rgba(7, 193, 96, 0.3);
    transition: left 0.3s ease;
  }
  
  .submit-btn {
    width: 100%;
    height: 100rpx;
    line-height: 100rpx;
    background-color: #07c160;
    color: #fff;
    border-radius: 50rpx;
    margin-top: 20rpx;
    font-size: 32rpx;
    font-weight: 500;
    box-shadow: 0 6rpx 20rpx rgba(7, 193, 96, 0.3);
    transition: all 0.3s ease;
  }
  
  .submit-btn:active {
    background-color: #06ad56;
    box-shadow: 0 3rpx 10rpx rgba(7, 193, 96, 0.2);
    transform: scale(0.98);
  }
  
  .submit-btn:disabled {
    background-color: #ccc;
    box-shadow: none;
  }
  
  .submit-btn-text {
    font-size: 32rpx;
    font-weight: 500;
  }
  
  /* 历史记录样式 */
  .history-container {
    background-color: #fff;
    border-radius: 30rpx;
    padding: 40rpx;
    margin-bottom: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08);
  }
  
  .history-header {
    display: flex;
    align-items: center;
    margin-bottom: 30rpx;
  }
  
  .history-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    margin-right: 10rpx;
  }
  
  .history-tip {
    font-size: 24rpx;
    color: #999;
    opacity: 0.8;
  }
  
  .history-list {
    display: flex;
    gap: 20rpx;
    overflow-x: auto;
    padding-right: 20rpx;
  }
  
  .history-item {
    position: relative;
    width: 180rpx;
    height: 180rpx;
    border-radius: 15rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    flex-shrink: 0;
  }
  
  .history-item:active {
    transform: scale(0.95);
  }
  
  .history-image {
    width: 100%;
    height: 100%;
  }
  
  .history-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
    padding: 15rpx;
  }
  
  .history-info {
    color: #fff;
    font-size: 22rpx;
    text-align: center;
    display: block;
  }
  
  /* 识别结果样式 */
  .recognition-container {
    background-color: #fff;
    border-radius: 30rpx;
    padding: 40rpx;
    margin-top: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08);
  }
  
  .recognition-title {
    font-size: 36rpx;
    font-weight: bold;
    margin-bottom: 30rpx;
    color: #333;
    display: block;
  }
  
  .recognition-list {
    display: flex;
    flex-direction: column;
    gap: 30rpx;
  }
  
  .recognition-card {
    background-color: #f9f9f9;
    border-radius: 20rpx;
    padding: 30rpx;
    transition: all 0.3s ease;
  }
  
  .recognition-card:active {
    box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.05);
    transform: translateY(2rpx);
  }
  
  .card-header {
    display: flex;
    align-items: center;
    margin-bottom: 25rpx;
  }
  
  .card-image {
    width: 160rpx;
    height: 140rpx;
    border-radius: 15rpx;
    margin-right: 25rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  }
  
  .card-info {
    flex: 1;
  }
  
  .card-filename {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }
  
  .card-stats {
    font-size: 26rpx;
    color: #666;
  }
  
  .card-results {
    display: flex;
    flex-direction: column;
    gap: 20rpx;
  }
  
  .result-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .result-class {
    font-size: 28rpx;
    font-weight: 500;
    color: #333;
    flex: 0 0 180rpx;
  }
  
  .confidence-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 15rpx;
  }
  
  .confidence-text {
    font-size: 26rpx;
    font-weight: bold;
    color: #07c160;
    width: 60rpx;
    text-align: right;
  }
  
  .confidence-bar {
    flex: 1;
    height: 15rpx;
    background-color: #f0f0f0;
    border-radius: 8rpx;
    overflow: hidden;
  }
  
  .confidence-fill {
    height: 100%;
    transition: width 0.5s ease;
  }
  
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40rpx;
  height: 80rpx;
}

.back-button {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #fff;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.back-button:active {
  background-color: #f5f5f5;
  transform: scale(0.95);
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.08);
}

.back-icon {
  width: 40rpx;
  height: 40rpx;
}

.header-placeholder {
  width: 80rpx;
}  

.title {
  font-size: 56rpx;
  font-weight: bold;
  text-align: center;
  color: #333;
  text-shadow: 2rpx 2rpx 4rpx rgba(0, 0, 0, 0.1);
  flex: 1;
  margin-bottom: 0;
}
</style>