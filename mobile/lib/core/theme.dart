import 'package:flutter/material.dart';

class AppTheme {
  // Brand
  static const Color primaryCyan = Color(0xFF6AADA8);
  static const Color primaryRed = Color(0xFFB56B52);
  static const Color hoverCyan = Color(0xFF528E8A);
  static const Color hoverRed = Color(0xFF965748);

  // Text
  static const Color textPrimary = Color(0xFF282826);
  static const Color textSecondary = Color(0xFF636360);
  static const Color textMuted = Color(0xFF9A9895);

  // Background
  static const Color bgPage = Color(0xFFEDEAE4);
  static const Color bgSurface = Color(0xFFF2EFE9);

  // Glass (Light Mode Equivalents)
  static const Color glassBg = Color(0x8CF2EFE9); 
  static const Color glassBorder = Color(0x2EA09B91); 
  static const Color glassEdge = Color(0x99FFFFFF); 
  static const Color glassShadow = Color(0x123C3732); 

  // Input
  static const Color inputBg = Color(0x73FFFFFF);
  static const Color inputFocusBorder = Color(0x7300CED1); 
  static const Color inputFocusShadow = Color(0x1F00CED1); 
  static const Color inputErrorBorder = Color(0x73E34234); 
  static const Color inputErrorBg = Color(0x1AE34234);
  
  static ThemeData get themeData {
    return ThemeData(
      colorScheme: ColorScheme.fromSeed(seedColor: primaryCyan),
      scaffoldBackgroundColor: bgPage,
      useMaterial3: true,
      textTheme: const TextTheme(
        bodyLarge: TextStyle(color: textPrimary),
        bodyMedium: TextStyle(color: textPrimary),
      ),
    );
  }
}
