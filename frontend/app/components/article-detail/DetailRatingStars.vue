<script setup lang="ts">
const props = withDefaults(defineProps<{
  modelValue: number
  readonly?: boolean
  size?: 'sm' | 'md' | 'lg'
}>(), {
  readonly: false,
  size: 'md'
})

const emit = defineEmits<{
  'update:modelValue': [value: number]
  hover: [value: number]
  leave: []
}>()

const stars = [1, 2, 3, 4, 5]

const handleSelect = (value: number) => {
  if (props.readonly) return
  emit('update:modelValue', value)
}

const handleHover = (value: number) => {
  if (props.readonly) return
  emit('hover', value)
}

const handleLeave = () => {
  if (props.readonly) return
  emit('leave')
}
</script>

<template>
  <div class="rating-stars" :class="[`rating-stars--${size}`, { 'is-readonly': readonly }]" @mouseleave="handleLeave">
    <button
      v-for="star in stars"
      :key="star"
      type="button"
      class="rating-stars__item"
      :class="{ 'is-active': star <= modelValue }"
      :disabled="readonly"
      @click="handleSelect(star)"
      @mouseenter="handleHover(star)"
    >
      ★
    </button>
  </div>
</template>

<style scoped>
.rating-stars {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.rating-stars__item {
  border: none;
  background: transparent;
  color: rgba(181, 107, 82, 0.28);
  cursor: pointer;
  line-height: 1;
  transition: transform 0.2s ease, color 0.2s ease;
}

.rating-stars__item.is-active {
  color: var(--primary-red);
}

.rating-stars__item:hover:not(:disabled) {
  transform: translateY(-1px) scale(1.03);
}

.rating-stars--sm .rating-stars__item {
  font-size: 16px;
}

.rating-stars--md .rating-stars__item {
  font-size: 22px;
}

.rating-stars--lg .rating-stars__item {
  font-size: 28px;
}

.is-readonly .rating-stars__item {
  cursor: default;
}
</style>