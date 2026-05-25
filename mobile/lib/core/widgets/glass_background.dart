import 'dart:ui';
import 'package:flutter/material.dart';

class GridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0x12000000) 
      ..strokeWidth = 1;
    
    for (double i = 0; i <= size.width; i += 32) {
      canvas.drawLine(Offset(i, 0), Offset(i, size.height), paint);
    }
    for (double i = 0; i <= size.height; i += 32) {
      canvas.drawLine(Offset(0, i), Offset(size.width, i), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class GlassBackground extends StatelessWidget {
  final Widget child;

  const GlassBackground({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Grid
        Positioned.fill(
          child: CustomPaint(painter: GridPainter()),
        ),
        
        // Blobs with ImageFiltered blur
        Positioned(
          top: -80,
          left: -100,
          child: ImageFiltered(
            imageFilter: ImageFilter.blur(sigmaX: 110, sigmaY: 110),
            child: Container(
              width: 480,
              height: 300,
              decoration: BoxDecoration(
                color: const Color(0x29B22222),
                borderRadius: BorderRadius.circular(999),
              ),
            ),
          ),
        ),
        
        Positioned(
          bottom: 40,
          right: -120,
          child: ImageFiltered(
            imageFilter: ImageFilter.blur(sigmaX: 110, sigmaY: 110),
            child: Container(
              width: 420,
              height: 420,
              decoration: BoxDecoration(
                color: const Color(0x2120B2AA),
                borderRadius: BorderRadius.circular(999),
              ),
            ),
          ),
        ),
        
        Positioned(
          top: MediaQuery.of(context).size.height * 0.45,
          left: MediaQuery.of(context).size.width * 0.35,
          child: ImageFiltered(
            imageFilter: ImageFilter.blur(sigmaX: 110, sigmaY: 110),
            child: Container(
              width: 180,
              height: 180,
              decoration: BoxDecoration(
                color: const Color(0x1420B2AA),
                borderRadius: BorderRadius.circular(999),
              ),
            ),
          ),
        ),
        
        // Content
        Positioned.fill(child: child),
      ],
    );
  }
}
