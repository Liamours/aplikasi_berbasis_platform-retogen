import 'dart:convert';
import 'dart:typed_data';

Map<String, dynamic> asMap(dynamic value) {
  if (value is Map<String, dynamic>) return value;
  if (value is Map) return Map<String, dynamic>.from(value);
  return <String, dynamic>{};
}

List<Map<String, dynamic>> asMapList(dynamic value) {
  if (value is! List) return const [];

  return value
      .whereType<Map>()
      .map((item) => Map<String, dynamic>.from(item))
      .toList();
}

List<String> asStringList(dynamic value) {
  if (value is List) {
    return value.map((item) => item.toString()).toList();
  }

  if (value is String && value.trim().isNotEmpty) {
    return value.split(',').map((item) => item.trim()).toList();
  }

  return const [];
}

String deriveArticlePreview(String content) {
  final normalized = content.replaceAll(RegExp(r'\s+'), ' ').trim();
  if (normalized.length <= 128) return normalized;
  return normalized.substring(0, 128);
}

Uint8List? decodeBase64Image(String? raw) {
  if (raw == null || raw.trim().isEmpty) return null;

  try {
    final value = raw.contains(',') ? raw.split(',').last : raw;
    return base64Decode(value);
  } catch (_) {
    return null;
  }
}

String formatRupiah(num value) {
  final digits = value.round().toString();
  final buffer = StringBuffer();

  for (var i = 0; i < digits.length; i++) {
    final position = digits.length - i;
    buffer.write(digits[i]);
    if (position > 1 && position % 3 == 1) {
      buffer.write('.');
    }
  }

  return 'Rp$buffer';
}
