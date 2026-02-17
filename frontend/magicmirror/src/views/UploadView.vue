<script setup>
import { ref } from 'vue'
let selectedFile = null
const duration = ref(30)

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

  const res = await fetch("http://localhost:8000/upload/single", {
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
}
</script>

<template>
  <input type="file" @change="onChange" />
  <br>
  <input type="number" name="duration" id="duration" v-model="duration"> Sekunden
  <br>
  <button type="submit" @click="onSubmit">Submit</button>
</template>