import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class KycUploadScreen extends StatelessWidget {
  const KycUploadScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'KYC Upload',
      description: 'Upload identity and property ownership documents for verification workflows.',
    );
  }
}
