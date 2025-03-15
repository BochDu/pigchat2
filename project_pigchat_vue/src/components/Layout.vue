<template>
  <div class="layout">
    <header class="header">
      <div class="header-left" @click="goToSICP">
        <img src="../assets/wild_boar.png" alt="PigChat Logo" class="logo">
        <h1 class="title">PigChat</h1>
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
});

watch(apiKey, (newValue, oldValue) => {
  console.log(`API Key 已更新，旧值: ${oldValue}，新值: ${newValue}`);
  localStorage.setItem("apiKey", newValue);
});

const goToSICP = () => {
  window.open("https://sicp.online", "_blank");
}

</script>

<style scoped>
/* 原有的样式代码保持不变 */
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
  cursor: pointer;
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
}
</style>