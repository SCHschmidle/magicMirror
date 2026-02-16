<script setup>
import { RouterLink } from 'vue-router';
</script>
<template>
<nav>
    <RouterLink to="/dashboard">Dashboard</RouterLink>
    <RouterLink to="/displayview">Display</RouterLink>
    <RouterLink to="/upload" class="upload">Upload</RouterLink>
</nav>
</template>
<style scoped>
nav{
    background-color: rgb(1, 0, 29);
    height: 10%;
}
</style>