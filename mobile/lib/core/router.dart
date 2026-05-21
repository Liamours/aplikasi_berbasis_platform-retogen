import 'package:go_router/go_router.dart';
import 'package:retogen/features/auth/login_page.dart';
import 'package:retogen/features/auth/register_page.dart';
import 'package:retogen/features/articles/article_detail_page.dart';
import 'package:retogen/features/main/main_page.dart';
import 'package:retogen/features/profile/profile_page.dart';

final router = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (ctx, state) {
        final extra = state.extra as Map<String, dynamic>?;
        final email = extra?['email'] as String?;
        final password = extra?['password'] as String?;
        return LoginPage(initialEmail: email, initialPassword: password);
      },
    ),
    GoRoute(path: '/register', builder: (ctx, state) => const RegisterPage()),
    GoRoute(path: '/articles', builder: (ctx, state) => const MainPage()),
    GoRoute(
      path: '/articles/:id',
      builder: (ctx, state) =>
          ArticleDetailPage(articleId: state.pathParameters['id'] ?? ''),
    ),
    GoRoute(path: '/profile', builder: (ctx, state) => const ProfilePage()),
  ],
);
