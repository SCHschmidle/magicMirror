<script setup>
import { ref } from 'vue';

const files = ref([
    {
        id: 1,
        name: 'eins',
        volume: '100gb',
        active: true
    },
    {
        id: 2,
        name: 'zwei',
        volume: '222gb',
        active: false
    }
])
</script>
<template>
<h1>Dashboard</h1>
<div>
    <table>
        <tr>
            <th>FileName</th>
            <th>Volume</th>
            <th>active</th>
        </tr>
        <tr v-for="file in files" :key="file" class="board">
            <th>{{ file.name }}</th>
            <th>{{ file.volume }}</th>
            <th><input type="checkbox" :checked="file.active" @change="changedActive(key)"></th>
        </tr>
    </table>
</div>
</template>
<style scoped>
tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
