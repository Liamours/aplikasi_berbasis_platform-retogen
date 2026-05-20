import 'package:flutter/material.dart';
import 'package:retogen/core/router.dart';
import 'package:retogen/core/theme.dart';

void main() {
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
