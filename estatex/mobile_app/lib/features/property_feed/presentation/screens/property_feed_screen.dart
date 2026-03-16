import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class PropertyFeedScreen extends StatelessWidget {
  const PropertyFeedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final listings = appState.filteredListings;

    return ScreenScaffold(
      title: 'Property Feed',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Welcome ${appState.userName ?? 'Guest'}'),
          Text('Role: ${appState.userRole.toUpperCase()}'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            children: [
              OutlinedButton(
                onPressed: () => context.go('/filters'),
                child: const Text('Search Filters'),
              ),
              OutlinedButton(
                onPressed: () => context.go('/kyc'),
                child: const Text('KYC Upload'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Expanded(
            child: ListView.builder(
              itemCount: listings.length,
              itemBuilder: (context, index) {
                final listing = listings[index];
                return Card(
                  child: ListTile(
                    title: Text(listing.title),
                    subtitle: Text('${listing.city} • ${listing.bhk} BHK • ₹${listing.price}'),
                    trailing: Icon(
                      listing.verified ? Icons.verified : Icons.hourglass_top,
                      color: listing.verified ? Colors.green : Colors.orange,
                    ),
                    onTap: () => context.go('/detail/${listing.id}'),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
