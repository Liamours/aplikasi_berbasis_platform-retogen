import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticlePriceTracker extends StatelessWidget {
  final ArticleDetail article;
  final bool isLoading;

  const ArticlePriceTracker({
    super.key,
    required this.article,
    required this.isLoading,
  });

  @override
  Widget build(BuildContext context) {
    final topPrices = article.topRatedPrices;
    final bestPrice = article.lowestPrice;

    return ArticleSectionCard(
      eyebrow: 'Monitor harga',
      title: 'Pantau harga',
      subtitle: 'Top 3 toko berdasarkan rating',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (bestPrice != null) ...[
            Row(
              children: [
                const Expanded(
                  child: Text(
                    'Harga terbaik',
                    style: TextStyle(
                      color: AppTheme.textSecondary,
                      fontSize: 13,
                    ),
                  ),
                ),
                Text(
                  formatRupiah(bestPrice.price),
                  style: const TextStyle(
                    color: AppTheme.textPrimary,
                    fontSize: 18,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ],
            ),
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 14),
              child: Divider(color: AppTheme.glassBorder, height: 1),
            ),
          ],
          if (isLoading && topPrices.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 12),
              child: Row(
                children: [
                  SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      color: AppTheme.primaryCyan,
                    ),
                  ),
                  SizedBox(width: 10),
                  Text(
                    'Memuat data harga.',
                    style: TextStyle(
                      color: AppTheme.textSecondary,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            )
          else if (topPrices.isEmpty)
            const Text(
              'Belum ada data harga.',
              style: TextStyle(color: AppTheme.textSecondary, fontSize: 13),
            )
          else
            ...topPrices.map(_PriceRow.new),
        ],
      ),
    );
  }
}

class _PriceRow extends StatelessWidget {
  final PriceEntry price;

  const _PriceRow(this.price);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.18),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppTheme.glassBorder),
            ),
            alignment: Alignment.center,
            child: Text(
              price.storeInitial,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: Text(
                        price.storeLabel,
                        style: const TextStyle(
                          color: AppTheme.textPrimary,
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                    Text(
                      '${price.ratingText}/5',
                      style: const TextStyle(
                        color: AppTheme.primaryCyan,
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  price.product,
                  style: const TextStyle(
                    color: AppTheme.textSecondary,
                    fontSize: 13,
                    height: 1.45,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  formatRupiah(price.price),
                  style: const TextStyle(
                    color: AppTheme.textPrimary,
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
