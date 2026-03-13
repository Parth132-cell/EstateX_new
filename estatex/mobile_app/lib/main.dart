import 'package:flutter/material.dart';

import 'core/router/app_router.dart';
import 'core/state/app_state.dart';
import 'core/theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(EstateXApp(appState: AppState()));
}

class EstateXApp extends StatelessWidget {
  EstateXApp({required this.appState, super.key});

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
