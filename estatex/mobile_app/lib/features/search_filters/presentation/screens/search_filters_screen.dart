import 'package:flutter/material.dart';

import '../../../../shared/widgets/screen_scaffold.dart';

class SearchFiltersScreen extends StatelessWidget {
  const SearchFiltersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const ScreenScaffold(
      title: 'Search Filters',
      description: 'Refine by city, min/max price, BHK, and verified-only filter toggles.',
    );
  }
}
