<script setup>
import { ref, onMounted } from 'vue';

const files = ref([''])


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
