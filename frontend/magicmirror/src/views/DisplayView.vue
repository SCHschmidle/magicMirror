<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const images = ref([]);
const currentIndex = ref(0);
let intervalId = null;

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/display');
    const data = await response.json();
    images.value = data.images;
    if (images.value.length > 0) {
      startSlideshow();
    }
  } catch (error) {
    console.error('Fehler beim Laden der Bilder:', error);
  }
});

const startSlideshow = () => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.value.length;
  }, 10000); 
};

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<template>
  <div>
    <h1>Bild-Show</h1>
    <div v-if="images.length > 0">
      <img :src="`/images/${images[currentIndex]}`" :alt="images[currentIndex]" style="max-width: 100%; height: auto;" />
      <p>{{ currentIndex + 1 }} / {{ images.length }}</p>
    </div>
    <div v-else>
      Keine Bilder vorhanden.
    </div>
  </div>
</template>