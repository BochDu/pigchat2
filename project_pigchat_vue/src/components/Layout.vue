<template>
  <div class="layout">
    <header class="header">
      <div class="header-left">
        <img src="../assets/wild_boar.png" alt="PigChat Logo" class="logo" />
        <h1 class="title">PigChat</h1>
      </div>
      <div class="header-right">
        <!-- 密钥输入框 -->
        <el-input
          v-model="apiKey"
          placeholder="请输入私人密钥..."
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
import { ref, watch } from "vue";

const apiKey = ref(localStorage.getItem("apiKey") || "");
// 新增一个响应式变量来记录是否正在输入
const isInputting = ref(false);

// 监听 apiKey 变化并保存到 localStorage
watch(apiKey, (newValue) => {
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

.api-key-input {
  width: 320px;
}

.api-key-input :deep(.el-input__wrapper) {
  /* 设置统一的背景色 */
  background-color: rgb(224, 224, 224);
  border-radius: 50px;
  padding: 8px 16px;
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
  font-size: 14px;
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
  font-size: 14px;
  margin-right: 8px;
}

.api-key-input :deep(.view-icon) {
  color: #999;
  font-size: 16px;
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

  .api-key-input {
    width: 240px;
  }

  .api-key-input :deep(.el-input__wrapper) {
    padding: 6px 12px;
  }

  .api-key-input :deep(.view-icon) {
    font-size: 14px;
  }
}
</style>