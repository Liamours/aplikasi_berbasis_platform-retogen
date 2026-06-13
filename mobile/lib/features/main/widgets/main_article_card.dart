import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/main/models/main_article.dart';

class MainArticleCard extends StatefulWidget {
  final MainArticle article;
  final String? activeTag;
  final void Function(String tag) onTagTap;

  const MainArticleCard({
    super.key,
    required this.article,
    required this.activeTag,
    required this.onTagTap,
  });

  @override
  State<MainArticleCard> createState() => _MainArticleCardState();
}

class _MainArticleCardState extends State<MainArticleCard> {
  Uint8List? _imageBytes;

  @override
  void initState() {
    super.initState();
    _imageBytes = decodeBase64Image(widget.article.imageBase64);
  }

  @override
  void didUpdateWidget(MainArticleCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.article.imageBase64 != widget.article.imageBase64) {
      _imageBytes = decodeBase64Image(widget.article.imageBase64);
    }
  }

  @override
  Widget build(BuildContext context) {
    final imageBytes = _imageBytes;

    return GestureDetector(
      onTap: () => context.push('/articles/${widget.article.id}'),
      child: Container(
        decoration: BoxDecoration(
          color: AppTheme.glassBg,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: AppTheme.glassBorder),
          boxShadow: const [
            BoxShadow(
              color: AppTheme.glassShadow,
              offset: Offset(0, 4),
              blurRadius: 14,
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ── Image ─────────────────────────────────
            ClipRRect(
              borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(17)),
              child: AspectRatio(
                aspectRatio: 16 / 9,
                child: imageBytes != null
                    ? Image.memory(imageBytes,
                        fit: BoxFit.cover, gaplessPlayback: true)
                    : Image.asset(
                        'assets/logo.jpg',
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => Container(
                          color: AppTheme.bgSurface,
                          child: const Center(
                            child: Icon(
                              Icons.image_outlined,
                              color: AppTheme.textMuted,
                              size: 36,
                            ),
                          ),
                        ),
                      ),
              ),
            ),

            // ── Text + tags ───────────────────────────
            Padding(
              padding: const EdgeInsets.fromLTRB(14, 12, 14, 14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    widget.article.title,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: AppTheme.textPrimary,
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                      height: 1.25,
                    ),
                  ),
                  if (widget.article.preview.isNotEmpty) ...[
                    const SizedBox(height: 6),
                    Text(
                      widget.article.preview,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        color: AppTheme.textSecondary,
                        fontSize: 13,
                        height: 1.5,
                      ),
                    ),
                  ],
                  if (widget.article.tags.isNotEmpty) ...[
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: widget.article.tags.map((tag) {
                        final isActive = tag == widget.activeTag;
                        return GestureDetector(
                          onTap: () => widget.onTagTap(tag),
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: isActive
                                  ? AppTheme.primaryCyan
                                      .withValues(alpha: 0.15)
                                  : AppTheme.primaryRed
                                      .withValues(alpha: 0.10),
                              borderRadius: BorderRadius.circular(8),
                              border: isActive
                                  ? Border.all(
                                      color: AppTheme.primaryCyan
                                          .withValues(alpha: 0.5))
                                  : null,
                            ),
                            child: Text(
                              tag,
                              style: TextStyle(
                                color: isActive
                                    ? AppTheme.primaryCyan
                                    : AppTheme.primaryRed,
                                fontSize: 11,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
