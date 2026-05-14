import 'package:go_router/go_router.dart';
import 'package:retogen/features/auth/login_page.dart';
import 'package:retogen/features/auth/register_page.dart';
import 'package:retogen/features/articles/articles_page.dart';

final router = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(path: '/login', builder: (ctx, state) => const LoginPage()),
    GoRoute(path: '/register', builder: (ctx, state) => const RegisterPage()),
    GoRoute(path: '/articles', builder: (ctx, state) => const ArticlesPage()),
  ],
);
