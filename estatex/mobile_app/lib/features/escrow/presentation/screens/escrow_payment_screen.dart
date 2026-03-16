import 'package:flutter/material.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class EscrowPaymentScreen extends StatelessWidget {
  const EscrowPaymentScreen({required this.listingId, super.key});

  final int listingId;

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final status = appState.paymentStatus[listingId] ?? 'none';

    return ScreenScaffold(
      title: 'Escrow Payment',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Escrow status: $status'),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => appState.createOrder(listingId),
            child: const Text('Create Order'),
          ),
          const SizedBox(height: 8),
          FilledButton.tonal(
            onPressed: status == 'order_created' || status == 'funds_held' ? () => appState.holdFunds(listingId) : null,
            child: const Text('Hold Funds'),
          ),
          const SizedBox(height: 8),
          FilledButton.tonal(
            onPressed: status == 'funds_held' ? () => appState.releaseFunds(listingId) : null,
            child: const Text('Release Funds'),
          ),
        ],
      ),
    );
  }
}
