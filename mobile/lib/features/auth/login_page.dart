import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/api_client.dart';
import '../../core/theme.dart';
import '../../core/widgets/glass_background.dart';
import '../../core/widgets/glass_card.dart';
import '../../core/widgets/glass_input.dart';
import '../../core/widgets/success_popup.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  
  bool _loading = false;
  String? _emailError;
  String? _passwordError;
  String? _generalError;

  bool validateForm() {
    setState(() {
      _emailError = null;
      _passwordError = null;
      _generalError = null;
    });
    
    bool isValid = true;
    final email = _emailCtrl.text.trim();
    final password = _passCtrl.text;
    
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
    }
    
    return isValid;
  }

  Future<void> _login() async {
    if (_loading || !validateForm()) return;
    
    setState(() => _loading = true);
    
    try {
      final res = await ApiClient.instance.post('/auth/login', data: {
        'email': _emailCtrl.text.trim(),
        'password': _passCtrl.text,
      });
      
      final confirmation = res.data['confirmation'];
      
      if (confirmation == 'login successful') {
        final token = res.data['access_token'];
        if (token != null) {
          await ApiClient.saveToken(token);
        }
        if (!mounted) return;
        SuccessPopup.show(context, 'Login berhasil.', () {
          context.go('/articles');
        });
        return;
      }
      
      if (confirmation == "email doesn't exist") {
        setState(() => _generalError = 'Email tidak terdaftar.');
        return;
      }
      
      if (confirmation == 'password incorrect' || confirmation == 'password is incorrect') {
        setState(() => _generalError = 'Password yang Anda masukkan salah.');
        return;
      }
      
      setState(() => _generalError = 'Login belum berhasil. Silakan coba lagi.');
      
    } catch (e) {
      setState(() => _generalError = 'Terjadi kendala saat menghubungkan ke server.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
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
                        'Masuk ke akun Anda',
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
                        label: 'Email',
                        placeholder: 'nama@email.com',
                        controller: _emailCtrl,
                        keyboardType: TextInputType.emailAddress,
                        error: _emailError,
                      ),
                      const SizedBox(height: 18),
                      GlassInput(
                        label: 'Password',
                        placeholder: 'Masukkan password',
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
                          onPressed: _loading ? null : _login,
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
                            : const Text('Masuk', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
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
                            'Belum punya akun? ',
                            style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
                          ),
                          GestureDetector(
                            onTap: () => context.push('/register'),
                            child: const Text(
                              'Daftar',
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
