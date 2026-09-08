/**
 * 网络请求封装（基于 uni.request / uni.uploadFile）
 *
 * 统一：拼接 baseUrl、携带 token、解析 FastAPI 的错误信息（detail / message）。
 * 所有方法均返回 Promise：
 *   - resolve：响应体（已解析的 JSON）
 *   - reject ：{ statusCode, message, data }
 */
import { getBaseUrl } from './apiConfig.js'

const TOKEN_KEY = 'token'

function buildUrl(path) {
  if (/^https?:\/\//i.test(path)) return path
  return getBaseUrl() + path
}

function authHeader() {
  try {
    const token = uni.getStorageSync(TOKEN_KEY)
    if (token) return { Authorization: `Bearer ${token}` }
  } catch (e) {}
  return {}
}

/** 从 FastAPI 返回体中提取可读错误信息 */
export function pickMessage(data, fallback) {
  if (!data) return fallback
  if (typeof data === 'string') return data || fallback
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail) && data.detail.length) {
    // pydantic 校验错误
    const first = data.detail[0]
    const field = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : ''
    return field ? `${field}：${first.msg}` : first.msg || fallback
  }
  return data.message || data.error || fallback
}

function fail(statusCode, message, data) {
  return { statusCode, message, data }
}

export function request(options) {
  const {
    url,
    method = 'GET',
    data = {},
    header = {},
    auth = true,
    timeout = 20000
  } = options

  return new Promise((resolve, reject) => {
    uni.request({
      url: buildUrl(url),
      method,
      data,
      timeout,
      header: {
        'content-type': 'application/json',
        ...(auth ? authHeader() : {}),
        ...header
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(fail(res.statusCode, pickMessage(res.data, `请求失败（${res.statusCode}）`), res.data))
        }
      },
      fail: (err) => {
        console.error('[request] 网络错误', url, err)
        reject(fail(0, '网络连接失败，请检查网络或服务器地址', err))
      }
    })
  })
}

export function upload(options) {
  const { url, filePath, name = 'file', formData = {}, auth = true, onProgress } = options

  return new Promise((resolve, reject) => {
    const task = uni.uploadFile({
      url: buildUrl(url),
      filePath,
      name,
      formData,
      header: auth ? authHeader() : {},
      success: (res) => {
        let body = res.data
        try {
          body = JSON.parse(res.data)
        } catch (e) {}
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(body)
        } else {
          reject(fail(res.statusCode, pickMessage(body, `上传失败（${res.statusCode}）`), body))
        }
      },
      fail: (err) => {
        console.error('[upload] 上传失败', url, err)
        reject(fail(0, '上传失败，请检查网络或服务器地址', err))
      }
    })

    if (task && typeof onProgress === 'function' && task.onProgressUpdate) {
      task.onProgressUpdate((e) => onProgress(e.progress || 0))
    }
  })
}

export default request
