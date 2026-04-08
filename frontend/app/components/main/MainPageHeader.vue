<template>
  <div class="main-header">
    <h1 class="page-title main-header__title">Artikel &amp; Ulasan</h1>
    <p class="main-header__sub">
      Jelajahi ulasan elektronik terkini dari komunitas RetoGen.
    </p>
  </div>
</template>

<style scoped>
.main-header {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--glass-border);
}

.main-header__title {
  margin-bottom: 8px;
}

.main-header__sub {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.5;
}

@media (max-width: 480px) {
  .main-header__sub { font-size: 14px; }
}
</style>
