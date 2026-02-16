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
  <div class="display-view">
    <img v-if="media.length > 0 && !isVideo(media[currentIndex])" :src="`/media/${media[currentIndex]}`" :alt="media[currentIndex]" />
    <video v-else-if="media.length > 0" :src="`/media/${media[currentIndex]}`" autoplay muted @loadedmetadata="onVideoLoaded"></video>
  </div>
</template>