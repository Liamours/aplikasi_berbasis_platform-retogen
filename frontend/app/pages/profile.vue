<script setup lang="ts">
import { onMounted } from 'vue'
import ProfileInfoCard from '~/components/profile/ProfileInfoCard.vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const {
  profile,
  isLoading,
  errorMessage,
  profileInitials,
  fetchProfile,
  formatDate
} = useUserProfile()

const { logout } = useAuth()

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <BasePageShell>
    <div class="profile-page">
      <ProfileInfoCard
        :profile="profile"
        :initials="profileInitials"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :format-date="formatDate"
        @logout="logout"
      />
    </div>
  </BasePageShell>
</template>

<style scoped>
.profile-page {
  min-height: calc(100vh - var(--navbar-height) - 64px);
  display: grid;
  place-items: center;
}
</style>