<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const media = ref([]);
const currentIndex = ref(0);
let intervalId = null;
const currentDuration = ref(10000);
let emptyCheckInterval = false;

const isVideo = (filename) => {
  const ext = filename.split('.').pop().toLowerCase();
  return ['mp4', 'avi', 'mov', 'webm'].includes(ext);
};

onMounted(async () => {
 get_data()
 startSlideshow()
});

const startSlideshow = () => {
  if (intervalId) clearInterval(intervalId);

  if (media.value.length === 0) {
    console.log("Keine Medien vorhanden → Warte-Modus aktiv");
    startEmptyCheck();
    return;
  }
  let duration = media.value[currentIndex.value]?.duration || 10;
  currentDuration.value = duration * 1000;

  get_data()

  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % media.value.length;
    clearInterval(intervalId);
    startSlideshow();
  }, currentDuration.value);
};

async function get_data(){
    try {
    const response = await fetch('http://127.0.0.1:8000/filedata');
    const data = await response.json();
    media.value = data.filter(item => item.active === true);
    if (media.value.length > 0) {
      
    }
  } catch (error) {
    console.error('Fehler beim Laden der Medien:', error);
  }
}

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

async function setActiveMedia(id) {
  const response = await fetch('http://127.0.0.1:8000/filedata');
  const data = await response.json();
  data[id]['active'] = 'True'
  await fetch('http://127.0.0.1:8000/activeupdate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updated)
  });
}
async function checkScheduledMedia() {
  const response = await fetch('http://127.0.0.1:8000/scheduled-media');
  const data = await response.json();
  if (data.media) {
    await setActiveMedia(data.media.id);
  } else {
    await setActiveMedia(-1);
  }
  const filedataResponse = await fetch('http://127.0.0.1:8000/filedata');
  const filedata = await filedataResponse.json();
  media.value = filedata.filter(item => item.active === true);
  currentIndex.value = 0;
  if (media.value.length > 0) {
    startSlideshow();
  } else {
    if (intervalId) clearInterval(intervalId);
  }
}

setInterval(checkScheduledMedia, 10000);

function startEmptyCheck() {

  if (emptyCheckInterval) return;

  emptyCheckInterval = setInterval(async () => {

    await get_data();

    if (media.value.length > 0) {
      console.log("Medien gefunden → Slideshow startet!");

      clearInterval(emptyCheckInterval);
      emptyCheckInterval = null;

      currentIndex.value = 0;
      startSlideshow();
    }

  }, 10000);
}

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
