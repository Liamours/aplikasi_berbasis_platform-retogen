<script setup lang="ts">
import { ref, computed } from 'vue'

const model = defineModel<string>({ default: '' })

const props = withDefaults(defineProps<{
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

const showPassword = ref(false)

const inputType = computed(() => {
  if (props.type === 'password') {
    return showPassword.value ? 'text' : 'password'
  }
  return props.type
})

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="field-group">
    <label v-if="label" class="field-label">{{ label }}</label>

    <div class="input-wrapper">
      <input
        v-model="model"
        :type="inputType"
        :placeholder="placeholder"
        class="base-input"
        :class="{ 'base-input--error': error, 'base-input--password': type === 'password' }"
      >
      <button
        v-if="type === 'password'"
        type="button"
        class="password-toggle"
        @click="toggleShowPassword"
      >
        <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
          <circle cx="12" cy="12" r="3" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
          <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
          <path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
          <line x1="2" y1="2" x2="22" y2="22" />
        </svg>
      </button>
    </div>

    <Transition name="glass-fade">
      <p v-if="error" class="field-error">{{ error }}</p>
    </Transition>
  </div>
</template>

<style scoped>
.input-wrapper {
  position: relative;
  width: 100%;
}

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

.base-input--password {
  padding-right: 48px;
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

.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  transition: var(--transition-fast);
  border-radius: 4px;
}

.password-toggle:hover {
  color: var(--primary-cyan);
}
</style>