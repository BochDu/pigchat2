<template>
  <div class="layout">
    <header class="header">
      <div class="header-left">
        <img src="../assets/wild_boar.png" alt="PigChat Logo" class="logo" />
        <h1 class="title">PigChat</h1>
        <!-- 新增日期显示元素 -->
        <div class="date-container">
          <span class="year">{{ currentYear }}</span>
          <span class="month-day"
            >{{ currentMonth }}<span class="day">{{ currentDay }}</span></span
          >
        </div>
      </div>
      <div class="header-right">
        <!-- 密钥输入框 -->
        <el-input
          v-model="apiKey"
          placeholder="Enter your private key"
          :type="isInputting ? 'text' : 'password'"
          clearable
          class="api-key-input"
          @focus="isInputting = true"
          @blur="isInputting = false"
        >
        </el-input>
      </div>
    </header>
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";

const apiKey = ref(localStorage.getItem("apiKey") || "");
// 新增一个响应式变量来记录是否正在输入
const isInputting = ref(false);
// 新增响应式变量来存储当前日期的各个部分
const currentYear = ref("");
const currentMonth = ref("");
const currentDay = ref("");

// 获取当前日期并格式化
const getCurrentDate = async () => {
  try {
    const { data } = await axios.get("/api/get_pig_timestamp");
    const timestamp = data.pig_timestamp.toString();
    if (!timestamp) {
      ElMessage.error("野猪跑路了，服务遇到问题");
      return;
    }
    const date = new Date(parseInt(timestamp) * 1000);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    currentYear.value = year;
    currentMonth.value = month;
    currentDay.value = day;
  } catch (error) {
    ElMessage.error("野猪跑路了，服务遇到问题");
    console.error(error);
  }
};

onMounted(async () => {
  // 挂载时获取当前日期
  await getCurrentDate();
});

// 监听 apiKey 变化并保存到 localStorage，同时增加日志输出
watch(apiKey, (newValue, oldValue) => {
  console.log(`API Key 已更新，旧值: ${oldValue}，新值: ${newValue}`);
  localStorage.setItem("apiKey", newValue);
});
</script>

<style scoped>
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
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 新增日期样式 */
.date-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 0.8rem;
  line-height: 1;
  margin-left: 0.5rem;
  /* 新增：设置固定宽度 */
  width: 60px;
}

.year {
  color: #666;
  /* 新增：文本居中 */
  text-align: center;
}

.month-day {
  color: #999;
  text-align: center;
}

.day {
  margin-left: 0px;
}

.api-key-input {
  width: 320px;
  /* 新增：调整输入框高度 */
  height: 36px;
}

.api-key-input :deep(.el-input__wrapper) {
  /* 设置统一的背景色 */
  background-color: rgb(224, 224, 224);
  border-radius: 50px;
  /* 调整内边距让输入框更精致 */
  padding: 6px 16px;
  box-shadow: none !important;
  border: 1px solid transparent;
}

/* 去除 hover 状态的背景色变化 */
.api-key-input :deep(.el-input__wrapper:hover) {
  background-color: rgb(224, 224, 224);
}

/* 去除 focus 状态的背景色变化 */
.api-key-input :deep(.el-input__wrapper.is-focus) {
  background-color: rgb(224, 224, 224);
  border-color: #e0e0e0;
}

.api-key-input :deep(.el-input__inner) {
  color: #666;
  /* 调整字体大小 */
  font-size: 13px;
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

  /* 调整日期样式在小屏幕下的表现 */
  .date-container {
    font-size: 0.7rem;
  }

  .api-key-input {
    /* 增大输入框宽度，方便手机用户输入 */
    width: 100%;
    /* 调整输入框高度，增大触摸区域 */
    height: 40px;
  }

  .api-key-input :deep(.el-input__wrapper) {
    padding: 8px 16px;
  }

  .api-key-input :deep(.view-icon) {
    font-size: 14px;
  }
}
</style>