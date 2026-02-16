<script setup>
import { ref, onMounted } from 'vue';

const images = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/display');
    const data = await response.json();
    images.value = data.images;
  } catch (error) {
    console.error('Fehler beim Laden der Bilder:', error);
  }
});
</script>
<template>
  <div>
    <h1>Alle Bilder</h1>
    <div v-for="image in images" :key="image">
      <img :src="`../../public/images/${image}`" :alt="image" style="max-width: 300px; margin: 10px;" />
    </div>
  </div>
</template>