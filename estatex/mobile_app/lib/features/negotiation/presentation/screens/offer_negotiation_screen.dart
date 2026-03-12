import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class OfferNegotiationScreen extends StatelessWidget {
  const OfferNegotiationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Offer & Negotiation',
      description: 'Create offers, submit counters, and view AI-assisted negotiation suggestions.',
    );
  }
}
