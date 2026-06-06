import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleDetailSkeleton extends StatefulWidget {
  final VoidCallback onBack;

  const ArticleDetailSkeleton({super.key, required this.onBack});

  @override
  State<ArticleDetailSkeleton> createState() => _ArticleDetailSkeletonState();
}

class _ArticleDetailSkeletonState extends State<ArticleDetailSkeleton>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1100),
    )..repeat(reverse: true);
    _opacity = Tween<double>(
      begin: 0.36,
      end: 0.88,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Widget _bone({required double height, double? width, double radius = 8}) {
    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        color: AppTheme.textMuted.withValues(alpha: 0.18),
        borderRadius: BorderRadius.circular(radius),
      ),
    );
  }

  Widget _pillBone({required double width}) {
    return Container(
      width: width,
      height: 34,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.16),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      alignment: Alignment.centerLeft,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: _bone(height: 12, width: width * 0.55, radius: 5),
    );
  }

  Widget _heroSkeleton() {
    return ArticleSurfaceCard(
      padding: 18,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              IconButton(
                onPressed: widget.onBack,
                icon: const Icon(Icons.arrow_back),
                tooltip: 'Kembali',
              ),
              Expanded(child: _bone(height: 14, width: 120)),
              _bone(height: 40, width: 40, radius: 20),
            ],
          ),
          const SizedBox(height: 14),
          ClipRRect(
            borderRadius: BorderRadius.circular(18),
            child: AspectRatio(
              aspectRatio: 4 / 3,
              child: Container(
                decoration: BoxDecoration(
                  color: AppTheme.textMuted.withValues(alpha: 0.14),
                  border: Border.all(color: AppTheme.glassBorder),
                ),
              ),
            ),
          ),
          const SizedBox(height: 18),
          _bone(height: 12, width: 112, radius: 5),
          const SizedBox(height: 10),
          _bone(height: 30, width: double.infinity),
          const SizedBox(height: 8),
          _bone(height: 30, width: 230),
          const SizedBox(height: 14),
          _bone(height: 14, width: double.infinity),
          const SizedBox(height: 7),
          _bone(height: 14, width: double.infinity),
          const SizedBox(height: 7),
          _bone(height: 14, width: 190),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _bone(height: 26, width: 74, radius: 8),
              _bone(height: 26, width: 88, radius: 8),
              _bone(height: 26, width: 62, radius: 8),
            ],
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _pillBone(width: 104),
              _pillBone(width: 118),
              _pillBone(width: 136),
            ],
          ),
        ],
      ),
    );
  }

  Widget _reviewSkeleton() {
    return _sectionSkeleton(
      titleWidth: 86,
      children: [
        _bone(height: 14, width: double.infinity),
        const SizedBox(height: 9),
        _bone(height: 14, width: double.infinity),
        const SizedBox(height: 9),
        _bone(height: 14, width: 260),
        const SizedBox(height: 16),
        _bone(height: 14, width: double.infinity),
        const SizedBox(height: 9),
        _bone(height: 14, width: 220),
      ],
    );
  }

  Widget _ratingSkeleton() {
    return _sectionSkeleton(
      titleWidth: 154,
      trailing: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          _bone(height: 25, width: 42),
          const SizedBox(height: 6),
          _bone(height: 11, width: 76, radius: 5),
        ],
      ),
      children: [
        _bone(height: 13, width: 190),
        const SizedBox(height: 14),
        Row(
          children: List.generate(
            5,
            (index) => Padding(
              padding: EdgeInsets.only(right: index == 4 ? 0 : 8),
              child: Icon(
                Icons.star_rounded,
                size: 31,
                color: AppTheme.primaryRed.withValues(alpha: 0.20),
              ),
            ),
          ),
        ),
        const SizedBox(height: 12),
        _bone(height: 32, width: 118, radius: 10),
      ],
    );
  }

  Widget _priceSkeleton() {
    return _sectionSkeleton(
      eyebrowWidth: 98,
      titleWidth: 128,
      subtitleWidth: 188,
      children: List.generate(
        3,
        (index) => Padding(
          padding: EdgeInsets.only(top: index == 0 ? 0 : 16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _bone(height: 40, width: 40, radius: 12),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(child: _bone(height: 14, width: 140)),
                        _bone(height: 12, width: 34, radius: 5),
                      ],
                    ),
                    const SizedBox(height: 7),
                    _bone(height: 12, width: double.infinity),
                    const SizedBox(height: 8),
                    _bone(height: 18, width: 108),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _discussionSkeleton() {
    return _sectionSkeleton(
      titleWidth: 160,
      subtitleWidth: 82,
      children: [
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.12),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppTheme.glassBorder),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _bone(height: 17, width: 118),
              const SizedBox(height: 12),
              _bone(height: 86, width: double.infinity, radius: 12),
              const SizedBox(height: 12),
              _bone(height: 40, width: double.infinity, radius: 10),
            ],
          ),
        ),
        const SizedBox(height: 14),
        _commentSkeleton(),
        const SizedBox(height: 12),
        _commentSkeleton(isReply: true),
      ],
    );
  }

  Widget _commentSkeleton({bool isReply = false}) {
    return Container(
      padding: EdgeInsets.all(isReply ? 12 : 14),
      decoration: BoxDecoration(
        color: isReply
            ? AppTheme.primaryCyan.withValues(alpha: 0.04)
            : AppTheme.bgSurface.withValues(alpha: 0.76),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              _bone(height: 38, width: 38, radius: 10),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _bone(height: 14, width: 126),
                    const SizedBox(height: 6),
                    _bone(height: 12, width: 34, radius: 5),
                  ],
                ),
              ),
              _bone(height: 26, width: 26, radius: 13),
            ],
          ),
          const SizedBox(height: 12),
          _bone(height: 13, width: double.infinity),
          const SizedBox(height: 8),
          _bone(height: 13, width: isReply ? 152 : 210),
          const SizedBox(height: 12),
          Align(
            alignment: Alignment.centerRight,
            child: _bone(height: 28, width: 76, radius: 14),
          ),
        ],
      ),
    );
  }

  Widget _sectionSkeleton({
    required double titleWidth,
    double? eyebrowWidth,
    double? subtitleWidth,
    Widget? trailing,
    required List<Widget> children,
  }) {
    return ArticleSurfaceCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (eyebrowWidth != null) ...[
            _bone(height: 12, width: eyebrowWidth, radius: 5),
            const SizedBox(height: 7),
          ],
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _bone(height: 22, width: titleWidth),
                    if (subtitleWidth != null) ...[
                      const SizedBox(height: 8),
                      _bone(height: 13, width: subtitleWidth, radius: 5),
                    ],
                  ],
                ),
              ),
              ?trailing,
            ],
          ),
          const SizedBox(height: 16),
          ...children,
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _opacity,
      builder: (context, child) {
        return Opacity(opacity: _opacity.value, child: child);
      },
      child: CustomScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 28),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                _heroSkeleton(),
                const SizedBox(height: 16),
                _reviewSkeleton(),
                const SizedBox(height: 16),
                _ratingSkeleton(),
                const SizedBox(height: 16),
                _priceSkeleton(),
                const SizedBox(height: 18),
                _discussionSkeleton(),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}
