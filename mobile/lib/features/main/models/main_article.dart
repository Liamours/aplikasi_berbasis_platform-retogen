import 'package:retogen/features/articles/utils/article_data_utils.dart';

class MainArticle {
  final String id;
  final String title;
  final String preview;
  final List<String> tags;
  final String? imageBase64;

  const MainArticle({
    required this.id,
    required this.title,
    required this.preview,
    required this.tags,
    required this.imageBase64,
  });

  factory MainArticle.fromJson(Map<String, dynamic> json) {
    // Backend may return article_tags (array) or article_tag (singular string).
    // asStringList handles both cases.
    final rawTags = json['article_tags'] ?? json['article_tag'];

    return MainArticle(
      id: json['article_id']?.toString() ?? '',
      title: json['article_title']?.toString() ?? '',
      preview: json['article_preview']?.toString() ?? '',
      tags: asStringList(rawTags),
      imageBase64: json['article_image']?.toString(),
    );
  }
}
