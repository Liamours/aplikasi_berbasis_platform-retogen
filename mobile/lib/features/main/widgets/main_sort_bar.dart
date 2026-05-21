import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';

const Map<String, String> kSortOptions = {
  'newest': 'Terbaru',
  'oldest': 'Terlama',
  'highest_rated': 'Nilai Tertinggi',
  'most_commented': 'Banyak Komentar',
};

class MainSortBar extends StatelessWidget {
  final String activeSort;
  final void Function(String sort) onSortSelected;

  const MainSortBar({
    super.key,
    required this.activeSort,
    required this.onSortSelected,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 36,
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        children: kSortOptions.entries.map((entry) {
          final isActive = activeSort == entry.key;
          return Padding(
            padding: const EdgeInsets.only(right: 8),
            child: GestureDetector(
              onTap: () => onSortSelected(entry.key),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 180),
                padding:
                    const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                decoration: BoxDecoration(
                  color: isActive
                      ? AppTheme.primaryRed.withValues(alpha: 0.12)
                      : AppTheme.glassBg,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(
                    color: isActive
                        ? AppTheme.primaryRed.withValues(alpha: 0.45)
                        : AppTheme.glassBorder,
                  ),
                ),
                child: Text(
                  entry.value,
                  style: TextStyle(
                    color:
                        isActive ? AppTheme.primaryRed : AppTheme.textSecondary,
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}
