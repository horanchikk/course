<template>
  <div class="w-full h-full flex items-center justify-center">
    <!-- Authorization -->
    <form v-if="auth.screen === 1" @submit.prevent=""
      class="p-5 rounded-lg border-[1px] border-white flex flex-col gap-3 items-center show-up">
      <p>Вход</p>

      <Input type="text" v-model="auth.login" placeholder="Логин" />
      <Input type="password" v-model="auth.password" placeholder="Пароль" />

      <div class="w-full py-2 text-center text-sm border-[1px] rounded-lg border-red-700 border-opacity-70"
        v-if="auth.error">{{ auth.error }}</div>

      <Button color="primary" type="submit" class="text-sm py-1 px-4"
        @click="Authorization.login()">Авторизироваться</Button>
      <Button color="error" class="text-sm py-1 px-4" @click="setScreen(2)">Нет аккаунта?</Button>
    </form>

    <!-- Registration -->
    <form v-if="auth.screen === 2" @submit.prevent=""
      class="p-5 rounded-lg border-[1px] border-white flex flex-col gap-3 items-center show-up">
      <p>Регистрация</p>

      <Input type="text" v-model="auth.name" placeholder="Имя" />
      <Input type="text" v-model="auth.surname" placeholder="Фамилия" />
      <Input type="text" v-model="auth.patronymic" placeholder="Отчество" />

      <Input type="email" v-model="auth.email" placeholder="Почта" />
      <Input type="text" v-model="auth.login" placeholder="Логин" />
      <Input type="password" v-model="auth.password" placeholder="Пароль" />
      <Input type="password" v-model="auth.password_repeat" placeholder="Повторите пароль" />

      <div class="w-full py-2 text-center text-sm border-[1px] rounded-lg border-red-700 border-opacity-70"
        v-if="auth.error">{{ auth.error }}</div>

      <Button color="warning" type="submit" class="text-sm py-1 px-4"
        @click="Authorization.reg()">Зарегистрироваться</Button>
      <Button color="primary" class="text-sm py-1 px-4" @click="setScreen(1)">Есть аккаунт?</Button>
    </form>

  </div>
</template>

<script setup>
import Button from '@/components/button-ui.vue';
import Input from '@/components/input-ui.vue'

import { reactive } from 'vue';
import { ui } from '../store/index';
import router from '@/router';

const auth = reactive({
  screen: 1,
  login: "",
  password: "",
  password_repeat: "",
  rules: false,
  name: "",
  surname: "",
  patronymic: "",
  email: "",
  error: undefined
})

function setScreen(screen) {
  // reset all states
  auth.screen = screen;

  auth.login = "";
  auth.password = "";
  auth.password_repeat = "";
  auth.name = "";
  auth.surname = "";
  auth.patronymic = "";
  auth.email = "";
  auth.rules = false;
}

const Authorization = {
  async login() {
    let response = await fetch(`http://127.0.0.1:8000/user/login?login=${auth.login}&password=${auth.password}`);

    if (response.ok) {
      let json = await response.json();

      try {
        ui.user.access_token = json.response.access_token
        let info = await fetch(`http://127.0.0.1:8000/user/?access_token=${json.response.access_token}`)
        if (info.ok) {
          const infoJson = await info.json();
          ui.user.info = infoJson.response;
          router.push('/');
        }
      } catch (e) {
        auth.error = json[0];
      }
    }
  },

  async reg() {
    let response = await fetch(`http://127.0.0.1:8000/user/reg`, {
      method: "POST",
      body: JSON.stringify({
        role: 3,
        login: auth.login,
        password: auth.password,
        password_repeat: auth.password_repeat,
        name: auth.name,
        surname: auth.surname,
        patronymic: auth.patronymic,
        email: auth.email,
      }),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    });

    if (response.ok) {
      let json = await response.json();

      try {
        ui.user.access_token = json.response.access_token;
        let info = await fetch(`http://127.0.0.1:8000/user/?access_token=${json.response.access_token}`);
        if (info.ok) {
          const infoJson = await info.json();
          ui.user.info = infoJson.response;
          router.push('/');
        }
      } catch (e) {
        auth.error = json;
      }
    } else {
      let json = await response.json();
      auth.error = json.detail;
    }
  }
}
</script>