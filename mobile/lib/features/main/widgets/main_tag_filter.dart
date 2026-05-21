import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';

/// Horizontally scrollable tag filter row.
/// Each tag pill has a subscribe ☆/★ toggle attached to the right.
class MainTagFilter extends StatelessWidget {
  final List<String> tags;
  final String activeTag;
  final Set<String> subscriptions;
  final void Function(String tag) onTagSelected;
  final VoidCallback onClearTag;
  final void Function(String tag) onToggleSubscription;

  const MainTagFilter({
    super.key,
    required this.tags,
    required this.activeTag,
    required this.subscriptions,
    required this.onTagSelected,
    required this.onClearTag,
    required this.onToggleSubscription,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 38,
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        children: [
          // "Semua" pill — no subscribe toggle
          _SemualPill(isActive: activeTag.isEmpty, onTap: onClearTag),
          if (tags.isNotEmpty) const SizedBox(width: 8),
          ...tags.asMap().entries.map((entry) {
            final tag = entry.value;
            return Padding(
              padding: const EdgeInsets.only(right: 8),
              child: _TagPill(
                tag: tag,
                isActive: activeTag == tag,
                isSubscribed: subscriptions.contains(tag),
                onTap: () => onTagSelected(tag),
                onToggleSub: () => onToggleSubscription(tag),
              ),
            );
          }),
        ],
      ),
    );
  }
}

class _SemualPill extends StatelessWidget {
  final bool isActive;
  final VoidCallback onTap;

  const _SemualPill({required this.isActive, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: isActive ? AppTheme.primaryCyan : AppTheme.glassBg,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: isActive ? AppTheme.primaryCyan : AppTheme.glassBorder,
          ),
        ),
        child: Text(
          'Semua',
          style: TextStyle(
            color: isActive ? Colors.white : AppTheme.textSecondary,
            fontSize: 13,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }
}

class _TagPill extends StatelessWidget {
  final String tag;
  final bool isActive;
  final bool isSubscribed;
  final VoidCallback onTap;
  final VoidCallback onToggleSub;

  const _TagPill({
    required this.tag,
    required this.isActive,
    required this.isSubscribed,
    required this.onTap,
    required this.onToggleSub,
  });

  @override
  Widget build(BuildContext context) {
    final dividerColor = isActive
        ? Colors.white.withValues(alpha: 0.30)
        : AppTheme.glassBorder;

    return AnimatedContainer(
      duration: const Duration(milliseconds: 180),
      decoration: BoxDecoration(
        color: isActive ? AppTheme.primaryCyan : AppTheme.glassBg,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: isActive ? AppTheme.primaryCyan : AppTheme.glassBorder,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Tag label
          GestureDetector(
            onTap: onTap,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 8, 8, 8),
              child: Text(
                tag,
                style: TextStyle(
                  color: isActive ? Colors.white : AppTheme.textSecondary,
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ),
          // Divider
          Container(width: 1, height: 20, color: dividerColor),
          // Subscribe toggle
          GestureDetector(
            onTap: onToggleSub,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
              child: Text(
                isSubscribed ? '★' : '☆',
                style: TextStyle(
                  fontSize: 13,
                  color: isSubscribed
                      ? AppTheme.primaryRed
                      : (isActive
                          ? Colors.white.withValues(alpha: 0.65)
                          : AppTheme.textMuted),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
