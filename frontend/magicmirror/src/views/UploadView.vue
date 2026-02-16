<template>
<input type="file" @change="onChange" />
<button type="submit" @click="onSubmit">Submit</button>
</template>

<script setup>
let selectedFile = null

const onChange = (e) => {
  selectedFile = e.target.files?.[0]
  console.log('Datei ausgewählt:', selectedFile?.name)
}

const onSubmit = async () => {
  if (!selectedFile) {
    console.log('Keine Datei ausgewählt')
    return
  }

  console.log('uploading')
  const form = new FormData()
  form.append("file", selectedFile)

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
  selectedFile = null // Datei-Auswahl zurücksetzen
}
</script>