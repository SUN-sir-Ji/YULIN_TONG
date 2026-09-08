<template>
  <view class="content">
    <view class="rectangle0">
      <view class="back-button" @click="$emit('goToHomepage1')">
        <text class="back-icon"> &lt; </text>
      </view>
      <input class="search1" placeholder="植物名称" v-model="searchresult" />
      <button class="search-button" @click="search">搜索</button>
    </view>
    <view class="tree-selector-container">
      <button class="tree-selector-button" @click="showTree">
        <text class="tree-selector-text">{{ selectedPath || '打开树形选择器' }}</text>
        <text class="tree-selector-arrow">▼</text>
      </button>
      <peng-tree
        ref="pengTree"
        :range="range"
        idKey="id"
        nameKey="name"
        allKey="value"
        :multiple="false"
        :cascade="false"
        :selectParent="true"  
        confirmColor="#007aff"
        cancelColor="#757575"
        title="植物百科导航"
        titleColor="#757575"
        @cancel="treeCancel"
        @confirm="treeConfirm"
      >
      </peng-tree>
    </view>
    <view class="plant-list-container">
      <view class="rectangle1">
        <view class="plant-grid" ref="plantGrid">
          <!-- 显示植物列表 -->
          <template v-if="plants.length > 0">
            <view class="plant-card" @click="goToPlantDetail(item)" v-for="(item, index) in plants" :key="index">
              <div class="plant-image-container">
                <image 
                  :src="item.image_path || '/static/plantphoto/plant.png'" 
                  class="plant-image"
                  @error="handleImageError($event, index)"
                />
              </div>
              <text class="plant-name">{{ item.species_chinese_name }}</text>
              <text class="plant-scientific-name">{{ item.species_latin_name }}</text>
            </view>
          </template>
          <!-- 无匹配结果时显示 -->
          <template v-else-if="hasSearched">
            <view class="no-results">
              <text>未找到相关植物</text>
              <text class="no-results-hint">请尝试选择其他分类或检查分类名称</text>
            </view>
          </template>
          <!-- 初始状态提示 -->
          <template v-else>
            <view class="initial-hint">
              <text>请从上方选择分类进行查询</text>
            </view>
          </template>
        </view>
        <!-- 加载更多提示 -->
        <view v-if="loading && plants.length > 0" class="loading-more">
          <text>加载中...</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import PengTree from '@/components/songPickerTree/songPickerTree.vue';
import API_CONFIG from '../../utils/apiConfig.js';
export default {
  components: {
    'peng-tree': PengTree
  },
  data() {
      return {
        searchresult: '',
        selectedPath: '',
        range: [], // 初始化为空数组，将通过API填充
        plants: [], // 植物列表，初始为空
        hasSearched: false, // 标记是否已进行过搜索
        selectedCategoryLevel: '', // 存储当前选中的分类级别
        selectedCategoryValue: '', // 存储当前选中的分类值
        page: 1, // 当前页码
        pageSize: 30, // 每页数量 - 平衡性能和用户体验
        hasMore: true, // 是否有更多数据
        loading: false // 是否正在加载
      }
    },
  mounted() {
    // 组件挂载时获取顶级分类数据
    this.fetchTopCategories();
    
    // 添加延迟确保DOM已渲染
    this.$nextTick(() => {
      this.addScrollListener();
    });
  },
  
  beforeDestroy() {
    // 移除滚动事件监听器，防止内存泄漏
    this.removeScrollListener();
  },
  
  methods: {
    // 添加滚动事件监听器
    addScrollListener() {
      const plantGrid = this.$refs.plantGrid;
      if (plantGrid) {
        plantGrid.addEventListener('scroll', this.handleGridScroll);
      }
    },
    
    // 移除滚动事件监听器
    removeScrollListener() {
      const plantGrid = this.$refs.plantGrid;
      if (plantGrid) {
        plantGrid.removeEventListener('scroll', this.handleGridScroll);
      }
    },
    
    // 处理内部滚动事件，实现滚动到底部加载更多
    handleGridScroll(event) {
      const { scrollTop, scrollHeight, clientHeight } = event.target;
      
      // 计算滚动距离底部的距离，当小于50px时触发加载更多
      const distanceToBottom = scrollHeight - scrollTop - clientHeight;
      
      console.log('内部滚动事件:', {
        scrollTop,
        scrollHeight,
        clientHeight,
        distanceToBottom,
        hasMore: this.hasMore,
        loading: this.loading,
        hasSearched: this.hasSearched
      });
      
      // 当滚动到底部附近，且有更多数据、不在加载中、已搜索过时，触发加载
      if (distanceToBottom < 50 && this.hasMore && !this.loading && this.hasSearched) {
        console.log('内部滚动到底部，开始加载更多数据');
        this.loadMorePlants();
      }
    },
    search() {
      console.log('搜索内容：', this.searchresult);
      // 如果有搜索内容，可以实现基于名称的搜索
      // 这里暂时留空，等待后端API支持
    },
    showTree() {
      this.$refs.pengTree._show();
    },
    treeCancel(e) {
      console.log("你点击了取消");
    },
    treeConfirm(e) {
      console.log("你点击了确定", e);
      if (Array.isArray(e) && e.length > 0) {
        const selectedItem = e[0];
        this.selectedPath = selectedItem.name;
        this.selectedCategoryValue = selectedItem.value;
        
        // 增强的分类层级判断逻辑
        let categoryLevel = 'phylum_latin_name'; // 默认设为门
        
        // 首先检查是否有明确的rank字段
        if (selectedItem.rank !== undefined) {
          console.log('使用rank字段判断层级:', selectedItem.rank);
          switch(selectedItem.rank) {
            case 0:
              categoryLevel = 'phylum_latin_name';
              break;
            case 1:
              categoryLevel = 'class_latin_name';
              break;
            case 2:
              categoryLevel = 'order_latin_name';
              break;
            case 3:
              categoryLevel = 'family_latin_name';
              break;
            case 4:
              categoryLevel = 'genus_latin_name';
              break;
          }
        }
        
        // 然后通过名称特征进行更精确的判断（覆盖rank判断结果）
        const name = selectedItem.name.toLowerCase();
        const value = selectedItem.value.toLowerCase();
        
        console.log('通过名称特征判断:', name, value);
        
        // 门的特征词
        if (name.includes('门') || value.includes('phyta') || value.includes('bacteria') || value.includes('fungi')) {
          categoryLevel = 'phylum_latin_name';
        }
        // 纲的特征词
        else if (name.includes('纲') || value.includes('opsida') || value.includes('phyceae') || value.includes('imycetes') || value.includes('class')) {
          categoryLevel = 'class_latin_name';
        }
        // 目的特征词
        else if (name.includes('目') || value.includes('ales') || value.includes('formes') || value.includes('ida') || value.includes('order')) {
          categoryLevel = 'order_latin_name';
        }
        // 科的特征词
        else if (name.includes('科') || value.includes('aceae') || value.includes('idae') || value.includes('aceae') || value.includes('family')) {
          categoryLevel = 'family_latin_name';
        }
        // 属的特征词
        else if (name.includes('属') || value.includes('genus') || (!value.includes('phyta') && !value.includes('opsida') && !value.includes('ales') && !value.includes('aceae'))) {
          categoryLevel = 'genus_latin_name';
        }
        
        this.selectedCategoryLevel = categoryLevel;
        
        // 添加详细日志记录，用于调试
        console.log('选中的分类信息:');
        console.log('- 名称:', selectedItem.name);
        console.log('- 值:', selectedItem.value);
        console.log('- Rank:', selectedItem.rank);
        console.log('- 确定的字段名:', this.selectedCategoryLevel);
        
        // 根据选择的分类筛选植物
        this.fetchPlantsByCategory(this.selectedCategoryLevel, this.selectedCategoryValue);
      }
    },
    
    // 根据分类获取植物列表 - 优化无限滚动初始化
    fetchPlantsByCategory(categoryLevel, categoryValue) {
      console.log('开始新的分类查询:', { categoryLevel, categoryValue });
      
      // 重置分页参数
      this.page = 1;
      this.plants = [];
      this.hasMore = true;
      this.hasSearched = false; // 重置搜索状态
      
      // 验证参数有效性
      if (!categoryLevel || !categoryValue) {
        console.error('查询参数无效:', categoryLevel, categoryValue);
        uni.showToast({ title: '查询参数无效', icon: 'none' });
        return;
      }
      
      // 保存当前分类信息，供loadMorePlants使用
      this.selectedCategoryLevel = categoryLevel;
      this.selectedCategoryValue = categoryValue;
      
      console.log(`开始查询 ${categoryLevel}: ${categoryValue} 的植物`);
      // 执行首次加载
      this.loadMorePlants(categoryLevel, categoryValue);
    },
    
    // 加载更多植物 - 支持无参数调用
    loadMorePlants(categoryLevel, categoryValue) {
      // 如果没有更多数据或正在加载，则不执行
      if (!this.hasMore || this.loading) return;
      
      // 使用传入的参数或当前已保存的分类信息
      // 对于首次加载，使用传入的参数；对于加载更多，使用已保存的值
      const finalCategoryLevel = categoryLevel || this.selectedCategoryLevel;
      const finalCategoryValue = categoryValue || this.selectedCategoryValue;
      
      // 验证参数有效性
      if (!finalCategoryLevel || !finalCategoryValue) {
        console.error('加载更多参数无效:', { finalCategoryLevel, finalCategoryValue });
        return;
      }
      
      console.log('加载更多植物数据:', {
        categoryLevel: finalCategoryLevel,
        categoryValue: finalCategoryValue,
        page: this.page,
        pageSize: this.pageSize
      });
      
      const apiUrl = API_CONFIG.baseUrl + API_CONFIG.plantsList;
      
      // 构建查询参数，包含分页信息
      const queryParams = {};
      queryParams[finalCategoryLevel] = finalCategoryValue;
      queryParams.page = this.page;
      queryParams.pageSize = this.pageSize;
      
      console.log('构建的查询参数:', JSON.stringify(queryParams));
      console.log('请求的API地址:', apiUrl);
      
      this.loading = true;
      if (this.page === 1) {
        uni.showLoading({ title: '正在查询...' });
      } else {
        console.log('加载下一页数据，当前页:', this.page, '总记录数:', this.plants.length);
      }
      
      uni.request({
        url: apiUrl,
        method: 'GET',
        data: queryParams,
        success: (res) => {
          console.log('API响应完整数据:', JSON.stringify(res));
          
          // 标记为已搜索
          this.hasSearched = true;
          
          if (res.data && res.data.code === 200) {
              // 检查返回的数据结构
              const responseData = res.data.data;
              let newPlants = [];
              let totalCount = 0;
              
              // 适配不同的数据结构
              if (Array.isArray(responseData)) {
                // 兼容旧的数据结构
                newPlants = responseData;
                totalCount = newPlants.length;
              } else if (responseData && Array.isArray(responseData.list)) {
                // 新的数据结构
                newPlants = responseData.list;
                totalCount = responseData.total || 0;
              }
              
              // 如果是第一页，直接替换；否则追加
              if (this.page === 1) {
                this.plants = newPlants;
                // 如果第一页就没有数据，显示提示
                if (newPlants.length === 0) {
                  uni.showToast({ title: '未找到相关植物', icon: 'none' });
                  console.log('该分类下没有植物数据');
                }
              } else {
                this.plants = [...this.plants, ...newPlants];
              }
              
              console.log(`植物列表获取成功: 当前${this.plants.length}条, 总计${totalCount}条`);
              
              // 判断是否还有更多数据
              console.log('响应数据中的total字段:', responseData && responseData.total);
              console.log('当前植物列表长度:', this.plants.length);
              
              // 优化分页判断逻辑
              if (responseData && responseData.total !== undefined && responseData.total !== null) {
                // 使用total字段判断 - 更可靠的方式
                this.hasMore = this.plants.length < responseData.total;
                console.log(`使用total判断 - 已加载${this.plants.length}/${responseData.total}条数据，是否有更多:`, this.hasMore);
              } else if (newPlants.length > 0) {
                // 当没有total字段时，如果返回的记录数等于请求的页大小，说明可能还有更多数据
                // 只有当返回的数据少于pageSize时，才认为没有更多数据
                this.hasMore = newPlants.length === this.pageSize;
                console.log(`使用分页大小判断 - 当前页返回${newPlants.length}/${this.pageSize}条数据，是否有更多:`, this.hasMore);
              } else {
                // 没有新数据，设置为没有更多
                this.hasMore = false;
                console.log('没有新数据 - 是否有更多数据:', this.hasMore);
              }
              
              // 增加页码
              if (this.hasMore) {
                this.page++;
              }
            } else {
              if (this.page === 1) {
                this.plants = [];
              }
              console.error('获取植物列表失败: 状态码:', res.data && res.data.code, '消息:', (res.data && res.data.message) || '未知错误');
              if (this.page === 1) {
                uni.showToast({ title: '查询失败，请重试', icon: 'none' });
              }
            }
          },
          fail: (err) => {
            if (this.page === 1) {
              this.plants = [];
              this.hasSearched = true;
            }
            console.error('请求植物列表失败:', err);
            console.log('网络错误详情:', JSON.stringify(err));
            if (this.page === 1) {
              uni.showToast({ title: '网络异常，请检查连接', icon: 'none' });
            }
        },
        complete: () => {
          this.loading = false;
          // 无论是否第一页，都隐藏加载浮窗
          uni.hideLoading();
        }
      });
    },
    
    // 滚动到底部时加载更多 - 优化无限滚动
    onReachBottom() {
      console.log('触发onReachBottom:', {
        hasMore: this.hasMore,
        loading: this.loading,
        hasCategory: !!this.selectedCategoryLevel && !!this.selectedCategoryValue,
        hasSearched: this.hasSearched
      });
      
      // 简化条件判断，确保只要有更多数据、不在加载中，且已经进行过搜索就触发加载
      // 不再依赖selectedCategoryLevel和selectedCategoryValue，因为加载更多时这些值不会改变
      if (this.hasMore && !this.loading && this.hasSearched) {
        console.log('开始加载更多数据，当前页码:', this.page);
        // 直接调用loadMorePlants，不需要再次传入参数
        this.loadMorePlants();
      }
    },
    
    // 处理图片加载失败
    handleImageError(event, index) {
      // 图片加载失败时使用默认图片
      event.target.src = '/static/plantphoto/plant.png';
    },
    
    // 跳转到植物详情页
    goToPlantDetail(plant) {
      // 将选中的植物信息存储到全局，方便详情页获取
      this.$emit('goToPlantimage', { plantId: plant.id });
    },
    
    // 获取顶级分类数据
    fetchTopCategories() {
      // 从后端API获取顶级分类（parent_id=0）
      const apiUrl = API_CONFIG.baseUrl + API_CONFIG.categories;
      uni.request({
        url: apiUrl,
        method: 'GET',
        data: { parent_id: 0 },
        success: (res) => {
          if (res.data && res.data.code === 200 && res.data.data) {
            // 将API返回的数据处理成树形组件需要的完整格式
            this.range = res.data.data.map(item => ({
              ...item,
              children: [], // 初始化为空数组，通过懒加载填充
              lastRank: false, // 先设置为false，确保显示折叠符号
              showChild: false,
              open: false,
              rank: 0, // 设置顶级分类层级为0
              show: 1,
              hasChildren: true // 强制设置为true，确保可以展开
            }));
            console.log('顶级分类数据获取成功:', this.range);
          } else {
            console.error('获取分类数据失败:', res.data && res.data.message ? res.data.message : '未知错误');
          }
        },
        fail: (err) => {
          console.error('请求分类数据失败:', err);
          uni.showToast({ title: '获取分类数据失败', icon: 'none' });
        }
      });
    }
  }
}
</script>


<style lang="scss">
// 定义颜色变量，保持原有色调
$background-color: #f8f8f8;
$card-background: #e6e3e3;
$button-background: #ffffff;
$input-background: #d6d4d4;
$plant-card-bg: #d0d0d0;
$text-primary: #333333;
$text-secondary: #757575;
$accent-color: #50e012;
$border-color: #000000;

// 全局样式重置
page {
  background-color: $background-color;
}

.content {
  width: 100%;
  height: 100vh;
  opacity: 1;
  background: linear-gradient(0deg, rgba(212, 210, 210, 0.4), rgba(212, 210, 210, 0.4)), 
              linear-gradient(180deg, rgba(0, 255, 242, 0.08) 0%, rgba(90, 252, 3, 0.07) 100%);
  display: flex;
  flex-direction: column;
}

// 顶部搜索栏
.rectangle0 {
  width: 100%;
  height: 180rpx;
  opacity: 1;
  background: $button-background;
  display: flex;
  justify-content: center;
  flex-direction: row;
  align-items: center;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

// 返回按钮优化
.back-button {
  width: 10%;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10rpx;
  border-radius: 15rpx;
  transition: all 0.3s ease;
}

.back-button:active {
  background-color: rgba(0, 0, 0, 0.05);
}

.back-icon {
  font-size: 60rpx;
  font-weight: bold;
  color: $text-primary;
}

// 搜索框优化
.search1 {
  margin-left: 10rpx;
  width: 60%;
  height: 40%;
  opacity: 1;
  background: $input-background;
  border-radius: 25rpx;
  padding: 0 20rpx;
  box-sizing: border-box;
  font-size: 28rpx;
  color: $text-primary;
}

.search1::placeholder {
  color: $text-secondary;
  font-size: 28rpx;
}

// 搜索按钮优化
.search-button {
  width: 20%;
  height: 40%;
  opacity: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-color: $accent-color;
  border-radius: 25rpx;
  border: none;
  color: white;
  font-size: 28rpx;
  font-weight: 500;
  transition: all 0.3s ease;
}

.search-button:active {
  opacity: 0.8;
  transform: scale(0.95);
}

// 树形选择器容器
.tree-selector-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 20rpx;
}

// 树形选择器按钮优化
.tree-selector-button {
  align-items: center;
  width: 80%;
  height: 80rpx;
  display: flex;
  background-color: $button-background;
  border-radius: 25rpx;
  color: $text-secondary;
  border: 0.8rpx solid rgba(0, 0, 0, 0.3);
  flex-direction: row;
  justify-content: space-between;
  padding: 0 20rpx;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.tree-selector-button:active {
  background-color: rgba(0, 0, 0, 0.05);
}

.tree-selector-text {
  width: 90%;
  text-align: left;
  font-size: 28rpx;
  color: $text-secondary;
}

.tree-selector-arrow {
  font-size: 24rpx;
  color: $text-secondary;
  transition: transform 0.3s ease;
}

// 植物列表容器
.content {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.plant-list-container {
  flex: 1;
  display: flex;
  justify-content: center;
  margin-top: 50rpx;
  margin-bottom: 20rpx;
  padding: 0 10rpx;
  overflow: hidden;
}

// 植物列表卡片容器
.rectangle1 {
  width: 95%;
  height: 100%;
  opacity: 1;
  background: $card-background;
  display: flex;
  justify-content: center;
  border-radius: 25rpx;
  color: $text-secondary;
  border: 0.8rpx solid rgba(0, 0, 0, 0.3);
  padding: 20rpx;
  box-sizing: border-box;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

// 植物网格布局
.plant-grid {
  align-content: flex-start;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: flex-start;
  overflow-y: auto;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20rpx;
  padding-bottom: 20rpx;
  -webkit-overflow-scrolling: touch; /* 提高iOS上的滚动体验 */
}

// 无结果提示样式
.no-results {
  width: 100%;
  height: 200rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  color: $text-secondary;
  font-size: 32rpx;
}

.no-results-hint {
  display: block;
  margin-top: 20rpx;
  font-size: 24rpx;
  color: $text-secondary;
}

.initial-hint {
  text-align: center;
  padding: 80rpx 50rpx;
  color: $text-secondary;
  font-size: 28rpx;
}

.loading-more {
  text-align: center;
  padding: 20rpx;
  color: $text-secondary;
  font-size: 26rpx;
}

// 自定义滚动条样式
.plant-grid::-webkit-scrollbar {
  width: 8rpx;
}

.plant-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4rpx;
}

.plant-grid::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4rpx;
}

// 植物卡片优化
.plant-card {
  width: 29.333%;
  max-height: 280rpx; /* 使用固定高度替代百分比高度 */
  opacity: 1;
  background: $plant-card-bg;
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  border-radius: 20rpx;
  padding: 15rpx;
  box-sizing: border-box;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.plant-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6rpx;
  background: linear-gradient(90deg, $accent-color, #81c784);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.plant-card:active {
  transform: translateY(4rpx) scale(0.98);
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.03);
}

.plant-card:active::before {
  opacity: 1;
}

// 植物图片容器
.plant-image-container {
  width: 100%;
  height: 60%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10rpx;
  overflow: hidden;
  border-radius: 15rpx;
  background-color: rgba(255, 255, 255, 0.5);
}

// 植物图片样式
.plant-image {
  width: 85%;
  height: 85%;
  object-fit: cover;
  border-radius: 10rpx;
  transition: transform 0.3s ease;
}

.plant-card:active .plant-image {
  transform: scale(1.05);
}

// 植物名称样式
.plant-name {
  width: 100%;
  text-align: center;
  font-size: 28rpx;
  font-weight: 500;
  color: $text-primary;
  margin-bottom: 5rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// 植物学名样式
.plant-scientific-name {
  width: 100%;
  text-align: center;
  font-size: 22rpx;
  color: $text-secondary;
  font-style: italic;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
