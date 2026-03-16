import 'package:estatex_mobile_app/core/state/app_state.dart';
import 'package:estatex_mobile_app/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('EstateX app renders login screen', (tester) async {
    await tester.pumpWidget(EstateXApp(appState: AppState()));
    expect(find.text('Login / Signup'), findsOneWidget);
    expect(find.text('Continue with OTP'), findsOneWidget);
  });
}
