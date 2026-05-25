import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleDetailHero extends StatelessWidget {
  final ArticleDetail article;
  final VoidCallback onBack;
  final VoidCallback onReportArticle;

  const ArticleDetailHero({
    super.key,
    required this.article,
    required this.onBack,
    required this.onReportArticle,
  });

  @override
  Widget build(BuildContext context) {
    final imageBytes = decodeBase64Image(article.imageBase64);

    return ArticleSurfaceCard(
      padding: 18,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              IconButton(
                onPressed: onBack,
                icon: const Icon(Icons.arrow_back),
                tooltip: 'Kembali',
              ),
              const Expanded(
                child: Text(
                  'Home / Article',
                  style: TextStyle(
                    color: AppTheme.textSecondary,
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              IconButton(
                onPressed: onReportArticle,
                icon: const Icon(Icons.flag_outlined),
                tooltip: 'Laporkan artikel',
                color: AppTheme.primaryRed,
              ),
            ],
          ),
          const SizedBox(height: 14),
          ClipRRect(
            borderRadius: BorderRadius.circular(18),
            child: AspectRatio(
              aspectRatio: 4 / 3,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  color: AppTheme.bgSurface,
                  border: Border.all(color: AppTheme.glassBorder),
                ),
                child: imageBytes == null
                    ? Image.asset(
                        'assets/logo.jpg',
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return const Icon(
                            Icons.image_outlined,
                            color: AppTheme.textMuted,
                            size: 42,
                          );
                        },
                      )
                    : Image.memory(imageBytes, fit: BoxFit.cover),
              ),
            ),
          ),
          const SizedBox(height: 18),
          const Text(
            'Electronic review',
            style: TextStyle(
              color: AppTheme.textMuted,
              fontSize: 12,
              fontWeight: FontWeight.w800,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            article.title,
            style: const TextStyle(
              color: AppTheme.textPrimary,
              fontSize: 28,
              fontWeight: FontWeight.w800,
              height: 1.08,
            ),
          ),
          if (article.preview.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              article.preview,
              style: const TextStyle(
                color: AppTheme.textSecondary,
                fontSize: 14,
                height: 1.7,
              ),
            ),
          ],
          if (article.tags.isNotEmpty) ...[
            const SizedBox(height: 14),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: article.tags.map(buildArticleTagChip).toList(),
            ),
          ],
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              ArticleMetaPill(
                icon: Icons.star_rounded,
                value: '${article.averageRatingText}/5',
                label: 'Rating',
              ),
              ArticleMetaPill(
                icon: Icons.chat_bubble_outline,
                value: article.totalComments.toString(),
                label: 'Komentar',
              ),
              if (article.lowestPrice != null)
                ArticleMetaPill(
                  icon: Icons.local_offer_outlined,
                  value: formatRupiah(article.lowestPrice!.price),
                  label: 'Harga terbaik',
                ),
            ],
          ),
        ],
      ),
    );
  }
}
