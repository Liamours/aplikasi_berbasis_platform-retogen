import 'package:flutter/material.dart';
import 'package:retogen/core/api_client.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class OtherUserProfileSheet extends StatefulWidget {
  final String userEmail;
  final bool isAdmin;

  const OtherUserProfileSheet({
    super.key,
    required this.userEmail,
    required this.isAdmin,
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
  List<dynamic> _reports = [];

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
      final endpoint = widget.isAdmin
          ? '/user/get_details'
          : '/report_user/get_user_profile';

      final response = await ApiClient.instance.post(
        endpoint,
        data: {'user_email': widget.userEmail},
      );

      final data = asMap(response.data);
      if (data['confirmation'] != 'successful') {
        setState(() => _error = 'Gagal memuat profil user.');
        return;
      }

      final user = asMap(data['user']);
      setState(() {
        _username = user['username']?.toString() ?? '-';
        _role = user['role']?.toString() ?? 'user';
        _createdAt = _formatDate(user['created_at']);
        _reports = asMapList(user['reports']);
        _loading = false;
      });
    } catch (_) {
      setState(() => _error = 'Gagal terhubung ke server.');
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  String _formatDate(dynamic raw) {
    if (raw == null) return '-';
    try {
      final dt = DateTime.parse(raw.toString()).toLocal();
      const months = [
        '', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
        'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'
      ];
      return '${dt.day} ${months[dt.month]} ${dt.year}';
    } catch (_) {
      return '-';
    }
  }

  String get _initials {
    return _username.isEmpty ? 'R' : _username[0].toUpperCase();
  }

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
            const SizedBox(height: 20),
            const CircularProgressIndicator(color: AppTheme.primaryCyan),
            const SizedBox(height: 20),
            const Text(
              'Memuat profil...',
              style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
            ),
            const SizedBox(height: 30),
          ] else if (_error != null) ...[
            const SizedBox(height: 20),
            const Icon(Icons.error_outline, color: AppTheme.primaryRed, size: 48),
            const SizedBox(height: 12),
            Text(
              _error!,
              style: const TextStyle(color: AppTheme.textSecondary, fontSize: 14),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
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
            // Eyebrow
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
            // Username
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
            // Created At
            Text(
              'Member since $_createdAt',
              style: const TextStyle(
                color: AppTheme.textSecondary,
                fontSize: 14,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),

            // Reports Section for Admin
            if (widget.isAdmin) ...[
              const Divider(color: AppTheme.glassBorder),
              const SizedBox(height: 10),
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'REPORTS (${_reports.length})',
                  style: const TextStyle(
                    color: AppTheme.textPrimary,
                    fontSize: 14,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              if (_reports.isEmpty)
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 10),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Tidak ada report untuk user ini.',
                      style: TextStyle(
                        color: AppTheme.textMuted,
                        fontStyle: FontStyle.italic,
                        fontSize: 13,
                      ),
                    ),
                  ),
                )
              else
                ConstrainedBox(
                  constraints: const BoxConstraints(maxHeight: 200),
                  child: ListView.builder(
                    shrinkWrap: true,
                    itemCount: _reports.length,
                    itemBuilder: (ctx, i) {
                      final r = asMap(_reports[i]);
                      final date = _formatDate(r['created_at']);
                      final desc = r['description']?.toString() ?? '';
                      return Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.05),
                          border: Border.all(color: AppTheme.glassBorder),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              date,
                              style: const TextStyle(
                                color: AppTheme.textMuted,
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              desc,
                              style: const TextStyle(
                                color: AppTheme.textSecondary,
                                fontSize: 13,
                                height: 1.45,
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ),
              const SizedBox(height: 10),
            ],
            const SizedBox(height: 10),
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
