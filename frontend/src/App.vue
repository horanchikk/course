<template>
  <div class="w-screen h-screen flex flex-col bg-black bg-opacity-80 text-white text-xl">
    <header class="w-full py-3 px-6 flex justify-between items-center">
      <router-link to="/" class="text-3xl text-red-500 hover:text-red-600 transition-all" active-class="text-red-700">NeNetFlix</router-link>
      <nav class="flex gap-5 items-center">
        <router-link to="/about" class="hover:text-red-600 transition-all" active-class="text-red-400">О нас</router-link>
        <router-link to="/place" class="hover:text-red-600 transition-all" active-class="text-red-400">Где нас найти?</router-link>
        <router-link to="/auth" v-if="ui.user.access_token === undefined">
          <Button color="primary">Вход и регистрация</Button>
        </router-link>
        <router-link to="/account" v-if="ui.user.access_token !== undefined">
          <Button>Аккаунт</Button>
        </router-link>
      </nav>
    </header>
    <main class="flex-auto overflow-y-scroll text-white text-xl hideScroll">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Button from './components/button-ui.vue';
import { ui } from './store'
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
