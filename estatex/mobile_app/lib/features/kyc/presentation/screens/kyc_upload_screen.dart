import 'package:flutter/material.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class KycUploadScreen extends StatefulWidget {
  const KycUploadScreen({super.key});

  @override
  State<KycUploadScreen> createState() => _KycUploadScreenState();
}

class _KycUploadScreenState extends State<KycUploadScreen> {
  final _docController = TextEditingController();

  @override
  void dispose() {
    _docController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);

    return ScreenScaffold(
      title: 'KYC Upload',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextField(
            controller: _docController,
            decoration: const InputDecoration(labelText: 'Document Number'),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              appState.submitKyc();
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('KYC submitted successfully.')));
            },
            child: const Text('Submit KYC'),
          ),
          const SizedBox(height: 16),
          Text(
            appState.kycSubmitted ? 'KYC status: Submitted' : 'KYC status: Pending',
            style: Theme.of(context).textTheme.titleMedium,
          ),
        ],
      ),
    );
  }
}
