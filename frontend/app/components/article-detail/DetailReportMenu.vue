<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const emit = defineEmits<{
  report: []
}>()

const isOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const closeMenu = () => {
  isOpen.value = false
}

const handleDocumentClick = (event: MouseEvent) => {
  const target = event.target as Node | null

  if (!menuRef.value || !target) return
  if (!menuRef.value.contains(target)) {
    closeMenu()
  }
}

const handleReport = () => {
  emit('report')
  closeMenu()
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
})
</script>

<template>
  <div ref="menuRef" class="report-menu">
    <button type="button" class="report-menu__trigger" aria-label="More actions" @click="toggleMenu">
      ⋯
    </button>

    <Transition name="glass-fade">
      <div v-if="isOpen" class="report-menu__dropdown">
        <button type="button" class="report-menu__action" @click="handleReport">
          Report
        </button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.report-menu {
  position: relative;
}

.report-menu__trigger {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.report-menu__trigger:hover {
  background: rgba(181, 107, 82, 0.12);
  border-color: rgba(181, 107, 82, 0.22);
}

.report-menu__dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 132px;
  padding: 8px;
  border-radius: 14px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  z-index: 20;
}

.report-menu__action {
  width: 100%;
  border: none;
  background: transparent;
  color: var(--primary-red);
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: var(--transition-fast);
}

.report-menu__action:hover {
  background: rgba(181, 107, 82, 0.1);
}
</style>