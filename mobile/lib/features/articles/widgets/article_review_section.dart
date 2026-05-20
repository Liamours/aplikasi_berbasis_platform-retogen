import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleReviewSection extends StatelessWidget {
  final ArticleDetail article;

  const ArticleReviewSection({super.key, required this.article});

  @override
  Widget build(BuildContext context) {
    final paragraphs = article.paragraphs;

    return ArticleSectionCard(
      title: 'Review',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: paragraphs.isEmpty
            ? const [
                Text(
                  'Konten review belum tersedia.',
                  style: TextStyle(
                    color: AppTheme.textSecondary,
                    fontSize: 14,
                    height: 1.7,
                  ),
                ),
              ]
            : paragraphs
                  .map(
                    (paragraph) => Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Text(
                        paragraph,
                        style: const TextStyle(
                          color: AppTheme.textSecondary,
                          fontSize: 14,
                          height: 1.75,
                        ),
                      ),
                    ),
                  )
                  .toList(),
      ),
    );
  }
}
