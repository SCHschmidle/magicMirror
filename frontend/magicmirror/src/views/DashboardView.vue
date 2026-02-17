<script setup>
import { ref, onMounted, computed } from 'vue';

const fileData = ref([])
onMounted(async() => {
    console.log('HomeView mounted')
    const response = await fetch('http://localhost:8000/filedata')
    fileData.value = await response.json()
})

async function changedParam(){
    
    const response = await fetch('http://localhost:8000/activeupdate', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(fileData.value)
    })
    const data = await response.json()

}

async function deleteFile(fileId){
    const response = await fetch(`http://localhost:8000/deletefile/${fileId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        
    })
    fileData.value = fileData.value.filter(file => file.id !== fileId)
    location.reload()
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
                <th>Index</th>
                <th>File Name</th>
                <th>Grösse</th>
                <th>Länge in Sekunden</th>
                <th>Status</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="file in fileData" :key="file.id" class="board">
                <td>{{ file.id }}</td>
                <td>{{ file.name }}</td>
                <td>{{ file.size }} MB</td>
                <td><input type="number"v-model="file.duration"></td>
                <td><input type="checkbox" v-model="file.active"></td>
                <td><button @click="deleteFile(file.id)">Löschen</button></td>
            </tr>
        </tbody>
    </table>
    <button @click="changedParam()">Save</button>
    <p><strong>Total Volume:</strong> {{ totalSize }}</p>
</div>
</template>
<style scoped>
tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
