// 统一API配置文件
const API_CONFIG = {
  // 修改为你的开发机实际IP地址
  baseUrl: 'http://localhost:8000', // 替换为你的IP
  // 各个API接口路径
  login: '/api/auth/login',
  uploadImage: '/api/upload/image',
  categories: '/api/plants/categories',
  plantsList: '/api/plants/list'
};

export default API_CONFIG;