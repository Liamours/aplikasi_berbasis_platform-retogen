<template>
  <!--
    Reusable glass dropdown panel.
    Parent must have `position: relative`.
    Pair with <Transition name="glass-fade"> in parent template.
  -->
  <div class="dropdown-panel" v-bind="$attrs">
    <!-- Edge highlight (light-catcher, same pattern as BaseGlassCard) -->
    <div class="dropdown-panel__edge" aria-hidden="true" />
    <slot />
  </div>
</template>

<style scoped>
.dropdown-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 220px;
  z-index: 2000;
  padding: 8px;

  /* Glass surface — BaseGlassCard tokens, dropdown-appropriate radius */
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
  overflow: hidden;
}

/* Identical edge-highlight pseudo pattern used in BaseGlassCard */
.dropdown-panel__edge {
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 50%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  pointer-events: none;
}
</style>
