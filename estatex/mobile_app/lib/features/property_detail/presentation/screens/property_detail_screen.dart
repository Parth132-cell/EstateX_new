import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class PropertyDetailScreen extends StatelessWidget {
  const PropertyDetailScreen({required this.listingId, super.key});

  final int listingId;

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final listing = appState.listingById(listingId);

    if (listing == null) {
      return const ScreenScaffold(
        title: 'Property Detail',
        child: Text('Listing not found.'),
      );
    }

    return ScreenScaffold(
      title: listing.title,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('${listing.city} • ${listing.bhk} BHK • ₹${listing.price}'),
          const SizedBox(height: 8),
          Text(listing.description),
          const SizedBox(height: 20),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              FilledButton(
                onPressed: () => context.go('/tour/$listingId'),
                child: const Text('Video Tour'),
              ),
              FilledButton(
                onPressed: () => context.go('/negotiation/$listingId'),
                child: const Text('Negotiate'),
              ),
              FilledButton(
                onPressed: () => context.go('/escrow/$listingId'),
                child: const Text('Escrow Payment'),
              ),
              OutlinedButton(
                onPressed: () => context.go('/ar/$listingId'),
                child: const Text('AR Preview'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
