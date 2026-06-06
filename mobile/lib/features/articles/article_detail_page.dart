import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:retogen/core/api_client.dart';
import 'package:retogen/core/location_service.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/core/widgets/glass_background.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/utils/article_data_utils.dart';
import 'package:retogen/features/articles/widgets/article_confirm_delete_sheet.dart';
import 'package:retogen/features/articles/widgets/article_detail_hero.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';
import 'package:retogen/features/articles/widgets/article_detail_skeleton.dart';
import 'package:retogen/features/articles/widgets/article_discussion_section.dart';
import 'package:retogen/features/articles/widgets/article_price_tracker.dart';
import 'package:retogen/features/articles/widgets/article_rating_section.dart';
import 'package:retogen/features/articles/widgets/article_report_sheet.dart';
import 'package:retogen/features/articles/widgets/article_review_section.dart';
import 'package:retogen/features/articles/widgets/other_user_profile_sheet.dart';

class ArticleDetailPage extends StatefulWidget {
  final String articleId;

  const ArticleDetailPage({super.key, required this.articleId});

  @override
  State<ArticleDetailPage> createState() => _ArticleDetailPageState();
}

class _ArticleDetailPageState extends State<ArticleDetailPage> {
  final _commentController = TextEditingController();
  final _editController = TextEditingController();
  final Map<String, TextEditingController> _replyControllers = {};

  ArticleDetail? _article;
  bool _loading = true;
  bool _pricesLoading = false;
  bool _ratingSaving = false;
  bool _commentSaving = false;
  String? _error;
  String? _feedback;
  int _ratingDraft = 0;
  String? _activeReplyId;
  String? _activeEditId;

  @override
  void initState() {
    super.initState();
    _fetchArticle();
  }

  @override
  void dispose() {
    _commentController.dispose();
    _editController.dispose();
    for (final controller in _replyControllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  bool get _hasValidArticleId {
    return RegExp(r'^[a-fA-F0-9]{24}$').hasMatch(widget.articleId);
  }

  Future<void> _fetchArticle() async {
    if (!_hasValidArticleId) {
      setState(() {
        _loading = false;
        _error = 'Artikel tidak valid.';
      });
      return;
    }

    setState(() {
      _loading = _article == null;
      _error = null;
      _feedback = null;
    });

    try {
      final response = await ApiClient.instance.post(
        '/article/view',
        data: {'article_id': widget.articleId},
      );
      final data = asMap(response.data);
      if (data['confirmation'] != 'successful') {
        setState(() {
          _loading = false;
          _error = 'Artikel tidak ditemukan.';
        });
        return;
      }

      final detail = ArticleDetail.fromJson(
        widget.articleId,
        data,
        prices: _article?.prices ?? const [],
      );

      setState(() {
        _article = detail;
        _ratingDraft = detail.currentUserRating;
        _loading = false;
      });

      await _fetchPrices(detail.productName ?? detail.title);
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        await ApiClient.clearToken();
        if (!mounted) return;
        context.go('/login');
        return;
      }

      setState(() {
        _error = 'Gagal memuat artikel. Pastikan backend berjalan.';
        _loading = false;
      });
    } catch (_) {
      setState(() {
        _error = 'Gagal memuat artikel. Pastikan backend berjalan.';
        _loading = false;
      });
    }
  }

  Future<void> _fetchPrices(String title) async {
    if (title.trim().isEmpty) return;

    setState(() => _pricesLoading = true);

    try {
      final location = await LocationService.getCurrentLocation();
      final payload = <String, dynamic>{'product_name': title, 'limit': 10};

      if (location != null) {
        payload.addAll(location.toJson());
      }

      final response = await ApiClient.instance.post(
        '/monitor/search',
        data: payload,
      );
      final data = asMap(response.data);
      final prices = asMapList(data['results'])
          .asMap()
          .entries
          .map((entry) => PriceEntry.fromJson(entry.value, entry.key))
          .toList();

      if (!mounted) return;
      setState(() {
        _article = _article?.copyWith(prices: prices);
      });
    } catch (_) {
      // Price monitoring is optional, so the article remains usable.
    } finally {
      if (mounted) {
        setState(() => _pricesLoading = false);
      }
    }
  }

  Future<void> _setRating(int value) async {
    final article = _article;
    if (article == null || _ratingSaving) return;

    final normalized = value.clamp(1, 5).toInt();
    final existingRating = article.ratingByCurrentUser;

    setState(() {
      _ratingSaving = true;
      _feedback = null;
    });

    try {
      final endpoint = existingRating == null
          ? '/rating/add'
          : '/rating/edit/update';
      final payload = existingRating == null
          ? {'article_id': article.id, 'rating_value': normalized}
          : {
              'rating_id': existingRating.ratingId,
              'article_id': article.id,
              'rating_value': normalized,
            };

      final response = await ApiClient.instance.post(endpoint, data: payload);
      final data = asMap(response.data);
      final confirmation = data['confirmation']?.toString() ?? '';

      if (confirmation == 'successful') {
        final updated = ArticleDetail.fromJson(
          article.id,
          data,
          prices: article.prices,
        );
        setState(() {
          _article = updated;
          _ratingDraft = normalized;
          _feedback = existingRating == null
              ? 'Rating disimpan'
              : 'Rating diperbarui';
        });
        return;
      }

      if (confirmation == 'already rated') {
        await _fetchArticle();
        setState(() {
          _feedback = 'Data rating disinkronkan kembali. Silakan coba lagi.';
        });
        return;
      }

      setState(() {
        _feedback = confirmation.isEmpty
            ? 'Gagal menyimpan rating'
            : confirmation;
      });
    } catch (_) {
      setState(() {
        _feedback = 'Gagal menyimpan rating';
      });
    } finally {
      if (mounted) {
        setState(() => _ratingSaving = false);
      }
    }
  }

  Future<void> _submitComment({String? parentId}) async {
    final article = _article;
    if (article == null || _commentSaving) return;

    final controller = parentId == null
        ? _commentController
        : _replyControllerFor(parentId);
    final text = controller.text.trim();
    if (text.isEmpty) return;

    setState(() => _commentSaving = true);

    try {
      final response = await ApiClient.instance.post(
        '/comment/add',
        data: {
          'article_id': article.id,
          'parent_comment_id': parentId,
          'comment_content': text,
        },
      );
      final data = asMap(response.data);
      if (data['confirmation'] == 'successful') {
        final updated = ArticleDetail.fromJson(
          article.id,
          data,
          prices: article.prices,
        );
        setState(() {
          _article = updated;
          controller.clear();
          _activeReplyId = null;
        });
      }
    } finally {
      if (mounted) {
        setState(() => _commentSaving = false);
      }
    }
  }

  void _toggleReply(String commentId) {
    setState(() {
      _activeEditId = null;
      _activeReplyId = _activeReplyId == commentId ? null : commentId;
    });
  }

  void _startEdit(ArticleComment comment) {
    if (!_isOwnComment(comment)) return;

    setState(() {
      _activeReplyId = null;
      _activeEditId = comment.commentId;
      _editController.text = comment.content;
    });
  }

  void _cancelEdit() {
    setState(() {
      _activeEditId = null;
      _editController.clear();
    });
  }

  Future<void> _saveEdit(ArticleComment comment) async {
    final article = _article;
    if (article == null || !_isOwnComment(comment)) return;

    final text = _editController.text.trim();
    if (text.isEmpty) return;

    setState(() => _commentSaving = true);

    try {
      final response = await ApiClient.instance.post(
        '/comment/edit/update',
        data: {
          'article_id': article.id,
          'comment_id': comment.commentId,
          'parent_comment_id': comment.parentCommentId,
          'comment_content': text,
        },
      );
      final data = asMap(response.data);
      if (data['confirmation'] == 'successful') {
        final updated = ArticleDetail.fromJson(
          article.id,
          data,
          prices: article.prices,
        );
        setState(() {
          _article = updated;
          _activeEditId = null;
          _editController.clear();
        });
      }
    } finally {
      if (mounted) {
        setState(() => _commentSaving = false);
      }
    }
  }

  Future<void> _confirmDeleteComment(ArticleComment comment) async {
    final confirmed = await showModalBottomSheet<bool>(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => ArticleConfirmDeleteSheet(owner: comment.owner),
    );

    if (confirmed != true) return;
    await _deleteComment(comment);
  }

  Future<void> _deleteComment(ArticleComment comment) async {
    final article = _article;
    if (article == null || !_isOwnComment(comment)) return;

    setState(() => _commentSaving = true);

    try {
      final response = await ApiClient.instance.post(
        '/comment/delete',
        data: {'comment_id': comment.commentId},
      );
      final data = asMap(response.data);
      if (data['confirmation'] == 'successful') {
        final updated = ArticleDetail.fromJson(
          article.id,
          data,
          prices: article.prices,
        );
        setState(() => _article = updated);
      }
    } finally {
      if (mounted) {
        setState(() => _commentSaving = false);
      }
    }
  }

  Future<void> _openReportArticle() async {
    final article = _article;
    if (article == null) return;

    final description = await showModalBottomSheet<String>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => ArticleReportSheet(
        title: 'Laporkan artikel',
        targetLabel: 'Artikel',
        targetText: article.title,
      ),
    );

    if (description == null || description.trim().isEmpty) return;

    try {
      final response = await ApiClient.instance.post(
        '/report_article/add',
        data: {'article_id': article.id, 'description': description.trim()},
      );
      final data = asMap(response.data);
      final confirmation = data['confirmation']?.toString() ?? '';
      _showSnack(
        confirmation.contains('successful')
            ? 'Report artikel terkirim.'
            : 'Report belum berhasil dikirim.',
      );
    } catch (_) {
      _showSnack('Report belum berhasil dikirim.');
    }
  }

  Future<void> _openReportComment(ArticleComment comment) async {
    if (comment.userEmail == null || _isOwnComment(comment)) return;

    final description = await showModalBottomSheet<String>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => ArticleReportSheet(
        title: 'Laporkan komentar',
        targetLabel: comment.owner,
        targetText: comment.content,
      ),
    );

    if (description == null || description.trim().isEmpty) return;

    try {
      final response = await ApiClient.instance.post(
        '/report_user/report_user',
        data: {
          'reported_user_email': comment.userEmail,
          'description': description.trim(),
        },
      );
      final data = asMap(response.data);
      final confirmation = data['confirmation']?.toString() ?? '';
      _showSnack(
        confirmation.contains('successful')
            ? 'Report komentar terkirim.'
            : 'Report belum berhasil dikirim.',
      );
    } catch (_) {
      _showSnack('Report belum berhasil dikirim.');
    }
  }

  Future<void> _openUserProfile(String email) async {
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => OtherUserProfileSheet(userEmail: email),
    );
  }

  TextEditingController _replyControllerFor(String commentId) {
    return _replyControllers.putIfAbsent(commentId, TextEditingController.new);
  }

  bool _isOwnComment(ArticleComment comment) {
    final article = _article;
    if (article == null || comment.userEmail == null) return false;
    return comment.userEmail!.toLowerCase() ==
        article.currentUserEmail.toLowerCase();
  }

  void _showSnack(String message) {
    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), behavior: SnackBarBehavior.floating),
    );
  }

  void _goBack() {
    if (context.canPop()) {
      context.pop();
    } else {
      context.go('/articles');
    }
  }

  String get _ratingLabel {
    if (_feedback != null && _feedback!.isNotEmpty) return _feedback!;
    if (_ratingDraft == 0) return 'Pilih rating untuk artikel ini';

    const labels = {
      1: 'Kurang memuaskan',
      2: 'Masih di bawah ekspektasi',
      3: 'Cukup baik',
      4: 'Solid dan layak',
      5: 'Sangat direkomendasikan',
    };

    return labels[_ratingDraft] ?? 'Pilih rating';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GlassBackground(
        child: SafeArea(
          child: AnimatedSwitcher(
            duration: const Duration(milliseconds: 200),
            child: _buildBody(),
          ),
        ),
      ),
    );
  }

  Widget _buildBody() {
    if (_loading) {
      return ArticleDetailSkeleton(onBack: _goBack);
    }

    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: ArticleSurfaceCard(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.info_outline,
                  color: AppTheme.primaryRed,
                  size: 32,
                ),
                const SizedBox(height: 12),
                Text(
                  _error!,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: AppTheme.textSecondary,
                    fontSize: 14,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 16),
                OutlinedButton.icon(
                  onPressed: _goBack,
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Kembali'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    final article = _article;
    if (article == null) {
      return const SizedBox.shrink();
    }

    return RefreshIndicator(
      color: AppTheme.primaryCyan,
      onRefresh: _fetchArticle,
      child: CustomScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 28),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                ArticleDetailHero(
                  article: article,
                  onBack: _goBack,
                  onReportArticle: _openReportArticle,
                ),
                const SizedBox(height: 16),
                ArticleReviewSection(article: article),
                const SizedBox(height: 16),
                ArticleRatingSection(
                  article: article,
                  ratingDraft: _ratingDraft,
                  isSaving: _ratingSaving,
                  helperLabel: _ratingLabel,
                  onRatingSelected: _setRating,
                ),
                const SizedBox(height: 16),
                ArticlePriceTracker(
                  article: article,
                  isLoading: _pricesLoading,
                ),
                const SizedBox(height: 18),
                ArticleDiscussionSection(
                  article: article,
                  commentController: _commentController,
                  editController: _editController,
                  activeReplyId: _activeReplyId,
                  activeEditId: _activeEditId,
                  isSaving: _commentSaving,
                  onSubmitComment: _submitComment,
                  onToggleReply: _toggleReply,
                  onStartEdit: _startEdit,
                  onCancelEdit: _cancelEdit,
                  onSaveEdit: _saveEdit,
                  onDelete: _confirmDeleteComment,
                  onReport: _openReportComment,
                  resolveReplyController: _replyControllerFor,
                  isOwnComment: _isOwnComment,
                  onOpenUserProfile: _openUserProfile,
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}
