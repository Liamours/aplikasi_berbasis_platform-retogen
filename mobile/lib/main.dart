import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:retogen/core/notification_service.dart';
import 'package:retogen/core/router.dart' show router;
import 'package:retogen/core/theme.dart';

/// Background / terminated message handler — must be a top-level function.
// Android otomatis tampilkan notifikasi dari FCM notification payload.
// Handler ini hanya wajib ada (tidak boleh dihapus) tapi tidak perlu show manual.
@pragma('vm:entry-point')
Future<void> _firebaseBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  FirebaseMessaging.onBackgroundMessage(_firebaseBackgroundHandler);

  // Minta izin notifikasi dari FCM (wajib agar getToken() tidak null)
  await FirebaseMessaging.instance.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );

  await NotificationService.init();

  // Notifikasi saat app foreground (Android tidak auto-show, harus manual)
  FirebaseMessaging.onMessage.listen((message) async {
    final title = message.notification?.title ?? '';
    if (title.isEmpty) return;
    await NotificationService.show(
      id: message.messageId?.hashCode ?? DateTime.now().millisecondsSinceEpoch,
      title: title,
      body: '',
    );
  });

  // Tap notifikasi saat app terminated → buka app lalu navigasi ke artikel
  final initial = await FirebaseMessaging.instance.getInitialMessage();
  if (initial != null) {
    final articleId = initial.data['article_id'];
    if (articleId != null && articleId.isNotEmpty) {
      pendingNotifArticleId = articleId;
    } else {
      pendingNotifNavigation = true;
    }
  }


  runApp(const RetoGenApp());
}

bool pendingNotifNavigation = false;
String? pendingNotifArticleId;

class RetoGenApp extends StatelessWidget {
  const RetoGenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'RetoGen',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.themeData,
      routerConfig: router,
    );
  }
}
