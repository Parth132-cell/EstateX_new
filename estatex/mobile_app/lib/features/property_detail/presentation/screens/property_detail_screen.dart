import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class PropertyDetailScreen extends StatelessWidget {
  const PropertyDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Property Detail',
      description: 'Gallery, amenities, co-broker visibility, verification confidence, and CTA actions.',
    );
  }
}
