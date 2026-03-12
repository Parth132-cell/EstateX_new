import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class LoginSignupScreen extends StatelessWidget {
  const LoginSignupScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Login / Signup',
      description: 'OTP-based authentication entrypoint for buyers, sellers, brokers, and admins.',
    );
  }
}
