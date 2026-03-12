import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class ARInteriorPreviewScreen extends StatelessWidget {
  const ARInteriorPreviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'AR Interior Preview',
      description: 'Visualize furniture and interior layouts in augmented reality for shortlisted properties.',
    );
  }
}
