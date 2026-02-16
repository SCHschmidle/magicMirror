<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const media = ref([]);
const currentIndex = ref(0);
let intervalId = null;
const currentDuration = ref(10000);  

const isVideo = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  return ['mp4', 'avi', 'mov', 'webm'].includes(ext);
};

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/display');
    const data = await response.json();
    media.value = data.media;
    if (media.value.length > 0) {
      startSlideshow();
    }
  } catch (error) {
    console.error('Fehler beim Laden der Medien:', error);
  }
});

const startSlideshow = () => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % media.value.length;
    currentDuration.value = 10000;
  }, currentDuration.value);
};

const onVideoLoaded = (event) => {
  currentDuration.value = event.target.duration * 1000;  
  if (intervalId) {
    clearInterval(intervalId);
    startSlideshow();
  }
};

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<template>
  <div>
    <h1>Medien-Show</h1>
    <div v-if="media.length > 0">
      <img v-if="!isVideo(media[currentIndex])" :src="`/media/${media[currentIndex]}`" :alt="media[currentIndex]" style="max-width: 100%; height: auto;" />
      <video v-else :src="`/media/${media[currentIndex]}`" controls autoplay muted style="max-width: 100%; height: auto;" @loadedmetadata="onVideoLoaded"></video>
    </div>
    <div v-else>
      Keine Medien vorhanden.
    </div>
  </div>
</template>