import 'dart:ui';
import 'package:flutter/material.dart';
import '../theme.dart';

class GlassInput extends StatefulWidget {
  final String label;
  final String? placeholder;
  final String? error;
  final bool obscureText;
  final TextEditingController controller;
  final TextInputType keyboardType;

  const GlassInput({
    super.key,
    required this.label,
    required this.controller,
    this.placeholder,
    this.error,
    this.obscureText = false,
    this.keyboardType = TextInputType.text,
  });

  @override
  State<GlassInput> createState() => _GlassInputState();
}

class _GlassInputState extends State<GlassInput> {
  final FocusNode _focusNode = FocusNode();
  bool _isFocused = false;
  bool? _obscureTextOverride;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      setState(() {
        _isFocused = _focusNode.hasFocus;
      });
    });
  }

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bool hasError = widget.error != null && widget.error!.isNotEmpty;
    final bool currentObscureText = _obscureTextOverride ?? widget.obscureText;
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (widget.label.isNotEmpty) ...[
          Text(
            widget.label,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.5,
              color: AppTheme.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
        ],
        Container(
          decoration: BoxDecoration(
            color: AppTheme.inputBg,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: hasError 
                  ? AppTheme.inputErrorBorder 
                  : (_isFocused ? AppTheme.inputFocusBorder : AppTheme.glassBorder),
            ),
            boxShadow: _isFocused && !hasError
                ? [
                    const BoxShadow(
                      color: AppTheme.inputFocusShadow,
                      spreadRadius: 3,
                    )
                  ]
                : null,
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
              child: TextField(
                controller: widget.controller,
                focusNode: _focusNode,
                obscureText: currentObscureText,
                keyboardType: widget.keyboardType,
                style: const TextStyle(color: AppTheme.textPrimary),
                decoration: InputDecoration(
                  hintText: widget.placeholder,
                  hintStyle: const TextStyle(color: AppTheme.textMuted),
                  border: InputBorder.none,
                  contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                  suffixIcon: widget.obscureText
                      ? IconButton(
                          icon: Icon(
                            currentObscureText ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                            color: AppTheme.textMuted,
                            size: 20,
                          ),
                          onPressed: () {
                            setState(() {
                              _obscureTextOverride = !currentObscureText;
                            });
                          },
                        )
                      : null,
                ),
              ),
            ),
          ),
        ),
        if (hasError) ...[
          const SizedBox(height: 4),
          Text(
            widget.error!,
            style: const TextStyle(
              color: AppTheme.primaryRed,
              fontSize: 13,
            ),
          ),
        ],
      ],
    );
  }
}
