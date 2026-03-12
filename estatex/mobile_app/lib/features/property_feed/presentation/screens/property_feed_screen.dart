import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class PropertyFeedScreen extends StatelessWidget {
  const PropertyFeedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Property Feed',
      description: 'Verified property listings stream with city, BHK, and budget segments.',
    );
  }
}
