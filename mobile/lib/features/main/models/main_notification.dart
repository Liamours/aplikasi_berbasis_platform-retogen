import 'package:retogen/features/articles/utils/article_data_utils.dart';

class MainNotification {
  final String id;
  final String articleId;
  final String articleTitle;
  final List<String> tags;
  final String createdAt;

  const MainNotification({
    required this.id,
    required this.articleId,
    required this.articleTitle,
    required this.tags,
    required this.createdAt,
  });

  factory MainNotification.fromJson(Map<String, dynamic> json) {
    return MainNotification(
      id: json['notification_id']?.toString() ?? '',
      articleId: json['article_id']?.toString() ?? '',
      articleTitle: json['article_title']?.toString() ?? 'Artikel baru',
      tags: asStringList(json['tags']),
      createdAt: json['created_at']?.toString() ?? '',
    );
  }
}
