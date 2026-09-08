import API_CONFIG from './apiConfig.js';

// 获取植物分类数据
export const getPlantCategories = async (parentId = 0) => {
  try {
    const url = `${API_CONFIG.baseUrl}/api/plants/categories?parent_id=${parentId}`;
    const response = await uni.request({
      url,
      method: 'GET'
    });
    
    if (response.statusCode === 200 && response.data.code === 200) {
      return response.data.data;
    } else {
      throw new Error(response.data?.message || '获取植物分类失败');
    }
  } catch (error) {
    console.error('获取植物分类数据错误:', error);
    throw error;
  }
};