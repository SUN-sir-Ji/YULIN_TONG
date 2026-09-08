/**
 * 统一 API 配置
 *
 * - baseUrl：后端服务地址。真机调试时请改为电脑的局域网 IP，
 *   也可以在「我的 → 服务器地址」中动态修改（保存在本地存储，优先级更高）。
 */
const DEFAULT_BASE_URL = 'http://localhost:8000'
const STORAGE_KEY = 'yl_base_url'

const API_CONFIG = {
  baseUrl: DEFAULT_BASE_URL,

  // 认证
  login: '/api/auth/login',
  register: '/api/auth/register',
  getCaptcha: '/api/auth/get-captcha',
  forgotCaptcha: '/api/auth/forgot-password/captcha',
  resetPassword: '/api/auth/reset-password',
  me: '/api/auth/me',

  // 植物
  uploadImage: '/api/upload/image',
  categories: '/api/plants/categories',
  plantsList: '/api/plants/list'
}

/** 获取当前生效的后端地址（本地覆盖 > 默认值） */
export function getBaseUrl() {
  try {
    const saved = uni.getStorageSync(STORAGE_KEY)
    if (saved && typeof saved === 'string') return saved
  } catch (e) {}
  return API_CONFIG.baseUrl
}

/** 设置后端地址；传空则恢复默认 */
export function setBaseUrl(url) {
  let value = (url || '').trim()
  if (value) {
    if (!/^https?:\/\//i.test(value)) value = 'http://' + value
    value = value.replace(/\/+$/, '')
    uni.setStorageSync(STORAGE_KEY, value)
  } else {
    uni.removeStorageSync(STORAGE_KEY)
  }
  return getBaseUrl()
}

export const DEFAULT_API_BASE_URL = DEFAULT_BASE_URL

export default API_CONFIG
