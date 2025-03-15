<script setup>
</script>

<template>
  <router-view></router-view>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
/* 解决 iOS 输入框点击后自动放大的问题 */
input, textarea {
  font-size: 16px !important;
}

html {
  -webkit-text-size-adjust: 100%; /* 禁止 iOS Safari 自动调整文本大小 */
}
</style>
