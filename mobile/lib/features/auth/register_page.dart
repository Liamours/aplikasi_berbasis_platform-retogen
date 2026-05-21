import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/api_client.dart';
import '../../core/theme.dart';
import '../../core/widgets/glass_background.dart';
import '../../core/widgets/glass_card.dart';
import '../../core/widgets/glass_input.dart';
import '../../core/widgets/success_popup.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _usernameCtrl = TextEditingController();
  final _fullnameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  
  bool _loading = false;
  String? _usernameError;
  String? _fullnameError;
  String? _emailError;
  String? _passwordError;
  String? _generalError;

  bool validateForm() {
    setState(() {
      _usernameError = null;
      _fullnameError = null;
      _emailError = null;
      _passwordError = null;
      _generalError = null;
    });
    
    bool isValid = true;
    final username = _usernameCtrl.text.trim();
    final fullname = _fullnameCtrl.text.trim();
    final email = _emailCtrl.text.trim();
    final password = _passCtrl.text;
    
    if (username.isEmpty) {
      _usernameError = 'Username wajib diisi.';
      isValid = false;
    } else if (!RegExp(r'^[a-zA-Z0-9]+$').hasMatch(username)) {
      _usernameError = 'Username hanya boleh huruf dan angka.';
      isValid = false;
    } else if (username.length < 8 || username.length > 16) {
      _usernameError = 'Username harus 8-16 karakter.';
      isValid = false;
    }
    
    if (fullname.isEmpty) {
      _fullnameError = 'Nama lengkap wajib diisi.';
      isValid = false;
    } else if (!RegExp(r'^[A-Za-z\s]+$').hasMatch(fullname)) {
      _fullnameError = 'Nama lengkap hanya boleh huruf dan spasi.';
      isValid = false;
    } else if (fullname.length < 4 || fullname.length > 32) {
      _fullnameError = 'Nama lengkap harus 4-32 karakter.';
      isValid = false;
    }
    
    if (email.isEmpty) {
      _emailError = 'Email wajib diisi.';
      isValid = false;
    } else if (!RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(email)) {
      _emailError = 'Format email tidak valid.';
      isValid = false;
    }
    
    if (password.isEmpty) {
      _passwordError = 'Password wajib diisi.';
      isValid = false;
    } else if (password.length < 8 || password.length > 16) {
      _passwordError = 'Password harus 8-16 karakter.';
      isValid = false;
    } else if (!RegExp(r'[A-Z]').hasMatch(password) || 
               !RegExp(r'[a-z]').hasMatch(password) || 
               !RegExp(r'[0-9]').hasMatch(password)) {
      _passwordError = 'Password harus mengandung huruf besar, huruf kecil, dan angka.';
      isValid = false;
    }
    
    return isValid;
  }

  void _applyServerError(String message) {
    final normalized = message.toLowerCase();
    setState(() {
      if (normalized.contains('email')) {
        _emailError = message;
      } else if (normalized.contains('username')) {
        _usernameError = message;
      } else if (normalized.contains('fullname') || normalized.contains('full name') || normalized.contains('name')) {
        _fullnameError = message;
      } else if (normalized.contains('password')) {
        _passwordError = message;
      } else {
        _generalError = message;
      }
    });
  }

  Future<void> _register() async {
    if (_loading || !validateForm()) return;
    
    setState(() => _loading = true);
    
    try {
      final res = await ApiClient.instance.post('/auth/registration', data: {
        'username': _usernameCtrl.text.trim(),
        'fullname': _fullnameCtrl.text.trim().replaceAll(RegExp(r'\s+'), ' '),
        'email': _emailCtrl.text.trim(),
        'password': _passCtrl.text,
      });
      
      final confirmation = res.data['confirmation']?.toString() ?? '';
      
      if (confirmation == 'register successful') {
        if (!mounted) return;
        final email = _emailCtrl.text.trim();
        final password = _passCtrl.text;
        SuccessPopup.show(context, 'Registrasi berhasil. Silakan masuk.', () {
          context.go('/login', extra: {'email': email, 'password': password});
        });
        return;
      }
      
      if (confirmation == 'email already registered') {
        setState(() => _emailError = 'Email sudah terdaftar.');
        return;
      }
      
      _applyServerError(confirmation.isEmpty ? 'Registrasi belum berhasil.' : confirmation);
      
    } catch (e) {
      setState(() => _generalError = 'Terjadi kendala saat menghubungkan ke server.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _usernameCtrl.dispose();
    _fullnameCtrl.dispose();
    _emailCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GlassBackground(
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 440),
                child: GlassCard(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Header
                      Row(
                        children: [
                          Container(
                            width: 44,
                            height: 44,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(14),
                              border: Border.all(color: AppTheme.glassBorder),
                              boxShadow: const [
                                BoxShadow(color: AppTheme.glassShadow, blurRadius: 16)
                              ]
                            ),
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(14),
                              child: Image.asset('assets/logo.jpg', fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) => const Icon(Icons.broken_image),
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          const Text(
                            'RETOGEN',
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 2,
                              color: AppTheme.textSecondary,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      const Text(
                        'Buat akun baru',
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 28),
                      
                      // General Error
                      if (_generalError != null) ...[
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: AppTheme.inputErrorBg,
                            border: Border.all(color: AppTheme.inputErrorBorder),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            _generalError!,
                            style: const TextStyle(color: AppTheme.primaryRed),
                          ),
                        ),
                        const SizedBox(height: 18),
                      ],
                      
                      // Form
                      GlassInput(
                        label: 'Username',
                        placeholder: '8-16 karakter, huruf dan angka',
                        controller: _usernameCtrl,
                        error: _usernameError,
                      ),
                      const SizedBox(height: 18),
                      GlassInput(
                        label: 'Full name',
                        placeholder: 'Nama lengkap',
                        controller: _fullnameCtrl,
                        error: _fullnameError,
                      ),
                      const SizedBox(height: 18),
                      GlassInput(
                        label: 'Email',
                        placeholder: 'nama@email.com',
                        controller: _emailCtrl,
                        keyboardType: TextInputType.emailAddress,
                        error: _emailError,
                      ),
                      const SizedBox(height: 18),
                      GlassInput(
                        label: 'Password',
                        placeholder: '8-16 karakter, kombinasi huruf besar, kecil, dan angka',
                        controller: _passCtrl,
                        obscureText: true,
                        error: _passwordError,
                      ),
                      const SizedBox(height: 24),
                      
                      // Submit Button
                      SizedBox(
                        width: double.infinity,
                        height: 48,
                        child: ElevatedButton(
                          onPressed: _loading ? null : _register,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.primaryCyan,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                            elevation: 0,
                          ),
                          child: _loading 
                            ? const SizedBox(
                                width: 24, height: 24, 
                                child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)
                              )
                            : const Text('Daftar', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                        ),
                      ),
                      
                      const SizedBox(height: 24),
                      const Divider(color: AppTheme.glassBorder),
                      const SizedBox(height: 16),
                      
                      // Footer
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text(
                            'Sudah punya akun? ',
                            style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
                          ),
                          GestureDetector(
                            onTap: () {
                              if (context.canPop()) {
                                context.pop();
                              } else {
                                context.go('/login');
                              }
                            },
                            child: const Text(
                              'Masuk',
                              style: TextStyle(
                                color: AppTheme.primaryCyan,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
