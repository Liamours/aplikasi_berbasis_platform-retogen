import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/help/help_item.dart';
import 'package:retogen/features/help/help_detail_page.dart';

class HelpPage extends StatelessWidget {
  const HelpPage({super.key});

  static const _items = [
    HelpItem(
      question: 'Bagaimana cara melakukan subscribe pada tag tertentu?',
      steps: [
        'Buka aplikasi dan pastikan sudah login.',
        'Di halaman utama, temukan tombol "Filter Tag".',
        'Tap "Filter Tag" tersebut untuk melihat tag yang tersedia.',
        'Tap ikon bintang yang muncul di sebelah nama tag.',
        'Setelah bintang berwarna orange, kamu akan mendapat notifikasi setiap ada artikel baru dengan tag tersebut.',
      ],
    ),
    HelpItem(
      question: 'Bagaimana cara report komentar user?',
      steps: [
        'Buka artikel yang berisi komentar yang ingin kamu laporkan.',
        'Scroll ke bagian komentar.',
        'Tekan titik tiga pada komentar yang ingin dilaporkan.',
        'Pilih opsi "Laporkan" dari menu yang muncul.',
        'Pilih alasan laporan dan konfirmasi.',
      ],
    ),
    HelpItem(
      question: 'Bagaimana cara report artikel?',
      steps: [
        'Buka artikel yang ingin kamu laporkan.',
        'Tap ikon bendera di pojok kanan atas halaman artikel.',
        'Pilih alasan laporan dan konfirmasi.',
      ],
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.bgPage,
      appBar: AppBar(
        backgroundColor: AppTheme.bgPage,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded,
              color: AppTheme.textPrimary, size: 18),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: const Text(
          'Pusat Bantuan',
          style: TextStyle(
            color: AppTheme.textPrimary,
            fontSize: 16,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: _items.length,
        separatorBuilder: (_, __) => const SizedBox(height: 8),
        itemBuilder: (context, i) {
          final item = _items[i];
          return GestureDetector(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => HelpDetailPage(item: item)),
            ),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              decoration: BoxDecoration(
                color: AppTheme.bgSurface,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.glassBorder),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      item.question,
                      style: const TextStyle(
                        color: AppTheme.textPrimary,
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Icon(Icons.chevron_right_rounded,
                      color: AppTheme.textSecondary, size: 20),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
