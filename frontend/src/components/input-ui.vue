<template>
    <input 
        class="outline-none text-black bg-white bg-opacity-70 px-4 w-2/3 rounded-md 
        placeholder:text-black placeholder:text-opacity-50 placeholder:text-sm
        focus:bg-opacity-100 transition-all"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
    />
</template>

<script setup>
defineProps(['modelValue'])
defineEmits(['update:modelValue'])
</script>