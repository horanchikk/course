<template>
    <button v-if="props.type === 'primary'" class="bg-green-600 hover:bg-green-500 active:bg-green-400 text-xl text-white rounded-lg py-2 px-4 transition-all"><slot /></button>
    <button v-else-if="props.type === 'warning'" class="bg-yellow-600 hover:bg-yellow-500 active:bg-yellow-400 text-xl text-white rounded-lg py-2 px-4 transition-all"><slot /></button>
    <button v-else-if="props.type === 'error'" class="bg-red-600 hover:bg-red-500 active:bg-red-400 text-xl text-white rounded-lg py-2 px-4 transition-all"><slot /></button>
</template>

<script setup>

const props = defineProps(['type'])

</script>
