<script setup lang="ts">
const model = defineModel<string>({ default: '' })

withDefaults(defineProps<{
  label?: string
  type?: string
  placeholder?: string
  error?: string
}>(), {
  label: '',
  type: 'text',
  placeholder: '',
  error: ''
})
</script>

<template>
  <div class="field-group">
    <label v-if="label" class="field-label">{{ label }}</label>

    <input
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      class="base-input"
      :class="{ 'base-input--error': error }"
    >

    <Transition name="glass-fade">
      <p v-if="error" class="field-error">{{ error }}</p>
    </Transition>
  </div>
</template>

<style scoped>
.base-input {
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  outline: none;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: var(--transition-fast);
}

.base-input::placeholder {
  color: var(--text-muted);
}

.base-input:focus {
  border-color: rgba(0, 206, 209, 0.45);
  box-shadow: 0 0 0 3px rgba(0, 206, 209, 0.12);
}

.base-input--error {
  border-color: rgba(227, 66, 52, 0.45);
}
</style>