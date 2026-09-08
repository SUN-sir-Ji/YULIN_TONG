<template>
  <view class="auth yl-page">
    <view class="auth__deco">
      <view class="auth__orb auth__orb--1"></view>
      <view class="auth__orb auth__orb--2"></view>
    </view>

    <yl-navbar title="" transparent></yl-navbar>

    <view class="auth__body yl-container">
      <view class="auth__head yl-anim-up">
        <text class="auth__title">创建账号</text>
        <text class="auth__desc">使用邮箱验证码注册，用户 ID 将作为你的登录账号</text>
      </view>

      <view class="auth__card yl-anim-up yl-delay-1">
        <!-- 用户 ID -->
        <view class="field" :class="{ 'is-focus': focus === 'username', 'is-error': errors.username }">
          <view class="field__icon">
            <uni-icons type="person-filled" size="20" :color="focus === 'username' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            type="number"
            v-model="form.username"
            placeholder="用户 ID（4-20 位数字）"
            placeholder-class="field__placeholder"
            maxlength="20"
            @focus="focus = 'username'"
            @blur="onBlur('username')"
            @input="errors.username = ''"
          />
        </view>
        <text v-if="errors.username" class="field__error">{{ errors.username }}</text>

        <!-- 邮箱 -->
        <view class="field" :class="{ 'is-focus': focus === 'email', 'is-error': errors.email }">
          <view class="field__icon">
            <uni-icons type="email-filled" size="20" :color="focus === 'email' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            type="text"
            v-model="form.email"
            placeholder="邮箱地址"
            placeholder-class="field__placeholder"
            maxlength="100"
            @focus="focus = 'email'"
            @blur="onBlur('email')"
            @input="errors.email = ''"
          />
        </view>
        <text v-if="errors.email" class="field__error">{{ errors.email }}</text>

        <!-- 验证码 -->
        <view class="field" :class="{ 'is-focus': focus === 'captcha', 'is-error': errors.captcha }">
          <view class="field__icon">
            <uni-icons type="auth-filled" size="20" :color="focus === 'captcha' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            type="text"
            v-model="form.captcha"
            placeholder="邮箱验证码"
            placeholder-class="field__placeholder"
            maxlength="10"
            @focus="focus = 'captcha'"
            @blur="focus = ''"
            @input="errors.captcha = ''"
          />
          <view class="field__code" :class="{ 'is-disabled': countdown > 0 || sending }" hover-class="yl-press" @click="sendCode">
            <text>{{ sending ? '发送中…' : countdown > 0 ? `${countdown}s 后重发` : '获取验证码' }}</text>
          </view>
        </view>
        <text v-if="errors.captcha" class="field__error">{{ errors.captcha }}</text>

        <!-- 密码 -->
        <view class="field" :class="{ 'is-focus': focus === 'password', 'is-error': errors.password }">
          <view class="field__icon">
            <uni-icons type="locked-filled" size="20" :color="focus === 'password' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            :password="!showPwd"
            v-model="form.password"
            placeholder="设置密码（至少 6 位）"
            placeholder-class="field__placeholder"
            maxlength="64"
            @focus="focus = 'password'"
            @blur="onBlur('password')"
            @input="errors.password = ''"
          />
          <view class="field__clear" @click="showPwd = !showPwd">
            <uni-icons :type="showPwd ? 'eye-filled' : 'eye-slash-filled'" size="20" color="#9AA5A0"></uni-icons>
          </view>
        </view>
        <text v-if="errors.password" class="field__error">{{ errors.password }}</text>
        <view v-if="form.password" class="strength">
          <view class="strength__bars">
            <view class="strength__bar" :class="strengthClass(1)"></view>
            <view class="strength__bar" :class="strengthClass(2)"></view>
            <view class="strength__bar" :class="strengthClass(3)"></view>
          </view>
          <text class="strength__text">{{ strengthText }}</text>
        </view>

        <!-- 确认密码 -->
        <view class="field" :class="{ 'is-focus': focus === 'confirm', 'is-error': errors.confirm }">
          <view class="field__icon">
            <uni-icons type="checkbox-filled" size="20" :color="focus === 'confirm' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            :password="!showPwd"
            v-model="form.confirm"
            placeholder="再次输入密码"
            placeholder-class="field__placeholder"
            maxlength="64"
            @focus="focus = 'confirm'"
            @blur="onBlur('confirm')"
            @input="errors.confirm = ''"
          />
        </view>
        <text v-if="errors.confirm" class="field__error">{{ errors.confirm }}</text>

        <button class="yl-btn yl-btn--primary auth__submit" style="margin-top: 40rpx" :disabled="loading" hover-class="yl-press" @click="submit">
          <view v-if="loading" class="yl-spinner auth__spinner"></view>
          <text>{{ loading ? '注册中…' : '注 册' }}</text>
        </button>

        <view class="auth__hint">
          <uni-icons type="info-filled" size="14" color="#146C43"></uni-icons>
          <text>验证码将发送至你的邮箱，10 分钟内有效；用户 ID 注册后不可修改。</text>
        </view>
      </view>

      <view class="auth__foot yl-anim-up yl-delay-2">
        <text class="auth__foot-text">已有账号？</text>
        <text class="auth__foot-link" hover-class="yl-hover" @click="toLogin()">去登录</text>
      </view>
    </view>

    <!-- 注册成功弹窗 -->
    <view v-if="successShow" class="modal">
      <view class="modal__card">
        <view class="modal__icon">
          <uni-icons type="checkmarkempty" size="48" color="#1DA462"></uni-icons>
        </view>
        <text class="modal__title">注册成功</text>
        <text class="modal__desc">你的登录账号：{{ form.username }}</text>
        <button class="yl-btn yl-btn--primary modal__btn" hover-class="yl-press" @click="toLogin(true)">
          <text>立即登录</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script>
import { register, getCaptcha } from '@/utils/api.js'

const EMAIL_RE = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

export default {
  data() {
    return {
      form: { username: '', email: '', captcha: '', password: '', confirm: '' },
      errors: { username: '', email: '', captcha: '', password: '', confirm: '' },
      focus: '',
      showPwd: false,
      loading: false,
      sending: false,
      countdown: 0,
      timer: null,
      successShow: false
    }
  },
  computed: {
    strength() {
      const p = this.form.password || ''
      if (!p) return 0
      let s = 0
      if (p.length >= 6) s++
      if (/[A-Za-z]/.test(p) && /\d/.test(p)) s++
      if (p.length >= 10 && /[^A-Za-z0-9]/.test(p)) s++
      return Math.max(1, s)
    },
    strengthText() {
      return ['', '弱', '中', '强'][this.strength] || ''
    }
  },
  onUnload() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    strengthClass(level) {
      if (this.strength < level) return ''
      return this.strength === 1 ? 'is-weak' : this.strength === 2 ? 'is-mid' : 'is-strong'
    },
    onBlur(field) {
      this.focus = ''
      this.validateField(field)
    },
    validateField(field) {
      const f = this.form
      let msg = ''
      if (field === 'username') {
        const u = (f.username || '').trim()
        if (!u) msg = '请输入用户 ID'
        else if (!/^\d+$/.test(u)) msg = '用户 ID 必须为纯数字'
        else if (u.length < 4 || u.length > 20) msg = '用户 ID 长度需为 4-20 位'
      } else if (field === 'email') {
        if (!f.email) msg = '请输入邮箱地址'
        else if (!EMAIL_RE.test(f.email.trim())) msg = '邮箱格式不正确'
      } else if (field === 'captcha') {
        if (!f.captcha.trim()) msg = '请输入邮箱验证码'
      } else if (field === 'password') {
        if (!f.password) msg = '请设置密码'
        else if (f.password.length < 6) msg = '密码长度不能少于 6 位'
      } else if (field === 'confirm') {
        if (f.confirm !== f.password) msg = '两次输入的密码不一致'
      }
      this.errors[field] = msg
      return !msg
    },
    validateAll() {
      return ['username', 'email', 'captcha', 'password', 'confirm'].map((k) => this.validateField(k)).every(Boolean)
    },
    startCountdown() {
      this.countdown = 60
      this.timer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(this.timer)
          this.timer = null
        }
      }, 1000)
    },
    async sendCode() {
      if (this.sending || this.countdown > 0) return
      if (!this.validateField('email')) {
        uni.showToast({ title: this.errors.email, icon: 'none' })
        return
      }
      this.sending = true
      try {
        const res = await getCaptcha(this.form.email.trim())
        if (res && res.status === 200) {
          uni.showToast({ title: '验证码已发送，请查收邮箱', icon: 'none' })
          this.startCountdown()
        } else {
          uni.showToast({ title: (res && res.message) || '发送失败，请重试', icon: 'none' })
        }
      } catch (e) {
        const msg = (e && e.message) || '发送失败，请重试'
        if (e && e.statusCode === 400) this.errors.email = msg
        uni.showToast({ title: msg, icon: 'none', duration: 2200 })
      } finally {
        this.sending = false
      }
    },
    async submit() {
      if (this.loading) return
      if (!this.validateAll()) {
        const first = Object.keys(this.errors).find((k) => this.errors[k])
        if (first) uni.showToast({ title: this.errors[first], icon: 'none' })
        return
      }
      this.loading = true
      try {
        const res = await register({
          username: this.form.username.trim(),
          email: this.form.email.trim(),
          password: this.form.password,
          captcha: this.form.captcha.trim()
        })
        if (res && (res.status === 200 || res.status === 201)) {
          this.successShow = true
        } else {
          uni.showToast({ title: (res && res.message) || '注册失败，请重试', icon: 'none' })
        }
      } catch (e) {
        const msg = (e && e.message) || '注册失败，请重试'
        if (/用户名/.test(msg)) this.errors.username = msg
        else if (/邮箱/.test(msg)) this.errors.email = msg
        else if (/验证码/.test(msg)) this.errors.captcha = msg
        uni.showToast({ title: msg, icon: 'none', duration: 2500 })
      } finally {
        this.loading = false
      }
    },
    toLogin(withUsername) {
      const url = withUsername ? `/pages/login/login?username=${this.form.username.trim()}` : '/pages/login/login'
      uni.redirectTo({ url })
    }
  }
}
</script>

<style lang="scss" scoped>
@import './auth.scss';
</style>
