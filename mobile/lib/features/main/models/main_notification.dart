import 'package:retogen/features/articles/utils/article_data_utils.dart';

class MainNotification {
  final String id;
  final String articleId;
  final String articleTitle;
  final List<String> tags;
  final String createdAt;
  final bool isRead;

  const MainNotification({
    required this.id,
    required this.articleId,
    required this.articleTitle,
    required this.tags,
    required this.createdAt,
    this.isRead = false,
  });

  factory MainNotification.fromJson(Map<String, dynamic> json) {
    return MainNotification(
      id: json['notification_id']?.toString() ?? '',
      articleId: json['article_id']?.toString() ?? '',
      articleTitle: json['article_title']?.toString() ?? 'Artikel baru',
      tags: asStringList(json['tags']),
      createdAt: json['created_at']?.toString() ?? '',
      isRead: json['is_read'] == true,
    );
  }
}
