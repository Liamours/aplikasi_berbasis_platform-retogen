import 'dart:async';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:retogen/core/notification_service.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/core/widgets/glass_background.dart';
import 'package:retogen/features/main/models/main_article.dart';
import 'package:retogen/features/main/models/main_notification.dart';
import 'package:retogen/features/main/services/main_service.dart';
import 'package:retogen/features/main/widgets/main_article_card.dart';
import 'package:retogen/features/main/widgets/main_article_skeleton.dart';
import 'package:retogen/features/main/widgets/main_notification_sheet.dart';
import 'package:retogen/features/main/widgets/main_sort_bar.dart';
import 'package:retogen/features/main/widgets/main_tag_filter.dart';
import 'package:retogen/core/api_client.dart';
import 'package:retogen/core/router.dart' show routeObserver;
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:retogen/main.dart' show pendingNotifNavigation, pendingNotifArticleId;

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> with RouteAware {
  final _searchCtrl = TextEditingController();
  Timer? _debounce;
  Timer? _articleTimer;
  Timer? _notifTimer;

  // Article list
  List<MainArticle> _articles = [];
  bool _loading = true;
  String? _error;

  // New article banner
  int _pendingNewCount = 0;
  bool _showNewBanner = false;
  List<MainArticle> _pendingArticles = [];

  // Filter state
  String _sort = 'newest';
  String _activeTag = '';

  // Subscriptions
  Set<String> _subscriptions = {};

  // Notifications
  List<MainNotification> _notifications = [];
  bool _notifLoading = false;
  // Static — persists across page rebuilds so we never re-show old notifications
  static final Set<String> _knownNotifIds = {};
  static bool _notifInitialized = false;

  // User
  String _username = '';
  StreamSubscription<RemoteMessage>? _fcmOpenedSub;

  // ── Lifecycle ────────────────────────────────────────────────────────────

  @override
  void initState() {
    super.initState();
    _init();

    // Handle tap notifikasi saat app background (fire setelah MainPage mount)
    _fcmOpenedSub = FirebaseMessaging.onMessageOpenedApp.listen((message) async {
      final articleId = message.data['article_id'];
      await _fetchArticles(clearFirst: true);
      if (mounted && articleId != null && articleId.isNotEmpty) {
        context.push('/articles/$articleId');
      }
    });

    // Auto-refresh artikel setiap 5 detik
    _articleTimer = Timer.periodic(
      const Duration(seconds: 5),
      (_) => _fetchArticles(silent: true),
    );

    // Poll notifikasi setiap 30 detik
    _notifTimer = Timer.periodic(
      const Duration(seconds: 10),
      (_) => _fetchNotifications(),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final route = ModalRoute.of(context);
    if (route != null) routeObserver.subscribe(this, route);
  }

  @override
  void didPopNext() {}

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    _fcmOpenedSub?.cancel();
    _debounce?.cancel();
    _articleTimer?.cancel();
    _notifTimer?.cancel();
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    await Future.wait([
      _fetchArticles(),
      _fetchSubscriptions(),
      _fetchNotifications(),
      _fetchUserDetails(),
      MainService.registerFcmToken(),
    ]);

    // App dibuka dari tap notifikasi saat terminated
    if (pendingNotifArticleId != null) {
      final articleId = pendingNotifArticleId!;
      pendingNotifArticleId = null;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) context.push('/articles/$articleId');
      });
    } else if (pendingNotifNavigation) {
      pendingNotifNavigation = false;
    }
  }

  // ── API calls ─────────────────────────────────────────────────────────────

  /// Builds the effective sort value to send to the backend.
  /// search_title takes priority, then by_tag, then the selected sort.
  String get _effectiveSort {
    if (_searchCtrl.text.trim().isNotEmpty) return 'search_title';
    if (_activeTag.isNotEmpty) return 'by_tag';
    return _sort;
  }

  Future<void> _fetchArticles({bool silent = false, bool clearFirst = false}) async {
    if (!mounted) return;
    if (!silent) {
      setState(() {
        if (clearFirst) _articles = [];
        _loading = clearFirst || _articles.isEmpty;
        _error = null;
      });
    }

    try {
      final result = await MainService.fetchArticles(
        sort: _effectiveSort,
        tag: _activeTag,
        search: _searchCtrl.text.trim(),
      );
      if (!mounted) return;
      final articles = result['articles'] as List<MainArticle>;
      final username = result['username'] as String? ?? '';

      if (silent && _articles.isNotEmpty) {
        // Deteksi perubahan
        final oldIds = _articles.map((a) => a.id).toSet();
        final newIds = articles.map((a) => a.id).toSet();
        final addedCount = newIds.difference(oldIds).length;
        final removedCount = oldIds.difference(newIds).length;

        if (addedCount > 0 || removedCount > 0) {
          setState(() {
            _pendingNewCount = addedCount;
            _pendingArticles = articles;
            _showNewBanner = true;
          });
          return; // Jangan update list dulu, tunggu user tap banner
        }
      }

      // Hanya update list jika ada perubahan nyata (hindari rebuild sia-sia)
      final oldIds = _articles.map((a) => a.id).toList();
      final newIds = articles.map((a) => a.id).toList();
      final listChanged = oldIds.length != newIds.length ||
          !oldIds.asMap().entries.every((e) => e.value == newIds[e.key]);

      setState(() {
        if (listChanged) _articles = articles;
        if (_username.isEmpty && username.isNotEmpty) _username = username;
        _loading = false;
        _showNewBanner = false;
      });
    } on DioException catch (e) {
      if (!mounted) return;
      if (e.response?.statusCode == 401) {
        await ApiClient.clearToken();
        context.go('/login');
        return;
      }
      if (!silent) {
        setState(() {
          _error = 'Gagal memuat artikel. Pastikan backend berjalan.';
          _loading = false;
        });
      }
    } catch (_) {
      if (!mounted) return;
      if (!silent) {
        setState(() {
          _error = 'Gagal memuat artikel. Pastikan backend berjalan.';
          _loading = false;
        });
      }
    }
  }

  void _applyPendingArticles() {
    setState(() {
      _articles = _pendingArticles;
      _pendingArticles = [];
      _pendingNewCount = 0;
      _showNewBanner = false;
    });
  }

  Future<void> _fetchSubscriptions() async {
    try {
      final tags = await MainService.fetchSubscriptions();
      if (!mounted) return;
      setState(() => _subscriptions = tags.toSet());
    } catch (_) {}
  }

  Future<void> _fetchNotifications() async {
    if (!mounted) return;
    setState(() => _notifLoading = true);
    try {
      final notifs = await MainService.fetchNotifications();
      if (!mounted) return;

      if (!_notifInitialized) {
        // Load pertama: simpan semua ID yang ada, jangan tampilkan notifikasi
        _knownNotifIds
          ..clear()
          ..addAll(notifs.map((n) => n.id));
        _notifInitialized = true;
      } else {
        // Load berikutnya: deteksi ID baru dan tampilkan di notification bar
        for (final notif in notifs) {
          if (!_knownNotifIds.contains(notif.id)) {
            _knownNotifIds.add(notif.id);
          }
        }
      }

      setState(() => _notifications = notifs);
    } catch (_) {
    } finally {
      if (mounted) setState(() => _notifLoading = false);
    }
  }

  Future<void> _fetchUserDetails() async {
    try {
      final data = await MainService.fetchUserDetails();
      final user = data['user'];
      if (user == null || !mounted) return;
      final name = user['username']?.toString() ?? '';
      if (name.isNotEmpty) setState(() => _username = name);
    } catch (_) {}
  }

  // ── User actions ──────────────────────────────────────────────────────────

  void _onSearchChanged(String value) {
    // Rebuild to show/hide the clear button immediately.
    setState(() {
      if (value.trim().isNotEmpty) _activeTag = '';
    });
    _debounce?.cancel();
    _debounce = Timer(
      const Duration(milliseconds: 400),
      () => _fetchArticles(clearFirst: true),
    );
  }

  void _setSort(String sort) {
    if (_sort == sort) return;
    _searchCtrl.clear();
    setState(() {
      _sort = sort;
      _activeTag = '';
    });
    _fetchArticles(clearFirst: true);
  }

  void _setTag(String tag) {
    if (_activeTag == tag) return;
    _searchCtrl.clear();
    setState(() => _activeTag = tag);
    _fetchArticles(clearFirst: true);
  }

  void _clearTag() {
    if (_activeTag.isEmpty && _searchCtrl.text.isEmpty) return;
    _searchCtrl.clear();
    setState(() => _activeTag = '');
    _fetchArticles(clearFirst: true);
  }

  Future<void> _toggleSubscription(String tag) async {
    final wasSubscribed = _subscriptions.contains(tag);

    // Optimistic update
    setState(() {
      final next = Set<String>.from(_subscriptions);
      wasSubscribed ? next.remove(tag) : next.add(tag);
      _subscriptions = next;
    });

    try {
      final confirmation = wasSubscribed
          ? await MainService.unsubscribeTag(tag)
          : await MainService.subscribeTag(tag);

      if (!mounted) return;

      if (confirmation == 'limit reached') {
        // Revert — subscription limit reached
        setState(() {
          final next = Set<String>.from(_subscriptions)..remove(tag);
          _subscriptions = next;
        });
        _showSnack('Batas subscribe 20 tag sudah tercapai.');
      }
    } catch (_) {
      // Revert on network error
      if (!mounted) return;
      setState(() {
        final next = Set<String>.from(_subscriptions);
        wasSubscribed ? next.add(tag) : next.remove(tag);
        _subscriptions = next;
      });
      _showSnack('Gagal memperbarui subscription.');
    }
  }

  Future<void> _openNotifications() async {
    if (!mounted) return;
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => MainNotificationSheet(
        notifications: _notifications,
        isLoading: false,
      ),
    );
    // Refresh setelah sheet ditutup supaya titik merah sinkron dengan is_read backend
    _fetchNotifications();
  }

  void _showSnack(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), behavior: SnackBarBehavior.floating),
    );
  }

  // ── Derived state ─────────────────────────────────────────────────────────

  /// Unique tags collected from the current article list, in insertion order.
  List<String> get _allTags {
    final seen = <String>{};
    final result = <String>[];
    for (final a in _articles) {
      for (final t in a.tags) {
        if (seen.add(t)) result.add(t);
      }
    }
    return result;
  }

  // ── Build ─────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GlassBackground(
        child: SafeArea(
          child: RefreshIndicator(
            color: AppTheme.primaryCyan,
            onRefresh: _fetchArticles,
            child: CustomScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              slivers: [
                SliverToBoxAdapter(child: _buildAppBar()),
                SliverToBoxAdapter(child: const SizedBox(height: 10)),
                SliverToBoxAdapter(child: _buildSearchBar()),
                SliverToBoxAdapter(child: const SizedBox(height: 10)),
                SliverToBoxAdapter(
                  child: MainSortBar(
                    activeSort: _sort,
                    onSortSelected: _setSort,
                  ),
                ),
                SliverToBoxAdapter(child: const SizedBox(height: 10)),
                SliverToBoxAdapter(
                  child: MainTagFilter(
                    tags: _allTags,
                    activeTag: _activeTag,
                    subscriptions: _subscriptions,
                    onTagSelected: _setTag,
                    onClearTag: _clearTag,
                    onToggleSubscription: _toggleSubscription,
                  ),
                ),
                SliverToBoxAdapter(child: const SizedBox(height: 14)),
                if (_showNewBanner) SliverToBoxAdapter(child: _buildNewBanner()),
                _buildArticleList(),
                const SliverToBoxAdapter(child: SizedBox(height: 32)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ── Sub-widgets ───────────────────────────────────────────────────────────

  Widget _buildAppBar() {
    final initial =
        _username.isEmpty ? null : _username[0].toUpperCase();

    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
      child: Row(
        children: [
          // Logo
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: Image.asset(
              'assets/logo.jpg',
              width: 36,
              height: 36,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(width: 10),
          const Text(
            'RETOGEN',
            style: TextStyle(
              color: AppTheme.textSecondary,
              fontSize: 13,
              fontWeight: FontWeight.w800,
              letterSpacing: 2,
            ),
          ),
          const Spacer(),

          // Notification bell
          _NavButton(
            tooltip: 'Notifikasi',
            onTap: _openNotifications,
            child: Stack(
              clipBehavior: Clip.none,
              children: [
                Icon(
                  _notifLoading
                      ? Icons.notifications_outlined
                      : Icons.notifications_outlined,
                  size: 20,
                  color: AppTheme.textSecondary,
                ),
                if (_notifications.any((n) => !n.isRead))
                  Positioned(
                    top: -3,
                    right: -3,
                    child: Container(
                      width: 8,
                      height: 8,
                      decoration: const BoxDecoration(
                        color: AppTheme.primaryRed,
                        shape: BoxShape.circle,
                      ),
                    ),
                  ),
              ],
            ),
          ),
          const SizedBox(width: 8),

          // Profile avatar
          GestureDetector(
            onTap: () => context.push('/profile'),
            child: Container(
              width: 36,
              height: 36,
              decoration: BoxDecoration(
                color: const Color(0x246AADA8),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.glassBorder),
              ),
              alignment: Alignment.center,
              child: initial != null
                  ? Text(
                      initial,
                      style: const TextStyle(
                        color: AppTheme.primaryCyan,
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                      ),
                    )
                  : const Icon(
                      Icons.person_rounded,
                      size: 18,
                      color: AppTheme.primaryCyan,
                    ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: TextField(
        controller: _searchCtrl,
        onChanged: _onSearchChanged,
        style: const TextStyle(color: AppTheme.textPrimary, fontSize: 14),
        decoration: InputDecoration(
          hintText: 'Cari artikel...',
          hintStyle: const TextStyle(color: AppTheme.textMuted),
          prefixIcon: const Icon(
            Icons.search_rounded,
            color: AppTheme.textMuted,
            size: 20,
          ),
          suffixIcon: _searchCtrl.text.isNotEmpty
              ? IconButton(
                  icon: const Icon(
                    Icons.clear_rounded,
                    size: 18,
                    color: AppTheme.textMuted,
                  ),
                  onPressed: () {
                    _searchCtrl.clear();
                    _fetchArticles();
                    setState(() {});
                  },
                )
              : null,
          filled: true,
          fillColor: AppTheme.inputBg,
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 11),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppTheme.glassBorder),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppTheme.glassBorder),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppTheme.primaryCyan),
          ),
        ),
      ),
    );
  }

  Widget _buildNewBanner() {
    final label = _pendingNewCount > 0
        ? '$_pendingNewCount Artikel Baru'
        : 'Ada Perubahan';
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 10),
      child: GestureDetector(
        onTap: _applyPendingArticles,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            color: AppTheme.primaryCyan,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: AppTheme.primaryCyan.withValues(alpha: 0.35),
                blurRadius: 10,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.arrow_upward_rounded,
                  size: 16, color: Colors.white),
              const SizedBox(width: 8),
              Text(
                label,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildArticleList() {
    // Loading skeleton
    if (_loading) {
      return SliverPadding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        sliver: SliverList(
          delegate: SliverChildBuilderDelegate(
            (_, __) => const Padding(
              padding: EdgeInsets.only(bottom: 12),
              child: MainArticleSkeleton(),
            ),
            childCount: 4,
          ),
        ),
      );
    }

    // Error banner
    if (_error != null) {
      return SliverToBoxAdapter(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: AppTheme.inputErrorBg,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: AppTheme.inputErrorBorder),
            ),
            child: Row(
              children: [
                const Icon(Icons.info_outline, color: AppTheme.primaryRed),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    _error!,
                    style: const TextStyle(
                      color: AppTheme.primaryRed,
                      fontSize: 13,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }

    // Empty state
    if (_articles.isEmpty) {
      return SliverToBoxAdapter(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 56),
            child: Column(
              children: [
                const Icon(
                  Icons.article_outlined,
                  size: 48,
                  color: AppTheme.textMuted,
                ),
                const SizedBox(height: 12),
                const Text(
                  'Tidak ada artikel ditemukan',
                  style:
                      TextStyle(color: AppTheme.textMuted, fontSize: 14),
                ),
              ],
            ),
          ),
        ),
      );
    }

    // Article cards
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: MainArticleCard(
              article: _articles[index],
              activeTag: _activeTag.isEmpty ? null : _activeTag,
              onTagTap: _setTag,
            ),
          ),
          childCount: _articles.length,
        ),
      ),
    );
  }
}

// ── Shared nav button widget ──────────────────────────────────────────────────

class _NavButton extends StatelessWidget {
  final Widget child;
  final VoidCallback onTap;
  final String tooltip;

  const _NavButton({
    required this.child,
    required this.onTap,
    required this.tooltip,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: AppTheme.glassBg,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: AppTheme.glassBorder),
          ),
          alignment: Alignment.center,
          child: child,
        ),
      ),
    );
  }
}
