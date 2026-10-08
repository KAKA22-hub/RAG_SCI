<template>
  <div class="login-page">
    <!-- 背景装饰层 -->
    <div class="bg-grid"></div>
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>

    <!-- 登录卡片 -->
    <div class="login-card">
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
        <h1 class="title">RAG 智能问答</h1>
        <p class="subtitle">Retrieval · Augmented · Generation</p>
        <div class="title-line"></div>
      </div>

      <!-- 模式切换用单选（纯 CSS 控制，不改 script） -->
      <input type="radio" name="login-mode" id="mode-captcha" class="mode-radio" checked>
      <input type="radio" name="login-mode" id="mode-password" class="mode-radio">

      <!-- 表单区 -->
      <form class="login-form" @submit.prevent>
        <!-- 模式切换 Tab -->
        <div class="mode-tabs">
          <span class="tab-slider"></span>
          <label for="mode-captcha" class="mode-tab">验证码登录</label>
          <label for="mode-password" class="mode-tab">密码登录</label>
        </div>

        <!-- ===== 验证码登录面板 ===== -->
        <div class="mode-panel panel-captcha">
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
                :disabled="isSend"
                v-model="email"
                placeholder="请输入邮箱地址"
                autocomplete="off"
              >
            </div>
          </div>

          <!-- 验证码 -->
          <div class="field">
            <label class="field-label">验证码</label>
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
                type="text"
                :disabled="!isSend"
                v-model="captcha"
                placeholder="请输入验证码"
                autocomplete="off"
              >
              <button
                type="button"
                class="send-btn"
                :disabled="isSend"
                @click="sendCaptcha"
              >
                {{ isSend ? '已发送' : '发送' }}
              </button>
            </div>
          </div>

          <!-- 登录按钮 -->
          <button
            type="button"
            class="login-btn"
            :disabled="!isSend"
            @click="login_by_captcha"
          >
            登 录
          </button>
        </div>

        <!-- ===== 密码登录面板 ===== -->
        <div class="mode-panel panel-password">
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
                autocomplete="current-password"
              >
            </div>
          </div>

          <!-- 登录按钮 -->
          <button
            type="button"
            class="login-btn"
            @click="login_by_password"
          >
            登 录
          </button>
        </div>
      </form>

      <p class="footer-tip">登录后即可进入知识库智能问答</p>
      <router-link to="/regist" class="register-btn">没有账号？立即注册</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from "vue";
import { ElMessage } from 'element-plus'

let proxy = getCurrentInstance().proxy
let isSend = ref(false);
let email = ref('');
let captcha = ref('');
let password = ref('');

function sendCaptcha(){
  isSend.value = !isSend.value
  proxy.$axios({
    url: 'users/sendCaptcha',
    method: 'get',
    params: {
      email: email.value,
    },
  }).then(res => {
    console.log(res);
    if (res.data.code === 200){
      ElMessage.success("验证码发送成功")
    }else{
      ElMessage.error(res.data.msg)
    }
  });
}

function login_by_captcha(){
  proxy.$axios({
    url: 'users/login',
    method: 'get',
    params: {
      email: email.value,
      captcha: captcha.value,
    },
  }).then(res => {
    console.log(res);
    if (res.data.code === 200){
      ElMessage.success("登陆成功")
      const userData = res.data.data;
      localStorage.setItem(
          "token",
          userData.token
      );
      // localStorage.setItem(
      //     "usersId",
      //     userData.user_id
      // );
      // localStorage.setItem(
      //     "nickname",
      //     userData.nickname
      // );
      setTimeout(() => {
        window.location.href = "/chat"
      }, 1000)
    }else{
      ElMessage.warning(res.data.msg)
    }
  });
}

function login_by_password(){
  proxy.$axios({
    url: 'users/login',
    method: 'post',
    params: {
      email: email.value,
      password: password.value,
    },
  }).then(res => {
    console.log(res);
    if (res.data.code === 200){
      ElMessage.success("登陆成功")
      const userData = res.data.data;
      localStorage.setItem(
          "token",
          userData.token
      );
      // localStorage.setItem(
      //     "usersId",
      //     userData.user_id
      // );
      // localStorage.setItem(
      //     "nickname",
      //     userData.nickname
      // );
      setTimeout(() => {
        window.location.href = "/chat"
      }, 1000)
    }else{
      ElMessage.warning(res.data.msg)
    }
  });
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
.login-page {
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

/* ============ 隐藏单选控制器 ============ */
.mode-radio {
  display: none;
}

/* ============ 登录卡片 ============ */
.login-card {
  position: relative;
  z-index: 2;
  width: 420px;
  max-width: 100%;
  padding: 40px 36px 30px;
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
}

.login-card::before {
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
  margin-bottom: 24px;
}

.logo {
  width: 52px; height: 52px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow:
    0 10px 26px rgba(37, 99, 235, .45),
    inset 0 1px 0 rgba(255, 255, 255, .30);
}

.title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 3px;
  background: linear-gradient(90deg, #eaf3ff, #6cb2ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #5c7699;
}

.title-line {
  width: 46px; height: 2px;
  margin: 16px auto 0;
  border-radius: 2px;
  background: linear-gradient(90deg, transparent, #38bdf8, transparent);
}

/* ============ 表单 ============ */
.login-form {
  display: block;
}

/* ============ 模式切换 Tab ============ */
.mode-tabs {
  position: relative;
  display: flex;
  padding: 4px;
  border-radius: 12px;
  background: rgba(8, 13, 24, 0.7);
  border: 1px solid rgba(90, 140, 200, 0.18);
  margin-bottom: 22px;
}

.tab-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  border-radius: 9px;
  background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 60%, #06b6d4 100%);
  box-shadow:
    0 6px 18px rgba(37, 99, 235, .42),
    inset 0 1px 0 rgba(255, 255, 255, .25);
  transition: transform .32s cubic-bezier(.4, 0, .2, 1);
  will-change: transform;
}

.mode-tab {
  position: relative;
  z-index: 1;
  flex: 1;
  text-align: center;
  padding: 10px 0;
  font-size: 13.5px;
  letter-spacing: 1px;
  color: #7d93b3;
  cursor: pointer;
  user-select: none;
  transition: color .25s;
}

.mode-tab:hover {
  color: #b8cee8;
}

/* 选中态：滑块位置 + 文字颜色 */
#mode-captcha:checked ~ .login-form .tab-slider {
  transform: translateX(0);
}
#mode-password:checked ~ .login-form .tab-slider {
  transform: translateX(100%);
}
#mode-captcha:checked ~ .login-form .mode-tab[for="mode-captcha"],
#mode-password:checked ~ .login-form .mode-tab[for="mode-password"] {
  color: #ffffff;
  font-weight: 600;
  text-shadow: 0 1px 6px rgba(0, 0, 0, .35);
}

/* ============ 面板切换 ============ */
.mode-panel {
  display: none;
  animation: panelIn .35s cubic-bezier(.22, .85, .3, 1) both;
}

@keyframes panelIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

#mode-captcha:checked ~ .login-form .panel-captcha {
  display: block;
}
#mode-password:checked ~ .login-form .panel-password {
  display: block;
}

/* ============ 字段 ============ */
.field {
  margin-bottom: 18px;
}

.field-label {
  display: block;
  margin-bottom: 8px;
  font-size: 12.5px;
  letter-spacing: 1px;
  color: #8ba6c9;
}

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

.input-wrap input {
  flex: 1;
  width: 100%;
  height: 48px;
  padding: 0 14px 0 42px;
  border: none;
  outline: none;
  background: transparent;
  color: #e8f1ff;
  font-size: 14px;
  letter-spacing: .4px;
}

.input-wrap input::placeholder {
  color: #4a6080;
}

.input-wrap input:disabled {
  color: #7d8ea6;
  cursor: not-allowed;
}

/* ============ 发送验证码按钮 ============ */
.send-btn {
  flex: none;
  height: 34px;
  margin-right: 7px;
  padding: 0 15px;
  border-radius: 9px;
  border: 1px solid rgba(59, 130, 246, .45);
  background: rgba(59, 130, 246, .12);
  color: #6cb2ff;
  font-size: 13px;
  letter-spacing: .5px;
  white-space: nowrap;
  cursor: pointer;
  transition: all .22s;
}

.send-btn:hover:not(:disabled) {
  background: rgba(59, 130, 246, .26);
  border-color: rgba(96, 165, 250, .8);
  color: #cfe6ff;
  box-shadow: 0 0 16px rgba(59, 130, 246, .35);
}

.send-btn:active:not(:disabled) {
  transform: scale(.97);
}

.send-btn:disabled {
  opacity: .45;
  cursor: not-allowed;
  border-color: rgba(120, 140, 170, .3);
  background: rgba(120, 140, 170, .1);
  color: #7d8ea6;
}

/* ============ 登录按钮 ============ */
.login-btn {
  width: 100%;
  height: 50px;
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

.login-btn::after {
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

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(37, 99, 235, .50);
  filter: brightness(1.06);
}

.login-btn:hover:not(:disabled)::after {
  left: 130%;
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 8px 18px rgba(37, 99, 235, .35);
}

.login-btn:disabled {
  background: rgba(120, 140, 170, .14);
  color: #64778f;
  box-shadow: none;
  cursor: not-allowed;
  letter-spacing: 6px;
}

/* ============ 底部提示 ============ */
.footer-tip {
  margin: 20px 0 0;
  text-align: center;
  font-size: 12px;
  letter-spacing: .5px;
  color: #4a6080;
}

/* ============ 注册按钮 ============ */
.register-btn {
  display: block;
  width: 100%;
  height: 44px;
  margin-top: 14px;
  line-height: 44px;
  text-align: center;
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, .45);
  background: rgba(59, 130, 246, .10);
  color: #6cb2ff;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1px;
  text-decoration: none;
  transition: all .22s;
}

.register-btn:hover {
  background: rgba(59, 130, 246, .22);
  border-color: rgba(96, 165, 250, .8);
  color: #cfe6ff;
  box-shadow: 0 0 18px rgba(59, 130, 246, .30);
}

.register-btn:active {
  transform: scale(.98);
}

/* ============ 响应式 ============ */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px 22px;
    border-radius: 16px;
  }

  .title {
    font-size: 19px;
    letter-spacing: 2px;
  }

  .send-btn {
    padding: 0 12px;
  }
}

@media (max-height: 680px) {
  .login-card {
    padding: 26px 32px 22px;
  }
  .brand { margin-bottom: 18px; }
  .logo  { width: 44px; height: 44px; margin-bottom: 12px; }
  .title { font-size: 19px; }
  .mode-tabs { margin-bottom: 16px; }
  .field { margin-bottom: 14px; }
  .input-wrap input { height: 44px; }
  .login-btn { height: 46px; }
  .footer-tip { margin-top: 14px; }
  .register-btn { height: 40px; line-height: 40px; margin-top: 10px; }
}
</style>