<template>
  <div class="register-page">
    <!-- 背景装饰层 -->
    <div class="bg-grid"></div>
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>

    <!-- 注册卡片 -->
    <div class="register-card">
      <!-- 品牌区 -->
      <div class="brand">
        <div class="logo">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none"
               stroke="currentColor" stroke-width="1.8"
               stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3 3 7.5v9L12 21l9-4.5v-9L12 3Z" />
            <path d="M12 12v9" />
            <path d="M3 7.5 12 12l9-4.5" />
          </svg>
        </div>
        <h1 class="title">创建账号</h1>
        <p class="subtitle">Join · RAG · Intelligence</p>
        <div class="title-line"></div>
      </div>

      <!-- 表单区 -->
      <form class="register-form" @submit.prevent>
        <!-- 昵称 -->
        <div class="field">
          <label class="field-label">昵称</label>
          <div class="input-wrap">
            <span class="icon">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none"
                   stroke="currentColor" stroke-width="1.8"
                   stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21c0-4 3.6-7 8-7s8 3 8 7" />
              </svg>
            </span>
            <input
              type="text"
              v-model="nickname"
              placeholder="请输入昵称"
              autocomplete="off"
            >
          </div>
        </div>

        <!-- 邮箱 -->
        <div class="field">
          <label class="field-label">邮箱号</label>
          <div class="input-wrap">
            <span class="icon">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none"
                   stroke="currentColor" stroke-width="1.8"
                   stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="4" width="20" height="16" rx="3" />
                <path d="m3 7 9 6 9-6" />
              </svg>
            </span>
            <input
              type="text"
              v-model="email"
              placeholder="请输入邮箱地址"
              autocomplete="off"
            >
          </div>
        </div>

        <!-- 密码 -->
        <div class="field">
          <label class="field-label">密码</label>
          <div class="input-wrap">
            <span class="icon">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none"
                   stroke="currentColor" stroke-width="1.8"
                   stroke-linecap="round" stroke-linejoin="round">
                <rect x="4" y="10" width="16" height="11" rx="2.5" />
                <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                <circle cx="12" cy="15.5" r="1.4" />
              </svg>
            </span>
            <input
              type="password"
              v-model="password"
              placeholder="请输入密码"
              autocomplete="new-password"
            >
          </div>
        </div>

        <!-- 邮箱授权码（可选） -->
        <div class="field">
          <label class="field-label">
            邮箱授权码
            <span class="optional-tag">选填</span>
          </label>
          <div class="input-wrap">
            <span class="icon">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none"
                   stroke="currentColor" stroke-width="1.8"
                   stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3 4 6v6c0 5 3.4 7.8 8 9 4.6-1.2 8-4 8-9V6l-8-3Z" />
                <path d="m9 12 2 2 4-4" />
              </svg>
            </span>
            <input
              type="password"
              v-model="email_password"
              placeholder="请输入邮箱授权码"
              autocomplete="off"
            >
          </div>
          <p class="field-hint">用于接收验证码与通知邮件，不填写将影响部分功能</p>
        </div>

        <!-- 注册按钮 -->
        <button
          type="button"
          class="register-btn"
          @click="regist"
        >
          注 册
        </button>
      </form>

      <p class="footer-tip">已有账号？<router-link to="/login" class="link">返回登录</router-link></p>
    </div>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted} from "vue";
import { useRouter } from "vue-router";
import {ElMessage} from 'element-plus'

let proxy = getCurrentInstance().proxy
let email = ref('');
let password = ref('');
let nickname = ref('');
let email_password = ref('');
let router = new useRouter();

function regist(){
  if (!email.value.trim() || !nickname.value.trim() || !password.value.trim()) {
    ElMessage.warning('请填写注册信息')
    return
  }
  if (!email_password.value.trim()){
    ElMessage.warning('若不填写邮箱授权码则部分功能受损')
  }
  proxy.$axios({
    url: 'users/regist',
    method: 'post',
    data: {
      email: email.value,
      nickname: nickname.value,
      password: password.value,
      roles_id: 0,
      email_password: email_password.value,
    },
  }).then(res => {
    console.log(res);
    if (res.data.code === 200){
      ElMessage.success("注册成功")
      router.push('/');
    }else{
      ElMessage.error(res.data.msg)
    }
  })
}
</script>

<style scoped>
/* ============ 强制铺满视口，干掉所有默认限制 ============ */
:global(html),
:global(body),
:global(#app) {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  max-width: none !important;
  min-width: 100vw;
  overflow: hidden;
}

:global(*) {
  box-sizing: border-box;
}

/* ============ 页面容器 ============ */
.register-page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  overflow: hidden;
  background:
    radial-gradient(circle at 18% 18%, #10294a 0%, transparent 55%),
    radial-gradient(circle at 82% 82%, #0a2540 0%, transparent 55%),
    linear-gradient(160deg, #070c16 0%, #04070d 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
    "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* ============ 科技网格背景 ============ */
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(80, 160, 255, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(80, 160, 255, 0.07) 1px, transparent 1px);
  background-size: 48px 48px;
  -webkit-mask-image: radial-gradient(circle at 50% 45%, #000 0%, transparent 72%);
  mask-image: radial-gradient(circle at 50% 45%, #000 0%, transparent 72%);
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  from { background-position: 0 0, 0 0; }
  to   { background-position: 48px 48px, 48px 48px; }
}

/* ============ 光晕 ============ */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: .45;
  pointer-events: none;
}

.glow-1 {
  width: 420px; height: 420px;
  top: -140px; left: -100px;
  background: #1b6bff;
  animation: floatA 14s ease-in-out infinite;
}

.glow-2 {
  width: 380px; height: 380px;
  bottom: -140px; right: -80px;
  background: #00d4ff;
  animation: floatB 16s ease-in-out infinite;
}

.glow-3 {
  width: 260px; height: 260px;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: #7c3aed;
  opacity: .22;
  animation: pulse 8s ease-in-out infinite;
}

@keyframes floatA {
  0%, 100% { transform: translate3d(0, 0, 0); }
  50%      { transform: translate3d(40px, 30px, 0); }
}

@keyframes floatB {
  0%, 100% { transform: translate3d(0, 0, 0); }
  50%      { transform: translate3d(-40px, -30px, 0); }
}

@keyframes pulse {
  0%, 100% { opacity: .18; transform: translate(-50%, -50%) scale(1); }
  50%      { opacity: .30; transform: translate(-50%, -50%) scale(1.15); }
}

/* ============ 注册卡片 ============ */
.register-card {
  position: relative;
  z-index: 2;
  width: 420px;
  max-width: 100%;
  max-height: calc(100vh - 40px);
  padding: 34px 36px 26px;
  border-radius: 20px;
  background: rgba(13, 20, 35, 0.72);
  border: 1px solid rgba(90, 160, 255, 0.20);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow:
    0 30px 70px rgba(0, 0, 0, .60),
    0 0 60px rgba(37, 99, 235, .10),
    inset 0 1px 0 rgba(255, 255, 255, .05);
  animation: cardIn .65s cubic-bezier(.22, .85, .3, 1) both;
  overflow: hidden;
}

/* 顶部高光描边 */
.register-card::before {
  content: "";
  position: absolute;
  top: 0; left: 12%;
  width: 76%; height: 1px;
  background: linear-gradient(90deg, transparent, #4d9bff, #22d3ee, transparent);
  opacity: .9;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(24px) scale(.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ============ 品牌区 ============ */
.brand {
  text-align: center;
  margin-bottom: 22px;
}

.logo {
  width: 48px; height: 48px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow:
    0 10px 26px rgba(37, 99, 235, .45),
    inset 0 1px 0 rgba(255, 255, 255, .30);
}

.title {
  margin: 0;
  font-size: 21px;
  font-weight: 600;
  letter-spacing: 3px;
  background: linear-gradient(90deg, #eaf3ff, #6cb2ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.subtitle {
  margin: 6px 0 0;
  font-size: 10.5px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #5c7699;
}

.title-line {
  width: 44px; height: 2px;
  margin: 13px auto 0;
  border-radius: 2px;
  background: linear-gradient(90deg, transparent, #38bdf8, transparent);
}

/* ============ 表单 ============ */
.register-form {
  display: block;
}

.field {
  margin-bottom: 13px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 12px;
  letter-spacing: 1px;
  color: #8ba6c9;
}

/* 选填标记 */
.optional-tag {
  display: inline-block;
  padding: 1px 7px;
  font-size: 10px;
  letter-spacing: .5px;
  border-radius: 5px;
  border: 1px solid rgba(59, 130, 246, .45);
  background: rgba(59, 130, 246, .10);
  color: #6cb2ff;
}

/* 字段下方提示 */
.field-hint {
  margin: 6px 2px 0;
  font-size: 11px;
  letter-spacing: .3px;
  color: #465d7d;
  line-height: 1.5;
}

/* 输入框外壳 */
.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  border-radius: 12px;
  background: rgba(8, 13, 24, 0.78);
  border: 1px solid rgba(90, 140, 200, 0.22);
  transition: border-color .25s, box-shadow .25s, background .25s;
}

.input-wrap:hover {
  border-color: rgba(90, 160, 255, 0.38);
}

.input-wrap:focus-within {
  border-color: #3b82f6;
  background: rgba(9, 16, 30, 0.95);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, .16),
              0 0 22px rgba(37, 99, 235, .18);
}

/* 图标 */
.input-wrap .icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  color: #4d6f9b;
  transition: color .25s;
  pointer-events: none;
}

.input-wrap:focus-within .icon {
  color: #60a5fa;
}

/* 输入框本体 */
.input-wrap input {
  flex: 1;
  width: 100%;
  height: 44px;
  padding: 0 14px 0 42px;
  border: none;
  outline: none;
  background: transparent;
  color: #e8f1ff;
  font-size: 13.5px;
  letter-spacing: .4px;
}

.input-wrap input::placeholder {
  color: #4a6080;
}

/* ============ 注册按钮 ============ */
.register-btn {
  width: 100%;
  height: 48px;
  margin-top: 10px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 55%, #06b6d4 100%);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 6px;
  text-indent: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform .22s, box-shadow .22s, filter .22s;
  box-shadow: 0 12px 28px rgba(37, 99, 235, .38);
}

/* 流光效果 */
.register-btn::after {
  content: "";
  position: absolute;
  top: 0; left: -120%;
  width: 60%; height: 100%;
  background: linear-gradient(
    100deg,
    transparent,
    rgba(255, 255, 255, .42),
    transparent
  );
  transition: left .6s ease;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(37, 99, 235, .50);
  filter: brightness(1.06);
}

.register-btn:hover::after {
  left: 130%;
}

.register-btn:active {
  transform: translateY(0);
  box-shadow: 0 8px 18px rgba(37, 99, 235, .35);
}

/* ============ 底部提示 ============ */
.footer-tip {
  margin: 16px 0 0;
  text-align: center;
  font-size: 12px;
  letter-spacing: .5px;
  color: #4a6080;
}

.link {
  color: #6cb2ff;
  text-decoration: none;
  transition: color .2s, text-shadow .2s;
}

.link:hover {
  color: #a9d4ff;
  text-shadow: 0 0 12px rgba(96, 165, 250, .6);
}

/* ============ 响应式 ============ */
@media (max-width: 480px) {
  .register-card {
    padding: 28px 22px 22px;
    border-radius: 16px;
  }

  .title {
    font-size: 19px;
    letter-spacing: 2px;
  }
}

/* 矮屏收紧 */
@media (max-height: 720px) {
  .register-card {
    padding: 22px 32px 18px;
  }
  .brand { margin-bottom: 14px; }
  .logo  { width: 42px; height: 42px; margin-bottom: 10px; }
  .title { font-size: 19px; }
  .subtitle { margin-top: 4px; font-size: 10px; }
  .title-line { margin-top: 10px; }
  .field { margin-bottom: 10px; }
  .field-hint { display: none; } /* 矮屏隐藏提示，避免出现滚动条 */
  .input-wrap input { height: 40px; }
  .register-btn { height: 44px; margin-top: 8px; }
  .footer-tip { margin-top: 12px; }
}
</style>