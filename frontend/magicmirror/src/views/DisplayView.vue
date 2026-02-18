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
    const response = await fetch('http://127.0.0.1:8000/filedata');
    const data = await response.json();
    media.value = data.filter(item => item.active === true);
    if (media.value.length > 0) {
      startSlideshow();
    }
  } catch (error) {
    console.error('Fehler beim Laden der Medien:', error);
  }
});

const startSlideshow = () => {
  if (intervalId) clearInterval(intervalId);

  let duration = media.value[currentIndex.value]?.duration || 10;
  currentDuration.value = duration * 1000;


  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % media.value.length;
    clearInterval(intervalId);
    startSlideshow();
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
  if (intervalId) clearInterval(intervalId);
});
</script>

<template>
  <div v-if="true">
  <div class="display-view">
    <div v-if="media.length > 0" class="display-media">
      <img
        v-if="!isVideo(media[currentIndex].name)"
        :src="`http://127.0.0.1:8000/images/${media[currentIndex].name}`"
        :alt="media[currentIndex].name"
      />
      <video
        v-else
        :src="`http://127.0.0.1:8000/images/${media[currentIndex].name}`"
        autoplay
        muted
        playsinline
        @loadedmetadata="onVideoLoaded"
      ></video>
    </div>
    <div v-else>
      Keine aktiven Medien vorhanden.
    </div>
  </div>
  </div>
</template>
