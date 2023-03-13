<template>
    <main v-if="cartInfo !== undefined" class="w-full h-full flex flex-col p-5 show-up">
        <div class="flex-auto flex flex-col gap-4 p-5">
            <div class="flex-auto bg-black bg-opacity-20 rounded-lg overflow-y-scroll hideScroll">
                {{ cartInfo.items }}
            </div>
            <div class="w-full flex justify-between cursor-default">
                <p>Стоимость: {{ cartInfo.price }} рублей</p>
                <p>Количество билетов: {{ cartInfo.size }}</p>
            </div>
        </div>
        <div class="w-full flex justify-end">
            <Button color="error" @click="logout()">Выйти из аккаунта</Button>
        </div>
    </main>
    <main v-else class="w-full h-full flex items-center justify-center show-left">
        Загрузка...
    </main>
</template>

<script setup>
import Button from '@/components/button-ui.vue';
import { ui } from '@/store';
import { onMounted, ref } from 'vue';
import router from '@/router';

function logout() {
    ui.user.access_token = undefined;
    ui.user.info = undefined;
    router.push('/about')
}

const cartInfo = ref(undefined);

onMounted(async () => {
    let cart = await fetch(`http://localhost:8000/user/cart?access_token=${ui.user.access_token}`)
    if (cart.ok) {
        const cartJson = await cart.json();
        cartInfo.value = cartJson.response;
    }
})
</script>