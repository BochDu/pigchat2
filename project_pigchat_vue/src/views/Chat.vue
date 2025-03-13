<template>
    <Layout>
      <div class="chat-room">
        <div class="messages" ref="messagesContainer">
          <div class="messages-container">
            <div v-for="(message, index) in messages" :key="index" 
                 class="message-item"
                 :class="{ 'with-emoji': message.isEmoji, 'selectable': canSelect }"
                 @click.stop="handleMessageClick(index)">
              <!-- 移除时间显示 -->
              <!-- <div class="message-time">{{ getCurrentTime() }}</div> -->
              <div class="message-content" 
                   :class="{ 
                     'is-emoji': message.isEmoji, 
                     'selected': selectedIndex === index,
                     'selectable': canSelect,
                     'user-message': message.isUser,  // 用户发送的消息添加 user-message 类
                     'reply-message': !message.isUser  // 回复的消息添加 reply-message 类
                   }">
                {{ message.content }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-area">
          <div class="input-wrapper">
            <textarea
            v-model="inputText"
            placeholder="输入消息..."
            @keyup.enter="handleSend"
            @input="() => console.log('输入框的值:', inputText.value)"
            class="custom-textarea"
            ></textarea>
  
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
  

  const fetchPigTimestamp = async () => {
  try {
    const lastFetchTime = localStorage.getItem('lastPigTimestampFetch')
    const now = Date.now()
    
    // 检查是否需要重新获取（一天 = 24 * 60 * 60 * 1000 毫秒）
    if (!lastFetchTime || (now - parseInt(lastFetchTime)) > 24 * 60 * 60 * 1000) {
      const { data } = await axios.get('/api/get_pig_timestamp')
      
      // 存储时间戳和最后获取时间
      localStorage.setItem('pigTimestamp', data.pig_timestamp.toString())
      localStorage.setItem('lastPigTimestampFetch', now.toString())
      
      console.log('成功获取新的pig_timestamp:', data.pig_timestamp)
    } else {
      console.log('使用缓存的pig_timestamp')
    }
  } catch (error) {
    console.error('获取pig_timestamp失败:', error)
    ElMessage.error('获取时间戳失败，请检查API服务是否正常运行')
  }
}

onMounted(async () => {
  await fetchPigTimestamp(); // 确保在组件挂载时获取时间戳
});

const handleSend = async () => {
  // 保存输入的文本，避免后续清空操作影响
  const inputValue = inputText.value.trim();
  if (inputValue) {
    // 发送的消息标记为用户消息，isUser 为 true
    messages.value.push({
      content: inputValue,
      isEmoji: false,
      time: getCurrentTime(),
      canConvert: true,
      isUser: true
    });
    canConvert.value = true;
    selectedIndex.value = -1;
    inputText.value = ''; // 清空输入框
    scrollToBottom();

    try {
      const timestamp = localStorage.getItem('pigTimestamp');
      if (!timestamp) {
        ElMessage.error('时间戳未获取，请稍后再试');
        return;
      }

      // 调用加密 API 进行转换，使用保存的输入值
      const { data } = await axios.post('/api/utf8_to_emoji', {
        utf8_str: inputValue,
        timestamp: timestamp,
        password: 'my_password'
      });

      console.log('接口返回的数据:', data); // 打印接口返回的数据

      if (data && data.result) {
        // 模拟收到回复消息，isUser 为 false，显示转换后的结果
        const newMessage = {
          content: data.result,
          isEmoji: true,
          time: getCurrentTime(),
          canConvert: true,
          isUser: false
        };
        messages.value.push(newMessage);
        console.log('添加的新消息:', newMessage); // 打印添加的新消息
        scrollToBottom();
      } else {
        console.error('接口返回数据格式错误:', data);
        ElMessage.error('接口返回数据格式错误，请检查 API 服务');
      }
    } catch (error) {
      console.error('转换失败:', error);
      ElMessage.error('转换失败，请稍后重试');
    }
  }
};
  
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
          canConvert: true,
          isUser: selectedMessage.isUser  // 保留原消息的 isUser 属性
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
          canConvert: true,
          isUser: selectedMessage.isUser  // 保留原消息的 isUser 属性
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
  /* 隐藏页面滚动条 */
  body {
    -ms-overflow-style: none;  /* IE 和 Edge */
    scrollbar-width: none;  /* Firefox */
  }
  
  /* Chrome, Safari 和 Opera */
  body::-webkit-scrollbar {
    display: none;
  }
  
  .chat-room {
    display: flex;
    flex-direction: column;
    height: calc(95vh - 80px);
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin: 1rem auto;
    position: relative;
    max-width: 1000px;
    width: calc(100% - 2rem);
    
    /* 新增隐藏滚动条的样式 */
    -ms-overflow-style: none;  /* IE 和 Edge */
    scrollbar-width: none;  /* Firefox */
  }
  
  /* Chrome, Safari 和 Opera */
  .chat-room::-webkit-scrollbar {
    display: none;
  }
  
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background: #f0f2f5;
    scroll-behavior: smooth;
    
    /* 新增隐藏滚动条的样式 */
    -ms-overflow-style: none;  /* IE 和 Edge */
    scrollbar-width: none;  /* Firefox */
  }
  
  /* Chrome, Safari 和 Opera */
  .messages::-webkit-scrollbar {
    display: none;
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
    padding: 12px 16px;
    border-radius: 18px 4px 18px 18px;
    max-width: 70%;
    word-break: break-all; /* 消息内容自动换行 */
    white-space: normal; /* 允许文本换行 */
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    position: relative;
    transition: all 0.3s ease;
    margin-right: 8px;
    font-size: 15px;
    line-height: 1.4;
    user-select: none;
  }
  
  /* 用户发送的消息样式 */
  .message-content.user-message {
    background: #a8d0e6;
    color: black;
    align-self: flex-end;
  }
  
  /* 回复消息的样式 */
  .message-content.reply-message {
    background: #c4e8c4;
    color: black;
    align-self: flex-start;
    border-radius: 4px 18px 18px 18px;
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
  
  /* 输入区域整体样式 */
  .input-area {
      padding: 16px;
      background: white;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
      position: relative;
      z-index: 10;
      height: 150px;
      min-height: 150px;
      display: flex;
      justify-content: center; /* 水平居中 */
      align-items: center; /* 垂直居中 */
  }
  
  /* 输入框包装器样式 */
  .input-wrapper {
      padding: 0;
      margin: 0;
      width: 100%;
      box-sizing: border-box;
      display: flex;
      gap: 20px;
      align-items: center;
      width: 100%; /* 宽度占满父容器 */
      max-width: 768px; /* 最大宽度限制 */
      padding: 0 4px;
      flex-wrap: nowrap;
      flex: 1;
  }
  
  .custom-textarea {
    width: 100%; /* 明确宽度 */
    height: 100%;
    min-height: 100px;
    padding: 12px;
    box-shadow: 0 0 0 1px #dcdfe6;
    transition: all 0.3s ease;
    border-radius: 24px;
    background: #f5f7fa;
    resize: none; /* 禁止用户调整大小 */
    border: none;
    outline: none;
    white-space: normal;
    word-break: break-all;
    color: black; /* 这里修改文字颜色 */
    -ms-overflow-style: none;  /* IE 和 Edge */
    scrollbar-width: none;  /* Firefox */
    
    /* 确保盒子模型包含内边距和边框 */
    box-sizing: border-box; 
  }
  
  /* Chrome, Safari 和 Opera */
  .custom-textarea::-webkit-scrollbar {
    display: none;
  }
  
  .custom-textarea:hover {
      box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2);
      background: white;
  }
  
  .custom-textarea:focus {
      box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2);
      background: white;
  }
  
  /* 输入图标样式 */
  .input-icon {
      font-size: 18px;
      color: #909399;
      margin-right: 4px;
      flex-shrink: 0; /* 防止图标缩小 */
  }
  
  .send-button {
    width: 100px; 
    height: 100px; 
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
  </style>