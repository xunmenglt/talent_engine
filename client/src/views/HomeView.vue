<template>
  <div class="talent-engine-container">
    <!-- 顶部标题和用户信息 -->
    <div class="app-header">
      <div class="header-content">
        <h1 class="app-title">人才数据查询引擎</h1>
        <div class="user-info">
          <el-avatar :size="36"
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNmda-mZTVuVNr-kOHsHowPkL7-fjMVD20oQ&s" />
          <span class="username">用户</span>
        </div>
      </div>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-area" ref="chatBoxRef">
      <div v-for="(msg, index) in messages" :key="index" class="message"
        :class="{ 'user-message': msg.role === 'user', 'ai-message': msg.role === 'ai' }">
        <!-- 用户消息 - 头像在右侧 -->
        <template v-if="msg.role === 'user'">
          <!-- 内容主体 -->
          <div class="message-content user-content">
            <div class="message-header">
              <span class="sender-name">你</span>
            </div>
            <el-card shadow="hover" class="message-card">
              <div class="text-content">{{ msg.content }}</div>
            </el-card>
            <div class="message-time">{{ formatMessageTime(msg.timestamp) }}</div>
          </div>
          <!-- 右侧用户头像 -->
          <div class="message-avatar">
            <el-avatar :size="36"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNmda-mZTVuVNr-kOHsHowPkL7-fjMVD20oQ&s" />
          </div>
        </template>

        <!-- AI消息 -->
        <template v-else-if="msg.role === 'ai'">
          <!-- 左侧 AI 头像 -->
          <div class="message-avatar">
            <el-avatar :size="36"
              src="https://img.freepik.com/premium-photo/3d-ai-assistant-icon-artificial-intelligence-virtual-helper-logo-illustration_762678-40617.jpg" />
          </div>
          <!-- 内容主体 -->
          <div class="message-content">
            <div class="message-header">
              <span class="sender-name">AI助手</span>
            </div>
            <el-card shadow="hover" class="message-card">

              <!-- 可折叠的处理步骤时间线 -->
              <div v-if="msg.steps.length > 0" class="timeline-container">
                <div class="think-head">
                  <el-button type="text" @click="toggleTimeline(index)" class="toggle-timeline-btn">
                    {{ showTimeline[index] ? '▲ 隐藏处理过程' : '▼ 显示处理过程' }}

                  </el-button>
                  <div v-if="isLoading" class="loading-container">
                    💭 思考中
                    <div class="loading-dots">
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                    </div>
                  </div>
                </div>

                <el-collapse-transition>
                  <el-timeline v-show="showTimeline[index]" class="process-timeline">
                    <el-timeline-item v-for="(step, stepIndex) in msg.steps.filter(s => s.type !== 10)" :key="stepIndex"
                      :timestamp="formatMessageTime(step.timestamp)" placement="top">
                      <div class="step-title">{{ getTypeDesc(step.type) }}</div>
                      <div class="step-content" v-if="step.type!=1 && step.type!=0">
                        <div v-if="typeof step.content === 'string'" class="markdown-body"
                             v-html="md.render(step.content)" />
                        <div v-else class="markdown-body"
                             v-html="getRenderedContent(step)" />
                      </div>

<!--                      原版-->
<!--                      <div class="step-title">{{ getTypeDesc(step.type) }}</div>-->
<!--                      <div class="step-content">-->
<!--                        <div v-if="typeof step.content === 'string'" class="markdown-body"-->
<!--                          v-html="md.render(step.content)" />-->
<!--                        <pre v-else>{{ JSON.stringify(step.content, null, 2) }}</pre>-->
<!--                      </div>-->
                    </el-timeline-item>
                  </el-timeline>
                </el-collapse-transition>
              </div>
              <!-- 直接显示最终回答 -->
              <div v-if="msg.finalAnswer" class="final-answer markdown-body" v-html="md.render(msg.finalAnswer)" />
            </el-card>
            <div class="message-time">{{ formatMessageTime(msg.timestamp) }}</div>
          </div>
        </template>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <div class="input-container">
        <el-input v-model="query" placeholder="输入关于人才数据的问题..." type="textarea" :rows="2" resize="none"
          @keyup.enter.exact="handleSendMessage" />
        <div class="input-actions">
          <el-tooltip content="发送消息" placement="top">
            <el-button type="primary" @click="handleSendMessage" :disabled="!query.trim() || isLoading">发送</el-button>
          </el-tooltip>
        </div>
      </div>
      <div class="input-footer">
        <span class="hint-text">按Enter发送，Shift+Enter换行</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import 'github-markdown-css/github-markdown.css'

const md = new MarkdownIt()
const query = ref('')
const messages = ref([])
const chatBoxRef = ref(null)
const isLoading = ref(false)
const messageHistory = ref([])
const currentAIResponse = ref(null)
const showTimeline = ref({}) // 控制每个消息的时间线显示状态

// 初始欢迎消息
const initialMessages = [
  {
    role: 'ai',
    finalAnswer: "您好！我是人才数据助手，可以帮助您查询和分析人才信息。今天有什么可以帮您的吗？",
    steps: [],
    timestamp: new Date().getTime()
  }
]

onMounted(() => {
  messages.value = initialMessages
  scrollToBottom()
})

// 切换时间线显示状态
const toggleTimeline = (index) => {
  showTimeline.value[index] = !showTimeline.value[index]
}

// 获取消息类型描述
const getTypeDesc = (type) => {
  const typeMap = {
    '-2': '❌ 错误',
    '-1': '✅ 完成',
    '0': '🚀 任务开始',
    '1': '🔍 解析问题',
    '2': '🧭 规划中',
    '3': '🔎 检索相似问题',
    '4': '📄 生成SQL草稿',
    '5': '🧠 相似度过滤',
    '6': '🛠️ 构建最终SQL',
    '7': '🧪 验证SQL',
    '8': '🔁 重写SQL',
    '9': '📊 执行查询',
    '10': '💡 最终回答',
    '11': '💬 信息',
    '12': '📌 问题结构'
  }
  return typeMap[type.toString()] || `📄 类型 ${type}`
}

//新增部分
const messageRenderers = {
  // 类型0和1删除null的显示
  0: () => '',
  1: () => '',

  // 类型2：问题规划，只展示 plan_list中的内容
  2: (content) => {
    if (!content?.plan_list) return '';
    return content.plan_list.map((plan, idx) => {
      return `${idx + 1}. ${plan}`;
    }).join('\n\n');
  },

  // 类型12：问题结构，只展示“question_skeleton”中的内容
  12: (content) => {
    if (!content?.question_skeleton) return '';
    return content.question_skeleton;
  },

  // 类型3：相似问题检索，只展示每个元素中的question、question_skeleton、query
  3: (content) => {
    if (!content?.similar_docs?.length) return '';

    return content.similar_docs.map((doc, idx) => {
      const sqlData = doc?.sql_data || {};
      return `${idx + 1}. ` +
          `问题: ${sqlData.question || '无'}\n\n` +
          `问题骨架: ${sqlData.question_skeleton || '无'}\n\n` +
          `SQL查询:\n\`\`\`sql\n${sqlData.query || '无'}\n\`\`\``;
    }).join('\n\n');
  },

  // 类型4：生成SQL草稿，只展示 query
  4: (content) => {
    if (!content?.sql?.query) return '';
    return `\`\`\`sql\n${content.sql.query}\n\`\`\``;
  },

  //类型5：相似度过滤，只展示每个元素中的question、question_skeleton、query
  5: (content) => {
    if (!content?.similar_docs?.length) return '';

    return content.similar_docs.map((doc, idx) => {
      const sqlData = doc?.sql_data || {};
      return `${idx + 1}. ` +
          `问题: ${sqlData.question || '无'}\n\n` +
          `问题骨架: ${sqlData.question_skeleton || '无'}\n\n` +
          `SQL查询:\n\`\`\`sql\n${sqlData.query || '无'}\n\`\`\``;
    }).join('\n\n');
  },

  //类型9：执行查询，只展示每个元素中的sql（sql语句）、exec_res（SQL语句执行的结果）
  9: (content) => {
    if (!content?.sql || !content?.exec_res) return '';
    return `执行的SQL:\n\`\`\`sql\n${content.sql}\n\`\`\`\n\n查询结果:\n\n${content.exec_res}`;
  },

  //类型6：构建最终SQL，只展示query
  6: (content) => {
    if (!content?.sql?.query) return '';
    return `\`\`\`sql\n${content.sql.query}\n\`\`\``;
  },

  // 默认渲染器（纯文本）
  default: (content) => {
    if (content === null) return '';
    if (typeof content === 'string') return content;
    return JSON.stringify(content, null, 2);
  }
};

// 新增，获取对应类型的渲染内容
const getRenderedContent = (step) => {
  const renderer = messageRenderers[step.type] || messageRenderers.default;
  let rawContent = renderer(step.content);

  return md.render(rawContent);
};

// 格式化消息时间
const formatMessageTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  const el = chatBoxRef.value
  if (el) {
    el.scrollTop = el.scrollHeight
    // 平滑滚动
    el.scrollTo({
      top: el.scrollHeight,
      behavior: 'smooth'
    })
  }
}

// 处理发送消息
const handleSendMessage = async () => {
  if (!query.value.trim() || isLoading.value) return

  try {
    isLoading.value = true
    const userMessage = {
      role: 'user',
      content: query.value,
      timestamp: new Date().getTime()
    }

    messages.value.push(userMessage)
    query.value = ''
    await scrollToBottom()

    // 创建新的AI响应对象
    currentAIResponse.value = {
      role: 'ai',
      finalAnswer: '',
      steps: [],
      timestamp: new Date().getTime()
    }
    messages.value.push(currentAIResponse.value)

    // 初始化时间线显示状态
    showTimeline.value[messages.value.length - 1] = false

    // 模拟API调用
    const response = await fetch('/chat/sql_chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream'
      },
      body: JSON.stringify({
        query: userMessage.content,
        history: messageHistory.value,
        question_score_threshold: 0.8,
        sql_score_threshold: 0.5,
        topk: 5,
        is_planing: true,
        sql_verfy_times: 2
      })
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const parts = buffer.split('\r\n\r\n')
      buffer = parts.pop() || ''

      for (const part of parts) {
        if (part.startsWith('data: ')) {
          const jsonStr = part.slice(6)
          try {
            const data = JSON.parse(jsonStr)
            data.timestamp = new Date().getTime()

            if (data.type === 10 && data.content?.chunk) {
              // 最终回答部分
              currentAIResponse.value.finalAnswer += data.content.chunk
            } else if (data.type === -1) {
              // 消息结束
              currentAIResponse.value.timestamp = data.timestamp
            } else {
              // 处理步骤
              currentAIResponse.value.steps.push(data)
            }

            await scrollToBottom()
          } catch (err) {
            console.error('SSE解析错误:', err)
            currentAIResponse.value.steps.push({
              type: -2,
              content: '响应处理错误',
              timestamp: new Date().getTime()
            })
          }
        }
      }
    }

    // 将对话添加到历史记录
    if (currentAIResponse.value.finalAnswer) {
      messageHistory.value.push(['user', userMessage.content])
      messageHistory.value.push(['assistant', currentAIResponse.value.finalAnswer])
    }

  } catch (error) {
    console.error('API调用失败:', error)
    if (currentAIResponse.value) {
      currentAIResponse.value.steps.push({
        type: -2,
        content: '从服务器获取响应失败',
        timestamp: new Date().getTime()
      })
    }
    ElMessage.error('发送消息失败')
  } finally {
    isLoading.value = false
    currentAIResponse.value = null
    await scrollToBottom()
  }
}
</script>

<style scoped>
@import 'github-markdown-css/github-markdown.css';

.talent-engine-container {
  display: flex;
  flex-direction: column;
  height: 90vh;
  max-width: 90%;
  margin: 0 auto;
  background-color: #f5f7fa;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.app-header {
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  color: white;
  padding: 16px 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 500;
}

.chat-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f0f2f5;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message.ai-message {
  align-self: flex-start;
}

.message.user-message {
  align-self: flex-end;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-content {
  align-items: flex-end;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.sender-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.message-type {
  font-size: 12px;
  color: #666;
  background-color: #f0f0f0;
  padding: 2px 6px;
  border-radius: 10px;
}

.message-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.ai-message .message-card {
  background-color: #ffffff;
  border-left: 4px solid #409eff;
}

.user-message .message-card {
  background-color: #f0f6ff;
  border-right: 4px solid #a0cfff;
}

.message-time {
  font-size: 11px;
  color: #999;
  text-align: right;
  margin-top: 4px;
}

.input-area {
  padding: 16px 24px;
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
}

.input-container {
  position: relative;
  display: flex;
  gap: 12px;
}

.input-actions {
  display: flex;
  align-items: flex-end;
}

.input-footer {
  margin-top: 8px;
}

.hint-text {
  font-size: 12px;
  color: #909399;
}

.loading-dots {
  display: flex;
  padding: 8px 0;
  gap: 6px;
  flex-direction: row;
}

.dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background-color: #c0c4cc;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 自定义滚动条 */
.chat-area::-webkit-scrollbar {
  width: 8px;
}

.chat-area::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chat-area::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.chat-area::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Markdown内容样式 */
.markdown-body {
  font-size: 14px;
  line-height: 1.6;
}

.markdown-body pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
}

.markdown-body code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 13px;
}

.text-content {
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.6;
}

/* 时间线容器 */
.timeline-container {
  border-bottom: 1px dashed #eaeaea;
}

.toggle-timeline-btn {
  padding: 0;
  font-size: 12px;
  color: #666;
}

.process-timeline {
  margin-top: 4px;
  padding-left: 10px;
}

.step-title {
  font-weight: 500;
  font-size: 13px;
  margin-bottom: 4px;
}

.step-content {
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-top: 4px;
  font-size: 13px;
}

.step-content pre {
  white-space: pre-wrap;
  font-family: monospace;
  background-color: #f0f2f5;
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

/* 最终回答样式 */
.final-answer {
  padding: 8px 0;
}

/* 调整时间线样式 */
:deep(.el-timeline-item__timestamp) {
  color: #666;
  font-size: 12px;
  margin-bottom: 4px;
}

:deep(.el-timeline-item__node) {
  background-color: #409eff;
}

.loading-container {
  display: flex;
}

.think-head {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.loading-container {
  font-size: 12px;
  color: rgb(73, 149, 255);
  font-weight: 900;
  height: 100%;
  display: flex;
  align-content: center;
  margin-left: 10px;
}
</style>