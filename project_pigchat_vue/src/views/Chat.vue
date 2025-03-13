<template>
  <Layout>
    <div class="chat-room">
      <div class="messages" ref="messagesContainer">
        <div class="messages-container">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message-item"
            :class="{ 'with-emoji': message.isEmoji, selectable: canSelect }"
            @click.stop="handleMessageClick(index)"
          >
            <!-- 移除时间显示 -->
            <!-- <div class="message-time">{{ getCurrentTime() }}</div> -->
            <div
              class="message-content"
              :class="{
                'is-emoji': message.isEmoji,
                selected: selectedIndex === index,
                selectable: canSelect,
                'user-message': message.isUser, // 用户发送的消息添加 user-message 类
                'reply-message': !message.isUser, // 回复的消息添加 reply-message 类
              }"
            >
              {{ message.content }}
            </div>
          </div>
        </div>
      </div>

      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="inputText"
            placeholder="Start a new encrypted chat"
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
import {
  ref,
  watch,
  onMounted,
  computed,
  onUnmounted,
  nextTick,
  defineProps,
} from "vue";
import { Message, Position, ChatRound } from "@element-plus/icons-vue";
import Layout from "../components/Layout.vue";
import { ElMessage } from "element-plus";
import axios from "axios";

// 接收父组件传递的 apiKey
const props = defineProps({
  apiKey: {
    type: String,
    default: "",
  },
});

const messages = ref([]);
const inputText = ref("");
const canConvert = ref(false);
const messagesContainer = ref(null);
const selectedIndex = ref(-1);
const canSelect = computed(() => messages.value.length >= 2);

const getCurrentTime = () => {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
};

const fetchPigTimestamp = async () => {
  try {
    const lastFetchTime = localStorage.getItem("lastPigTimestampFetch");
    const now = Date.now();

    // 检查是否需要重新获取（一天 = 24 * 60 * 60 * 1000 毫秒）
    if (!lastFetchTime || now - parseInt(lastFetchTime) > 24 * 60 * 60 * 1000) {
      const { data } = await axios.get("/api/get_pig_timestamp");

      // 存储时间戳和最后获取时间
      localStorage.setItem("pigTimestamp", data.pig_timestamp.toString());
      localStorage.setItem("lastPigTimestampFetch", now.toString());

      console.log("成功获取新的pig_timestamp:", data.pig_timestamp);
    } else {
      console.log("使用缓存的pig_timestamp");
    }
  } catch (error) {
    console.error("获取pig_timestamp失败:", error);
    ElMessage.error("野猪跑路了，服务遇到问题");
  }
};

onMounted(async () => {
  await fetchPigTimestamp(); // 确保在组件挂载时获取时间戳
});

const handleSend = async () => {
  // 保存输入的文本，避免后续清空操作影响
  const inputValue = inputText.value.trim();
  if (inputValue) {
    // step1 getpigtime
    try {
      // 每次都获取最新的时间戳
      const { data } = await axios.get("/api/get_pig_timestamp");
      const timestamp = data.pig_timestamp.toString();
      if (!timestamp) {
        ElMessage.error("野猪跑路了，服务遇到问题");
        return;
      }

      // step2 checkstr
      const response = await axios.post("/api/str_operation", {
        input_str: inputValue,
      });

      // 从响应中获取 result 字段
      const result = response.data.result;

      if (result === "encrypt") {
        // 字符串不包含字典里emoji的情况
        console.log("字符串不包含字典里emoji，需要进行加密操作");

        // step3 push send_str
        messages.value.push({
          content: inputValue,
          isEmoji: false,
          time: getCurrentTime(),
          canConvert: true,
          isUser: true,
        });
        canConvert.value = true;
        selectedIndex.value = -1;
        inputText.value = ""; // 清空输入框
        scrollToBottom();

        // step4 change
        const { data } = await axios.post("/api/utf8_to_emoji", {
          utf8_str: inputValue,
          timestamp: timestamp,
          password: props.apiKey,
        });

        console.log("接口返回的数据:", data); // 打印接口返回的数据

        // step5 push rec_str
        if (data && data.result) {
          const newMessage = {
            content: data.result,
            isEmoji: true,
            time: getCurrentTime(),
            canConvert: true,
            isUser: false,
          };
          messages.value.push(newMessage);
          console.log("添加的新消息:", newMessage);
          scrollToBottom();
        } else {
          console.error("接口返回数据格式错误:", data);
        }
      } else if (result === "decrypt") {
        // 字符串全由字典里emoji组成的情况
        console.log("字符串全由字典里emoji组成，需要进行解密操作");

        // step3 push send_str
        messages.value.push({
          content: inputValue,
          isEmoji: false,
          time: getCurrentTime(),
          canConvert: true,
          isUser: true,
        });
        canConvert.value = true;
        selectedIndex.value = -1;
        inputText.value = ""; // 清空输入框
        scrollToBottom();

        // step4 change
        const { data } = await axios.post("/api/emoji_to_utf8", {
          emoji_str: inputValue,
          timestamp: timestamp,
          password: props.apiKey,
        });

        console.log("接口返回的数据:", data); // 打印接口返回的数据
        if (data && data.result === "") {
          ElMessage.error("野猪不会，时间或密钥错误");
          messages.value.pop();
          // 可根据需要滚动到合适的位置，这里简单处理为滚动到倒数第二条消息
          scrollToBottom();
        } else {
          // step5 push rec_str
          if (data && data.result) {
            const newMessage = {
              content: data.result,
              isEmoji: true,
              time: getCurrentTime(),
              canConvert: true,
              isUser: false,
            };
            messages.value.push(newMessage);
            console.log("添加的新消息:", newMessage);
            scrollToBottom();
          } else {
            console.error("接口返回数据格式错误:", data);
          }
        }
        // 这里可以添加解密相关的逻辑，如果有的话
      } else {
        // 其他情况，视为异常
        ElMessage.error("野猪看不懂，去除emoji试试");

        return;
      }
    } catch (error) {
      console.error("转换失败:", error);
      ElMessage.error("野猪跑路了，服务遇到问题");
    }
  }
};

const handleMessageClick = (index) => {
  if (!canSelect.value) return;
  selectedIndex.value = selectedIndex.value === index ? -1 : index;

  // 复制消息内容到剪贴板
  const messageToCopy = messages.value[index].content;
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(messageToCopy)
      .then(() => {
        ElMessage.success("已复制");
      })
      .catch((err) => {
        console.error("复制失败:", err);
      });
  } else {
    // 对于不支持 navigator.clipboard 的浏览器，可以使用 document.execCommand('copy')
    const textarea = document.createElement("textarea");
    textarea.value = messageToCopy;
    textarea.style.position = "fixed";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      ElMessage.success("已复制");
    } catch (err) {
      console.error("复制失败:", err);
    } finally {
      document.body.removeChild(textarea);
    }
  }
};

const scrollToBottom = () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  }, 100);
};

watch(
  messages,
  () => {
    scrollToBottom();
  },
  { deep: true }
);
</script>
  
  <style scoped>
/* 隐藏页面滚动条 */
body {
  -ms-overflow-style: none; /* IE 和 Edge */
  scrollbar-width: none; /* Firefox */
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
  -ms-overflow-style: none; /* IE 和 Edge */
  scrollbar-width: none; /* Firefox */
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
  -ms-overflow-style: none; /* IE 和 Edge */
  scrollbar-width: none; /* Firefox */
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

.message-item.selectable .message-content:hover {
  opacity: 0.8;
  transform: scale(1.02);
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
  -ms-overflow-style: none; /* IE 和 Edge */
  scrollbar-width: none; /* Firefox */

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
  background: #ffe5e5;
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
  content: "";
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