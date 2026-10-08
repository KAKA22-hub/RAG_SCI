<template>
  <div class="chat-page">
    <!-- 背景装饰 -->
    <div class="bg-grid"></div>
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>

    <!-- ============ 侧边栏 ============ -->
    <aside class="sidebar">
      <!-- 品牌 -->
      <div class="sidebar-head">
        <div class="logo">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none"
               stroke="currentColor" stroke-width="1.8"
               stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3 3 7.5v9L12 21l9-4.5v-9L12 3Z" />
            <path d="M12 12v9" />
            <path d="M3 7.5 12 12l9-4.5" />
          </svg>
        </div>
        <span class="brand-name">SCI · RAG</span>
      </div>

      <!-- 新建对话 -->
      <button class="new-chat" @click="createNewChat">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none"
             stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14M5 12h14" />
        </svg>
        <span>新建对话</span>
      </button>

      <!-- 历史记录 -->
      <div class="history">
        <p class="history-title">历史记录</p>
        <div class="history-list">
          <div
            v-for="h in historyList"
            :key="h.historyId"
            class="history-item"
            :class="{ active: currentHistoryId === h.historyId }"
            @click="selectHistory(h.historyId)"
          >
            <span class="history-dot"></span>
            <span class="history-text">{{ h.question }}</span>
            <button class="history-del" @click.stop="deleteHistory(h.historyId)">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none"
                   stroke="currentColor" stroke-width="2"
                   stroke-linecap="round">
                <path d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>
          <p v-if="historyList.length === 0" class="history-empty">暂无历史记录</p>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="user-area">
        <div class="user-row">
          <div class="user-avatar">{{ nickname.charAt(0).toUpperCase() }}</div>
          <span class="user-name">{{ nickname }}</span>
        </div>
        <div class="user-btns">
          <button @click="handleUserCommand('profile')">个人中心</button>
          <button @click="handleUserCommand('settings')">设置</button>
          <button class="logout" @click="logout">退出</button>
        </div>
      </div>
    </aside>

    <!-- ============ 主区域 ============ -->
    <main class="main">
      <!-- 顶部标题栏 -->
      <header class="chat-head">
        <div class="head-left">
          <h2 class="head-title">{{ currentTitle }}</h2>
        </div>
        <div class="head-right">
          <span class="status-dot"></span>
          <span class="status-text">RAG 引擎在线</span>
        </div>
      </header>

      <!-- 消息区 -->
      <div class="messages" ref="messageBox">
        <!-- 欢迎屏 -->
        <div v-if="messages.length === 0" class="welcome">
          <div class="welcome-logo">
            <svg viewBox="0 0 24 24" width="32" height="32" fill="none"
                 stroke="currentColor" stroke-width="1.5"
                 stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 3 3 7.5v9L12 21l9-4.5v-9L12 3Z" />
              <path d="M12 12v9" />
              <path d="M3 7.5 12 12l9-4.5" />
            </svg>
          </div>
          <h1 class="welcome-title">SCI 期刊智能问答</h1>
          <p class="welcome-sub">Retrieval · Augmented · Generation</p>
          <div class="suggestions">
            <button
              v-for="(q, i) in suggestQuestions"
              :key="i"
              class="suggestion"
              @click="quickAsk(q)"
            >
              <span class="sug-dot">✦</span>
              <span class="sug-text">{{ q }}</span>
            </button>
          </div>
        </div>

        <!-- 消息列表 -->
        <template v-else>
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="msg"
            :class="msg.role === 'user' ? 'msg-user' : 'msg-ai'"
          >
            <div class="msg-avatar">
              <template v-if="msg.role === 'user'">
                {{ nickname.charAt(0).toUpperCase() }}
              </template>
              <template v-else>AI</template>
            </div>
            <div
              class="msg-bubble"
              :class="{ 'md-body': msg.role !== 'user' }"
              v-html="renderMarkdown(msg.content)"
            ></div>
          </div>
        </template>
      </div>

      <!-- 输入区 -->
      <footer class="input-area">
        <div class="input-wrap">
          <input
            v-model="question"
            @keyup.enter="hendleEnter"
            placeholder="输入关于 SCI 期刊的问题..."
            autocomplete="off"
          >
          <button
            class="send-btn"
            :disabled="isButtonDisabled || isLoading"
            @click="chat"
          >
            <svg v-if="!isLoading" viewBox="0 0 24 24" width="16" height="16"
                 fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 2 11 13" />
              <path d="M22 2l-7 20-4-9-9-4 20-7Z" />
            </svg>
            <span>{{ isLoading ? '思考中' : '发送' }}</span>
          </button>
        </div>
        <p class="input-tip">内容由 AI 生成，请自行甄别</p>
      </footer>
    </main>
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted, watch, computed, nextTick} from "vue";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";
import { marked } from 'marked';
import DOMPurify from 'dompurify';

marked.setOptions({
  breaks: true,
  gfm: true,
  pedantic: false
})
function renderMarkdown(text) {
  if (!text) return ''
  return DOMPurify.sanitize(marked.parse(text))
}

let proxy = getCurrentInstance().proxy
let question = ref("");
let isButtonDisabled = ref(true);
let isLoading = ref(false);
let globalHistoryId = ref(0);
const payload = JSON.parse(atob(localStorage.getItem('token').split('.')[1]))

watch(question,(newQuestion) => {
  console.log(newQuestion)
  isButtonDisabled.value = !(newQuestion.length > 0 && newQuestion.trim());
});

let messages = ref([]);

function chat(){
  isLoading.value = true;
  let myQuestion = question.value.trim();
  question.value = "";
  messages.value.push({role:'user',content:myQuestion});
  messages.value.push({role:'system',content:'正在努力思考中......'});

  let params = new URLSearchParams({question:myQuestion,historyId:globalHistoryId.value,token: localStorage.getItem('token')});
  let sse = new EventSource("http://localhost:8000/chat/sci?" + params);
  let s = ""
  sse.onmessage = (event) => {
    let content = JSON.parse(event.data).content;
    console.log(event)
    if (content === '[DONE]'){
      sse.close();
      console.log('SSE连接关闭');
      isLoading.value = false;
      saveChatResult(myQuestion, s);
      return;
    }
    s += content;
    messages.value[messages.value.length - 1].content = s;
  };
  sse.onerror = (event) => {
    console.log("SSE请求错误：",event);
    isLoading.value = false;
    sse.close();
  };
  sse.onopen = (event) => {
    console.log("建立SSE连接")
  };
}

let router = new useRouter();
let nickname = ref("");
let historyList = ref([]);
let currentHistoryId = ref(null);

const currentTitle = computed(() => {
  const cur = historyList.value.find(h => h.id === currentHistoryId.value);
  return cur ? cur.question : '新的对话';
});
const suggestQuestions = [
  '有关化学的sci期刊有哪些？',
  '影响因子较高的sci期刊有哪些？',
  'sci期刊小类中包含计算机的有哪些？',
]
let messageBox = ref(null);

watch(messages,() => {
  nextTick(() => {
    if (messageBox.value){
      messageBox.value.scrollTop = messageBox.value.scrollHeight;
    }
  });
},{deep:true});

function saveChatResult(question,answer){
  let parmas = {
    usersId: payload.usersId,
    question: question,
    answer: answer,
    parentId: globalHistoryId.value
  }
  proxy.$axios({
    url: 'history/saveChatResult/',
    method: "post",
    data: JSON.stringify(parmas)
  }).then(res => {
    if (globalHistoryId.value === 0){
      globalHistoryId.value = res.data.data;
      queryHistoryMenu();
    }
  });
}

function queryHistoryMenu(){
  proxy.$axios({
    url:'history/queryHistoryMenu/' + payload.usersId,
    method: "get",
    headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
  }).then(res => {
    historyList.value = res.data.data;
  });
}
onMounted(() => {
  nickname.value = payload.nickname || 'undefined';
  queryHistoryMenu();
})

function selectHistory(historyId){
  globalHistoryId.value = historyId;
  proxy.$axios({
    url: 'history/queryHistoryList/' + historyId,
    method: "get",
  }).then(res => {
    messages.value = res.data.data
  })
}

function createNewChat(){
  globalHistoryId.value = 0;
  currentHistoryId.value = null;
  messages.value = [];
  question.value = '';
}

function deleteHistory(historyId){
  proxy.$axios({
    url: 'history/deleteChatHistory/' + historyId,
    method: "post",
  }).then(res => {
    console.log(res);
    if (res.data.code === 200){
      ElMessage.success("删除成功");
      if (globalHistoryId.value === historyId){
        globalHistoryId.value = 0;
        messages.value = [];
      }
      historyList.value = historyList.value.filter(h => h.historyId !== historyId);
    }else{
      ElMessage.error(res.data.msg);
    }
  })
}

function hendleEnter(){
  if (!isButtonDisabled.value){
    chat();
  }
}

function quickAsk(text){
  question.value = text;
  chat()
}

function handleUserCommand(command){
  switch (command){
    case 'profile':
      ElMessage.info('个人中心功能开发中');
      break;
    case 'settings':
      ElMessage.info('设置功能开发中');
      break;
    case 'logout':
      logout();
      break;
    default:
      break;
  }
}

function logout(){
  localStorage.removeItem('token');
  ElMessage.success('已退出登录');
  router.push('/');
}
</script>

<style scoped>
:global(*),
:global(*::before),
:global(*::after) {
  box-sizing: border-box;
}
/* ============ 全局页面 ============ */
.chat-page {
  position: fixed;
  inset: 0;
  display: flex;
  overflow: hidden;
  background:
    radial-gradient(circle at 12% 18%, #10294a 0%, transparent 55%),
    radial-gradient(circle at 88% 82%, #0a2540 0%, transparent 55%),
    linear-gradient(160deg, #070c16 0%, #04070d 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
    "PingFang SC", "Microsoft YaHei", sans-serif;
  color: #d6e4f7;
}

/* ============ 科技网格背景 ============ */
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(80, 160, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(80, 160, 255, 0.06) 1px, transparent 1px);
  background-size: 52px 52px;
  -webkit-mask-image: radial-gradient(circle at 50% 40%, #000 0%, transparent 78%);
  mask-image: radial-gradient(circle at 50% 40%, #000 0%, transparent 78%);
  animation: gridMove 24s linear infinite;
  pointer-events: none;
}

@keyframes gridMove {
  from { background-position: 0 0, 0 0; }
  to   { background-position: 52px 52px, 52px 52px; }
}

/* ============ 光晕 ============ */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: .38;
  pointer-events: none;
}

.glow-1 {
  width: 480px; height: 480px;
  top: -160px; left: -120px;
  background: #1b6bff;
  animation: floatA 15s ease-in-out infinite;
}
.glow-2 {
  width: 420px; height: 420px;
  bottom: -160px; right: -100px;
  background: #00d4ff;
  animation: floatB 17s ease-in-out infinite;
}
.glow-3 {
  width: 300px; height: 300px;
  top: 50%; left: 45%;
  transform: translate(-50%, -50%);
  background: #7c3aed;
  opacity: .18;
  animation: pulse 9s ease-in-out infinite;
}

@keyframes floatA {
  0%, 100% { transform: translate3d(0, 0, 0); }
  50%      { transform: translate3d(50px, 40px, 0); }
}
@keyframes floatB {
  0%, 100% { transform: translate3d(0, 0, 0); }
  50%      { transform: translate3d(-50px, -40px, 0); }
}
@keyframes pulse {
  0%, 100% { opacity: .14; transform: translate(-50%, -50%) scale(1); }
  50%      { opacity: .28; transform: translate(-50%, -50%) scale(1.15); }
}

/* ============ 侧边栏 ============ */
.sidebar {
  position: relative;
  z-index: 3;
  width: 272px;
  flex: none;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px 16px 16px;
  background: rgba(9, 15, 26, 0.82);
  border-right: 1px solid rgba(90, 160, 255, 0.14);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 品牌 */
.sidebar-head {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 4px 6px 20px;
}

.logo {
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow:
    0 8px 20px rgba(37, 99, 235, .40),
    inset 0 1px 0 rgba(255, 255, 255, .30);
}

.brand-name {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 2px;
  background: linear-gradient(90deg, #eaf3ff, #6cb2ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* 新建对话 */
.new-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 44px;
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, .45);
  background: linear-gradient(135deg,
    rgba(37, 99, 235, .22),
    rgba(6, 182, 212, .18));
  color: #8fc6ff;
  font-size: 13.5px;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all .22s;
}

.new-chat:hover {
  border-color: rgba(96, 165, 250, .9);
  color: #d6eaff;
  background: linear-gradient(135deg,
    rgba(37, 99, 235, .36),
    rgba(6, 182, 212, .28));
  box-shadow: 0 0 22px rgba(59, 130, 246, .35);
}

.new-chat:active { transform: scale(.985); }

/* 历史记录 */
.history {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 22px;
  min-height: 0;
}

.history-title {
  margin: 0 0 10px;
  padding-left: 6px;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #4d6f9b;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.history-list::-webkit-scrollbar { display: none; }

.history-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 9px;
  height: 38px;
  padding: 0 8px 0 10px;
  margin-bottom: 4px;
  border-radius: 9px;
  font-size: 13px;
  color: #9db4cf;
  cursor: pointer;
  transition: background .18s, color .18s;
}

.history-item:hover {
  background: rgba(59, 130, 246, .10);
  color: #cfe3ff;
}

.history-item.active {
  background: rgba(59, 130, 246, .18);
  color: #eaf3ff;
}

.history-dot {
  flex: none;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #3b82f6;
  box-shadow: 0 0 8px rgba(59, 130, 246, .9);
  opacity: 0;
  transition: opacity .18s;
}

.history-item:hover .history-dot,
.history-item.active .history-dot {
  opacity: 1;
}

.history-text {
  flex: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.history-del {
  flex: none;
  width: 22px; height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #627b9c;
  cursor: pointer;
  opacity: 0;
  transition: all .18s;
}

.history-item:hover .history-del { opacity: 1; }

.history-del:hover {
  background: rgba(239, 68, 68, .18);
  color: #ff8b8b;
}

.history-empty {
  margin: 12px 0 0;
  padding-left: 6px;
  font-size: 12px;
  color: #3f5573;
}

/* 用户区 */
.user-area {
  padding-top: 14px;
  border-top: 1px solid rgba(90, 160, 255, .12);
}

.user-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 4px 12px;
}

.user-avatar {
  flex: none;
  width: 34px; height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow: 0 6px 16px rgba(37, 99, 235, .35);
}

.user-name {
  font-size: 13.5px;
  color: #c3d6ef;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.user-btns {
  display: flex;
  gap: 6px;
}

.user-btns button {
  flex: 1;
  height: 32px;
  border-radius: 8px;
  border: 1px solid rgba(90, 140, 200, .22);
  background: rgba(8, 13, 24, 0.6);
  color: #8ba6c9;
  font-size: 12px;
  cursor: pointer;
  transition: all .18s;
}

.user-btns button:hover {
  border-color: rgba(96, 165, 250, .6);
  color: #cfe3ff;
  background: rgba(59, 130, 246, .14);
}

.user-btns button.logout:hover {
  border-color: rgba(239, 68, 68, .5);
  color: #ff9b9b;
  background: rgba(239, 68, 68, .12);
}

/* ============ 主区域 ============ */
.main {
  position: relative;
  z-index: 2;
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

/* 顶部标题栏 */
.chat-head {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 40px;
  border-bottom: 1px solid rgba(90, 160, 255, .10);
  background: rgba(9, 15, 26, 0.55);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.head-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: .6px;
  color: #e6f0ff;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 60vw;
}

.head-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: none;
}

.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #22d3ee;
  box-shadow: 0 0 10px rgba(34, 211, 238, .9);
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%      { opacity: .35; }
}

.status-text {
  font-size: 12px;
  letter-spacing: 1px;
  color: #4d6f9b;
}

/* ============ 消息区 ============ */
.messages {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 32px 40px 8px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.messages::-webkit-scrollbar { display: none; }

/* 欢迎屏 */
.welcome {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  animation: fadeUp .7s cubic-bezier(.22, .85, .3, 1) both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.welcome-logo {
  width: 74px; height: 74px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 22px;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow:
    0 16px 40px rgba(37, 99, 235, .45),
    inset 0 1px 0 rgba(255, 255, 255, .30);
  margin-bottom: 24px;
}

.welcome-title {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
  letter-spacing: 4px;
  background: linear-gradient(90deg, #eaf3ff, #6cb2ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.welcome-sub {
  margin: 12px 0 34px;
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #4d6f9b;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 11px;
  width: 100%;
  max-width: 520px;
}

.suggestion {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 13px;
  border: 1px solid rgba(90, 140, 200, .20);
  background: rgba(13, 20, 35, 0.6);
  color: #b8cee8;
  font-size: 13.5px;
  text-align: left;
  cursor: pointer;
  transition: all .22s;
}

.suggestion:hover {
  border-color: rgba(96, 165, 250, .65);
  background: rgba(37, 99, 235, .14);
  color: #eaf3ff;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(37, 99, 235, .22);
}

.sug-dot {
  flex: none;
  color: #38bdf8;
  font-size: 13px;
  text-shadow: 0 0 12px rgba(56, 189, 248, .9);
}

/* 消息气泡 */
.msg {
  display: flex;
  gap: 12px;
  margin-bottom: 22px;
  animation: msgIn .35s cubic-bezier(.22, .85, .3, 1) both;
}

@keyframes msgIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.msg-user {
  flex-direction: row-reverse;
}

.msg-avatar {
  flex: none;
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .5px;
  color: #d8ecff;
  background: linear-gradient(140deg, #1d4ed8, #06b6d4);
  box-shadow: 0 6px 16px rgba(37, 99, 235, .35);
}

.msg-ai .msg-avatar {
  background: linear-gradient(140deg, #0f2a52, #0b3b52);
  border: 1px solid rgba(90, 160, 255, .35);
  color: #6cb2ff;
  box-shadow: 0 6px 16px rgba(6, 182, 212, .22);
}

.msg-bubble {
  max-width: 72%;
  padding: 13px 18px;
  border-radius: 14px;
  font-size: 14.5px;
  line-height: 1.75;
  word-break: break-word;
  white-space: normal;
  letter-spacing: .2px;
}

.msg-user .msg-bubble {
  background: linear-gradient(135deg, #2563eb, #0ea5e9);
  color: #fff;
  border-top-right-radius: 4px;
  box-shadow: 0 10px 26px rgba(37, 99, 235, .32);
}

.msg-ai .msg-bubble {
  background: rgba(18, 28, 46, 0.82);
  border: 1px solid rgba(90, 140, 200, .20);
  color: #d6e4f7;
  border-top-left-radius: 4px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* ============ 输入区 ============ */
.input-area {
  flex: none;
  padding: 16px 40px 20px;
  border-top: 1px solid rgba(90, 160, 255, .10);
  background: rgba(9, 15, 26, 0.6);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 7px 7px 20px;
  border-radius: 16px;
  background: rgba(8, 13, 24, 0.85);
  border: 1px solid rgba(90, 140, 200, .22);
  transition: border-color .25s, box-shadow .25s, background .25s;
}

.input-wrap:hover {
  border-color: rgba(90, 160, 255, 0.38);
}

.input-wrap:focus-within {
  border-color: #3b82f6;
  background: rgba(9, 16, 30, 0.95);
  box-shadow:
    0 0 0 3px rgba(59, 130, 246, .15),
    0 0 26px rgba(37, 99, 235, .20);
}

.input-wrap input {
  flex: 1;
  height: 42px;
  border: none;
  outline: none;
  background: transparent;
  color: #e8f1ff;
  font-size: 14.5px;
  letter-spacing: .3px;
  min-width: 0;
}

.input-wrap input::placeholder {
  color: #4a6080;
}

.send-btn {
  flex: none;
  display: flex;
  align-items: center;
  gap: 7px;
  height: 42px;
  padding: 0 22px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 55%, #06b6d4 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform .2s, box-shadow .2s, filter .2s;
  box-shadow: 0 10px 24px rgba(37, 99, 235, .35);
}

.send-btn::after {
  content: "";
  position: absolute;
  top: 0; left: -120%;
  width: 60%; height: 100%;
  background: linear-gradient(
    100deg,
    transparent,
    rgba(255, 255, 255, .40),
    transparent
  );
  transition: left .6s ease;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(37, 99, 235, .48);
  filter: brightness(1.06);
}

.send-btn:hover:not(:disabled)::after {
  left: 130%;
}

.send-btn:active:not(:disabled) {
  transform: translateY(0);
}

.send-btn:disabled {
  background: rgba(120, 140, 170, .14);
  color: #64778f;
  box-shadow: none;
  cursor: not-allowed;
}

.input-tip {
  margin: 10px 0 0;
  text-align: center;
  font-size: 11.5px;
  letter-spacing: .5px;
  color: #3f5573;
}

/* ============ 响应式 ============ */
@media (max-width: 900px) {
  .sidebar { width: 224px; }
  .messages { padding: 24px 20px 8px; }
  .chat-head { padding: 16px 20px; }
  .input-area { padding: 12px 20px 16px; }
  .welcome-title { font-size: 22px; letter-spacing: 2px; }
  .msg-bubble { max-width: 84%; }
}

@media (max-width: 640px) {
  .sidebar { display: none; }
  .send-btn span { display: none; }
  .send-btn { padding: 0 14px; }
}
/* ============ Markdown 正文样式 ============ */
.md-body :deep(p) {
  margin: 0 0 10px;
}
.md-body :deep(p:last-child) {
  margin-bottom: 0;
}

.md-body :deep(h1),
.md-body :deep(h2),
.md-body :deep(h3),
.md-body :deep(h4) {
  margin: 18px 0 10px;
  font-weight: 600;
  color: #eaf3ff;
  line-height: 1.4;
}
.md-body :deep(h1) { font-size: 19px; }
.md-body :deep(h2) {
  font-size: 17px;
  padding-left: 10px;
  border-left: 3px solid #3b82f6;
}
.md-body :deep(h3) { font-size: 15.5px; }

.md-body :deep(ul),
.md-body :deep(ol) {
  margin: 8px 0 10px;
  padding-left: 22px;
}
.md-body :deep(li) {
  margin-bottom: 5px;
}
.md-body :deep(li::marker) {
  color: #38bdf8;
}

.md-body :deep(strong) {
  color: #eaf3ff;
  font-weight: 600;
}
.md-body :deep(em) { color: #b8cee8; }

.md-body :deep(a) {
  color: #4fa8ff;
  text-decoration: none;
  border-bottom: 1px dashed rgba(79, 168, 255, .5);
}
.md-body :deep(a:hover) { color: #8fc6ff; }

/* 行内代码 */
.md-body :deep(code) {
  padding: 2px 6px;
  border-radius: 5px;
  background: rgba(56, 189, 248, .12);
  border: 1px solid rgba(90, 160, 255, .20);
  color: #7dd3fc;
  font-family: "JetBrains Mono", Consolas, Monaco, monospace;
  font-size: 13px;
}

/* 代码块 */
.md-body :deep(pre) {
  margin: 12px 0;
  padding: 14px 16px;
  border-radius: 10px;
  background: rgba(5, 10, 20, 0.92);
  border: 1px solid rgba(90, 160, 255, .18);
  overflow-x: auto;
  scrollbar-width: thin;
}
.md-body :deep(pre code) {
  padding: 0;
  background: transparent;
  border: none;
  color: #cfe3ff;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre;
}

/* 引用 */
.md-body :deep(blockquote) {
  margin: 10px 0;
  padding: 6px 14px;
  border-left: 3px solid rgba(59, 130, 246, .6);
  background: rgba(59, 130, 246, .07);
  border-radius: 0 8px 8px 0;
  color: #a8c0dc;
}

/* 表格 */
.md-body :deep(table) {
  width: 100%;
  margin: 12px 0;
  border-collapse: collapse;
  font-size: 13.5px;
  display: block;
  overflow-x: auto;
}
.md-body :deep(th),
.md-body :deep(td) {
  padding: 8px 12px;
  border: 1px solid rgba(90, 140, 200, .22);
  text-align: left;
}
.md-body :deep(th) {
  background: rgba(59, 130, 246, .14);
  color: #eaf3ff;
  font-weight: 600;
  white-space: nowrap;
}
.md-body :deep(tr:nth-child(even) td) {
  background: rgba(255, 255, 255, .02);
}

/* 分割线 */
.md-body :deep(hr) {
  margin: 16px 0;
  border: none;
  border-top: 1px solid rgba(90, 160, 255, .18);
}

/* 代码块滚动条 */
.md-body :deep(pre::-webkit-scrollbar) { height: 6px; }
.md-body :deep(pre::-webkit-scrollbar-thumb) {
  background: rgba(90, 160, 255, .3);
  border-radius: 3px;
}
</style>