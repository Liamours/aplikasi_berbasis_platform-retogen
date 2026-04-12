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
      id: 'price-1',
      store: 'Tokopedia',
      price: 5299000,
      shippingNote: 'Gratis ongkir kota besar',
      url: '#',
      updatedAt: '10 menit lalu',
      trend: 'down'
    },
    {
      id: 'price-2',
      store: 'Shopee',
      price: 5345000,
      shippingNote: 'Voucher toko tersedia',
      url: '#',
      updatedAt: '18 menit lalu',
      trend: 'stable'
    },
    {
      id: 'price-3',
      store: 'Bukalapak',
      price: 5489000,
      shippingNote: 'Pengiriman same day terbatas',
      url: '#',
      updatedAt: '32 menit lalu',
      trend: 'up'
    }
  ],
  ratings: [
    { rating_id: 'rating-1', owner: 'Aldo', user_email: 'aldo@example.com', rating_value: 5 },
    { rating_id: 'rating-2', owner: 'Nadia', user_email: 'nadia@example.com', rating_value: 4 },
    { rating_id: 'rating-3', owner: 'Raka', user_email: 'raka@example.com', rating_value: 5 }
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
    }
  ]
})
