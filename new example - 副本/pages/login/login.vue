<template>
  <view class="auth yl-page">
    <view class="auth__deco">
      <view class="auth__orb auth__orb--1"></view>
      <view class="auth__orb auth__orb--2"></view>
    </view>

    <yl-navbar title="" transparent back-to="/pages/index/index"></yl-navbar>

    <view class="auth__body yl-container">
      <!-- 头部文案 -->
      <view class="auth__head yl-anim-up">
        <view class="auth__badge">
          <image class="auth__badge-logo" src="/static/logo.png" mode="aspectFit"></image>
        </view>
        <text class="auth__title">欢迎回来 👋</text>
        <text class="auth__desc">登录后可同步你的识别记录，继续探索雨林</text>
      </view>

      <!-- 表单 -->
      <view class="auth__card yl-anim-up yl-delay-1">
        <view class="field" :class="{ 'is-focus': focus === 'username', 'is-error': errors.username }">
          <view class="field__icon">
            <uni-icons type="person-filled" size="20" :color="focus === 'username' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            type="number"
            v-model="form.username"
            placeholder="用户 ID（数字）"
            placeholder-class="field__placeholder"
            maxlength="20"
            confirm-type="next"
            @focus="focus = 'username'"
            @blur="focus = ''"
            @input="errors.username = ''"
          />
          <view v-if="form.username" class="field__clear" @click="form.username = ''">
            <uni-icons type="clear" size="18" color="#C3CBC7"></uni-icons>
          </view>
        </view>
        <text v-if="errors.username" class="field__error">{{ errors.username }}</text>

        <view class="field" :class="{ 'is-focus': focus === 'password', 'is-error': errors.password }">
          <view class="field__icon">
            <uni-icons type="locked-filled" size="20" :color="focus === 'password' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            :password="!showPwd"
            v-model="form.password"
            placeholder="密码"
            placeholder-class="field__placeholder"
            maxlength="64"
            confirm-type="done"
            @focus="focus = 'password'"
            @blur="focus = ''"
            @input="errors.password = ''"
            @confirm="submit"
          />
          <view class="field__clear" @click="showPwd = !showPwd">
            <uni-icons :type="showPwd ? 'eye-filled' : 'eye-slash-filled'" size="20" color="#9AA5A0"></uni-icons>
          </view>
        </view>
        <text v-if="errors.password" class="field__error">{{ errors.password }}</text>

        <view class="auth__row">
          <view class="auth__remember" @click="remember = !remember">
            <view class="auth__check" :class="{ 'is-on': remember }">
              <uni-icons v-if="remember" type="checkmarkempty" size="12" color="#fff"></uni-icons>
            </view>
            <text>记住账号</text>
          </view>
          <text class="auth__link" hover-class="yl-hover" @click="go('/pages/login/findpassword')">忘记密码？</text>
        </view>

        <button class="yl-btn yl-btn--primary auth__submit" :disabled="loading" hover-class="yl-press" @click="submit">
          <view v-if="loading" class="yl-spinner auth__spinner"></view>
          <text>{{ loading ? '登录中…' : '登 录' }}</text>
        </button>
      </view>

      <view class="auth__foot yl-anim-up yl-delay-2">
        <text class="auth__foot-text">还没有账号？</text>
        <text class="auth__foot-link" hover-class="yl-hover" @click="go('/pages/login/register')">立即注册</text>
      </view>

      <view class="auth__guest yl-anim-up yl-delay-3" hover-class="yl-hover" @click="guest">
        <uni-icons type="navigate" size="14" color="#9AA5A0"></uni-icons>
        <text>暂不登录，先逛逛</text>
      </view>
    </view>
  </view>
</template>

<script>
import { login } from '@/utils/api.js'
import { saveLogin } from '@/utils/auth.js'

const KEY_REMEMBER = 'yl_remember_username'

export default {
  data() {
    return {
      form: { username: '', password: '' },
      errors: { username: '', password: '' },
      focus: '',
      showPwd: false,
      remember: true,
      loading: false
    }
  },
  onLoad(options) {
    const remembered = uni.getStorageSync(KEY_REMEMBER)
    if (remembered) this.form.username = String(remembered)
    if (options && options.username) this.form.username = String(options.username)
  },
  methods: {
    validate() {
      let ok = true
      const u = (this.form.username || '').trim()
      if (!u) {
        this.errors.username = '请输入用户 ID'
        ok = false
      } else if (!/^\d+$/.test(u)) {
        this.errors.username = '用户 ID 必须为纯数字'
        ok = false
      }
      if (!this.form.password) {
        this.errors.password = '请输入密码'
        ok = false
      } else if (this.form.password.length < 6) {
        this.errors.password = '密码长度不能少于 6 位'
        ok = false
      }
      return ok
    },
    async submit() {
      if (this.loading || !this.validate()) return
      this.loading = true
      try {
        const res = await login(this.form.username.trim(), this.form.password)
        if (res && res.code === 200 && res.data) {
          saveLogin(res.data)
          if (this.remember) uni.setStorageSync(KEY_REMEMBER, this.form.username.trim())
          else uni.removeStorageSync(KEY_REMEMBER)

          uni.showToast({ title: '登录成功', icon: 'success', duration: 1200 })
          setTimeout(() => {
            uni.reLaunch({ url: '/pages/main/main' })
          }, 600)
        } else {
          uni.showToast({ title: (res && res.message) || '登录失败，请重试', icon: 'none' })
        }
      } catch (e) {
        const msg = (e && e.message) || '登录失败，请重试'
        if (e && e.statusCode === 401) {
          if (/密码/.test(msg)) this.errors.password = msg
          else this.errors.username = msg
        }
        uni.showToast({ title: msg, icon: 'none', duration: 2200 })
      } finally {
        this.loading = false
      }
    },
    go(url) {
      uni.navigateTo({ url })
    },
    guest() {
      uni.reLaunch({ url: '/pages/main/main' })
    }
  }
}
</script>

<style lang="scss" scoped>
@import './auth.scss';
</style>
