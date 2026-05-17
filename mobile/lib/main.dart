import 'package:flutter/material.dart';
import 'package:retogen/core/router.dart';

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
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6C63FF)),
        useMaterial3: true,
      ),
      routerConfig: router,
    );
  }
}
