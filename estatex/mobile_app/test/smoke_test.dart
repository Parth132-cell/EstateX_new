import 'package:estatex_mobile_app/core/network/api_client.dart';
import 'package:estatex_mobile_app/core/repositories/estatex_repository.dart';
import 'package:estatex_mobile_app/core/state/app_state.dart';
import 'package:estatex_mobile_app/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('EstateX app renders login screen', (tester) async {
    final appState = AppState(
      repository: EstateXRepository(
        apiClient: ApiClient(baseUrl: 'http://localhost:8000'),
      ),
    );

    await tester.pumpWidget(EstateXApp(appState: appState));
    expect(find.text('Login / Signup'), findsOneWidget);
    expect(find.text('Continue with OTP'), findsOneWidget);
  });
}
