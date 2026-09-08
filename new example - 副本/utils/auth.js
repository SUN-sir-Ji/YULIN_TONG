/**
 * 登录状态管理（本地存储）
 */
const KEY_TOKEN = 'token'
const KEY_USER = 'userInfo'
const KEY_LOGGED = 'isLoggedIn'
const KEY_LOGIN_TIME = 'yl_login_time'

export function saveLogin(data) {
  if (!data) return
  uni.setStorageSync(KEY_USER, {
    userId: data.userId,
    username: data.username
  })
  if (data.token) uni.setStorageSync(KEY_TOKEN, data.token)
  uni.setStorageSync(KEY_LOGGED, true)
  uni.setStorageSync(KEY_LOGIN_TIME, Date.now())
}

export function getToken() {
  try {
    return uni.getStorageSync(KEY_TOKEN) || ''
  } catch (e) {
    return ''
  }
}

export function getUserInfo() {
  try {
    return uni.getStorageSync(KEY_USER) || null
  } catch (e) {
    return null
  }
}

export function isLoggedIn() {
  try {
    return !!getToken() && !!uni.getStorageSync(KEY_LOGGED)
  } catch (e) {
    return false
  }
}

export function getLoginTime() {
  try {
    return uni.getStorageSync(KEY_LOGIN_TIME) || 0
  } catch (e) {
    return 0
  }
}

export function logout() {
  uni.removeStorageSync(KEY_TOKEN)
  uni.removeStorageSync(KEY_USER)
  uni.removeStorageSync(KEY_LOGGED)
  uni.removeStorageSync(KEY_LOGIN_TIME)
}

/** 未登录则跳转到启动页 */
export function ensureLogin() {
  if (isLoggedIn()) return true
  uni.reLaunch({ url: '/pages/index/index' })
  return false
}
