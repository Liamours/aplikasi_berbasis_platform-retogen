import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:retogen/core/api_client.dart';

/// Handles FCM token registration and foreground/background message routing.
class FcmService {
  static final _messaging = FirebaseMessaging.instance;

  static Future<void> init() async {
    // Request permission (iOS / Android 13+)
    await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );
    // Foreground FCM intentionally NOT shown here.
    // The polling timer in MainPage detects new notifications and shows them
    // once via flutter_local_notifications — preventing duplicates.
    // Background / terminated messages are handled by _firebaseBackgroundHandler in main.dart.
  }

  /// Call this right after the user logs in (auth token must already be saved).
  static Future<void> registerToken() async {
    try {
      final token = await _messaging.getToken();
      if (token == null) return;

      await ApiClient.instance.post(
        '/notification/register_fcm_token',
        data: {'token': token},
      );

      // Refresh token when it rotates
      _messaging.onTokenRefresh.listen((newToken) async {
        await ApiClient.instance.post(
          '/notification/register_fcm_token',
          data: {'token': newToken},
        );
      });
    } catch (_) {
      // Non-fatal — app works fine without push
    }
  }
}
