import 'package:flutter/material.dart';

import 'core/network/api_client.dart';
import 'core/repositories/estatex_repository.dart';
import 'core/router/app_router.dart';
import 'core/state/app_state.dart';
import 'core/theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  final apiClient = ApiClient(baseUrl: const String.fromEnvironment('ESTATEX_API_URL', defaultValue: 'http://localhost:8000'));
  final repository = EstateXRepository(apiClient: apiClient);
  runApp(EstateXApp(appState: AppState(repository: repository)));
}

class EstateXApp extends StatelessWidget {
  const EstateXApp({required this.appState, super.key});

  final AppState appState;

  @override
  Widget build(BuildContext context) {
    return AppStateScope(
      notifier: appState,
      child: MaterialApp.router(
        title: 'EstateX',
        theme: AppTheme.lightTheme,
        routerConfig: AppRouter.router,
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
