import 'package:flutter/material.dart';
import 'package:retogen/core/api_client.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class OtherUserProfileSheet extends StatefulWidget {
  final String userEmail;

  const OtherUserProfileSheet({
    super.key,
    required this.userEmail,
  });

  @override
  State<OtherUserProfileSheet> createState() => _OtherUserProfileSheetState();
}

class _OtherUserProfileSheetState extends State<OtherUserProfileSheet> {
  bool _loading = true;
  String? _error;

  String _username = '';
  String _role = '';
  String _createdAt = '';

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final response = await ApiClient.instance.post(
        '/report_user/get_user_profile',
        data: {'user_email': widget.userEmail},
      );

      final data = asMap(response.data);
      if (data['confirmation'] != 'successful') {
        setState(() {
          _error = 'Gagal memuat profil user.';
          _loading = false;
        });
        return;
      }

      final user = asMap(data['user']);
      setState(() {
        _username = user['username']?.toString() ?? '-';
        _role = user['role']?.toString() ?? 'user';
        _createdAt = _formatDate(user['created_at']);
        _loading = false;
      });
    } catch (_) {
      setState(() {
        _error = 'Gagal terhubung ke server.';
        _loading = false;
      });
    }
  }

  String _formatDate(dynamic raw) {
    if (raw == null) return '-';
    try {
      final dt = DateTime.parse(raw.toString()).toLocal();
      const months = [
        '', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
        'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des',
      ];
      return '${dt.day} ${months[dt.month]} ${dt.year}';
    } catch (_) {
      return '-';
    }
  }

  String get _initials =>
      _username.isEmpty ? '?' : _username[0].toUpperCase();

  @override
  Widget build(BuildContext context) {
    return ArticleBottomSheetSurface(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Align(
            alignment: Alignment.centerRight,
            child: IconButton(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.close),
              tooltip: 'Tutup',
            ),
          ),
          if (_loading) ...[
            const SizedBox(height: 16),
            const CircularProgressIndicator(color: AppTheme.primaryCyan),
            const SizedBox(height: 14),
            const Text(
              'Memuat profil...',
              style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
            ),
            const SizedBox(height: 24),
          ] else if (_error != null) ...[
            const SizedBox(height: 12),
            const Icon(Icons.error_outline, color: AppTheme.primaryRed, size: 44),
            const SizedBox(height: 10),
            Text(
              _error!,
              style: const TextStyle(color: AppTheme.textSecondary, fontSize: 14),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: _fetchProfile,
                child: const Text('Coba Lagi'),
              ),
            ),
            const SizedBox(height: 10),
          ] else ...[
            // Avatar
            Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                color: const Color(0x246AADA8),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppTheme.glassBorder),
              ),
              alignment: Alignment.center,
              child: Text(
                _initials,
                style: const TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.w800,
                  color: AppTheme.primaryCyan,
                ),
              ),
            ),
            const SizedBox(height: 14),
            Text(
              _role.toUpperCase(),
              style: const TextStyle(
                color: AppTheme.textMuted,
                fontSize: 12,
                fontWeight: FontWeight.w800,
                letterSpacing: 0.8,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              _username,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontSize: 24,
                fontWeight: FontWeight.w800,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 4),
            Text(
              'Member since $_createdAt',
              style: const TextStyle(
                color: AppTheme.textSecondary,
                fontSize: 14,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Tutup'),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
