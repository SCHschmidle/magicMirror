<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const media = ref([]);
const currentIndex = ref(0);
let intervalId = null;
const currentDuration = ref(10000);
let emptyCheckInterval = false;
const base_url = import.meta.env.VITE_API_BASE_URL

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
    console.log("yippi");
  }, currentDuration.value);
};

async function get_data(){
    try {
    const response = await fetch(base_url+'/filedata');
    const data = await response.json();
    media.value = data.filter(item => item.active === true);
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
  const response = await fetch(base_url+'/filedata');
  const data = await response.json();
  data[id]['active'] = 'True'

  await fetch(base_url+'/activeupdate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
}
async function checkScheduledMedia() {
  const response = await fetch(base_url+'/scheduled-media');
  const data = await response.json();
  if (data.media) {
    data.media.forEach(async medias => {
      await setActiveMedia(medias.id);
    });
  }
  const filedataResponse = await fetch(base_url+'/filedata');
  const filedata = await filedataResponse.json();
  const newMedia = filedata.filter(item => item.active === true);
  const currentName = media.value[currentIndex.value]?.name;

  media.value = newMedia;

  const newIndex = media.value.findIndex(item => item.name === currentName);

  if (media.value.length === 0) {
    if (intervalId) clearInterval(intervalId);
    currentIndex.value = 0;
  } else if (newIndex === -1) {
    currentIndex.value = 0;
  } else {
    currentIndex.value = newIndex;
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
