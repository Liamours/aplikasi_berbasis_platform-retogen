import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';

/// Horizontally scrollable tag filter row with a multi-select dropdown button.
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

  void _openTagSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => _TagSelectSheet(
        tags: tags,
        activeTag: activeTag,
        subscriptions: subscriptions,
        onTagSelected: (tag) {
          Navigator.of(context).pop();
          onTagSelected(tag);
        },
        onClearTag: () {
          Navigator.of(context).pop();
          onClearTag();
        },
        onToggleSubscription: onToggleSubscription,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 38,
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        children: [
          // "Semua" pill
          _SemualPill(isActive: activeTag.isEmpty, onTap: onClearTag),
          const SizedBox(width: 8),

          // Active tag pill (if any)
          if (activeTag.isNotEmpty) ...[
            _ActiveTagPill(tag: activeTag, onClear: onClearTag),
            const SizedBox(width: 8),
          ],

          // Filter button
          GestureDetector(
            onTap: () => _openTagSheet(context),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: activeTag.isNotEmpty
                    ? AppTheme.primaryCyan.withValues(alpha: 0.15)
                    : AppTheme.glassBg,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                  color: activeTag.isNotEmpty
                      ? AppTheme.primaryCyan
                      : AppTheme.glassBorder,
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.tune_rounded,
                    size: 14,
                    color: activeTag.isNotEmpty
                        ? AppTheme.primaryCyan
                        : AppTheme.textSecondary,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    'Filter Tag',
                    style: TextStyle(
                      color: activeTag.isNotEmpty
                          ? AppTheme.primaryCyan
                          : AppTheme.textSecondary,
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Active tag pill (shown in row when a tag is selected) ──────────────────────

class _ActiveTagPill extends StatelessWidget {
  final String tag;
  final VoidCallback onClear;

  const _ActiveTagPill({required this.tag, required this.onClear});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 180),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: AppTheme.primaryCyan,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppTheme.primaryCyan),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            tag,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 13,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(width: 6),
          GestureDetector(
            onTap: onClear,
            child: const Icon(Icons.close_rounded, size: 14, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

// ── "Semua" pill ───────────────────────────────────────────────────────────────

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

// ── Tag Select Bottom Sheet ────────────────────────────────────────────────────

class _TagSelectSheet extends StatelessWidget {
  final List<String> tags;
  final String activeTag;
  final Set<String> subscriptions;
  final void Function(String tag) onTagSelected;
  final VoidCallback onClearTag;
  final void Function(String tag) onToggleSubscription;

  const _TagSelectSheet({
    required this.tags,
    required this.activeTag,
    required this.subscriptions,
    required this.onTagSelected,
    required this.onClearTag,
    required this.onToggleSubscription,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppTheme.surface,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      padding: EdgeInsets.fromLTRB(
        20, 12, 20,
        MediaQuery.of(context).viewInsets.bottom + 24,
      ),
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
          const Text(
            'Pilih Tag',
            style: TextStyle(
              color: AppTheme.textPrimary,
              fontSize: 20,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Pilih tag untuk filter artikel',
            style: TextStyle(color: AppTheme.textMuted, fontSize: 13),
          ),
          const SizedBox(height: 20),

          // "Semua" option
          GestureDetector(
            onTap: onClearTag,
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: activeTag.isEmpty
                    ? AppTheme.primaryCyan.withValues(alpha: 0.15)
                    : AppTheme.glassBg,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: activeTag.isEmpty
                      ? AppTheme.primaryCyan
                      : AppTheme.glassBorder,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.apps_rounded,
                    size: 18,
                    color: activeTag.isEmpty
                        ? AppTheme.primaryCyan
                        : AppTheme.textMuted,
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Semua Artikel',
                    style: TextStyle(
                      color: activeTag.isEmpty
                          ? AppTheme.primaryCyan
                          : AppTheme.textPrimary,
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const Spacer(),
                  if (activeTag.isEmpty)
                    const Icon(
                      Icons.check_circle_rounded,
                      size: 18,
                      color: AppTheme.primaryCyan,
                    ),
                ],
              ),
            ),
          ),

          // Tag grid
          if (tags.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 20),
              child: Center(
                child: Text(
                  'Belum ada tag tersedia',
                  style: TextStyle(color: AppTheme.textMuted, fontSize: 14),
                ),
              ),
            )
          else
            ConstrainedBox(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.45,
              ),
              child: SingleChildScrollView(
                child: Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: tags.map((tag) {
                    final isActive = activeTag == tag;
                    final isSubscribed = subscriptions.contains(tag);
                    return _TagChip(
                      tag: tag,
                      isActive: isActive,
                      isSubscribed: isSubscribed,
                      onTap: () => onTagSelected(tag),
                      onToggleSub: () => onToggleSubscription(tag),
                    );
                  }).toList(),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

// ── Tag chip inside the sheet ─────────────────────────────────────────────────

class _TagChip extends StatelessWidget {
  final String tag;
  final bool isActive;
  final bool isSubscribed;
  final VoidCallback onTap;
  final VoidCallback onToggleSub;

  const _TagChip({
    required this.tag,
    required this.isActive,
    required this.isSubscribed,
    required this.onTap,
    required this.onToggleSub,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: isActive
              ? AppTheme.primaryCyan
              : AppTheme.glassBg,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isActive ? AppTheme.primaryCyan : AppTheme.glassBorder,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              tag,
              style: TextStyle(
                color: isActive ? Colors.white : AppTheme.textPrimary,
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(width: 8),
            GestureDetector(
              onTap: onToggleSub,
              child: Text(
                isSubscribed ? '★' : '☆',
                style: TextStyle(
                  fontSize: 14,
                  color: isSubscribed
                      ? AppTheme.primaryRed
                      : (isActive
                          ? Colors.white.withValues(alpha: 0.65)
                          : AppTheme.textMuted),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
