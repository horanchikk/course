<template>
    <button v-if="props.color === 'primary'" class="bg-green-600 hover:bg-green-500 active:bg-green-400 text-xl text-white rounded-lg py-2 px-4 transition-all">
        <slot />
    </button>
    <button v-else-if="props.color === 'warning'" class="bg-yellow-600 hover:bg-yellow-500 active:bg-yellow-400 text-xl text-white rounded-lg py-2 px-4 transition-all">
        <slot />
    </button>
    <button v-else-if="props.color === 'error'" class="bg-red-600 hover:bg-red-500 active:bg-red-400 text-xl text-white rounded-lg py-2 px-4 transition-all">
        <slot />
    </button>
    <button v-else class="bg-black bg-opacity-20 hover:bg-opacity-30 active:bg-opacity-40 text-xl text-white rounded-lg py-2 px-4 transition-all">
        <slot />
    </button>
</template>

<script setup>
const props = defineProps(['color'])
</script>
