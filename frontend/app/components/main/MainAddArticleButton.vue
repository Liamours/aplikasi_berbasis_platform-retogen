<script setup lang="ts">
const { data } = useAuth()
const isAdmin = computed(() => data.value?.role === 'admin')
</script>

<template>
  <NuxtLink v-if="isAdmin" to="/articles/create">
    <BaseButton variant="ghost">+ Artikel</BaseButton>
  </NuxtLink>
</template>
