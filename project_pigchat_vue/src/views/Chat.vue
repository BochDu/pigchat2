<template>
  <Layout>
    <div class="chat-room">
      <div class="messages" ref="messagesContainer">
        <div class="messages-container">
          <div v-for="(message, index) in messages" :key="index" 
               class="message-item"
               :class="{ 'with-emoji': message.isEmoji, 'selectable': canSelect }"
               @click.stop="handleMessageClick(index)">
            <div class="message-time">{{ getCurrentTime() }}</div>
            <div class="message-content" 
                 :class="{ 
                   'is-emoji': message.isEmoji, 
                   'selected': selectedIndex === index,
                   'selectable': canSelect 
                 }">
              {{ message.content }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <div class="input-wrapper">
          <el-input
            v-model="inputText"
            placeholder="输入消息..."
            clearable
            @keyup.enter="handleSend"
          >
            <template #prefix>
              <el-icon class="input-icon"><ChatRound /></el-icon>
            </template>
          </el-input>
            <el-button type="primary" @click="handleSend" class="send-button">
              <img src="../assets/wild_boar.png" alt="Convert" class="pig-icon" />
            </el-button>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, watch, onMounted, computed, onUnmounted, nextTick } from 'vue'
import { Message, Position, ChatRound } from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const messages = ref([])
const inputText = ref('')
const canConvert = ref(false)
const messagesContainer = ref(null)
const selectedIndex = ref(-1)
const canSelect = computed(() => messages.value.length >= 2)

const getCurrentTime = () => {
  const now = new Date()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}

const handleSend = () => {
  if (inputText.value.trim()) {
    messages.value.push({
      content: inputText.value,
      isEmoji: false,
      time: getCurrentTime(),
      canConvert: true
    })
    canConvert.value = true
    selectedIndex.value = -1
    inputText.value = ''
    scrollToBottom()
  }
}

const handleMessageClick = (index) => {
  if (!canSelect.value) return
  selectedIndex.value = selectedIndex.value === index ? -1 : index
}

const convertToEmoji = async (event) => {
  if (isDragging.value) return
  
  // 如果只有一条消息，直接转换它
  if (messages.value.length === 1) {
    selectedIndex.value = 0
  } 
  // 如果有多条消息但没有选中任何消息，不执行转换
  else if (messages.value.length >= 2 && selectedIndex.value === -1) {
    return
  }
  
  const selectedMessage = messages.value[selectedIndex.value]
  if (!selectedMessage) return

  try {
    const timestamp = localStorage.getItem('pigTimestamp')
    if (!timestamp) {
      ElMessage.error('时间戳未获取，请稍后再试')
      return
    }

    if (!selectedMessage.isEmoji) {
      const { data } = await axios.post('/api/utf8_to_emoji', {
        utf8_str: selectedMessage.content,
        timestamp: timestamp,
        password: 'my_password'
      })
      
      messages.value[selectedIndex.value] = {
        content: data.result,
        isEmoji: true,
        time: selectedMessage.time,
        canConvert: true
      }
    } else {
      const { data } = await axios.post('/api/emoji_to_utf8', {
        emoji_str: selectedMessage.content,
        timestamp: timestamp,
        password: 'my_password'
      })
      
      messages.value[selectedIndex.value] = {
        content: data.result,
        isEmoji: false,
        time: selectedMessage.time,
        canConvert: true
      }
    }
    
    // 重置选择状态
    selectedIndex.value = -1
    
  } catch (error) {
    console.error('转换失败:', error)
    ElMessage.error('转换失败，请稍后重试')
  }
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 100)
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })


</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 1rem auto;
  position: relative;
  max-width: 1000px;
  width: calc(100% - 2rem);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f0f2f5;
  scroll-behavior: smooth;
}

.messages-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.message-item {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  position: relative;
  transition: all 0.3s ease;
}

.message-item.with-emoji {
  margin-bottom: 24px;
}

.message-time {
  font-size: 12px;
  color: #8a8a8a;
  margin-bottom: 4px;
  padding: 0 4px;
}

.message-content {
  background: #1989fa;
  color: white;
  padding: 12px 16px;
  border-radius: 18px 4px 18px 18px;
  max-width: 70%;
  word-break: break-all;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  margin-right: 8px;
  font-size: 15px;
  line-height: 1.4;
  user-select: none;
}

.message-content.selectable {
  cursor: pointer;
}

.message-content.is-emoji {
  background: transparent;
  font-size: 4rem;
  padding: 4px;
  box-shadow: none;
  margin-right: 0;
  line-height: 1;
}

.message-content.selected {
  box-shadow: 0 0 0 2px #409eff;
  transform: scale(1.02);
}

.message-content.is-emoji.selected {
  box-shadow: 0 0 0 2px #409eff;
  transform: scale(1.05);
  background: rgba(64, 158, 255, 0.1);
}

.message-item.selectable .message-content:hover {
  opacity: 0.8;
  transform: scale(1.02);
}

.message-item.selectable .message-content.is-emoji:hover {
  opacity: 0.8;
  transform: scale(1.05);
  background: rgba(64, 158, 255, 0.05);
}

.input-area {
  padding: 16px;
  background: white;
  border-top: 1px solid #ebeef5;
  position: relative;
  z-index: 10;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
  max-width: 768px;
  margin: 0 auto;
  padding: 0 4px;
}

.input-wrapper .el-input {
  flex: 1;
}

.input-wrapper :deep(.el-input__wrapper) {
  padding-left: 12px;
  box-shadow: 0 0 0 1px #dcdfe6;
  transition: all 0.3s ease;
  border-radius: 24px;
  background: #f5f7fa;
}

.input-wrapper :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #409eff;
  background: white;
}

.input-wrapper :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409eff;
  background: white;
}

.input-icon {
  font-size: 18px;
  color: #909399;
  margin-right: 4px;
}

.send-button {
  width: 10vw;
  height: 10vw; 
  max-width: 60px;
  max-height: 60px;
  border-radius: 50%;
  background: #FFE5E5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: move;
  opacity: 0.95;
  position: relative;
  top: 0;
  left: 0;
  z-index: 1000;
  box-shadow: 0 0 5px rgba(255, 154, 158, 0.3);
  user-select: none;
  touch-action: none;
  will-change: transform;
  border: none;
  outline: none;
  transition: all 0.3s ease;
}

.send-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  box-shadow: 0 0 0 rgba(255, 154, 158, 0);
  transition: all 0.3s ease;
  z-index: -1;
}

.send-button:not(.dragging):not(.wiggle) {
  transition: all 0.3s ease;
}

.send-button.dragging {
  cursor: grabbing;
}

.send-button.dragging::before {
  box-shadow: 0 0 20px rgba(255, 154, 158, 0.7);
}

.send-button:hover:not(.dragging):not(.wiggle) {
  transform: translate3d(var(--button-x), var(--button-y), 0) scale(1.1);
}

.send-button:hover:not(.dragging):not(.wiggle)::before {
  box-shadow: 0 0 30px rgba(255, 154, 158, 0.8);
}

.send-button.wiggle::before {
  box-shadow: 0 0 30px rgba(255, 154, 158, 0.8);
}

.send-button.wiggle {
  opacity: 1;
  animation: wiggle 1s ease infinite;
}

.send-button:active {
  outline: none;
}

.send-button:focus {
  outline: none;
}

@keyframes wiggle {
  0% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(5deg);
  }
  50% {
    transform: rotate(0deg);
  }
  75% {
    transform: rotate(-5deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

@media (max-width: 600px) {
  .send-button {
    /* 确保在小屏幕下宽高仍然相等 */
    width: 36px;
    height: 36px;
    max-width: 60px;
    max-height: 60px;
  }
}

.pig-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
  pointer-events: none;
}

.pig-tooltip {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  white-space: nowrap;
  pointer-events: none;
  animation: fadeIn 0.3s ease;
  font-weight: 500;
}

.pig-tooltip::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 12px;
  height: 12px;
  background: #333;
  border-radius: 2px;
}

@keyframes wiggle {
  0% { transform: translate3d(var(--button-x), var(--button-y), 0) rotate(0deg) scale(1.1); }
  25% { transform: translate3d(var(--button-x), var(--button-y), 0) rotate(-10deg) scale(1.1); }
  50% { transform: translate3d(var(--button-x), var(--button-y), 0) rotate(0deg) scale(1.1); }
  75% { transform: translate3d(var(--button-x), var(--button-y), 0) rotate(10deg) scale(1.1); }
  100% { transform: translate3d(var(--button-x), var(--button-y), 0) rotate(0deg) scale(1.1); }
}

@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translate(-50%, -5px); 
  }
  to { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
}

@media (max-width: 768px) {
  .chat-room {
    height: calc(100vh - 72px);
    margin: 0.5rem;
    width: calc(100% - 1rem);
    border-radius: 12px;
  }
  
  .messages-container {
    padding: 0 8px;
  }
  
  .message-content {
    max-width: 85%;
    font-size: 14px;
    padding: 10px 14px;
  }
  
  .input-area {
    padding: 16px;
    background: white;
    border-top: 1px solid #ebeef5;
    position: relative;
    z-index: 10;
    /* 固定容器的高度，例如 200px，你可以根据实际需求调整 */
    height: 200px; 
    /* 使用 flex 布局来控制子元素的排列 */
    display: flex;
  }

  .input-wrapper {
    display: flex;
    gap: 12px;
    align-items: center;
    max-width: 768px;
    margin: 0 auto;
    padding: 0 4px;
    /* 防止输入框容器换行 */
    flex-wrap: nowrap;
    /* 让输入框容器占满容器的垂直空间 */
    flex: 1; 
  }

  .input-wrapper .el-input {
    flex: 1;
    /* 让输入框充满输入区域 */
    height: 100%; 
  }

  .input-wrapper :deep(.el-input__wrapper) {
    padding-left: 12px;
    box-shadow: 0 0 0 1px #dcdfe6;
    transition: all 0.3s ease;
    border-radius: 24px;
    background: #f5f7fa;
    /* 让输入框内部容器充满输入框 */
    height: 100%; 
  }

  .send-button {
    /* 设置固定宽度，例如 80px */
    width: 100px; 
    height: 100px;
    font-size: 14px;
    flex-shrink: 0; 
  }

  /* 小屏幕下的样式 */
  @media (max-width: 600px) {
    .send-button {
      /* 确保在小屏幕下宽高仍然相等 */
      width: 36px;
      height: 36px;
      max-width: 60px;
      max-height: 60px;
      flex-shrink: 0; 
    }
  }
}

.message-item.selectable {
  cursor: pointer;
}

.message-item.selectable:hover .message-content {
  opacity: 0.8;
  transform: scale(1.02);
}

.message-item.selectable:hover .message-content.is-emoji {
  opacity: 0.8;
  transform: scale(1.05);
}

/* 移除不需要的样式 */
.message-content-wrapper,
.message-checkbox,
.message-content.with-checkbox,
.message-content.is-emoji.with-checkbox {
  display: none;
}
</style> 