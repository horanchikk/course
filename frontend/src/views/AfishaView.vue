<template>
  <main v-if="!items" class="w-full h-full flex items-center justify-center text-3xl font-bold">
    Загрузка...
  </main>
  <main v-else class="h-full w-full flex show-left">
    <div class="h-full flex flex-col p-6">
      <label for="sort-by" class="text-white">Сортировать по</label>
      <select v-model="sortBy" id="sort-by"
        class="outline-none rounded-lg px-2 py-4 mt-2 text-white bg-black bg-opacity-40 focus:bg-opacity-60 transition-all">
        <option value="byDate">по дате показа</option>
        <option value="byName">по наименованию</option>
        <option value="byAge">по возрастному цензу</option>
      </select>
    </div>
    <div class="grid grid-cols-4 gap-10 p-6 overflow-y-scroll hideScroll">
      <section v-for="item in items" :key="item.id" class="w-fit p-3 flex flex-col bg-black bg-opacity-10 cursor-default rounded-md border-[1px] border-opacity-20 
                hover:bg-opacity-30 hover:border-opacity-90 transition-all select-none">
        <img :src="`http://localhost:8000/assets/${item.imageUrl}`" :alt="item.title"
          @click="router.push(`/film/${item.id}`)" class="rounded-lg cursor-pointer hover:scale-105 transition-all">
        <div class="flex-auto flex flex-col items-center justify-between py-2">
          <p class="text-sm font-bold">{{ item.title }}</p>
          <div class="w-full flex justify-between gap-10">
            <p>{{ item.price }}₽</p>
            <p>{{ item.age_limit }}+</p>
          </div>
          <p class="text-sm">{{ ui.getDate(item.date) }}</p>
          <div v-if="item.genres">
            <p class="text-sm font-bold mt-2">
              {{ item.genres.response.items.join(', ') === '' ? 'Жанр не указан' : item.genres.response.items.join(', ')
              }}
            </p>
          </div>
          <Button v-if="ui.user.access_token" color="primary" class="text-sm mt-5" @click="buyTicket(item.id)">В
            корзину</Button>
          <Button v-else @click="router.push('/auth')" class="text-sm mt-5">Войдите, чтобы приобрести билет</Button>
          <Transition name="fade">
            <div v-if="popup.show && popup.id === item.id"
              :class="`my-4 w-full text-center text-sm border-[1px] ${popup.type === 'error' ? 'border-red-600' : 'border-green-600'} rounded-lg`">
              {{ popup.text }}
            </div>
          </Transition>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';

import Button from '@/components/button-ui.vue';
import router from '@/router';
import { ui } from '@/store';
import { reactive } from 'vue'

const items = ref(undefined);
const sortBy = ref('byDate');
const popup = reactive({
  id: undefined,
  show: false,
  text: "",
  type: undefined,
})

watch(() => sortBy.value, () => {
  if (sortBy.value === 'byName') {
    items.value.sort(function (prev, next) {
      if (prev.title.toLowerCase() < next.title.toLowerCase()) {
        return -1;
      }
      if (prev.title.toLowerCase() > next.title.toLowerCase()) {
        return 1;
      }
      return 0;
    })
  } else if (sortBy.value === 'byAge') {
    items.value.sort((next, prev) => { return prev.age_limit - next.age_limit })
  } else if (sortBy.value === 'byDate') {
    items.value.sort((next, prev) => { return next.date - prev.date })
  }
})

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

function showPopup(id, text, type) {
  popup.id = id;
  popup.text = text;
  popup.type = type;
  popup.show = true;

  setTimeout(() => {
    popup.show = false;
  }, 2000);
}

onMounted(async () => {
  let response = await fetch('http://localhost:8000/session/?count=100')
  let currentDate = Math.floor(new Date().getTime() / 1000); // get unix time in SECONDS

  if (response.ok) {
    let json = await response.json();
    items.value = json.response.items;
    items.value.sort((next, prev) => { return next.date - prev.date });

    items.value.forEach(async (item) => {
      if (item.date < currentDate) {
        items.value = items.value.filter((currentItem) => currentItem !== item)
      } else {
        let response = await fetch(`http://localhost:8000/session/genres${item.id}`);
        if (response.ok) {
          let json = await response.json();
          item['genres'] = json;
        }
      }
    })
  }
});
</script>

<style>
#sort-by>option {
  text-align: center;
}
</style>