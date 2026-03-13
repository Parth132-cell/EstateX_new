import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1565C0)),
      useMaterial3: true,
      scaffoldBackgroundColor: const Color(0xFFF7FAFF),
      appBarTheme: const AppBarTheme(centerTitle: false),
    );
  }
}
