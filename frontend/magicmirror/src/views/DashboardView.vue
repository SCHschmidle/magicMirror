<script setup>
import { ref, onMounted, computed } from 'vue';

const fileData = ref([])
onMounted(async() => {
    console.log('HomeView mounted')
    const response = await fetch('http://localhost:8000/filedata')
    fileData.value = await response.json()
    console.log(fileData.value)
})

async function changedActive (key){
    const response = await fetch('http://localhost:8000/activeupdate', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "key": key })
    })
    const data = await response.json()
    console.log(data)
}

async function deleteFile(fileId){
    const response = await fetch(`http://localhost:8000/deletefile/${fileId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        
    })
    fileData.value = fileData.value.filter(file => file.id !== fileId)
}

const totalSize = computed(() => {
    return fileData.value.reduce((sum, file) => {
        return Math.round(((sum + Number(file.size)) /1024) *1024* 100)/100
    }, 0)
})



</script>
<template>
<h1>Dashboard</h1>
<div>
    <table>
        <thead>
            <tr>
                <th>index</th>
                <th>FileName</th>
                <th>Volume</th>
                <th>active</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="file in fileData" :key="file.id" class="board">
                <td>{{ file.id }}</td>
                <td>{{ file.name }}</td>
                <td>{{ file.size }}</td>
                <td><input type="checkbox" :checked="file.active" @change="changedActive(fileData.indexOf(file))"></td>
                <button @click="deleteFile(file.name)">Löschen</button>
            </tr>
        </tbody>
    </table>
    <p><strong>Total Volume:</strong> {{ totalSize }}</p>
</div>
</template>
<style scoped>
tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
