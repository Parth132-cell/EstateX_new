import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class BrokerDashboardScreen extends StatelessWidget {
  const BrokerDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Broker Dashboard',
      description: 'Manage leads, active deals, co-broker requests, reminders, and conversion metrics.',
    );
  }
}
