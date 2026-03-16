import 'package:flutter/material.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class OfferNegotiationScreen extends StatefulWidget {
  const OfferNegotiationScreen({required this.listingId, super.key});

  final int listingId;

  @override
  State<OfferNegotiationScreen> createState() => _OfferNegotiationScreenState();
}

class _OfferNegotiationScreenState extends State<OfferNegotiationScreen> {
  final _offerController = TextEditingController();

  @override
  void dispose() {
    _offerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final items = appState.offers[widget.listingId] ?? [];

    return ScreenScaffold(
      title: 'Offer & Negotiation',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextField(
            controller: _offerController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Amount'),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            children: [
              FilledButton(
                onPressed: () {
                  final amount = int.tryParse(_offerController.text);
                  if (amount != null) appState.createOffer(widget.listingId, amount);
                },
                child: const Text('Make Offer'),
              ),
              OutlinedButton(
                onPressed: () {
                  final amount = int.tryParse(_offerController.text);
                  if (amount != null) appState.createCounter(widget.listingId, amount);
                },
                child: const Text('Counter Offer'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Expanded(
            child: ListView(
              children: items.map((entry) => ListTile(title: Text(entry))).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
