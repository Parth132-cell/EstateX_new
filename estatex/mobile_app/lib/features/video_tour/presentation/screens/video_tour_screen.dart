import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class VideoTourScreen extends StatelessWidget {
  const VideoTourScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Video Tour',
      description: 'Join live WebRTC property tours with broker host controls and signaling state.',
    );
  }
}
