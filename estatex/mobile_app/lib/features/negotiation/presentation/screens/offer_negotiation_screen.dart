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
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      AppStateScope.of(context).loadOfferHistory(widget.listingId);
    });
  }

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
                onPressed: () async {
                  final amount = int.tryParse(_offerController.text);
                  if (amount != null) await appState.createOffer(widget.listingId, amount);
                },
                child: const Text('Make Offer'),
              ),
              OutlinedButton(
                onPressed: () async {
                  final amount = int.tryParse(_offerController.text);
                  if (amount != null) await appState.createCounter(widget.listingId, amount);
                },
                child: const Text('Counter Offer'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Expanded(
            child: items.isEmpty
                ? const Center(child: Text('No negotiation history yet.'))
                : ListView(
                    children: items.map((entry) => ListTile(title: Text(entry))).toList(),
                  ),
          ),
        ],
      ),
    );
  }
}
