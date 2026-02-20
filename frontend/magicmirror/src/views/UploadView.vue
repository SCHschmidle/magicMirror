<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
let selectedFile = null
const duration = ref(30)
const router = useRouter()
const scheduled_date = ref('')
const base_url = import.meta.env.VITE_API_BASE_URL

const onChange = (e) => {
  selectedFile = e.target.files?.[0]
  if (selectedFile && selectedFile.type.startsWith('video/')) {
    const video = document.createElement('video')
    video.preload = 'metadata'
    video.onloadedmetadata = () => {
      duration.value = Math.round(video.duration)
      URL.revokeObjectURL(video.src)
    }
    video.src = URL.createObjectURL(selectedFile)
  }
}

const onSubmit = async () => {
  if (!selectedFile) {
    console.log('Keine Datei ausgewählt')
    return
  }

  console.log('uploading')
  const form = new FormData()
  form.append("file", selectedFile)
  form.append("duration", duration.value)
  form.append("scheduled_date", scheduled_date.value)

  const res = await fetch(base_url+"/upload/single", {
    method: "POST",
    body: form,
  })

  if (!res.ok) {
    const text = await res.text()
    console.error("Upload fehlgeschlagen:", res.status, text)
    return
  }

  const data = await res.json()
  console.log("Upload erfolgreich:", data)
  selectedFile = null 
  duration.value = 30

  router.push('/')

}
</script>

<template>
  <input type="file" @change="onChange" />
  <br>
  <input type="number" name="duration" id="duration" v-model="duration"> Sekunden
  <br>
  <input type="date" name="scheduled_date" id="scheduled_date" v-model="scheduled_date"> Datum
  <br>
  <button type="submit" @click="onSubmit">Submit</button>
</template>