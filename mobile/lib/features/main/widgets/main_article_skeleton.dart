import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';

/// Animated placeholder shown while articles are loading.
class MainArticleSkeleton extends StatefulWidget {
  const MainArticleSkeleton({super.key});

  @override
  State<MainArticleSkeleton> createState() => _MainArticleSkeletonState();
}

class _MainArticleSkeletonState extends State<MainArticleSkeleton>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _anim;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1100),
    )..repeat(reverse: true);
    _anim = Tween<double>(begin: 0.35, end: 0.9).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  Widget _bone({required double height, double? width, double radius = 8}) {
    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        color: AppTheme.glassBorder,
        borderRadius: BorderRadius.circular(radius),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _anim,
      builder: (_, __) => Opacity(
        opacity: _anim.value,
        child: Container(
          decoration: BoxDecoration(
            color: AppTheme.glassBg,
            borderRadius: BorderRadius.circular(18),
            border: Border.all(color: AppTheme.glassBorder),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Image placeholder
              ClipRRect(
                borderRadius:
                    const BorderRadius.vertical(top: Radius.circular(17)),
                child: AspectRatio(
                  aspectRatio: 16 / 9,
                  child: Container(color: AppTheme.glassBorder),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(14, 12, 14, 14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _bone(height: 18, width: double.infinity),
                    const SizedBox(height: 6),
                    _bone(height: 14, width: 220),
                    const SizedBox(height: 10),
                    Row(children: [
                      _bone(height: 22, width: 64, radius: 6),
                      const SizedBox(width: 6),
                      _bone(height: 22, width: 80, radius: 6),
                    ]),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
