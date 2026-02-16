<script setup>
import { ref, onMounted } from 'vue';

const files = ref([''])


</script>
<template>
<h1>Dashboard</h1>
<div>
    <table>
        <thead>
            <tr>
                <th>FileName</th>
                <th>Volume</th>
                <th>active</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="file in files" :key="file" class="board">
                <td>{{ file.name }}</td>
                <td>{{ file.volume }}</td>
                <td><input type="checkbox" :checked="file.active" @change="changedActive(key)"></td>
            </tr>
        </tbody>
    </table>
</div>
</template>
<style scoped>
tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
