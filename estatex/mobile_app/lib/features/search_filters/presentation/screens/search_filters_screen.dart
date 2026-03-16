import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/state/app_state.dart';
import '../../../../shared/widgets/screen_scaffold.dart';

class SearchFiltersScreen extends StatefulWidget {
  const SearchFiltersScreen({super.key});

  @override
  State<SearchFiltersScreen> createState() => _SearchFiltersScreenState();
}

class _SearchFiltersScreenState extends State<SearchFiltersScreen> {
  late String _city;
  late double _maxPrice;
  int? _bhk;
  bool _initialized = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_initialized) return;
    final state = AppStateScope.of(context);
    _city = state.cityFilter;
    _maxPrice = state.maxPriceFilter.toDouble();
    _bhk = state.bhkFilter;
    _initialized = true;
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);

    return ScreenScaffold(
      title: 'Search Filters',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DropdownButtonFormField<String>(
            value: _city,
            items: const [
              DropdownMenuItem(value: 'All', child: Text('All Cities')),
              DropdownMenuItem(value: 'Mumbai', child: Text('Mumbai')),
              DropdownMenuItem(value: 'Pune', child: Text('Pune')),
              DropdownMenuItem(value: 'Bengaluru', child: Text('Bengaluru')),
            ],
            onChanged: (value) => setState(() => _city = value ?? 'All'),
            decoration: const InputDecoration(labelText: 'City'),
          ),
          const SizedBox(height: 16),
          Text('Max Price: ₹${_maxPrice.round()}'),
          Slider(
            min: 5000000,
            max: 30000000,
            divisions: 25,
            value: _maxPrice,
            label: _maxPrice.round().toString(),
            onChanged: (value) => setState(() => _maxPrice = value),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: [
              ChoiceChip(label: const Text('Any BHK'), selected: _bhk == null, onSelected: (_) => setState(() => _bhk = null)),
              ChoiceChip(label: const Text('2 BHK'), selected: _bhk == 2, onSelected: (_) => setState(() => _bhk = 2)),
              ChoiceChip(label: const Text('3 BHK'), selected: _bhk == 3, onSelected: (_) => setState(() => _bhk = 3)),
            ],
          ),
          const SizedBox(height: 20),
          FilledButton(
            onPressed: () async {
              await appState.applyFilters(city: _city, maxPrice: _maxPrice.round(), bhk: _bhk);
              if (!context.mounted) return;
              context.go('/feed');
            },
            child: const Text('Apply Filters'),
          ),
        ],
      ),
    );
  }
}
