import type { ArticleListItem, MainPageRequest, MainPageResponse, SortOption } from '~/types/api'

/**
 * All filter/sort/search state for the main article listing page.
 * Server handles sorting and filtering — no local computed sort.
 * useState keys ensure all components on the page share one instance.
 */

/** Sort options the user can pick. by_tag / search_title / most_reported are auto-derived. */
export type UISortOption = Extract<SortOption, 'newest' | 'oldest' | 'highest_rated' | 'most_commented'>

export const useArticleFilter = () => {
  const { post } = useApi()

  const articles    = useState<ArticleListItem[]>('mp-articles', () => [])
  const isLoading   = useState<boolean>('mp-loading', () => false)
  const fetchError  = useState<string | null>('mp-error', () => null)
  const searchQuery = useState<string>('mp-search', () => '')
  const activeSort  = useState<UISortOption>('mp-sort', () => 'newest')
  const activeTag   = useState<string>('mp-tag', () => '')

  /** Tags extracted from the current result set — used by MainTagFilter pills. */
  const allTags = computed(() => {
    const set = new Set<string>()
    articles.value.forEach(a => a.article_tags.forEach(t => set.add(t)))
    return Array.from(set).sort()
  })

  /** Build the request body from current UI state. */
  function buildRequest(): MainPageRequest {
    const q = searchQuery.value.trim()
    if (q)                return { sort: 'search_title', search: q }
    if (activeTag.value)  return { sort: 'by_tag', tag: activeTag.value }
    return { sort: activeSort.value }
  }

  async function fetchArticles() {
    isLoading.value  = true
    fetchError.value = null
    try {
      const res = await post<MainPageResponse>('/article/main_page', buildRequest(), true)
      if (res.confirmation === 'fetch data successful') {
        // Normalise tag field: backend may return article_tag (string) or
        // article_tags (array). Always expose article_tags as string[].
        articles.value = res.list_article.map((a: any) => ({
          ...a,
          article_tags: Array.isArray(a.article_tags) && a.article_tags.length
            ? a.article_tags
            : typeof a.article_tag === 'string' && a.article_tag.trim()
              ? a.article_tag.split(',').map((t: string) => t.trim()).filter(Boolean)
              : [],
        }))
      } else {
        fetchError.value = res.confirmation
      }
    } catch {
      fetchError.value = 'Gagal memuat artikel. Periksa koneksi atau login ulang.'
    } finally {
      isLoading.value = false
    }
  }

  /** Toggle a tag filter — clears search, re-fetches. */
  function setTag(tag: string) {
    searchQuery.value = ''
    activeTag.value   = activeTag.value === tag ? '' : tag
    fetchArticles()
  }

  function resetFilters() {
    searchQuery.value = ''
    activeTag.value   = ''
    activeSort.value  = 'newest'
    fetchArticles()
  }

  // Re-fetch when sort dropdown changes.
  watch(activeSort, fetchArticles)

  // Debounced re-fetch when search query changes — clears tag filter.
  let _searchTimer: ReturnType<typeof setTimeout> | null = null
  watch(searchQuery, (val) => {
    if (_searchTimer) clearTimeout(_searchTimer)
    _searchTimer = setTimeout(() => {
      if (val.trim()) activeTag.value = ''
      fetchArticles()
    }, 400)
  })

  return {
    articles,
    isLoading,
    fetchError,
    searchQuery,
    activeSort,
    activeTag,
    allTags,
    fetchArticles,
    setTag,
    resetFilters,
  }
}
