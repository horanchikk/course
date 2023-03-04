<template>
  <div class="w-full h-full flex items-center justify-center text-3xl font-bold" v-if="!items">
    Загрузка...
  </div>
  <div class="h-full py-16 px-6 grid grid-cols-2 gap-10" v-else>
    <section class="w-fit p-3 flex flex-col rounded-lg bg-black bg-opacity-10 cursor-pointer border-[1px] border-white border-opacity-20 hover:bg-opacity-30 hover:border-opacity-90 transition-all" v-for="item in items" :key="item.id">
      
      <p>{{ item.title }}</p>
      <div class="w-full flex justify-between">
        <p>{{ item.price }}</p>
        <p>{{ item.age_limit }}+</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';

const items = ref(undefined);

onMounted(async () => {
  let response = await fetch('http://localhost:8000/session/');

  if (response.ok) {
    let json = await response.json();
    items.value = json.response.items;
  }
})
</script>