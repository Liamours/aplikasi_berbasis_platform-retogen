import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:retogen/core/notification_service.dart';
import 'package:retogen/core/router.dart';
import 'package:retogen/core/theme.dart';

/// Background / terminated message handler — must be a top-level function.
@pragma('vm:entry-point')
Future<void> _firebaseBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  await NotificationService.init();
  final title = message.notification?.title ?? 'RetoGen';
  final body  = message.notification?.body  ?? '';
  if (title.isEmpty && body.isEmpty) return;
  await NotificationService.show(
    id: message.messageId?.hashCode ?? DateTime.now().millisecondsSinceEpoch,
    title: title,
    body: body,
  );
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  FirebaseMessaging.onBackgroundMessage(_firebaseBackgroundHandler);
  await NotificationService.init();
  runApp(const RetoGenApp());
}

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
