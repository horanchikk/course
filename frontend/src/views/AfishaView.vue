<template>
  <main v-if="!items" class="w-full h-full flex items-center justify-center text-3xl font-bold">
    Загрузка...
  </main>
  <main v-else class="h-full w-full flex">
    <div class="h-full flex flex-col p-6">
      <label for="sort-by" class="text-white">Сортировать по</label>
      <select v-model="sortBy" id="sort-by" class="outline-none rounded-lg px-2 py-4 mt-2 text-white bg-black bg-opacity-40 focus:bg-opacity-60 transition-all">
        <option value="byDate">по дате показа</option>
        <option value="byName">по наименованию</option>
        <option value="byAge">по возрастному цензу</option>
      </select>
    </div>
    <div class="grid grid-cols-4 gap-10 p-6 overflow-y-scroll hideScroll">
      <section 
        v-for="item in items" 
        :key="item.id"
        @click="router.push(`/film/${item.id}`)"
        class="w-fit p-3 flex flex-col bg-black bg-opacity-10 cursor-pointer rounded-md border-[1px] border-opacity-20 
        hover:bg-opacity-30 hover:border-opacity-90 transition-all select-none"
      >
      <img 
        :src="`http://localhost:8000/assets/${item.imageUrl}`" 
        :alt="item.title"
        class="rounded-lg pointer-events-none"  
      >
      <div class="flex-auto flex flex-col items-center justify-between py-2">
        <p class="text-sm font-bold">{{ item.title }}</p>
        <div class="w-full flex justify-between gap-10">
          <p>{{ item.price }}₽</p>
          <p>{{ item.age_limit }}+</p>
        </div>
        <p class="text-sm">{{ getDate(item.date) }}</p>
        <div v-if="item.genres">
          <p class="text-sm font-bold mt-2">
            {{ item.genres.response.items.join(', ') === '' ? 'Жанр не указан' : item.genres.response.items.join(', ') }}
          </p>
        </div>
      </div>
    </section>
  </div>
  </main>
</template>

<script setup>
import router from '@/router';
import {onMounted, ref, watch} from 'vue';

const items = ref(undefined);
const sortBy = ref('byDate');

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
    items.value.sort((next, prev) => {return prev.age_limit - next.age_limit})
  } else if (sortBy.value === 'byDate') {
    items.value.sort((next, prev) => {return next.date - prev.date})
  }
})

function getDate(input) {
  let formatDate = new Date(input * 1000);
  let date = formatDate.getDate();

  let months = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря',
  ];
  let month = months[formatDate.getMonth()];

  return `${date} ${month}`;
}

onMounted(async () => {
  let response = await fetch('http://localhost:8000/session/')
  let currentDate = Math.floor(new Date().getTime() / 1000); // get unix time in SECONDS

  if (response.ok) {
    let json = await response.json();
    items.value = json.response.items;
    items.value.sort((next, prev) => {return next.date - prev.date});

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
#sort-by > option {
  text-align: center;
}
</style>