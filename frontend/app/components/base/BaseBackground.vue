<template>
  <div aria-hidden="true">
    <div class="bg-grid" />
    <div class="blob blob--red" />
    <div class="blob blob--cyan-lg" />
    <div class="blob blob--cyan-sm" />
  </div>
</template>

<style scoped>
.bg-grid {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background-image:
    linear-gradient(var(--grid-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
  background-size: 32px 32px;
}

.blob {
  position: fixed;
  border-radius: 999px;
  filter: blur(110px);
  pointer-events: none;
  z-index: 1;
}

.blob--red {
  width: 480px;
  height: 300px;
  top: -80px;
  left: -100px;
  background: #B22222;
  opacity: 0.16;
}

.blob--cyan-lg {
  width: 420px;
  height: 420px;
  bottom: 40px;
  right: -120px;
  background: #20B2AA;
  opacity: 0.13;
}

.blob--cyan-sm {
  width: 180px;
  height: 180px;
  top: 45%;
  left: 35%;
  background: #20B2AA;
  opacity: 0.08;
}
</style>
