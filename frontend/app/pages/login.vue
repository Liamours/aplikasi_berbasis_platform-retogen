<script setup lang="ts">
definePageMeta({ middleware: 'guest' })
</script>

<template>
  <BasePageShell>
    <section class="login-page">
      <AuthLoginCard />
    </section>
  </BasePageShell>
</template>

<style scoped>
.login-page {
  min-height: calc(100vh - var(--navbar-height));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 0;
}

@media (max-width: 480px) {
  .login-page { padding: 16px 0; }
}
</style>
