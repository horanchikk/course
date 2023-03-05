<template>
    <main class="w-full h-full">

    </main>
</template>

<script setup>
import router from '../router'

console.log(router.currentRoute.value.params.id) // get id from params (router/index.js)
</script>