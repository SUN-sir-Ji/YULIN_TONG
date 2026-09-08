<template>
  <view class="auth yl-page">
    <view class="auth__deco">
      <view class="auth__orb auth__orb--1"></view>
      <view class="auth__orb auth__orb--2"></view>
    </view>

    <yl-navbar title="" transparent></yl-navbar>

    <view class="auth__body yl-container">
      <view class="auth__head yl-anim-up">
        <view class="auth__badge">
          <uni-icons type="locked-filled" size="44" color="#1DA462"></uni-icons>
        </view>
        <text class="auth__title">找回密码</text>
        <text class="auth__desc">输入注册时使用的邮箱，我们会发送验证码帮助你找回密码</text>
      </view>

      <view class="auth__card yl-anim-up yl-delay-1">
        <view class="field" :class="{ 'is-focus': focus === 'email', 'is-error': errors.email }">
          <view class="field__icon">
            <uni-icons type="email-filled" size="20" :color="focus === 'email' ? '#1DA462' : '#9AA5A0'"></uni-icons>
          </view>
          <input
            class="field__input"
            type="text"
            v-model="form.email"
            placeholder="注册邮箱"
            placeholder-class="field__placeholder"
            maxlength="100"
            @focus="focus = 'email'"
            @blur="focus = ''"
            @input="errors.email = ''"
          />
        </view>
        <text v-if="errors.email" class="field__error">{{ errors.email }}</text>

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
            @confirm="submit"
          />
          <view class="field__code" :class="{ 'is-disabled': countdown > 0 || sending }" hover-class="yl-press" @click="sendCode">
            <text>{{ sending ? '发送中…' : countdown > 0 ? `${countdown}s 后重发` : '获取验证码' }}</text>
          </view>
        </view>
        <text v-if="errors.captcha" class="field__error">{{ errors.captcha }}</text>

        <button class="yl-btn yl-btn--primary auth__submit" style="margin-top: 40rpx" :disabled="loading" hover-class="yl-press" @click="submit">
          <view v-if="loading" class="yl-spinner auth__spinner"></view>
          <text>{{ loading ? '验证中…' : '确认找回' }}</text>
        </button>

        <view class="auth__hint">
          <uni-icons type="info-filled" size="14" color="#146C43"></uni-icons>
          <text>验证通过后将直接显示你的密码，请妥善保管，不要泄露给他人。</text>
        </view>
      </view>

      <view class="auth__foot yl-anim-up yl-delay-2">
        <text class="auth__foot-text">想起密码了？</text>
        <text class="auth__foot-link" hover-class="yl-hover" @click="toLogin">返回登录</text>
      </view>
    </view>

    <!-- 密码结果弹窗 -->
    <view v-if="resultShow" class="modal">
      <view class="modal__card">
        <view class="modal__icon">
          <uni-icons type="checkmarkempty" size="48" color="#1DA462"></uni-icons>
        </view>
        <text class="modal__title">验证成功</text>
        <text class="modal__desc">这是与邮箱 {{ form.email }} 关联的密码</text>

        <view class="modal__pwd">
          <text class="modal__pwd-text">{{ reveal ? password : masked }}</text>
          <view class="modal__pwd-actions">
            <uni-icons :type="reveal ? 'eye-filled' : 'eye-slash-filled'" size="22" color="#5B6660" @click="reveal = !reveal"></uni-icons>
            <uni-icons type="paperclip" size="22" color="#1DA462" @click="copy"></uni-icons>
          </view>
        </view>

        <button class="yl-btn yl-btn--primary modal__btn" hover-class="yl-press" @click="toLogin">
          <text>去登录</text>
        </button>
        <text class="modal__cancel" @click="resultShow = false">关闭</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getForgotCaptcha, resetPassword } from '@/utils/api.js'

const EMAIL_RE = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

export default {
  data() {
    return {
      form: { email: '', captcha: '' },
      errors: { email: '', captcha: '' },
      focus: '',
      loading: false,
      sending: false,
      countdown: 0,
      timer: null,
      resultShow: false,
      password: '',
      reveal: false
    }
  },
  computed: {
    masked() {
      return '•'.repeat(Math.max(6, (this.password || '').length))
    }
  },
  onUnload() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    validateEmail() {
      const v = (this.form.email || '').trim()
      if (!v) this.errors.email = '请输入注册邮箱'
      else if (!EMAIL_RE.test(v)) this.errors.email = '邮箱格式不正确'
      else this.errors.email = ''
      return !this.errors.email
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
      if (!this.validateEmail()) {
        uni.showToast({ title: this.errors.email, icon: 'none' })
        return
      }
      this.sending = true
      try {
        const res = await getForgotCaptcha(this.form.email.trim())
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
      if (!this.validateEmail()) {
        uni.showToast({ title: this.errors.email, icon: 'none' })
        return
      }
      if (!this.form.captcha.trim()) {
        this.errors.captcha = '请输入邮箱验证码'
        uni.showToast({ title: this.errors.captcha, icon: 'none' })
        return
      }
      this.loading = true
      try {
        const res = await resetPassword(this.form.email.trim(), this.form.captcha.trim())
        if (res && res.success) {
          this.password = res.password || ''
          this.reveal = false
          this.resultShow = true
        } else {
          uni.showToast({ title: (res && res.message) || '验证码错误或已过期', icon: 'none' })
        }
      } catch (e) {
        const msg = (e && e.message) || '验证失败，请重试'
        if (/验证码/.test(msg)) this.errors.captcha = msg
        uni.showToast({ title: msg, icon: 'none', duration: 2200 })
      } finally {
        this.loading = false
      }
    },
    copy() {
      uni.setClipboardData({
        data: this.password,
        success: () => uni.showToast({ title: '密码已复制', icon: 'none' })
      })
    },
    toLogin() {
      uni.redirectTo({ url: '/pages/login/login' })
    }
  }
}
</script>

<style lang="scss" scoped>
@import './auth.scss';
</style>
