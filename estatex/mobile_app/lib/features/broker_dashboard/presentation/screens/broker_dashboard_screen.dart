import 'package:flutter/material.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class BrokerDashboardScreen extends StatelessWidget {
  const BrokerDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final liveTours = appState.tourStatus.values.where((value) => value == 'live').length;
    final activeDeals = appState.paymentStatus.values.where((value) => value == 'funds_held').length;
    final closedDeals = appState.paymentStatus.values.where((value) => value == 'released').length;

    return ScreenScaffold(
      title: 'Broker Dashboard',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Broker: ${appState.userName ?? 'Unassigned'}'),
          const SizedBox(height: 16),
          _metric('Leads in feed', appState.filteredListings.length.toString()),
          _metric('Live tours', '$liveTours'),
          _metric('Deals in escrow', '$activeDeals'),
          _metric('Deals closed', '$closedDeals'),
        ],
      ),
    );
  }

  Widget _metric(String label, String value) {
    return Card(
      child: ListTile(
        title: Text(label),
        trailing: Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
      ),
    );
  }
}
