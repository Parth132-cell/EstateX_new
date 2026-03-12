import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class EscrowPaymentScreen extends StatelessWidget {
  const EscrowPaymentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Escrow Payment',
      description: 'Create escrow orders and track hold/release state for safe transaction completion.',
    );
  }
}
