import 'package:flutter/material.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class VideoTourScreen extends StatelessWidget {
  const VideoTourScreen({required this.listingId, super.key});

  final int listingId;

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final status = appState.tourStatus[listingId] ?? 'not_scheduled';

    return ScreenScaffold(
      title: 'Video Tour',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Tour status: $status'),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => appState.scheduleTour(listingId),
            child: const Text('Schedule Tour'),
          ),
          const SizedBox(height: 8),
          FilledButton.tonal(
            onPressed: status == 'scheduled' || status == 'live' ? () => appState.joinTour(listingId) : null,
            child: const Text('Join Room'),
          ),
        ],
      ),
    );
  }
}
