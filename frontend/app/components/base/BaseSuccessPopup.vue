<script setup lang="ts">
defineProps<{
  message: string
}>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-fade">
      <div class="popup-overlay">
        <div class="popup-content">
          <div class="popup-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <h3>Berhasil!</h3>
          <p>{{ message }}</p>
          <BaseButton @click="emit('close')">OK</BaseButton>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: var(--bg-surface);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  width: min(90%, 400px);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  box-shadow: var(--glass-shadow);
}

.popup-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(106, 173, 168, 0.15);
  color: var(--primary-cyan);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-icon svg {
  width: 32px;
  height: 32px;
}

.popup-content h3 {
  font-size: 24px;
  margin: 0;
  color: var(--text-primary);
}

.popup-content p {
  color: var(--text-secondary);
  font-size: 15px;
  margin-bottom: 8px;
}
</style>
