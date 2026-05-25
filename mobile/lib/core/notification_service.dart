import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  static final _plugin = FlutterLocalNotificationsPlugin();
  static bool _ready = false;

  static Future<void> init() async {
    if (_ready) return;

    // Android init — pakai app icon sebagai notif icon
    const androidSettings =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    const settings = InitializationSettings(android: androidSettings);
    await _plugin.initialize(settings);

    final android = _plugin.resolvePlatformSpecificImplementation<
        AndroidFlutterLocalNotificationsPlugin>();

    // Buat notification channel (wajib Android 8+)
    await android?.createNotificationChannel(
      const AndroidNotificationChannel(
        'retogen_channel',
        'RetoGen',
        description: 'Artikel baru dari tag yang kamu subscribe',
        importance: Importance.high,
      ),
    );

    // Minta izin notifikasi (Android 13+)
    await android?.requestNotificationsPermission();

    _ready = true;
  }

  /// Tampilkan notifikasi sistem.
  /// [id] harus unik per notifikasi — gunakan hashCode dari notification_id.
  static Future<void> show({
    required int id,
    required String title,
    required String body,
  }) async {
    if (!_ready) return;

    const details = NotificationDetails(
      android: AndroidNotificationDetails(
        'retogen_channel',
        'RetoGen',
        channelDescription: 'Artikel baru dari tag yang kamu subscribe',
        importance: Importance.high,
        priority: Priority.high,
        icon: '@mipmap/ic_launcher',
      ),
    );

    await _plugin.show(id, title, body, details);
  }
}
