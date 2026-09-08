/**
 * 后端接口封装（FastAPI）
 * 后端接口保持不变，这里只做前端侧的统一调用。
 */
import API_CONFIG from './apiConfig.js'
import { request, upload } from './request.js'

/* ============================ 认证 ============================ */

/** 登录：username 为数字 user_id */
export const login = (username, password) =>
  request({
    url: API_CONFIG.login,
    method: 'POST',
    data: { username, password },
    auth: false
  })

/** 注册 */
export const register = ({ username, email, password, captcha }) =>
  request({
    url: API_CONFIG.register,
    method: 'POST',
    data: { username, email, password, captcha },
    auth: false
  })

/** 发送注册验证码 */
export const getCaptcha = (email) =>
  request({
    url: API_CONFIG.getCaptcha,
    method: 'POST',
    data: { email },
    auth: false
  })

/** 发送找回密码验证码 */
export const getForgotCaptcha = (email) =>
  request({
    url: API_CONFIG.forgotCaptcha,
    method: 'POST',
    data: { email },
    auth: false
  })

/** 验证码找回密码 */
export const resetPassword = (email, captcha) =>
  request({
    url: API_CONFIG.resetPassword,
    method: 'POST',
    data: { email, captcha },
    auth: false
  })

/** 当前用户信息 */
export const getMe = () => request({ url: API_CONFIG.me })

/* ============================ 植物 ============================ */

/** 植物分类（parent_id = 0 为顶级「门」） */
export const getPlantCategories = async (parentId = 0) => {
  const res = await request({
    url: API_CONFIG.categories,
    method: 'GET',
    data: { parent_id: parentId }
  })
  if (res && res.code === 200) return res.data || []
  throw new Error((res && res.message) || '获取植物分类失败')
}

/**
 * 植物列表
 * @param {Object} params
 * @param {String} params.field  过滤字段：phylum_latin_name / class_latin_name / order_latin_name / family_latin_name / genus_latin_name
 * @param {String} params.value  拉丁名
 * @param {Number} params.page
 * @param {Number} params.pageSize
 * @returns {{ list: Array, total: Number }}
 */
export const getPlants = async ({ field, value, page = 1, pageSize = 20 } = {}) => {
  const data = { page, pageSize }
  if (field && value) data[field] = value

  const res = await request({ url: API_CONFIG.plantsList, method: 'GET', data })
  if (res && res.code === 200) {
    const d = res.data || {}
    if (Array.isArray(d)) return { list: d, total: d.length }
    return { list: d.list || [], total: typeof d.total === 'number' ? d.total : (d.list || []).length }
  }
  throw new Error((res && res.message) || '获取植物列表失败')
}

/** 上传单张图片并识别 */
export const uploadImage = (filePath, onProgress) =>
  upload({ url: API_CONFIG.uploadImage, filePath, name: 'file', onProgress })

export default {
  login,
  register,
  getCaptcha,
  getForgotCaptcha,
  resetPassword,
  getMe,
  getPlantCategories,
  getPlants,
  uploadImage
}
