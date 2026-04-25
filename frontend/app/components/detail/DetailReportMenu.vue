<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = withDefaults(defineProps<{
  showEdit?: boolean
  showDelete?: boolean
  showReport?: boolean
  reportLabel?: string
  editLabel?: string
  deleteLabel?: string
}>(), {
  showEdit: false,
  showDelete: false,
  showReport: true,
  reportLabel: 'Laporkan artikel',
  editLabel: 'Edit',
  deleteLabel: 'Hapus'
})

const emit = defineEmits<{
  report: []
  edit: []
  remove: []
}>()

const isOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const hasActions = computed(() => props.showEdit || props.showDelete || props.showReport)

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

const handleEdit = () => {
  emit('edit')
  closeMenu()
}

const handleRemove = () => {
  emit('remove')
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
  <div v-if="hasActions" ref="menuRef" class="report-menu">
    <button
      type="button"
      class="report-menu__trigger"
      aria-label="Menu aksi"
      @click="toggleMenu"
    >
      <span aria-hidden="true">⋯</span>
    </button>

    <Transition name="glass-fade">
      <div v-if="isOpen" class="report-menu__dropdown">
        <button
          v-if="showEdit"
          type="button"
          class="report-menu__action report-menu__action--edit"
          @click="handleEdit"
        >
          {{ editLabel }}
        </button>

        <button
          v-if="showDelete"
          type="button"
          class="report-menu__action report-menu__action--delete"
          @click="handleRemove"
        >
          {{ deleteLabel }}
        </button>

        <button
          v-if="showReport"
          type="button"
          class="report-menu__action report-menu__action--report"
          @click="handleReport"
        >
          {{ reportLabel }}
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
  background: rgba(106, 173, 168, 0.1);
  border-color: rgba(106, 173, 168, 0.22);
}

.report-menu__dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 172px;
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
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: var(--transition-fast);
}

.report-menu__action--edit {
  color: var(--primary-cyan);
}

.report-menu__action--edit:hover {
  background: rgba(106, 173, 168, 0.1);
}

.report-menu__action--delete,
.report-menu__action--report {
  color: var(--primary-red);
}

.report-menu__action--delete:hover,
.report-menu__action--report:hover {
  background: rgba(181, 107, 82, 0.1);
}
</style>