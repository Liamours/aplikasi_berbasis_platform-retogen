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

  /* Solid surface — no transparency, always readable regardless of background */
  background: var(--bg-surface);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  box-shadow: 0 8px 28px rgba(60, 55, 50, 0.16), 0 2px 8px rgba(60, 55, 50, 0.08);
  overflow: hidden;
}

.dark-mode .dropdown-panel {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5), 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Edge highlight kept as subtle top-border accent */
.dropdown-panel__edge {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
  pointer-events: none;
}
</style>
