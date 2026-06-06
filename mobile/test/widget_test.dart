import 'package:flutter_test/flutter_test.dart';
import 'package:retogen/main.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const RetoGenApp());
    expect(find.byType(RetoGenApp), findsOneWidget);

    await tester.pump(const Duration(milliseconds: 1700));
    await tester.pump();
  });
}
