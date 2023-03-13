<template>
    <main v-if="!currentFilm" class="w-full h-full flex items-center justify-center">
        Загрузка...
    </main>
    <main v-else class="w-full h-full flex flex-col p-20 show-up">
        <div class="w-full flex px-3">
            <Button color="warning" class="text-sm" @click="router.push('/')">На главную</Button>
        </div>
        <section class="w-full p-3 flex gap-5 select-none">
            <img :src="`http://localhost:8000/assets/${currentFilm.imageUrl}`" :alt="currentFilm.title"
                class="rounded-lg pointer-events-none">
            <div class="flex-auto flex flex-col text-start gap-5 p-2">
                <p class="text-5xl font-bold">{{ currentFilm.title }}</p>
                <div class="w-full flex gap-10">
                    <p>{{ currentFilm.price }}₽</p>
                    <p>{{ currentFilm.age_limit }}+</p>
                </div>
                <p class="text-sm">{{ ui.getDate(currentFilm.date) }}</p>
                <p class="text-sm">{{ currentFilm.description }}</p>
                <div v-if="currentFilm.genres" class="flex flex-col gap-5 w-fit">
                    <p class="text-sm font-bold mt-2">
                        {{ currentFilm.genres.response.items.join(', ') === '' ? 'Жанр не указан' :
                            currentFilm.genres.response.items.join(', ') }}
                    </p>
                    <Button v-if="ui.user.access_token" color="primary" class="text-sm mt-5"
                        @click="buyTicket(currentFilm.id)">
                        В корзину</Button>
                    <Button v-else @click="router.push('/auth')" class="text-sm mt-5">Войдите, чтобы приобрести
                        билет</Button>
                    <Transition name="fade">
                        <div v-if="popup.show && popup.id === currentFilm.id"
                            :class="`my-4 p-2 w-full text-center text-sm border-[1px] ${popup.type === 'error' ? 'border-red-600' : 'border-green-600'} rounded-lg`">
                            {{ popup.text }}
                        </div>
                    </Transition>
                </div>
            </div>
        </section>
    </main>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';

import { ui } from '@/store'

import router from '../router'
import Button from '@/components/button-ui.vue';

const currentFilm = ref(undefined);

const popup = reactive({
    id: undefined,
    show: false,
    text: "",
    type: undefined,
})

function showPopup(id, text, type) {
    popup.id = id;
    popup.text = text;
    popup.type = type;
    popup.show = true;

    setTimeout(() => {
        popup.show = false;
    }, 2000);
}

async function buyTicket(session_id, user_id = ui.user.info.id) {
    let response = await fetch(`http://localhost:8000/user/addToCart${user_id}?session_id=${session_id}`, {
        method: "PATCH"
    })

    if (response.ok) {
        let responseJson = await response.json();
        if (responseJson.error) {
            showPopup(
                session_id,
                responseJson.error === 'session tickets is ended' ? 'Билеты закончились' : popup.text,
                'error'
            )
        } else {
            showPopup(session_id, 'Билет успешно приобретён', 'success')
        }
    }
}

onMounted(async () => {
    let response = await fetch(`http://localhost:8000/session/id${router.currentRoute.value.params.id}`)

    if (response.ok) {
        let json = await response.json();

        currentFilm.value = json.response;

        let res_genres = await fetch(`http://localhost:8000/session/genres${router.currentRoute.value.params.id}`);
        if (res_genres.ok) {
            let json = await res_genres.json();
            currentFilm.value['genres'] = json;
        }
    }
});
</script>