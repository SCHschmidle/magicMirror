<script setup>
import { ref } from 'vue';
const file = ref('')

async function sendToBackend(){
    const response = await fetch('https://example.com/api', {
        method: 'POST',
        body: JSON.stringify({ file: file.value })
    });
    
    console.log('Antwort erhalten', response);
}


</script>
<template>
<div class="upload">
    <input type="file" @:change="file">
    <button @click="sendToBackend">send</button>
</div>
</template>
<style scoped>

</style>