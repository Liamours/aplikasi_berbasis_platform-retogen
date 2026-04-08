import { computed } from 'vue'
import type { SortOption, ArticleCard } from '~/types/api'
import { useMockArticles } from './useMockArticles'

/**
 * Shared reactive filter/sort/search state for the main article listing page.
 * Uses useState so all components on the same page share a single instance.
 * Swap useMockArticles() for a real API call when the backend is live.
 */
export const useArticleFilter = () => {
  const articles: ArticleCard[] = useMockArticles()

  const searchQuery = useState('mp-search', () => '')
  const activeSort  = useState<SortOption>('mp-sort', () => 'newest' as SortOption)
  const activeTag   = useState('mp-tag', () => '')

  const allTags = computed(() => {
    const tagSet = new Set<string>()
    articles.forEach(a => a.article_tags.forEach(t => tagSet.add(t)))
    return Array.from(tagSet).sort()
  })

  const filteredArticles = computed(() => {
    let result = [...articles]

    const q = searchQuery.value.trim().toLowerCase()
    if (q) {
      result = result.filter(a =>
        a.article_title.toLowerCase().includes(q) ||
        a.article_preview.toLowerCase().includes(q) ||
        a.article_tags.some(t => t.includes(q)),
      )
    }

    if (activeTag.value) {
      result = result.filter(a => a.article_tags.includes(activeTag.value))
    }

    switch (activeSort.value) {
      case 'newest':         result.sort((a, b) => b.created_at.localeCompare(a.created_at)); break
      case 'oldest':         result.sort((a, b) => a.created_at.localeCompare(b.created_at)); break
      case 'highest_rated':  result.sort((a, b) => b.rating_avg - a.rating_avg);              break
      case 'most_commented': result.sort((a, b) => b.comment_count - a.comment_count);        break
    }

    return result
  })

  function setTag(tag: string) {
    activeTag.value = activeTag.value === tag ? '' : tag
  }

  function resetFilters() {
    searchQuery.value = ''
    activeTag.value   = ''
    activeSort.value  = 'newest'
  }

  return {
    searchQuery,
    activeSort,
    activeTag,
    allTags,
    filteredArticles,
    setTag,
    resetFilters,
  }
}
