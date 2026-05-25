import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleRatingSection extends StatelessWidget {
  final ArticleDetail article;
  final int ratingDraft;
  final bool isSaving;
  final String helperLabel;
  final ValueChanged<int> onRatingSelected;

  const ArticleRatingSection({
    super.key,
    required this.article,
    required this.ratingDraft,
    required this.isSaving,
    required this.helperLabel,
    required this.onRatingSelected,
  });

  @override
  Widget build(BuildContext context) {
    return ArticleSectionCard(
      title: 'Rating pengguna',
      trailing: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(
            article.averageRatingText,
            style: const TextStyle(
              color: AppTheme.textPrimary,
              fontSize: 26,
              height: 1,
              fontWeight: FontWeight.w800,
            ),
          ),
          Text(
            'dari ${article.ratings.length} rating',
            style: const TextStyle(color: AppTheme.textSecondary, fontSize: 11),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            helperLabel,
            style: const TextStyle(
              color: AppTheme.textSecondary,
              fontSize: 13,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: List.generate(5, (index) {
              final value = index + 1;
              final active = value <= ratingDraft;
              return IconButton(
                visualDensity: VisualDensity.compact,
                onPressed: isSaving ? null : () => onRatingSelected(value),
                icon: Icon(
                  active ? Icons.star_rounded : Icons.star_outline_rounded,
                  color: active ? AppTheme.primaryRed : AppTheme.textMuted,
                  size: 32,
                ),
                tooltip: '$value dari 5',
              );
            }),
          ),
          if (ratingDraft > 0)
            Container(
              margin: const EdgeInsets.only(top: 8),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: AppTheme.primaryRed.withValues(alpha: 0.10),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                'Rating Anda: $ratingDraft/5',
                style: const TextStyle(
                  color: AppTheme.primaryRed,
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
