<template>
  <div class="layout">
    <header class="header">
      <div class="header-left">
        <img
          src="../assets/wild_boar.png"
          alt="PigChat Logo"
          class="logo"
          @click="handleClick"
          style="user-select: none"
        />
        <h1 class="title" @click="handleClick">PigChat</h1>
        <div class="date-container">
          <span class="time">{{ currentDate }}</span>
        </div>
      </div>
      <div class="header-right">
        <!-- 密钥输入框 -->
        <el-input
          v-model="apiKey"
          placeholder="Enter your private key"
          clearable
          class="api-key-input"
        >
        </el-input>
      </div>
    </header>
    <!-- 新增显示信息的区域，添加 @click 事件 -->
    <transition name="message-box-fade">
      <div
        :class="{ 'message-box': true, 'message-box--visible': showMessage }"
        @click="handleMessageBoxClick"
      >
        <div v-html="formattedMessages"></div>
      </div>
    </transition>
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>
  
  <script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
import moment from "moment";

const apiKey = ref(localStorage.getItem("apiKey") || "");
const currentDate = ref("");
const showMessage = ref(false);
const messages = ref([
  {
    title: "产品介绍",
    content: [
      "PigChat 是一款提供特殊编码服务的程序",
      "私人密钥和当天日期定制的编码算法遥遥领先",
    ],
  },
  {
    title: "使用指南",
    content: [
      "- 建议填入密钥并妥善保管",
      "- 输入原文或密文发送",
      "- 点击消息框自动复制信息",
      "- 密文仅支持当天日期内解密",
    ],
  },
  {
    title: "免责声明",
    content: [
      "本站仅提供编码服务，严禁参与违法活动或滥用",
      "禁止一切网络入侵、数据窃取等网络非法活动",
      "继续使用本站，即表示您同意遵守以上声明和条款",
    ],
  },
  {
    title: "项目介绍",
    content: [
      "项目代号 <野猪聊天> ",
      "经历多轮方案讨论和产品迭代",
      "于2025年3月15日正式部署上线",
      'Github仓库 <a href="https://github.com/BochDu/pigchat2">https://github.com/BochDu/pigchat2</a>',
    ],
  },
  {
    title: "贡献个人及企业",
    content: [
      "BochDu、quaeast、SyZdog",
      'SIB集团 <a href="https://sicp.online">https://sicp.online</a>',
    ],
  },
]);

const formattedMessages = ref("");

const getCurrentDate = async () => {
  try {
    const { data } = await axios.get("/api/pigtime");
    const timestamp = data.pigtime.toString();
    if (!timestamp) {
      ElMessage.error("野猪跑路了，服务遇到问题");
      return;
    }
    const date = new Date(parseInt(timestamp) * 1000);
    currentDate.value = moment(date).format("DD MMM");
  } catch (error) {
    ElMessage.error("野猪跑路了，服务遇到问题");
    console.error(error);
  }
};

onMounted(async () => {
  await getCurrentDate();
  formattedMessages.value = messages.value
    .map(
      (item) => `
        <h3>${item.title}</h3>
        <p>${item.content.map((line) => line + "<br>").join("")}</p>
      `
    )
    .join("");
});

watch(apiKey, (newValue, oldValue) => {
  console.log(`API Key 已更新，旧值: ${oldValue}，新值: ${newValue}`);
  localStorage.setItem("apiKey", newValue);
});

// 点击事件处理函数
const handleClick = () => {
  console.log("你点击了 PigChat 标题或图标");
  showMessage.value = !showMessage.value;
};

// 点击介绍容器的处理函数
const handleMessageBoxClick = (event) => {
  if (event.target.tagName === "A") {
    return;
  }
  showMessage.value = false;
};
</script>
  
  <style scoped>
/* 样式部分保持不变 */
.layout {
  min-height: 100vh;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.header {
  background: white;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 100;
  flex-shrink: 0;
  height: 64px;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-right {
  display: flex;
  align-items: center;
}

.logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
  cursor: pointer;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  cursor: pointer;
  /* 禁止选中文本 */
  user-select: none;
}

.date-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 0.8rem;
  line-height: 1;
  margin-top: 0.3rem;
}

.time {
  color: #666;
  text-align: center;
  /* 禁止选中文本 */
  user-select: none;
}

.api-key-input {
  width: 320px;
  height: 36px;
}

.api-key-input :deep(.el-input__wrapper) {
  background-color: rgb(224, 224, 224);
  border-radius: 50px;
  padding: 6px 16px;
  box-shadow: none !important;
  border: 1px solid transparent;
}

.api-key-input :deep(.el-input__wrapper:hover) {
  background-color: rgb(224, 224, 224);
}

.api-key-input :deep(.el-input__wrapper.is-focus) {
  background-color: rgb(224, 224, 224);
  border-color: #e0e0e0;
}

.api-key-input :deep(.el-input__inner) {
  color: #666;
  font-size: 13px;
}

/* 禁止选择占位符文本 */
.api-key-input :deep(.el-input__inner::placeholder) {
  user-select: none;
}

.api-key-input :deep(.el-input__inner::placeholder) {
  color: #999;
}

.api-key-input :deep(.el-input__suffix) {
  display: inline-flex;
  align-items: center;
}

.api-key-input :deep(.el-input__clear) {
  color: #999;
  font-size: 13px;
  margin-right: 8px;
}

.api-key-input :deep(.view-icon) {
  color: #999;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
}

.api-key-input :deep(.view-icon:hover) {
  color: #666;
}

.main-content {
  flex: 1;
  background: #f5f7fa;
  position: relative;
  overflow-y: auto;
  height: calc(100vh - 64px);
  box-sizing: border-box;
}

.message-box {
  display: none;
  background-color: #ffffff;
  position: absolute;
  top: 64px; /* 状态栏高度 */
  left: 0;
  right: 0;
  bottom: 0;
  padding: 20px;
  text-align: left; /* 修改为左对齐 */
  font-size: 14px;
  border-bottom: 1px solid #ccc;
  z-index: 99; /* 确保在内容之上 */
  color: #333; /* 字体颜色改为黑色 */
  font-family: Arial, sans-serif; /* 选择一个好看的字体 */
  line-height: 1.6; /* 增加行间距 */
  letter-spacing: 0.5px; /* 增加字间距 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.message-box h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #007bff;
}

.message-box p {
  margin-top: 0;
  margin-bottom: 20px;
}

.message-box--visible {
  display: block;
}

.message-box-fade-enter-active,
.message-box-fade-leave-active {
  transition: opacity 0.3s;
}

.message-box-fade-enter,
.message-box-fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header {
    padding: 0.75rem;
    height: 56px;
  }

  .main-content {
    height: calc(100vh - 56px);
  }

  .title {
    font-size: 1.1rem;
  }

  .date-container {
    font-size: 0.7rem;
  }

  .api-key-input {
    width: 100%;
    height: 40px;
  }

  .api-key-input :deep(.el-input__wrapper) {
    padding: 8px 16px;
  }

  .api-key-input :deep(.view-icon) {
    font-size: 14px;
  }

  .message-box {
    top: 56px; /* 小屏幕状态栏高度 */
    padding: 15px;
  }
}
</style>