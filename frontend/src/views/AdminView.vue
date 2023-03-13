<template>
    <main class="w-full h-full flex flex-col items-center gap-5">
        <nav class="flex gap-3">
            <Button @click="screen = 0" :color="screen === 0 ? 'primary' : 'warning'" class="py-1 px-4">Заказы</Button>
            <Button @click="screen = 1" :color="screen === 1 ? 'primary' : 'warning'" class="py-1 px-4">Сеансы</Button>
            <Button @click="screen = 2" :color="screen === 2 ? 'primary' : 'warning'" class="py-1 px-4">Жанры</Button>
        </nav>
        <div class="flex-auto w-full flex flex-col p-5">
            <section class="flex-auto flex items-center justify-center show-up" v-if="screen === 0">
                Заказы
            </section>
            <section class="flex-auto flex items-center justify-center show-up" v-if="screen === 1">
                Сеансы
            </section>
            <section class="flex-auto flex items-center justify-center show-up" v-if="screen === 2">
                Жанры
            </section>
            <div class="w-full flex justify-end">
                <Button @click="logout()" color="error">Выйти из аккаунта</Button>
            </div>
        </div>
    </main>
</template>

<script setup>
import Button from '@/components/button-ui.vue';
import router from '@/router';
import { ui } from '@/store';
import { ref } from 'vue';

const screen = ref(0);

function logout() {
    ui.user.access_token = undefined;
    ui.user.info = undefined;
    router.push('/about')
}
</script>