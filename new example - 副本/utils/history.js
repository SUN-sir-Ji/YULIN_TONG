/**
 * 识别记录（本地存储）
 */
const KEY = 'yl_history'
const MAX_RECORDS = 60

function pad(n) {
  return n < 10 ? '0' + n : '' + n
}

export function formatTime(ts) {
  const d = new Date(ts)
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

/** 相对时间：刚刚 / 5 分钟前 / 今天 14:20 / 昨天 09:10 / 03-12 18:00 */
export function relativeTime(ts) {
  const now = Date.now()
  const diff = now - ts
  if (diff < 60 * 1000) return '刚刚'
  if (diff < 60 * 60 * 1000) return `${Math.floor(diff / 60000)} 分钟前`

  const d = new Date(ts)
  const today = new Date()
  const sameDay = d.toDateString() === today.toDateString()
  const yesterday = new Date(today.getTime() - 86400000)
  const isYesterday = d.toDateString() === yesterday.toDateString()
  const hm = `${pad(d.getHours())}:${pad(d.getMinutes())}`

  if (sameDay) return `今天 ${hm}`
  if (isYesterday) return `昨天 ${hm}`
  if (d.getFullYear() === today.getFullYear()) return `${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${hm}`
  return formatTime(ts)
}

export function getRecords() {
  try {
    const list = uni.getStorageSync(KEY)
    return Array.isArray(list) ? list : []
  } catch (e) {
    return []
  }
}

function saveRecords(list) {
  uni.setStorageSync(KEY, list.slice(0, MAX_RECORDS))
}

/**
 * 新增一条记录
 * @param {Object} payload { image, results, filename }
 */
export function addRecord(payload) {
  const results = Array.isArray(payload.results) ? payload.results : []
  const best = results[0] || { class: '未识别', confidence: 0 }
  const record = {
    id: `r_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    image: payload.image || '',
    filename: payload.filename || '',
    results,
    best,
    time: Date.now()
  }
  const list = getRecords()
  list.unshift(record)
  saveRecords(list)
  return record
}

export function removeRecord(id) {
  const list = getRecords().filter((r) => r.id !== id)
  saveRecords(list)
  return list
}

export function clearRecords() {
  uni.removeStorageSync(KEY)
}

/** 统计：识别次数 / 识别到的物种数 */
export function getStats() {
  const list = getRecords()
  const species = new Set()
  list.forEach((r) => {
    if (r.best && r.best.class && r.best.confidence > 0) species.add(r.best.class)
  })
  return { count: list.length, species: species.size }
}

/** 置信度等级 */
export function confidenceLevel(c) {
  const v = Number(c) || 0
  if (v >= 0.8) return { text: '高', color: '#1DA462', bg: '#E3F6EA' }
  if (v >= 0.5) return { text: '中', color: '#F5A524', bg: '#FFF4DF' }
  return { text: '低', color: '#E5484D', bg: '#FDECEC' }
}

export function percent(c) {
  return Math.round((Number(c) || 0) * 100)
}

/**
 * App 端把临时图片保存到本地，避免缓存被清理后记录丢图。
 * 其他平台原样返回。
 */
export function persistImage(tempPath) {
  return new Promise((resolve) => {
    // #ifdef APP-PLUS
    uni.saveFile({
      tempFilePath: tempPath,
      success: (res) => resolve(res.savedFilePath || tempPath),
      fail: () => resolve(tempPath)
    })
    return
    // #endif
    // eslint-disable-next-line no-unreachable
    resolve(tempPath)
  })
}
