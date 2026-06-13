import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:go_router/go_router.dart';
import 'package:retogen/core/api_client.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';
import 'package:retogen/features/main/models/main_notification.dart';

class MainNotificationSheet extends StatefulWidget {
  final List<MainNotification> notifications;
  final bool isLoading;

  const MainNotificationSheet({
    super.key,
    required this.notifications,
    required this.isLoading,
  });

  @override
  State<MainNotificationSheet> createState() => _MainNotificationSheetState();
}

class _MainNotificationSheetState extends State<MainNotificationSheet> {
  static const _storage = FlutterSecureStorage();
  static const _readKey = 'read_notification_ids';

  Set<String> _readIds = {};
  bool _loadingRead = true;

  @override
  void initState() {
    super.initState();
    _loadReadIds();
  }

  Future<void> _loadReadIds() async {
    final raw = await _storage.read(key: _readKey);
    final localIds = raw != null && raw.isNotEmpty
        ? raw.split(',').toSet()
        : <String>{};

    setState(() {
      _readIds = localIds;
      _loadingRead = false;
    });

    // Sync notifikasi yang sudah dibaca lokal tapi belum tercatat di backend
    for (final notif in widget.notifications) {
      if (!notif.isRead && localIds.contains(notif.id)) {
        ApiClient.instance
            .post('/notification/mark_read', data: {'notification_id': notif.id})
            .catchError((_) {});
      }
    }
  }

  Future<void> _markAsRead(String id) async {
    // Update lokal dulu supaya UI responsif
    final next = {..._readIds, id};
    await _storage.write(key: _readKey, value: next.join(','));
    if (mounted) setState(() => _readIds = next);
    // Sync ke backend (fire-and-forget, tidak di-await)
    ApiClient.instance
        .post('/notification/mark_read', data: {'notification_id': id})
        .catchError((_) {});
  }

  // Unread = backend belum tandai is_read DAN belum di-tap sesi ini
  List<MainNotification> get _unreadNotifs => widget.notifications
      .where((n) => !n.isRead && !_readIds.contains(n.id))
      .toList();

  @override
  Widget build(BuildContext context) {
    final unread = _unreadNotifs;

    return ArticleBottomSheetSurface(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Handle bar
          Center(
            child: Container(
              width: 40,
              height: 4,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: AppTheme.glassBorder,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),

          // Header
          Row(
            children: [
              const Text(
                'Notifikasi',
                style: TextStyle(
                  color: AppTheme.textPrimary,
                  fontSize: 20,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const Spacer(),
              if (unread.isNotEmpty)
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 9, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppTheme.primaryRed.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    '${unread.length} baru',
                    style: const TextStyle(
                      color: AppTheme.primaryRed,
                      fontSize: 12,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 4),
          const Text(
            'Artikel baru dari tag yang kamu subscribe',
            style: TextStyle(color: AppTheme.textMuted, fontSize: 13),
          ),
          const SizedBox(height: 16),

          // Body
          if (widget.isLoading || _loadingRead)
            const Center(
              child: Padding(
                padding: EdgeInsets.symmetric(vertical: 28),
                child: CircularProgressIndicator(color: AppTheme.primaryCyan),
              ),
            )
          else if (unread.isEmpty)
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 28),
                child: Column(
                  children: const [
                    Icon(
                      Icons.notifications_none_rounded,
                      size: 42,
                      color: AppTheme.textMuted,
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Semua notifikasi sudah dibaca',
                      style: TextStyle(color: AppTheme.textMuted, fontSize: 14),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'Subscribe tag untuk mendapat notifikasi baru',
                      style: TextStyle(color: AppTheme.textMuted, fontSize: 12),
                    ),
                  ],
                ),
              ),
            )
          else
            ConstrainedBox(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.45,
              ),
              child: ListView.separated(
                shrinkWrap: true,
                physics: const ClampingScrollPhysics(),
                itemCount: unread.length,
                separatorBuilder: (_, __) => const Divider(
                  color: AppTheme.glassBorder,
                  height: 1,
                ),
                itemBuilder: (context, index) {
                  final notif = unread[index];
                  return _NotifTile(
                    notification: notif,
                    onTap: () {
                      final articleId = notif.articleId;
                      final go = GoRouter.of(context);
                      // Mark read di background, jangan await
                      _markAsRead(notif.id);
                      // Tutup sheet lalu navigate pakai router yang sudah di-capture
                      Navigator.of(context).pop();
                      go.push('/articles/$articleId');
                    },
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}

class _NotifTile extends StatelessWidget {
  final MainNotification notification;
  final VoidCallback onTap;

  const _NotifTile({required this.notification, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(10),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Icon
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: AppTheme.primaryCyan.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(
                Icons.article_outlined,
                color: AppTheme.primaryCyan,
                size: 20,
              ),
            ),
            const SizedBox(width: 12),

            // Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    notification.articleTitle,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: AppTheme.textPrimary,
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      height: 1.3,
                    ),
                  ),
                  if (notification.tags.isNotEmpty) ...[
                    const SizedBox(height: 5),
                    Wrap(
                      spacing: 4,
                      runSpacing: 4,
                      children: notification.tags
                          .map(
                            (tag) => Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 7, vertical: 2),
                              decoration: BoxDecoration(
                                color: AppTheme.primaryRed
                                    .withValues(alpha: 0.10),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(
                                tag,
                                style: const TextStyle(
                                  color: AppTheme.primaryRed,
                                  fontSize: 10,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ),
                          )
                          .toList(),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(width: 8),
            const Icon(
              Icons.arrow_forward_ios_rounded,
              size: 13,
              color: AppTheme.textMuted,
            ),
          ],
        ),
      ),
    );
  }
}
