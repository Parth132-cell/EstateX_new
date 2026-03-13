import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class LoginSignupScreen extends StatefulWidget {
  const LoginSignupScreen({super.key});

  @override
  State<LoginSignupScreen> createState() => _LoginSignupScreenState();
}

class _LoginSignupScreenState extends State<LoginSignupScreen> {
  final _nameController = TextEditingController(text: 'Demo User');
  String _role = 'buyer';

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);

    return ScreenScaffold(
      title: 'Login / Signup',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Full Name'),
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: _role,
            items: const [
              DropdownMenuItem(value: 'buyer', child: Text('Buyer')),
              DropdownMenuItem(value: 'seller', child: Text('Seller')),
              DropdownMenuItem(value: 'broker', child: Text('Broker')),
              DropdownMenuItem(value: 'admin', child: Text('Admin')),
            ],
            onChanged: (value) => setState(() => _role = value ?? 'buyer'),
            decoration: const InputDecoration(labelText: 'Role'),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              appState.login(name: _nameController.text.trim(), role: _role);
              context.go('/feed');
            },
            child: const Text('Continue with OTP'),
          ),
        ],
      ),
    );
  }
}
