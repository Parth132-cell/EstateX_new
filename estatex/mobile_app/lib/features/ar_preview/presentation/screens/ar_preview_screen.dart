import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class ARInteriorPreviewScreen extends StatefulWidget {
  const ARInteriorPreviewScreen({required this.listingId, super.key});

  final int listingId;

  @override
  State<ARInteriorPreviewScreen> createState() => _ARInteriorPreviewScreenState();
}

class _ARInteriorPreviewScreenState extends State<ARInteriorPreviewScreen> {
  String _room = 'Living Room';
  String _theme = 'Modern';

  @override
  Widget build(BuildContext context) {
    return ScreenScaffold(
      title: 'AR Interior Preview',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DropdownButtonFormField<String>(
            value: _room,
            decoration: const InputDecoration(labelText: 'Room'),
            items: const [
              DropdownMenuItem(value: 'Living Room', child: Text('Living Room')),
              DropdownMenuItem(value: 'Bedroom', child: Text('Bedroom')),
              DropdownMenuItem(value: 'Kitchen', child: Text('Kitchen')),
            ],
            onChanged: (value) => setState(() => _room = value ?? _room),
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            value: _theme,
            decoration: const InputDecoration(labelText: 'Theme'),
            items: const [
              DropdownMenuItem(value: 'Modern', child: Text('Modern')),
              DropdownMenuItem(value: 'Minimal', child: Text('Minimal')),
              DropdownMenuItem(value: 'Classic', child: Text('Classic')),
            ],
            onChanged: (value) => setState(() => _theme = value ?? _theme),
          ),
          const SizedBox(height: 16),
          Text('Preview ready for Listing #${widget.listingId}: $_room • $_theme'),
          const SizedBox(height: 12),
          const Placeholder(fallbackHeight: 200),
        ],
      ),
    );
  }
}
