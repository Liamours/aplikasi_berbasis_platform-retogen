import type { DetailArticle } from '~/types/api'

export const useMockArticleDetail = (articleId: string): DetailArticle => ({
  article_id: articleId,
  article_title: 'Sony WH-1000XM5',
  article_preview:
    'Headphone ANC premium dengan karakter suara seimbang, kenyamanan tinggi, dan pengalaman harian yang konsisten untuk kerja, hiburan, dan perjalanan.',
  article_content: `Sony WH-1000XM5 menawarkan kombinasi yang matang antara active noise cancelling, kualitas mikrofon, dan kenyamanan untuk penggunaan jangka panjang.

Untuk kebutuhan harian, tuning suaranya terasa aman dan modern. Vokal cukup jelas, bass hadir tanpa terasa berlebihan, dan detail di frekuensi tinggi tetap terjaga untuk musik, podcast, maupun video conference.

Desainnya ringan dan bersih. Clamp force nyaman, ear cup terasa luas, dan pengalaman pemakaian beberapa jam tetap stabil tanpa cepat melelahkan.

Nilai utamanya ada pada konsistensi. Performa ANC, call quality, dan integrasi aplikasi membuat produk ini cocok untuk user yang ingin perangkat audio premium yang praktis dipakai setiap hari.

Jika fokus utama Anda adalah headphone wireless premium dengan pengalaman serba seimbang, model ini tetap relevan sebagai pilihan kuat di kelasnya.`,
  article_tags: ['audio', 'headphone', 'wireless', 'premium'],
  article_image: '/logo.jpg',
  prices: [
    {
      id: 'monitor-1',
      product: 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones',
      store: 'Tokopedia',
      price: 5199000,
      rating: 5.0,
      logo: '/tokopedia.png',
      url: '#',
      updatedAt: '10 menit lalu'
    },
    {
      id: 'monitor-2',
      product: 'Sony WH-1000XM5 Headphone ANC Original',
      store: 'Shopee',
      price: 5249000,
      rating: 4.9,
      logo: '/shopee.png',
      url: '#',
      updatedAt: '18 menit lalu'
    },
    {
      id: 'monitor-3',
      product: 'Sony WH-1000XM5 Bluetooth Headphone Premium',
      store: 'Bukalapak',
      price: 5399000,
      rating: 4.8,
      logo: '/bukalapak.png',
      url: '#',
      updatedAt: '32 menit lalu'
    },
    {
      id: 'monitor-4',
      product: 'Sony WH-1000XM5 Noise Cancelling Headset',
      store: 'Tokopedia',
      price: 5125000,
      rating: 4.6,
      logo: '/tokopedia.png',
      url: '#',
      updatedAt: '45 menit lalu'
    }
  ],
  ratings: [
    { rating_id: 'rating-1', owner: 'Aldo', user_email: 'aldo@example.com', rating_value: 5 },
    { rating_id: 'rating-2', owner: 'Nadia', user_email: 'nadia@example.com', rating_value: 4 },
    { rating_id: 'rating-3', owner: 'Raka', user_email: 'raka@example.com', rating_value: 5 },
    { rating_id: 'rating-current-user', owner: 'You', user_email: 'you@retogen.local', rating_value: 4 }
  ],
  comments: [
    {
      comment_id: 'comment-1',
      parent_comment_id: null,
      owner: 'Nadia',
      user_email: 'nadia@example.com',
      comment_content: 'ANC-nya terasa sangat stabil buat kerja di kafe. Mic juga jauh lebih aman untuk meeting dibanding beberapa model lain di kelas harga yang sama.',
      created_at: '2026-03-12T09:10:00.000Z'
    },
    {
      comment_id: 'comment-2',
      parent_comment_id: 'comment-1',
      owner: 'Raka',
      user_email: 'raka@example.com',
      comment_content: 'Setuju. Buat call quality memang salah satu yang paling konsisten. Saya juga suka karena dipakai lama tetap nyaman.',
      created_at: '2026-03-12T10:25:00.000Z'
    },
    {
      comment_id: 'comment-3',
      parent_comment_id: null,
      owner: 'Aldo',
      user_email: 'aldo@example.com',
      comment_content: 'Karakter suaranya aman untuk banyak genre. Tidak terlalu fun, tapi justru enak buat dipakai harian.',
      created_at: '2026-03-13T07:40:00.000Z'
    },
    {
      comment_id: 'comment-4',
      parent_comment_id: null,
      owner: 'You',
      user_email: 'you@retogen.local',
      comment_content: 'Dipakai beberapa jam masih nyaman. Menurut saya, kekuatan utamanya ada di ANC dan kualitas mikrofon.',
      created_at: '2026-03-13T11:15:00.000Z'
    },
    {
      comment_id: 'comment-5',
      parent_comment_id: 'comment-4',
      owner: 'You',
      user_email: 'you@retogen.local',
      comment_content: 'Untuk harga promo, produk ini masih sangat kompetitif di kelas headphone premium.',
      created_at: '2026-03-13T11:30:00.000Z'
    }
  ]
})