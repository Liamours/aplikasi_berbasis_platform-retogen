import 'package:retogen/core/api_client.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/main/models/main_article.dart';
import 'package:retogen/features/main/models/main_notification.dart';

class MainService {
  /// POST /article/main_page
  /// Returns { articles, username }.
  static Future<Map<String, dynamic>> fetchArticles({
    String sort = 'newest',
    String tag = '',
    String search = '',
  }) async {
    final response = await ApiClient.instance.post(
      '/article/main_page',
      data: {'sort': sort, 'tag': tag, 'search': search},
    );
    final data = asMap(response.data);
    final articles = asMapList(data['list_article'])
        .map(MainArticle.fromJson)
        .toList();
    return {
      'articles': articles,
      'username': data['username']?.toString() ?? '',
    };
  }

  /// POST /subscription/get — returns list of subscribed tag strings.
  static Future<List<String>> fetchSubscriptions() async {
    final response = await ApiClient.instance.post('/subscription/get');
    return asStringList(asMap(response.data)['tags']);
  }

  /// POST /subscription/subscribe
  static Future<String> subscribeTag(String tag) async {
    final response = await ApiClient.instance.post(
      '/subscription/subscribe',
      data: {'tag': tag},
    );
    return asMap(response.data)['confirmation']?.toString() ?? '';
  }

  /// POST /subscription/unsubscribe
  static Future<String> unsubscribeTag(String tag) async {
    final response = await ApiClient.instance.post(
      '/subscription/unsubscribe',
      data: {'tag': tag},
    );
    return asMap(response.data)['confirmation']?.toString() ?? '';
  }

  /// POST /notification/get — returns newest-first list of notifications.
  static Future<List<MainNotification>> fetchNotifications() async {
    final response = await ApiClient.instance.post('/notification/get');
    return asMapList(asMap(response.data)['notifications'])
        .map(MainNotification.fromJson)
        .toList();
  }

  /// POST /user/get_details (own profile, no body required).
  static Future<Map<String, dynamic>> fetchUserDetails() async {
    final response = await ApiClient.instance.post('/user/get_details');
    return asMap(response.data);
  }
}
