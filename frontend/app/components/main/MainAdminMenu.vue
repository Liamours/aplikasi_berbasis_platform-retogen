<script setup lang="ts">
// TODO: replace `true` with `useAuthStore().isAdmin` once auth is live.
const isAdmin = true

const isOpen  = ref(false)
const rootRef = ref<HTMLElement | null>(null)

const toggle = () => { isOpen.value = !isOpen.value }
const close  = () => { isOpen.value = false }

function onOutsideClick(e: MouseEvent) {
  if (rootRef.value && !rootRef.value.contains(e.target as Node)) close()
}

onMounted(()  => document.addEventListener('mousedown', onOutsideClick))
onUnmounted(() => document.removeEventListener('mousedown', onOutsideClick))
</script>

<template>
  <div v-if="isAdmin" ref="rootRef" class="admin-menu">

    <!-- Hamburger trigger — same size/shape as other icon buttons -->
    <BaseButton
      variant="icon"
      :aria-expanded="isOpen"
      aria-haspopup="menu"
      aria-label="Menu admin"
      @click="toggle"
    >
      ☰
    </BaseButton>

    <!-- Panel reuses BaseDropdownPanel + BaseDropdownItem — no extra CSS needed -->
    <Transition name="glass-fade">
      <BaseDropdownPanel v-if="isOpen" role="menu">
        <BaseDropdownItem to="/articles/create" @click="close">
          Tambah Artikel
        </BaseDropdownItem>
        <BaseDropdownItem to="/user-management" @click="close">
          User Management
        </BaseDropdownItem>
      </BaseDropdownPanel>
    </Transition>

  </div>
</template>

<style scoped>
/* Only positioning wrapper — all visuals from BaseButton, BaseDropdownPanel, BaseDropdownItem */
.admin-menu {
  position: relative;
}
</style>
