<template>
  <div class="w-screen h-screen flex flex-col bg-black bg-opacity-80 text-white text-xl">
    <header class="w-full py-3 px-6 flex justify-between items-center">
      <router-link to="/" class="text-3xl text-red-600 hover:text-red-700 transition-all">NeNetFlix</router-link>
      <nav class="flex gap-5 items-center">
        <router-link to="/about" class="hover:text-red-600 transition-all">О нас</router-link>
        <router-link to="/afisha" class="hover:text-red-600 transition-all">Афиша</router-link>
        <router-link to="/place" class="hover:text-red-600 transition-all">Где нас найти?</router-link>
        <router-link to="auth">
          <Button type="primary">Вход и регистрация</Button>
        </router-link>
      </nav>
    </header>
    <main class="flex-auto overflow-y-scroll text-white text-xl hideScroll">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Button from './components/button-ui.vue'
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.hideScroll::-webkit-scrollbar {
  width: 0;
}
</style>
