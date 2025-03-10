<template>
  <Layout>
    <div class="chat-container">
      <div class="chat-card">
        <div class="logo-section">
          <img src="../assets/wild_boar.png" alt="PigChat Logo" class="main-logo">
          <h2 class="welcome-text">开始一个新的加密聊天</h2>
        </div>
        
        <div class="form-section">
          <el-form :model="form" class="chat-form">
            <el-form-item>
              <el-input
                v-model="form.privateKey"
                placeholder="请输入私钥"
                :prefix-icon="Key"
                clearable
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" class="start-button" round @click="startChat">
                开始聊天
                <el-icon class="el-icon--right"><ArrowRight /></el-icon>
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref } from 'vue'
import { Key, ArrowRight } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import Layout from '../components/Layout.vue'

const router = useRouter()
const form = ref({
  privateKey: ''
})

const startChat = () => {
  if (form.value.privateKey.trim()) {
    router.push('/chat')
  } else {
    ElMessage.warning('请输入私钥')
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
}

.chat-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  width: 100%;
  max-width: 480px;
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.main-logo {
  width: 120px;
  height: 120px;
  margin-bottom: 1.5rem;
}

.welcome-text {
  color: #303133;
  font-size: 1.5rem;
  margin: 0;
  font-weight: 600;
}

.chat-form {
  width: 100%;
}

.start-button {
  width: 100%;
  height: 44px;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .chat-card {
    padding: 2rem;
    margin: 1rem;
  }

  .main-logo {
    width: 100px;
    height: 100px;
  }

  .welcome-text {
    font-size: 1.2rem;
  }
}
</style> 