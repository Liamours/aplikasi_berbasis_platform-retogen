export interface ApiBaseResponse {
  confirmation: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse extends ApiBaseResponse {
  token?: string
}

export interface RegisterRequest {
  username: string
  fullname: string
  email: string
  password: string
}

export interface RegisterResponse extends ApiBaseResponse {}

export interface UserProfile {
  user_id: string
  username: string
  email: string
  fullname: string
  role: string
  created_at: string
  updated_at?: string
  reports?: unknown[]
}

export interface UserDetailsResponse extends ApiBaseResponse {
  user: UserProfile
}

export type SortOption =
  | 'newest'
  | 'oldest'
  | 'highest_rated'
  | 'most_commented'
  | 'most_reported'
  | 'by_tag'
  | 'search_title'

export interface ArticleListItem {
  article_id: string
  article_title: string
  article_preview: string
  article_tags: string[]
  article_image: string | null
}

/** Extends ArticleListItem with display-only fields used by mock data and the main page card. */
export interface ArticleCard extends ArticleListItem {
  rating_avg: number
  comment_count: number
  created_at: string
}

export interface MainPageRequest {
  sort?: string
  tag?: string
  search?: string
}

export interface MainPageResponse extends ApiBaseResponse {
  username: string
  sort: string
  tag: string
  search: string
  list_article: ArticleListItem[]
}

export interface ArticleComment {
  comment_id: string
  parent_comment_id: string | null
  owner: string
  user_email: string
  comment_content: string
}

export interface ArticleRating {
  rating_id: string
  owner: string
  user_email: string
  rating_value: number
}

export interface ArticleReport {
  report_id: string
  description: string
  created_at: string
}

export interface ArticleViewResponse extends ApiBaseResponse {
  userclass: 'user' | 'admin'
  user_email: string
  username: string
  article_title: string
  article_content: string
  article_tags: string[]
  article_image: string | null
  comments: ArticleComment[]
  ratings: ArticleRating[]
  reports?: ArticleReport[]
}

// Monitor harga API types
export interface MonitorSearchRequest {
  product_name: string
  limit?: number
}

export interface MonitorPriceResult {
  product: string
  store: string | null
  price: number
  rating: number | null
}

export interface MonitorSearchResponse {
  results: MonitorPriceResult[]
  errors: string[]
  total: number
}

// Article detail page types
export type DetailPriceTrend = 'down' | 'up' | 'stable'

export interface DetailPriceEntry extends MonitorPriceResult {
  id: string
  logo?: string

  /**
   * Optional display fields kept for backward compatibility with older mock/detail UI.
   * Backend /monitor/search does not need to return these fields.
   */
  shippingNote?: string
  url?: string
  updatedAt?: string
  trend?: DetailPriceTrend
}

export interface DetailRating {
  rating_id: string
  owner: string
  user_email: string
  rating_value: number
}

export interface DetailComment {
  comment_id: string
  parent_comment_id: string | null
  owner: string
  user_email: string
  comment_content: string
  created_at: string
  updated_at?: string
}

export interface DetailCommentTree extends DetailComment {
  children: DetailCommentTree[]
}

export interface DetailArticle {
  article_id: string
  article_title: string
  article_preview: string
  article_content: string
  article_tags: string[]
  article_image: string | null
  prices: DetailPriceEntry[]
  comments: DetailComment[]
  ratings: DetailRating[]
}